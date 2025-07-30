import aiohttp
import configparser
import logging
import asyncio
import os
import json
import hashlib
import hmac
import time
import ssl
from logging import Formatter
from enum import Enum
from pybreaker import CircuitBreaker, CircuitBreakerError
from pybreaker.storage import CircuitBreakerStorage
from pybreaker.storage.memory import CircuitBreakerMemoryStorage
from typing import Dict, Optional, Type, Any, Union, List, Literal, AsyncIterator, Callable, Set
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict, SecretStr
from datetime import datetime, timedelta
from cachetools import TTLCache
from contextlib import asynccontextmanager
import weakref
from dataclasses import dataclass
from cryptography.fernet import Fernet
import secrets
import ipaddress


# --- Enhanced Security Configuration ---
@dataclass
class SecurityConfig:
    """Конфигурация безопасности для бота."""
    max_request_size: int = 50 * 1024 * 1024  # 50MB
    rate_limit_requests: int = 30
    rate_limit_window: int = 60  # секунд
    allowed_ips: Optional[Set[str]] = None
    webhook_secret_token: Optional[str] = None
    encrypt_sensitive_data: bool = True
    max_concurrent_requests: int = 100
    request_timeout_multiplier: float = 1.5
    enable_request_signing: bool = True
    connection_pool_size: int = 100  # Новое: размер пула соединений
    connection_pool_ttl: int = 300   # Новое: TTL для соединений


# --- Enhanced Exceptions ---
class TelegramAPIError(Exception):
    """Base exception for Telegram API errors."""
    def __init__(self, message: str, error_code: Optional[int] = None, 
                 description: Optional[str] = None, response_data: Optional[Dict] = None,
                 retry_after: Optional[int] = None):
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.response_data = response_data
        self.retry_after = retry_after
        self.timestamp = datetime.now()

class TelegramUnauthorizedError(TelegramAPIError):
    """Exception for 401 Unauthorized error (invalid bot token)."""
    pass

class TelegramForbiddenError(TelegramAPIError):
    """Exception for 403 Forbidden error (bot blocked by user/channel)."""
    pass

class TelegramBadRequestError(TelegramAPIError):
    """Exception for 400 Bad Request error (incorrect request parameters)."""
    pass

class TelegramNotFoundError(TelegramAPIError):
    """Exception for 404 Not Found error (resource not found)."""
    pass

class TelegramTooManyRequestsError(TelegramAPIError):
    """Exception for 429 Too Many Requests error (request limit exceeded)."""
    pass

class SecurityError(Exception):
    """Exception for security-related errors."""
    pass

class RateLimitError(Exception):
    """Exception for rate limiting errors."""
    pass


# --- Enhanced Smart Cache ---
class SmartCache:
    """Умный кэш с метриками доступа и автоочисткой."""
    
    def __init__(self, maxsize: int, ttl: int):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.access_count = {}
        self.last_access = {}
        self.hit_count = 0
        self.miss_count = 0
        self._lock = asyncio.Lock()
    
    async def get(self, key, default=None):
        async with self._lock:
            if key in self.cache:
                self.access_count[key] = self.access_count.get(key, 0) + 1
                self.last_access[key] = time.time()
                self.hit_count += 1
                return self.cache[key]
            self.miss_count += 1
            return default
    
    async def set(self, key, value):
        async with self._lock:
            self.cache[key] = value
            self.access_count[key] = 1
            self.last_access[key] = time.time()
    
    async def clear_old_entries(self, max_age: int = 3600):
        """Очищает старые записи для экономии памяти."""
        async with self._lock:
            current_time = time.time()
            old_keys = [
                key for key, last_time in self.last_access.items()
                if current_time - last_time > max_age
            ]
            for key in old_keys:
                self.cache.pop(key, None)
                self.access_count.pop(key, None)
                self.last_access.pop(key, None)
    
    def get_stats(self) -> Dict:
        """Возвращает статистику кэша."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': hit_rate,
            'most_accessed': sorted(self.access_count.items(), key=lambda x: x[1], reverse=True)[:5]
        }


# --- Enhanced Rate Limiter with Exponential Backoff ---
class RateLimiter:
    """Продвинутый rate limiter с экспоненциальным backoff."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        self.backoff_factor = 1.0
        self.max_backoff = 60.0
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """Проверяет, можно ли выполнить запрос."""
        async with self._lock:
            now = time.time()
            # Удаляем старые запросы
            self.requests = [req_time for req_time in self.requests 
                           if now - req_time < self.window_seconds]
            
            if len(self.requests) >= self.max_requests:
                # Увеличиваем backoff при превышении лимита
                self.backoff_factor = min(self.backoff_factor * 1.5, self.max_backoff)
                return False
            
            self.requests.append(now)
            # Уменьшаем backoff при успешном запросе
            self.backoff_factor = max(self.backoff_factor * 0.9, 1.0)
            return True
    
    async def wait_if_needed(self):
        """Ждет с учетом экспоненциального backoff."""
        while not await self.acquire():
            wait_time = min(0.1 * self.backoff_factor, 5.0)
            await asyncio.sleep(wait_time)
    
    def get_stats(self) -> Dict:
        """Возвращает статистику rate limiter."""
        return {
            'current_requests': len(self.requests),
            'max_requests': self.max_requests,
            'backoff_factor': self.backoff_factor,
            'window_seconds': self.window_seconds
        }


# --- Enhanced Retry Strategy ---
class RetryStrategy:
    """Улучшенная стратегия повторов с различными алгоритмами."""
    
    def __init__(self, max_retries: int = 5, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff_factors = [1, 2, 4, 8, 16]  # Exponential backoff
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """Выполняет функцию с повторами."""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except TelegramTooManyRequestsError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = e.retry_after or (self.base_delay * self.backoff_factors[min(attempt, len(self.backoff_factors)-1)])
                # Добавляем jitter для избежания thundering herd
                jitter = secrets.randbelow(1000) / 1000
                await asyncio.sleep(wait_time + jitter)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt == self.max_retries - 1:
                    break
                wait_time = self.base_delay * self.backoff_factors[min(attempt, len(self.backoff_factors)-1)]
                await asyncio.sleep(wait_time)
        
        raise TelegramAPIError(f"All retries failed: {last_exception}")


# --- Enhanced Connection Pool Manager ---
class ConnectionPoolManager:
    """Менеджер пула соединений для оптимизации производительности."""
    
    def __init__(self, pool_size: int = 100, ttl: int = 300):
        self.pool_size = pool_size
        self.ttl = ttl
        self._sessions = {}
        self._session_created = {}
        self._lock = asyncio.Lock()
    
    async def get_session(self, base_url: str) -> aiohttp.ClientSession:
        """Получает сессию из пула или создает новую."""
        async with self._lock:
            now = time.time()
            
            # Очищаем старые сессии
            expired_keys = [
                key for key, created_time in self._session_created.items()
                if now - created_time > self.ttl
            ]
            
            for key in expired_keys:
                session = self._sessions.pop(key, None)
                if session and not session.closed:
                    await session.close()
                self._session_created.pop(key, None)
            
            # Возвращаем существующую сессию или создаем новую
            if base_url in self._sessions and not self._sessions[base_url].closed:
                return self._sessions[base_url]
            
            # Создаем новую сессию
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=self.pool_size,
                limit_per_host=30,
                ttl_dns_cache=300,
                use_dns_cache=True,
                enable_cleanup_closed=True,
                keepalive_timeout=60
            )
            
            timeout = aiohttp.ClientTimeout(
                total=120,
                connect=10,
                sock_read=30
            )
            
            session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'CustomGiftSend/2.1 (Enhanced Performance)',
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
            )
            
            self._sessions[base_url] = session
            self._session_created[base_url] = now
            
            return session
    
    async def close_all(self):
        """Закрывает все сессии в пуле."""
        async with self._lock:
            for session in self._sessions.values():
                if not session.closed:
                    await session.close()
            self._sessions.clear()
            self._session_created.clear()


# --- Enhanced Enums ---
class GiftAlias(str, Enum):
    """Enum для псевдонимов подарков."""
    PREMIUM_1_MONTH = "premium_1_month"
    PREMIUM_3_MONTHS = "premium_3_months"
    PREMIUM_6_MONTHS = "premium_6_months"
    PREMIUM_12_MONTHS = "premium_12_months"
    STAR_PACK_1 = "star_pack_1"
    STAR_PACK_2 = "star_pack_2"
    STAR_PACK_3 = "star_pack_3"
    STAR_PACK_4 = "star_pack_4"
    STAR_PACK_5 = "star_pack_5"
    STAR_PACK_6 = "star_pack_6"
    STAR_PACK_7 = "star_pack_7"
    STAR_PACK_8 = "star_pack_8"
    STAR_PACK_9 = "star_pack_9"
    STAR_PACK_10 = "star_pack_10"
    STAR_PACK_11 = "star_pack_11"
    STAR_PACK_12 = "star_pack_12"
    STAR_PACK_13 = "star_pack_13"
    STAR_PACK_14 = "star_pack_14"
    STAR_PACK_15 = "star_pack_15"

class MessageType(str, Enum):
    """Типы сообщений."""
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    VOICE = "voice"
    STICKER = "sticker"
    ANIMATION = "animation"
    LOCATION = "location"
    CONTACT = "contact"

class ChatType(str, Enum):
    """Типы чатов."""
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


# --- Enhanced Pydantic Models with Better Validation ---
class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None
    can_connect_to_business: Optional[bool] = None
    
    @field_validator('id')
    @classmethod
    def validate_user_id(cls, v):
        if v <= 0 or v > 10**15:  # Telegram user ID limits
            raise ValueError('User ID must be positive and within Telegram limits')
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is not None:
            if not v.startswith('@'):
                v = '@' + v
            if len(v) < 2 or len(v) > 33:  # Telegram username limits
                raise ValueError('Username must be 1-32 characters long')
        return v

class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

class Chat(BaseModel):
    id: int
    type: ChatType
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    active_usernames: Optional[List[str]] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[datetime] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    has_aggressive_anti_spam_enabled: Optional[bool] = None
    
    @field_validator('id')
    @classmethod
    def validate_chat_id(cls, v):
        if v == 0 or abs(v) > 10**15:
            raise ValueError('Invalid chat_id range')
        return v

class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None
    
    @field_validator('width', 'height')
    @classmethod
    def validate_dimensions(cls, v):
        if v <= 0 or v > 10000:  # Reasonable limits
            raise ValueError('Image dimensions must be positive and reasonable')
        return v

class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumbnail: Optional[PhotoSize] = None
    
    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v < 0 or v > 86400:  # Max 24 hours
            raise ValueError('Audio duration must be reasonable')
        return v

class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    
    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v):
        if v is not None and (v < 0 or v > 2 * 1024 * 1024 * 1024):  # 2GB limit
            raise ValueError('File size must be reasonable')
        return v

class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

class Message(BaseModel):
    message_id: int
    from_user: Optional[User] = Field(None, alias='from')
    sender_chat: Optional[Chat] = None
    date: datetime
    chat: Chat
    text: Optional[str] = None
    photo: Optional[List[PhotoSize]] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    video: Optional[Video] = None
    voice: Optional[Voice] = None
    reply_to_message: Optional['Message'] = None
    forward_from: Optional[User] = None
    forward_date: Optional[datetime] = None
    edit_date: Optional[datetime] = None
    
    model_config = ConfigDict(populate_by_name=True)
    
    @property
    def message_type(self) -> MessageType:
        """Определяет тип сообщения."""
        if self.text:
            return MessageType.TEXT
        elif self.photo:
            return MessageType.PHOTO
        elif self.video:
            return MessageType.VIDEO
        elif self.audio:
            return MessageType.AUDIO
        elif self.document:
            return MessageType.DOCUMENT
        elif self.voice:
            return MessageType.VOICE
        else:
            return MessageType.TEXT

class ChatMember(BaseModel):
    status: str
    user: User

class ChatMemberOwner(ChatMember):
    status: Literal['creator']
    is_anonymous: bool
    custom_title: Optional[str] = None

class ChatMemberAdministrator(ChatMember):
    status: Literal['administrator']
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None

class ChatMemberMember(ChatMember):
    status: Literal['member']

class ChatMemberRestricted(ChatMember):
    status: Literal['restricted']
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: Optional[datetime] = None

class ChatMemberLeft(ChatMember):
    status: Literal['left']

class ChatMemberBanned(ChatMember):
    status: Literal['kicked']
    until_date: Optional[datetime] = None

AnyChatMember = Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, 
                     ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned]

class CallbackQuery(BaseModel):
    id: str
    from_user: User = Field(alias='from')
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class InlineQuery(BaseModel):
    id: str
    from_user: User = Field(alias='from')
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Any] = None

    model_config = ConfigDict(populate_by_name=True)

class ChosenInlineResult(BaseModel):
    result_id: str
    from_user: User = Field(alias='from')
    location: Optional[Any] = None
    inline_message_id: Optional[str] = None
    query: str

    model_config = ConfigDict(populate_by_name=True)

class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None

class WebhookInfo(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None

class AvailableGift(BaseModel):
    gift_id: str
    gift_name: str
    gift_url: Optional[str] = None
    price_stars: Optional[int] = None
    usd_price: Optional[str] = None
    currency_code: Optional[str] = None
    image_url: Optional[str] = None

class ChecklistTask(BaseModel):
    task_id: str
    text: str
    is_checked: bool

class Checklist(BaseModel):
    checklist_id: str
    title: str
    tasks: List[ChecklistTask]

class InputChecklistTask(BaseModel):
    text: str
    is_checked: Optional[bool] = False

class InputChecklist(BaseModel):
    title: str
    tasks: List[InputChecklistTask]

class ChecklistTasksDone(BaseModel):
    checklist_id: str
    tasks_ids: List[str]
    from_user: User = Field(alias='from')

    model_config = ConfigDict(populate_by_name=True)

class ChecklistTasksAdded(BaseModel):
    checklist_id: str
    tasks: List[ChecklistTask]
    from_user: User = Field(alias='from')

    model_config = ConfigDict(populate_by_name=True)

class RevenueWithdrawalState(BaseModel):
    state: str

# --- Enhanced Parameter Models with Better Validation ---
class SendGiftParams(BaseModel):
    chat_id: Union[int, str]
    gift_id: str
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    
    @field_validator('chat_id')
    @classmethod
    def validate_chat_id_enhanced(cls, v):
        if isinstance(v, str):
            if not v.startswith('@') and not v.lstrip('-').isdigit():
                raise ValueError('String chat_id must be username (@username) or numeric')
        elif isinstance(v, int):
            if v == 0 or abs(v) > 10**15:
                raise ValueError('Invalid chat_id range')
        return v
    
    @field_validator('gift_id')
    @classmethod
    def validate_gift_id(cls, v):
        if not v or len(v) > 100:
            raise ValueError('Gift ID must be non-empty and reasonable length')
        return v

class GiftPremiumParams(BaseModel):
    user_id: int
    months: int
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    
    @field_validator('months')
    @classmethod
    def validate_months(cls, v):
        if v not in [1, 3, 6, 12]:
            raise ValueError('Months must be 1, 3, 6, or 12')
        return v
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v <= 0 or v > 10**15:
            raise ValueError('Invalid user_id')
        return v

class TransferGiftParams(BaseModel):
    recipient_user_id: int
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class GetUpdatesParams(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = Field(None, ge=1, le=100)
    timeout: Optional[int] = Field(None, ge=0, le=50)
    allowed_updates: Optional[List[str]] = None

class SetWebhookParams(BaseModel):
    url: str
    certificate: Optional[Any] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = Field(None, ge=1, le=100)
    allowed_updates: Optional[List[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v.startswith('https://'):
            raise ValueError('Webhook URL must use HTTPS')
        if len(v) > 2048:
            raise ValueError('URL too long')
        return v

class DeleteWebhookParams(BaseModel):
    drop_pending_updates: Optional[bool] = None

class GetUserChatBoostsParams(BaseModel):
    chat_id: Union[int, str]
    user_id: int

class RefundStarPaymentParams(BaseModel):
    user_id: int
    telegram_payment_charge_id: str

class SendMessageParams(BaseModel):
    chat_id: Union[int, str]
    text: str = Field(..., max_length=4096)
    message_thread_id: Optional[int] = None
    parse_mode: Optional[str] = None
    entities: Optional[List[Dict]] = None
    link_preview_options: Optional[Dict] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    business_connection_id: Optional[str] = None
    
    @field_validator('parse_mode')
    @classmethod
    def validate_parse_mode(cls, v):
        if v is not None and v not in ['HTML', 'Markdown', 'MarkdownV2']:
            raise ValueError('Invalid parse_mode')
        return v

class EditMessageTextParams(BaseModel):
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    text: str = Field(..., max_length=4096)
    parse_mode: Optional[str] = None
    entities: Optional[List[Dict]] = None
    link_preview_options: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class DeleteMessageParams(BaseModel):
    chat_id: Union[int, str]
    message_id: int

class ForwardMessageParams(BaseModel):
    chat_id: Union[int, str]
    from_chat_id: Union[int, str]
    message_id: int
    message_thread_id: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None

class AnswerInlineQueryParams(BaseModel):
    inline_query_id: str
    results: List[Dict]
    cache_time: Optional[int] = None
    is_personal: Optional[bool] = None
    next_offset: Optional[str] = None
    button: Optional[Dict] = None

class GetChatParams(BaseModel):
    chat_id: Union[int, str]

class GetChatAdministratorsParams(BaseModel):
    chat_id: Union[int, str]

class KickChatMemberParams(BaseModel):
    chat_id: Union[int, str]
    user_id: int
    until_date: Optional[int] = None
    revoke_messages: Optional[bool] = None

class UnbanChatMemberParams(BaseModel):
    chat_id: Union[int, str]
    user_id: int
    only_if_banned: Optional[bool] = False

class SendChecklistParams(BaseModel):
    chat_id: Union[int, str]
    checklist: InputChecklist
    message_thread_id: Optional[int] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class EditMessageChecklistParams(BaseModel):
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    checklist: InputChecklist
    reply_markup: Optional[Dict] = None

class HideKeyboardParams(BaseModel):
    chat_id: Union[int, str]
    message_id: int


# --- Enhanced Security Manager ---
class SecurityManager:
    """Менеджер безопасности для защиты бота."""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.rate_limiter = RateLimiter(
            config.rate_limit_requests, 
            config.rate_limit_window
        )
        self.encryption_key = Fernet.generate_key() if config.encrypt_sensitive_data else None
        self.cipher = Fernet(self.encryption_key) if self.encryption_key else None
        self.request_signatures = {}
        self._cleanup_task = None
        
    async def start_cleanup_task(self):
        """Запускает задачу периодической очистки."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
    
    async def stop_cleanup_task(self):
        """Останавливает задачу очистки."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
    
    async def _periodic_cleanup(self):
        """Периодическая очистка старых подписей."""
        while True:
            try:
                await asyncio.sleep(300)  # Каждые 5 минут
                current_time = time.time()
                expired_signatures = [
                    sig for sig, timestamp in self.request_signatures.items()
                    if current_time - timestamp > 600  # 10 минут
                ]
                for sig in expired_signatures:
                    del self.request_signatures[sig]
            except asyncio.CancelledError:
                break
            except Exception:
                pass  # Игнорируем ошибки в cleanup
        
    def validate_ip(self, ip: str) -> bool:
        """Проверяет, разрешен ли IP адрес."""
        if not self.config.allowed_ips:
            return True
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            for allowed_ip in self.config.allowed_ips:
                if ip_obj in ipaddress.ip_network(allowed_ip, strict=False):
                    return True
            return False
        except ValueError:
            return False
    
    def encrypt_data(self, data: str) -> str:
        """Шифрует чувствительные данные."""
        if not self.cipher:
            return data
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Расшифровывает данные."""
        if not self.cipher:
            return encrypted_data
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def generate_request_signature(self, method: str, params: Dict) -> str:
        """Генерирует подпись запроса."""
        if not self.config.enable_request_signing:
            return ""
        
        # Создаем детерминированную строку из параметров
        sorted_params = json.dumps(params, sort_keys=True, separators=(',', ':'))
        data = f"{method}:{sorted_params}:{time.time():.0f}"
        
        signature = hmac.new(
            self.encryption_key or b"default_key",
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        self.request_signatures[signature] = time.time()
        return signature
    
    def verify_request_signature(self, signature: str, max_age: int = 300) -> bool:
        """Проверяет подпись запроса."""
        if not self.config.enable_request_signing:
            return True
        
        if signature not in self.request_signatures:
            return False
        
        timestamp = self.request_signatures[signature]
        if time.time() - timestamp > max_age:
            del self.request_signatures[signature]
            return False
        
        return True
    
    async def check_rate_limit(self) -> bool:
        """Проверяет лимит запросов."""
        return await self.rate_limiter.acquire()
    
    async def wait_for_rate_limit(self):
        """Ждет освобождения лимита запросов."""
        await self.rate_limiter.wait_if_needed()
    
    def get_stats(self) -> Dict:
        """Возвращает статистику безопасности."""
        return {
            'rate_limiter': self.rate_limiter.get_stats(),
            'active_signatures': len(self.request_signatures),
            'encryption_enabled': self.cipher is not None
        }


# --- Enhanced Analytics with Detailed Metrics ---
class BotAnalytics:
    """Расширенная аналитика для бота."""
    
    def __init__(self):
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'messages_sent': 0,
            'gifts_sent': 0,
            'errors_by_type': {},
            'response_times': [],
            'methods_stats': {},  # Статистика по методам
            'hourly_stats': {},   # Почасовая статистика
            'start_time': datetime.now()
        }
        self._lock = asyncio.Lock()
    
    async def record_request(self, method: str, success: bool, response_time: float, error_type: str = None):
        """Записывает детальную статистику запроса."""
        async with self._lock:
            self.stats['requests_total'] += 1
            
            # Общая статистика
            if success:
                self.stats['requests_success'] += 1
            else:
                self.stats['requests_failed'] += 1
                if error_type:
                    self.stats['errors_by_type'][error_type] = self.stats['errors_by_type'].get(error_type, 0) + 1
            
            # Время ответа
            self.stats['response_times'].append(response_time)
            if len(self.stats['response_times']) > 1000:
                self.stats['response_times'] = self.stats['response_times'][-500:]
            
            # Статистика по методам
            if method not in self.stats['methods_stats']:
                self.stats['methods_stats'][method] = {
                    'total': 0, 'success': 0, 'failed': 0, 'avg_time': 0, 'times': []
                }
            
            method_stats = self.stats['methods_stats'][method]
            method_stats['total'] += 1
            method_stats['times'].append(response_time)
            
            if success:
                method_stats['success'] += 1
            else:
                method_stats['failed'] += 1
            
            # Обновляем среднее время
            if len(method_stats['times']) > 100:
                method_stats['times'] = method_stats['times'][-50:]
            method_stats['avg_time'] = sum(method_stats['times']) / len(method_stats['times'])
            
            # Почасовая статистика
            current_hour = datetime.now().strftime('%Y-%m-%d %H:00')
            if current_hour not in self.stats['hourly_stats']:
                self.stats['hourly_stats'][current_hour] = {'requests': 0, 'errors': 0}
            
            self.stats['hourly_stats'][current_hour]['requests'] += 1
            if not success:
                self.stats['hourly_stats'][current_hour]['errors'] += 1
            
            # Специальные счетчики
            if method == 'sendMessage' and success:
                self.stats['messages_sent'] += 1
            elif method == 'sendGift' and success:
                self.stats['gifts_sent'] += 1
    
    async def record_detailed_request(self, method_metrics: Dict):
        """Записывает детальные метрики запроса."""
        async with self._lock:
            method = method_metrics.get('method')
            if method and method not in self.stats['methods_stats']:
                self.stats['methods_stats'][method] = {
                    'total': 0, 'success': 0, 'failed': 0, 'avg_time': 0, 
                    'times': [], 'params_sizes': [], 'response_sizes': []
                }
            
            if method:
                method_stats = self.stats['methods_stats'][method]
                
                # Размеры запросов и ответов
                if 'params_size' in method_metrics:
                    method_stats['params_sizes'].append(method_metrics['params_size'])
                    if len(method_stats['params_sizes']) > 100:
                        method_stats['params_sizes'] = method_stats['params_sizes'][-50:]
                
                if 'response_size' in method_metrics:
                    method_stats['response_sizes'].append(method_metrics['response_size'])
                    if len(method_stats['response_sizes']) > 100:
                        method_stats['response_sizes'] = method_stats['response_sizes'][-50:]
    
    def get_stats(self) -> Dict:
        """Возвращает расширенную статистику."""
        uptime = datetime.now() - self.stats['start_time']
        avg_response_time = sum(self.stats['response_times']) / len(self.stats['response_times']) if self.stats['response_times'] else 0
        
        # Топ методов по использованию
        top_methods = sorted(
            [(method, stats['total']) for method, stats in self.stats['methods_stats'].items()],
            key=lambda x: x[1], reverse=True
        )[:5]
        
        # Топ ошибок
        top_errors = sorted(
            self.stats['errors_by_type'].items(),
            key=lambda x: x[1], reverse=True
        )[:5]
        
        return {
            **self.stats,
            'uptime_seconds': uptime.total_seconds(),
            'average_response_time': avg_response_time,
            'success_rate': self.stats['requests_success'] / max(self.stats['requests_total'], 1) * 100,
            'requests_per_minute': self.stats['requests_total'] / max(uptime.total_seconds() / 60, 1),
            'top_methods': top_methods,
            'top_errors': top_errors,
            'response_time_percentiles': self._calculate_percentiles(self.stats['response_times'])
        }
    
    def _calculate_percentiles(self, times: List[float]) -> Dict:
        """Вычисляет перцентили времени ответа."""
        if not times:
            return {}
        
        sorted_times = sorted(times)
        length = len(sorted_times)
        
        return {
            'p50': sorted_times[int(length * 0.5)],
            'p90': sorted_times[int(length * 0.9)],
            'p95': sorted_times[int(length * 0.95)],
            'p99': sorted_times[int(length * 0.99)] if length > 100 else sorted_times[-1]
        }


# --- Custom JSON Encoder for Better Serialization ---
class TelegramJSONEncoder(json.JSONEncoder):
    """Кастомный JSON encoder для оптимизации сериализации."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif hasattr(obj, 'model_dump'):
            return obj.model_dump()
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='ignore')
        return super().default(obj)


# --- Context Logger for Better Logging ---
class ContextLogger:
    """Контекстный логгер для структурированного логирования."""
    
    def __init__(self, logger, context: Dict):
        self.logger = logger
        self.context = context
    
    def _log_with_context(self, level, message, **kwargs):
        extra_data = kwargs.get('extra', {}).get('extra_data', {})
        extra_data.update(self.context)
        kwargs['extra'] = {'extra_data': extra_data}
        getattr(self.logger, level)(message, **kwargs)
    
    def info(self, message, **kwargs):
        self._log_with_context('info', message, **kwargs)
    
    def warning(self, message, **kwargs):
        self._log_with_context('warning', message, **kwargs)
    
    def error(self, message, **kwargs):
        self._log_with_context('error', message, **kwargs)
    
    def debug(self, message, **kwargs):
        self._log_with_context('debug', message, **kwargs)


# --- Enhanced Main Class ---
class CustomGiftSend:
    """
    Улучшенный асинхронный клиент для Telegram Bot API с поддержкой подарков, Stars,
    списков задач и других функций версии 9.1.
    """
    
    def __init__(self, token: str, config_path: Optional[str] = None,
                 base_url: str = "https://api.telegram.org/bot",
                 max_retries: int = 5, retry_delay: int = 2,
                 conn_timeout: int = 10, request_timeout: int = 60,
                 security_config: Optional[SecurityConfig] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Инициализирует улучшенный клиент Telegram Bot API.
        """
        self.token = SecretStr(self._load_token(token, config_path))
        self.base_url = f"{base_url}{self.token.get_secret_value()}"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.conn_timeout = conn_timeout
        self.request_timeout = request_timeout
        
        # Настройка безопасности
        self.security_config = security_config or SecurityConfig()
        self.security_manager = SecurityManager(self.security_config)
        
        # Настройка аналитики
        self.analytics = BotAnalytics()
        
        # Настройка логирования
        self.logger = logger or self._setup_logger()
        
        # Семафор для ограничения concurrent запросов
        self._semaphore = asyncio.Semaphore(self.security_config.max_concurrent_requests)
        
        # Настройка Circuit Breaker
        self._setup_circuit_breaker()
        
        # Улучшенные кэши
        self.available_gifts_cache = SmartCache(maxsize=10, ttl=3600)
        self.star_balance_cache = SmartCache(maxsize=10, ttl=300)
        self.chat_cache = SmartCache(maxsize=1000, ttl=3600)
        
        # Менеджер пула соединений
        self.connection_pool = ConnectionPoolManager(
            pool_size=self.security_config.connection_pool_size,
            ttl=self.security_config.connection_pool_ttl
        )
        
        # Стратегия повторов
        self.retry_strategy = RetryStrategy(max_retries=max_retries, base_delay=retry_delay)
        
        # Обработчики событий
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Webhook валидация
        self._webhook_validators = []
        
        # Задачи для очистки
        self._cleanup_tasks = []
    
    def _setup_logger(self) -> logging.Logger:
        """Настраивает улучшенное логирование."""
        logger = logging.getLogger(f"{__name__}.{id(self)}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # JSON форматтер для структурированных логов
            class JSONFormatter(Formatter):
                def format(self, record):
                    log_data = {
                        'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                        'level': record.levelname,
                        'logger': record.name,
                        'message': record.getMessage(),
                        'module': record.module,
                        'function': record.funcName,
                        'line': record.lineno
                    }
                    if hasattr(record, 'extra_data'):
                        log_data.update(record.extra_data)
                    return json.dumps(log_data, ensure_ascii=False, cls=TelegramJSONEncoder)
            
            handler = logging.StreamHandler()
            handler.setFormatter(JSONFormatter())
            logger.addHandler(handler)
        
        return logger
    
    def _setup_circuit_breaker(self):
        """Настраивает Circuit Breaker."""
        fail_exceptions = (
            TelegramBadRequestError,
            TelegramForbiddenError,
            TelegramNotFoundError,
            aiohttp.ClientError,
            SecurityError
        )
        
        self.breaker_storage = CircuitBreakerMemoryStorage()
        self.circuit_breaker = CircuitBreaker(
            fail_max=5,
            reset_timeout=60,
            exclude=TelegramTooManyRequestsError,
            fail_exceptions=fail_exceptions,
            storage=self.breaker_storage
        )
        self.circuit_breaker.add_listener(self._circuit_breaker_listener)
    
    def _circuit_breaker_listener(self, *args, **kwargs):
        """Улучшенный слушатель Circuit Breaker."""
        event_name = kwargs.get('event_name')
        extra_data = {'circuit_breaker_event': event_name}
        
        if event_name == 'state_change':
            old_state = kwargs.get('old_state')
            new_state = kwargs.get('new_state')
            extra_data.update({'old_state': old_state, 'new_state': new_state})
            self.logger.warning("Circuit Breaker state changed", extra={'extra_data': extra_data})
        elif event_name == 'failure':
            exc = kwargs.get('exception')
            extra_data.update({'exception': str(exc)})
            self.logger.warning("Circuit Breaker failure", extra={'extra_data': extra_data})
        elif event_name == 'success':
            self.logger.info("Circuit Breaker success", extra={'extra_data': extra_data})
    
    def _load_token(self, token: str, config_path: Optional[str]) -> str:
        """Загружает токен с улучшенной безопасностью."""
        if config_path:
            try:
                config = configparser.ConfigParser()
                config.read(config_path)
                loaded_token = config['telegram']['bot_token']
                
                # Проверяем формат токена
                if not self._validate_token_format(loaded_token):
                    raise ValueError("Invalid token format")
                
                return loaded_token
            except (configparser.Error, KeyError) as e:
                self.logger.error("Failed to read token from config", extra={'extra_data': {'error': str(e)}})
                raise ValueError("Invalid config file or missing bot_token")
        elif token:
            if not self._validate_token_format(token):
                raise ValueError("Invalid token format")
            return token
        else:
            # Пробуем загрузить из переменной окружения
            env_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if env_token and self._validate_token_format(env_token):
                return env_token
            raise ValueError("No valid token provided")
    
    def _validate_token_format(self, token: str) -> bool:
        """Проверяет формат токена бота."""
        import re
        pattern = r'^\d+:[A-Za-z0-9_-]{35}$'
        return bool(re.match(pattern, token))
    
    async def _start_background_tasks(self):
        """Запускает фоновые задачи."""
        # Задача очистки кэшей
        cleanup_task = asyncio.create_task(self._periodic_cache_cleanup())
        self._cleanup_tasks.append(cleanup_task)
        
        # Задача очистки security manager
        await self.security_manager.start_cleanup_task()
    
    async def _periodic_cache_cleanup(self):
        """Периодическая очистка кэшей."""
        while True:
            try:
                await asyncio.sleep(1800)  # Каждые 30 минут
                await self.available_gifts_cache.clear_old_entries()
                await self.star_balance_cache.clear_old_entries()
                await self.chat_cache.clear_old_entries()
                
                self.logger.info("Cache cleanup completed", extra={
                    'extra_data': {
                        'gifts_cache': self.available_gifts_cache.get_stats(),
                        'balance_cache': self.star_balance_cache.get_stats(),
                        'chat_cache': self.chat_cache.get_stats()
                    }
                })
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cache cleanup: {e}")
    
    async def close(self):
        """Безопасно закрывает все ресурсы."""
        # Останавливаем фоновые задачи
        for task in self._cleanup_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Останавливаем security manager
        await self.security_manager.stop_cleanup_task()
        
        # Закрываем пул соединений
        await self.connection_pool.close_all()
        
        # Очищаем кэши
        self.available_gifts_cache.cache.clear()
        self.star_balance_cache.cache.clear()
        self.chat_cache.cache.clear()
        
        # Сохраняем финальную статистику
        stats = self.analytics.get_stats()
        self.logger.info("Final statistics", extra={'extra_data': stats})
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._start_background_tasks()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def _handle_api_error(self, response_data: Dict, method: str) -> None:
        """Централизованная обработка API ошибок с детальным логированием."""
        error_code = response_data.get("error_code")
        description = response_data.get("description", "Unknown error")
        
        # Специальная обработка для разных типов ошибок
        if error_code == 400 and "chat not found" in description.lower():
            raise TelegramNotFoundError(f"Chat not found in {method}", error_code, description, response_data)
        elif error_code == 403 and "bot was blocked" in description.lower():
            raise TelegramForbiddenError(f"Bot blocked by user in {method}", error_code, description, response_data)
        elif error_code == 502:  # Bad Gateway - можно повторить
            await asyncio.sleep(1)
            return  # Сигнал для повтора
        
        # Создаем соответствующее исключение
        exception_class = self._get_exception_class(error_code)
        if error_code == 429:
            parameters = response_data.get("parameters", {})
            retry_after = parameters.get("retry_after", 1)
            raise exception_class(description, error_code, description, response_data, retry_after)
        else:
            raise exception_class(description, error_code, description, response_data)
    
    async def _make_request(self, method: str, params: Dict, 
                          response_model: Optional[Type[BaseModel]] = None,
                          validate_response: bool = True) -> Any:
        """
        Улучшенный метод для выполнения HTTP запросов с повышенной безопасностью.
        """
        start_time = time.perf_counter()
        
        # Создаем контекстный логгер
        context_logger = ContextLogger(self.logger, {'method': method, 'chat_id': params.get('chat_id')})
        
        # Проверка лимита запросов
        await self.security_manager.wait_for_rate_limit()
        
        # Ограничение concurrent запросов
        async with self._semaphore:
            session = await self.connection_pool.get_session(self.base_url)
            
            # Генерация подписи запроса
            signature = self.security_manager.generate_request_signature(method, params)
            
            # Метрики запроса
            method_metrics = {
                'method': method,
                'params_size': len(json.dumps(params, cls=TelegramJSONEncoder)),
                'attempt': 0
            }
            
            # Логирование запроса (без чувствительных данных)
            safe_params = {k: v for k, v in params.items() if k not in ['token', 'certificate']}
            context_logger.info(f"Making request to {method}", extra={
                'extra_data': {
                    'params_keys': list(safe_params.keys()),
                    'signature': signature[:8] + '...' if signature else None,
                    'params_size': method_metrics['params_size']
                }
            })
            
            # Используем стратегию повторов
            async def make_single_request():
                # Проверка размера запроса
                request_size = method_metrics['params_size']
                if request_size > self.security_config.max_request_size:
                    raise SecurityError(f"Request size {request_size} exceeds limit")
                
                # Сериализация с кастомным encoder
                request_data = json.dumps(params, cls=TelegramJSONEncoder, separators=(',', ':'))
                
                async with session.post(
                    f"{self.base_url}/{method}",
                    data=request_data,
                    headers={
                        'Content-Type': 'application/json',
                        'X-Request-Signature': signature
                    } if signature else {'Content-Type': 'application/json'}
                ) as response:
                    response_time = time.perf_counter() - start_time
                    response_text = await response.text()
                    
                    # Проверка размера ответа
                    if len(response_text) > self.security_config.max_request_size:
                        raise SecurityError("Response size exceeds limit")
                    
                    method_metrics.update({
                        'response_time': response_time,
                        'response_size': len(response_text),
                        'status_code': response.status
                    })
                    
                    try:
                        response_data = json.loads(response_text)
                    except json.JSONDecodeError as e:
                        await self.analytics.record_request(method, False, response_time, "json_decode_error")
                        raise TelegramAPIError(f"Invalid JSON response: {e}")
                    
                    if not response_data.get("ok"):
                        await self._handle_api_error(response_data, method)
                    
                    # Успешный ответ
                    method_metrics['success'] = True
                    await self.analytics.record_request(method, True, response_time)
                    await self.analytics.record_detailed_request(method_metrics)
                    
                    result = response_data.get("result")
                    
                    if not validate_response or response_model is None:
                        return result
                    
                    try:
                        return response_model.model_validate(result)
                    except ValidationError as e:
                        context_logger.error(f"Response validation failed for {method}", extra={
                            'extra_data': {'validation_error': str(e)}
                        })
                        if validate_response:
                            raise
                        return result
            
            try:
                async with self.circuit_breaker:
                    return await self.retry_strategy.execute_with_retry(make_single_request)
            
            except CircuitBreakerError as e:
                response_time = time.perf_counter() - start_time
                await self.analytics.record_request(method, False, response_time, "circuit_breaker")
                raise TelegramAPIError(f"Circuit breaker open for {method}")
            
            except Exception as e:
                response_time = time.perf_counter() - start_time
                error_type = type(e).__name__
                await self.analytics.record_request(method, False, response_time, error_type)
                
                context_logger.error(f"Request failed: {method}", extra={
                    'extra_data': {
                        'error': str(e),
                        'error_type': error_type,
                        'response_time': response_time
                    }
                })
                raise
    
    def _get_exception_class(self, error_code: int) -> Type[TelegramAPIError]:
        """Возвращает соответствующий класс исключения для кода ошибки."""
        error_map = {
            400: TelegramBadRequestError,
            401: TelegramUnauthorizedError,
            403: TelegramForbiddenError,
            404: TelegramNotFoundError,
            429: TelegramTooManyRequestsError
        }
        return error_map.get(error_code, TelegramAPIError)
    
    # --- Event System ---
    def add_event_handler(self, event_type: str, handler: Callable):
        """Добавляет обработчик события."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def remove_event_handler(self, event_type: str, handler: Callable):
        """Удаляет обработчик события."""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    async def _emit_event(self, event_type: str, data: Any):
        """Вызывает обработчики события."""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_type}", extra={
                        'extra_data': {'error': str(e)}
                    })
    
    # --- Enhanced Gift Methods ---
    async def send_gift(self, chat_id: Union[int, str], gift_id: str, **kwargs) -> Message:
        """Отправляет подарок по его ID с улучшенной валидацией."""
        params = SendGiftParams(chat_id=chat_id, gift_id=gift_id, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("sendGift", params, response_model=Message)
        await self._emit_event("gift_sent", {"chat_id": chat_id, "gift_id": gift_id})
        return result
    
    async def send_simple_gift(self, chat_id: Union[int, str], gift_id: Union[GiftAlias, str], **kwargs) -> Message:
        """Отправляет простой подарок с улучшенной обработкой."""
        if isinstance(gift_id, GiftAlias):
            gift_id_str = gift_id.value
        elif isinstance(gift_id, str):
            gift_id_str = gift_id
        else:
            raise ValueError(f"Invalid gift_id type: {type(gift_id)}")
        
        params = SendGiftParams(chat_id=chat_id, gift_id=gift_id_str, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("sendGift", params, response_model=Message)
        await self._emit_event("simple_gift_sent", {"chat_id": chat_id, "gift_id": gift_id_str})
        return result
    
    async def gift_premium_subscription(self, user_id: int, months: int, **kwargs) -> Message:
        """Дарит Premium-подписку с валидацией."""
        params = GiftPremiumParams(user_id=user_id, months=months, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("giftPremiumSubscription", params, response_model=Message)
        await self._emit_event("premium_gifted", {"user_id": user_id, "months": months})
        return result
    
    async def transfer_gift(self, recipient_user_id: int, **kwargs) -> bool:
        """Переводит подарок другому пользователю."""
        params = TransferGiftParams(recipient_user_id=recipient_user_id, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("transferGift", params)
        await self._emit_event("gift_transferred", {"recipient_user_id": recipient_user_id})
        return result
    
    async def get_star_balance(self, force_refresh: bool = False) -> int:
        """Получает баланс Stars с улучшенным кэшированием."""
        if force_refresh or await self.star_balance_cache.get("balance") is None:
            response = await self._make_request("getStarBalance", {})
            balance = response.get("stars", 0)
            await self.star_balance_cache.set("balance", balance)
            self.logger.info("Star balance retrieved from API", extra={'extra_data': {'balance': balance}})
        else:
            balance = await self.star_balance_cache.get("balance")
            self.logger.info("Star balance retrieved from cache", extra={'extra_data': {'balance': balance}})
        
        await self._emit_event("balance_checked", {"balance": balance})
        return balance
    
    async def get_available_gifts(self, force_refresh: bool = False) -> List[AvailableGift]:
        """Получает список доступных подарков с улучшенным кэшированием."""
        if force_refresh or await self.available_gifts_cache.get("gifts") is None:
            response = await self._make_request("getAvailableGifts", {})
            gifts = [AvailableGift.model_validate(g) for g in response.get("gifts", [])]
            await self.available_gifts_cache.set("gifts", gifts)
            self.logger.info("Available gifts retrieved from API", extra={'extra_data': {'count': len(gifts)}})
        else:
            gifts = await self.available_gifts_cache.get("gifts")
            self.logger.info("Available gifts retrieved from cache", extra={'extra_data': {'count': len(gifts)}})
        
        return gifts
    
    async def get_revenue_withdrawal_state(self) -> RevenueWithdrawalState:
        """Получает состояние вывода средств."""
        result = await self._make_request("getRevenueWithdrawalState", {}, response_model=RevenueWithdrawalState)
        await self._emit_event("withdrawal_state_checked", {"state": result.state})
        return result
    
    async def refund_star_payment(self, user_id: int, telegram_payment_charge_id: str) -> bool:
        """Возвращает платеж Stars."""
        params = RefundStarPaymentParams(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id
        ).model_dump(exclude_none=True)
        result = await self._make_request("refundStarPayment", params)
        await self._emit_event("payment_refunded", {"user_id": user_id, "charge_id": telegram_payment_charge_id})
        return result
    
    # --- Enhanced Message Methods ---
    async def send_message(self, chat_id: Union[int, str], text: str, **kwargs) -> Message:
        """Отправляет сообщение с улучшенной валидацией."""
        params = SendMessageParams(chat_id=chat_id, text=text, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("sendMessage", params, response_model=Message)
        await self._emit_event("message_sent", {"chat_id": chat_id, "message_id": result.message_id})
        return result
    
    async def send_message_safe(self, chat_id: Union[int, str], text: str, **kwargs) -> Optional[Message]:
        """Безопасная отправка сообщения (не вызывает исключения)."""
        try:
            return await self.send_message(chat_id, text, **kwargs)
        except TelegramAPIError as e:
            self.logger.warning(f"Failed to send message safely", extra={
                'extra_data': {'chat_id': chat_id, 'error': str(e)}
            })
            return None
    
    async def edit_message_text(self, text: str, **kwargs) -> Union[Message, bool]:
        """Редактирует текст сообщения."""
        params = EditMessageTextParams(text=text, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("editMessageText", params, response_model=Message)
        await self._emit_event("message_edited", {"text": text[:50] + "..." if len(text) > 50 else text})
        return result
    
    async def delete_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Удаляет сообщение."""
        params = DeleteMessageParams(chat_id=chat_id, message_id=message_id).model_dump(exclude_none=True)
        result = await self._make_request("deleteMessage", params)
        await self._emit_event("message_deleted", {"chat_id": chat_id, "message_id": message_id})
        return result
    
    async def forward_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], 
                            message_id: int, **kwargs) -> Message:
        """Пересылает сообщение."""
        params = ForwardMessageParams(
            chat_id=chat_id, 
            from_chat_id=from_chat_id, 
            message_id=message_id, 
            **kwargs
        ).model_dump(exclude_none=True)
        result = await self._make_request("forwardMessage", params, response_model=Message)
        await self._emit_event("message_forwarded", {
            "from_chat_id": from_chat_id, 
            "to_chat_id": chat_id, 
            "message_id": message_id
        })
        return result
    
    async def answer_inline_query(self, inline_query_id: str, results: List[Dict], **kwargs) -> bool:
        """Отвечает на inline-запрос."""
        params = AnswerInlineQueryParams(
            inline_query_id=inline_query_id, 
            results=results, 
            **kwargs
        ).model_dump(exclude_none=True)
        result = await self._make_request("answerInlineQuery", params)
        await self._emit_event("inline_query_answered", {"query_id": inline_query_id})
        return result
    
    # --- Enhanced Updates and Webhook Methods ---
    async def get_updates(self, offset: Optional[int] = None, limit: Optional[int] = None,
                          timeout: Optional[int] = None, allowed_updates: Optional[List[str]] = None) -> List[Update]:
        """Получает обновления с улучшенной обработкой."""
        params = GetUpdatesParams(
            offset=offset,
            limit=limit,
            timeout=timeout if timeout is not None else 60,
            allowed_updates=allowed_updates
        ).model_dump(exclude_none=True)
        result = await self._make_request("getUpdates", params)
        updates = [Update.model_validate(upd) for upd in result]
        
        for update in updates:
            await self._emit_event("update_received", update)
        
        return updates
    
    async def updates_stream(self, timeout: int = 60, limit: int = 100,
                           allowed_updates: Optional[List[str]] = None,
                           error_handler: Optional[Callable] = None) -> AsyncIterator[Update]:
        """Улучшенный поток обновлений с обработкой ошибок."""
        offset = None
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        self.logger.info("Starting updates stream", extra={
            'extra_data': {'timeout': timeout, 'limit': limit}
        })
        
        while True:
            try:
                updates = await self.get_updates(
                    offset=offset,
                    limit=limit,
                    timeout=timeout,
                    allowed_updates=allowed_updates
                )
                
                consecutive_errors = 0  # Сбрасываем счетчик ошибок
                
                if updates:
                    for update in updates:
                        yield update
                        if offset is None or update.update_id >= offset:
                            offset = update.update_id + 1
                else:
                    self.logger.debug("No new updates")
            
            except TelegramTooManyRequestsError as e:
                consecutive_errors += 1
                retry_after = e.retry_after or 10
                self.logger.warning(f"Rate limited in updates stream, waiting {retry_after}s")
                await asyncio.sleep(retry_after)
            
            except TelegramAPIError as e:
                consecutive_errors += 1
                self.logger.error(f"API error in updates stream: {e.description}")
                
                if error_handler:
                    try:
                        await error_handler(e)
                    except Exception as handler_error:
                        self.logger.error(f"Error in error handler: {handler_error}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.critical("Too many consecutive errors, stopping updates stream")
                    break
                
                await asyncio.sleep(min(5 * consecutive_errors, 60))
            
            except Exception as e:
                consecutive_errors += 1
                self.logger.critical(f"Unexpected error in updates stream: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    break
                
                await asyncio.sleep(min(10 * consecutive_errors, 120))
    
    async def set_webhook(self, url: str, **kwargs) -> bool:
        """Устанавливает webhook с валидацией."""
        params = SetWebhookParams(url=url, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("setWebhook", params)
        await self._emit_event("webhook_set", {"url": url})
        return result
    
    async def delete_webhook(self, **kwargs) -> bool:
        """Удаляет webhook."""
        params = DeleteWebhookParams(**kwargs).model_dump(exclude_none=True)
        result = await self._make_request("deleteWebhook", params)
        await self._emit_event("webhook_deleted", {})
        return result
    
    async def get_webhook_info(self) -> WebhookInfo:
        """Получает информацию о webhook."""
        return await self._make_request("getWebhookInfo", {}, response_model=WebhookInfo)
    
    # --- Enhanced Chat Methods ---
    async def get_chat(self, chat_id: Union[int, str], force_refresh: bool = False) -> Chat:
        """Получает информацию о чате с кэшированием."""
        if force_refresh or await self.chat_cache.get(chat_id) is None:
            params = GetChatParams(chat_id=chat_id).model_dump(exclude_none=True)
            result = await self._make_request("getChat", params, response_model=Chat)
            await self.chat_cache.set(chat_id, result)
            self.logger.info(f"Chat info retrieved from API", extra={'extra_data': {'chat_id': chat_id}})
        else:
            result = await self.chat_cache.get(chat_id)
            self.logger.info(f"Chat info retrieved from cache", extra={'extra_data': {'chat_id': chat_id}})
        
        return result
    
    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[AnyChatMember]:
        """Получает администраторов чата."""
        params = GetChatAdministratorsParams(chat_id=chat_id).model_dump(exclude_none=True)
        result = await self._make_request("getChatAdministrators", params)
        
        members = []
        for member_data in result:
            status = member_data.get('status')
            if status == 'creator':
                members.append(ChatMemberOwner.model_validate(member_data))
            elif status == 'administrator':
                members.append(ChatMemberAdministrator.model_validate(member_data))
            else:
                members.append(ChatMember.model_validate(member_data))
        
        return members
    
    async def kick_chat_member(self, chat_id: Union[int, str], user_id: int, **kwargs) -> bool:
        """Исключает участника из чата."""
        params = KickChatMemberParams(chat_id=chat_id, user_id=user_id, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("kickChatMember", params)
        await self._emit_event("member_kicked", {"chat_id": chat_id, "user_id": user_id})
        return result
    
    async def unban_chat_member(self, chat_id: Union[int, str], user_id: int, **kwargs) -> bool:
        """Разбанивает участника чата."""
        params = UnbanChatMemberParams(chat_id=chat_id, user_id=user_id, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("unbanChatMember", params)
        await self._emit_event("member_unbanned", {"chat_id": chat_id, "user_id": user_id})
        return result
    
    # --- Enhanced Checklist Methods ---
    async def send_checklist(self, chat_id: Union[int, str], checklist: InputChecklist, **kwargs) -> Message:
        """Отправляет чеклист."""
        params = SendChecklistParams(chat_id=chat_id, checklist=checklist, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("sendChecklist", params, response_model=Message)
        await self._emit_event("checklist_sent", {"chat_id": chat_id, "title": checklist.title})
        return result
    
    async def edit_message_checklist(self, checklist: InputChecklist, **kwargs) -> Message:
        """Редактирует чеклист."""
        params = EditMessageChecklistParams(checklist=checklist, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("editMessageChecklist", params, response_model=Message)
        await self._emit_event("checklist_edited", {"title": checklist.title})
        return result
    
    # --- New Enhanced Methods ---
    async def get_bot_info(self) -> User:
        """Получает информацию о боте."""
        return await self._make_request("getMe", {}, response_model=User)
    
    async def get_file(self, file_id: str) -> Dict:
        """Получает информацию о файле."""
        params = {"file_id": file_id}
        return await self._make_request("getFile", params)
    
    async def download_file(self, file_path: str) -> bytes:
        """Скачивает файл."""
        url = f"https://api.telegram.org/file/bot{self.token.get_secret_value()}/{file_path}"
        
        session = await self.connection_pool.get_session(url)
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise TelegramAPIError(f"Failed to download file: {response.status}")
    
    async def upload_file_chunked(self, file_path: str, chunk_size: int = 1024*1024) -> str:
        """Загрузка больших файлов по частям."""
        # Реализация chunked upload для больших файлов
        file_size = os.path.getsize(file_path)
        
        if file_size <= chunk_size:
            # Обычная загрузка для маленьких файлов
            with open(file_path, 'rb') as f:
                return await self.send_document(chat_id="@channel", document=f.read())
        
        # Chunked upload для больших файлов
        chunks = []
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
        
        # Загружаем по частям (упрощенная реализация)
        for i, chunk in enumerate(chunks):
            self.logger.info(f"Uploading chunk {i+1}/{len(chunks)}")
            # Здесь должна быть логика загрузки частей
        
        return "file_uploaded"
    
    async def send_photo(self, chat_id: Union[int, str], photo: Union[str, bytes], **kwargs) -> Message:
        """Отправляет фото."""
        params = {"chat_id": chat_id, "photo": photo, **kwargs}
        return await self._make_request("sendPhoto", params, response_model=Message)
    
    async def send_document(self, chat_id: Union[int, str], document: Union[str, bytes], **kwargs) -> Message:
        """Отправляет документ."""
        params = {"chat_id": chat_id, "document": document, **kwargs}
        return await self._make_request("sendDocument", params, response_model=Message)
    
    async def get_chat_member_count(self, chat_id: Union[int, str]) -> int:
        """Получает количество участников чата."""
        params = {"chat_id": chat_id}
        result = await self._make_request("getChatMemberCount", params)
        return result
    
    async def set_chat_title(self, chat_id: Union[int, str], title: str) -> bool:
        """Устанавливает название чата."""
        params = {"chat_id": chat_id, "title": title}
        result = await self._make_request("setChatTitle", params)
        await self._emit_event("chat_title_changed", {"chat_id": chat_id, "title": title})
        return result
    
    async def set_chat_description(self, chat_id: Union[int, str], description: str) -> bool:
        """Устанавливает описание чата."""
        params = {"chat_id": chat_id, "description": description}
        result = await self._make_request("setChatDescription", params)
        await self._emit_event("chat_description_changed", {"chat_id": chat_id})
        return result
    
    async def pin_chat_message(self, chat_id: Union[int, str], message_id: int, 
                              disable_notification: bool = False) -> bool:
        """Закрепляет сообщение в чате."""
        params = {
            "chat_id": chat_id,
            "message_id": message_id,
            "disable_notification": disable_notification
        }
        result = await self._make_request("pinChatMessage", params)
        await self._emit_event("message_pinned", {"chat_id": chat_id, "message_id": message_id})
        return result
    
    async def unpin_chat_message(self, chat_id: Union[int, str], message_id: Optional[int] = None) -> bool:
        """Открепляет сообщение в чате."""
        params = {"chat_id": chat_id}
        if message_id:
            params["message_id"] = message_id
        
        result = await self._make_request("unpinChatMessage", params)
        await self._emit_event("message_unpinned", {"chat_id": chat_id, "message_id": message_id})
        return result
    
    async def leave_chat(self, chat_id: Union[int, str]) -> bool:
        """Покидает чат."""
        params = {"chat_id": chat_id}
        result = await self._make_request("leaveChat", params)
        await self._emit_event("chat_left", {"chat_id": chat_id})
        return result
    
    # --- Business Connection Methods ---
    async def get_business_connection(self, business_connection_id: str) -> Dict:
        """Получает информацию о бизнес-соединении."""
        params = {"business_connection_id": business_connection_id}
        return await self._make_request("getBusinessConnection", params)
    
    async def hide_keyboard(self, **kwargs) -> bool:
        """Скрывает клавиатуру в Web App."""
        params = HideKeyboardParams(**kwargs).model_dump(exclude_none=True)
        return await self._make_request("hideKeyboard", params)
    
    # --- Enhanced Batch Operations ---
    async def batch_send_gifts(self, operations: List[Dict], max_concurrent: int = 5) -> List[Dict]:
        """Массовая отправка подарков с ограничением concurrency."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def send_single_gift(operation):
            async with semaphore:
                try:
                    return await self.send_gift(**operation)
                except Exception as e:
                    return {"error": str(e), "operation": operation}
        
        tasks = [send_single_gift(op) for op in operations]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Логируем результаты
        success_count = sum(1 for r in results if not isinstance(r, Exception) and "error" not in r)
        self.logger.info(f"Batch gift operation completed", extra={
            'extra_data': {
                'total': len(operations),
                'success': success_count,
                'failed': len(operations) - success_count
            }
        })
        
        return results
    
    async def bulk_send_message(self, chat_ids: List[Union[int, str]], text: str, 
                               delay: float = 0.1, **kwargs) -> List[Optional[Message]]:
        """Массовая отправка сообщений с контролем скорости."""
        results = []
        
        for i, chat_id in enumerate(chat_ids):
            try:
                message = await self.send_message(chat_id, text, **kwargs)
                results.append(message)
                
                # Прогресс для больших списков
                if len(chat_ids) > 100 and (i + 1) % 50 == 0:
                    self.logger.info(f"Bulk send progress: {i+1}/{len(chat_ids)}")
                
            except Exception as e:
                self.logger.warning(f"Failed to send bulk message to {chat_id}: {e}")
                results.append(None)
            
            if delay > 0:
                await asyncio.sleep(delay)
        
        # Финальная статистика
        success_count = sum(1 for r in results if r is not None)
        self.logger.info(f"Bulk message operation completed", extra={
            'extra_data': {
                'total': len(chat_ids),
                'success': success_count,
                'failed': len(chat_ids) - success_count
            }
        })
        
        return results
    
    # --- Enhanced Utility Methods ---
    def get_analytics(self) -> Dict:
        """Возвращает расширенную аналитику бота."""
        analytics = self.analytics.get_stats()
        
        # Добавляем статистику кэшей
        analytics['caches'] = {
            'gifts_cache': self.available_gifts_cache.get_stats(),
            'balance_cache': self.star_balance_cache.get_stats(),
            'chat_cache': self.chat_cache.get_stats()
        }
        
        # Добавляем статистику безопасности
        analytics['security'] = self.security_manager.get_stats()
        
        return analytics
    
    async def detailed_health_check(self) -> Dict:
        """Детальная проверка здоровья системы."""
        checks = {}
        
        # Проверка API соединения
        try:
            start_time = time.time()
            bot_info = await self.get_bot_info()
            checks['api_connection'] = {
                'status': 'healthy',
                'response_time': time.time() - start_time,
                'bot_username': bot_info.username,
                'bot_id': bot_info.id
            }
        except Exception as e:
            checks['api_connection'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # Проверка кэшей
        checks['caches'] = {
            'gifts_cache': self.available_gifts_cache.get_stats(),
            'balance_cache': self.star_balance_cache.get_stats(),
            'chat_cache': self.chat_cache.get_stats()
        }
        
        # Проверка безопасности
        checks['security'] = self.security_manager.get_stats()
        
        # Проверка circuit breaker
        checks['circuit_breaker'] = {
            'state': self.circuit_breaker.current_state,
            'failure_count': self.circuit_breaker.fail_counter,
            'last_failure_time': getattr(self.circuit_breaker, 'last_failure_time', None)
        }
        
        # Общий статус
        overall_healthy = all(
            check.get('status') == 'healthy' 
            for check in checks.values() 
            if 'status' in check
        )
        
        return {
            'overall_status': 'healthy' if overall_healthy else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'checks': checks,
            'analytics': self.get_analytics()
        }
    
    async def health_check(self) -> Dict:
        """Быстрая проверка состояния бота."""
        try:
            bot_info = await self.get_bot_info()
            return {
                "status": "healthy",
                "bot_username": bot_info.username,
                "bot_id": bot_info.id,
                "analytics": self.get_analytics(),
                "circuit_breaker_state": self.circuit_breaker.current_state
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "analytics": self.get_analytics(),
                "circuit_breaker_state": self.circuit_breaker.current_state
            }
    
    async def export_metrics(self, format: str = 'prometheus') -> str:
        """Экспорт метрик в различных форматах."""
        stats = self.get_analytics()
        
        if format == 'prometheus':
            return f"""
# HELP telegram_requests_total Total number of requests
# TYPE telegram_requests_total counter
telegram_requests_total {stats['requests_total']}

# HELP telegram_requests_success_total Successful requests
# TYPE telegram_requests_success_total counter  
telegram_requests_success_total {stats['requests_success']}

# HELP telegram_requests_failed_total Failed requests
# TYPE telegram_requests_failed_total counter
telegram_requests_failed_total {stats['requests_failed']}

# HELP telegram_messages_sent_total Messages sent
# TYPE telegram_messages_sent_total counter
telegram_messages_sent_total {stats['messages_sent']}

# HELP telegram_gifts_sent_total Gifts sent
# TYPE telegram_gifts_sent_total counter
telegram_gifts_sent_total {stats['gifts_sent']}

# HELP telegram_average_response_time Average response time in seconds
# TYPE telegram_average_response_time gauge
telegram_average_response_time {stats['average_response_time']}

# HELP telegram_success_rate Success rate percentage
# TYPE telegram_success_rate gauge
telegram_success_rate {stats['success_rate']}
"""
        elif format == 'json':
            return json.dumps(stats, cls=TelegramJSONEncoder, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def add_webhook_validator(self, validator: Callable[[Dict], bool]):
        """Добавляет валидатор для webhook."""
        self._webhook_validators.append(validator)
    
    def validate_webhook_data(self, data: Dict) -> bool:
        """Проверяет данные webhook."""
        # Базовая валидация
        if not isinstance(data, dict) or 'update_id' not in data:
            return False
        
        # Кастомные валидаторы
        for validator in self._webhook_validators:
            try:
                if not validator(data):
                    return False
            except Exception as e:
                self.logger.error(f"Webhook validator error: {e}")
                return False
        
        return True