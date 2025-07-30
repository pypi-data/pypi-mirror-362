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


# --- Security Configuration ---
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


# --- Rate Limiter ---
class RateLimiter:
    """Продвинутый rate limiter с поддержкой различных стратегий."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """Проверяет, можно ли выполнить запрос."""
        async with self._lock:
            now = time.time()
            # Удаляем старые запросы
            self.requests = [req_time for req_time in self.requests 
                           if now - req_time < self.window_seconds]
            
            if len(self.requests) >= self.max_requests:
                return False
            
            self.requests.append(now)
            return True
    
    async def wait_if_needed(self):
        """Ждет, если превышен лимит запросов."""
        while not await self.acquire():
            await asyncio.sleep(0.1)


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


# --- Enhanced Pydantic Models ---
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
        if v <= 0:
            raise ValueError('User ID must be positive')
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

class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None

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

class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumbnail: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

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

# --- Enhanced Parameter Models ---
class SendGiftParams(BaseModel):
    chat_id: Union[int, str]
    gift_id: str
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    
    @field_validator('chat_id')
    @classmethod
    def validate_chat_id(cls, v):
        if isinstance(v, int) and v == 0:
            raise ValueError('Chat ID cannot be 0')
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
        
        data = f"{method}:{json.dumps(params, sort_keys=True)}"
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


# --- Enhanced Analytics ---
class BotAnalytics:
    """Аналитика для бота."""
    
    def __init__(self):
        self.stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'messages_sent': 0,
            'gifts_sent': 0,
            'errors_by_type': {},
            'response_times': [],
            'start_time': datetime.now()
        }
        self._lock = asyncio.Lock()
    
    async def record_request(self, method: str, success: bool, response_time: float, error_type: str = None):
        """Записывает статистику запроса."""
        async with self._lock:
            self.stats['requests_total'] += 1
            if success:
                self.stats['requests_success'] += 1
            else:
                self.stats['requests_failed'] += 1
                if error_type:
                    self.stats['errors_by_type'][error_type] = self.stats['errors_by_type'].get(error_type, 0) + 1
            
            self.stats['response_times'].append(response_time)
            if len(self.stats['response_times']) > 1000:  # Ограничиваем размер
                self.stats['response_times'] = self.stats['response_times'][-500:]
            
            if method == 'sendMessage':
                self.stats['messages_sent'] += 1
            elif method == 'sendGift':
                self.stats['gifts_sent'] += 1
    
    def get_stats(self) -> Dict:
        """Возвращает статистику."""
        uptime = datetime.now() - self.stats['start_time']
        avg_response_time = sum(self.stats['response_times']) / len(self.stats['response_times']) if self.stats['response_times'] else 0
        
        return {
            **self.stats,
            'uptime_seconds': uptime.total_seconds(),
            'average_response_time': avg_response_time,
            'success_rate': self.stats['requests_success'] / max(self.stats['requests_total'], 1) * 100
        }


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
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_refs = weakref.WeakSet()
        
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
        
        # Кэши с улучшенной безопасностью
        self.available_gifts_cache = TTLCache(maxsize=1, ttl=3600)
        self.star_balance_cache = TTLCache(maxsize=1, ttl=300)
        self.chat_cache = TTLCache(maxsize=1000, ttl=3600)
        
        # Обработчики событий
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Webhook валидация
        self._webhook_validators = []
    
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
                    return json.dumps(log_data, ensure_ascii=False)
            
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
    
    async def _ensure_session(self):
        """Создает защищенную сессию aiohttp."""
        if self._session is None or self._session.closed:
            # Настройка SSL контекста
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            # Настройка коннектора
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300,
                use_dns_cache=True,
                enable_cleanup_closed=True
            )
            
            # Настройка таймаутов
            timeout = aiohttp.ClientTimeout(
                total=self.request_timeout * self.security_config.request_timeout_multiplier,
                connect=self.conn_timeout,
                sock_read=30
            )
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'CustomGiftSend/2.0 (Enhanced Security)',
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate'
                }
            )
            self._session_refs.add(self._session)
    
    async def close(self):
        """Безопасно закрывает все ресурсы."""
        if self._session and not self._session.closed:
            await self._session.close()
            self.logger.info("Session closed safely")
        
        # Очищаем кэши
        self.available_gifts_cache.clear()
        self.star_balance_cache.clear()
        self.chat_cache.clear()
        
        # Сохраняем статистику
        stats = self.analytics.get_stats()
        self.logger.info("Final statistics", extra={'extra_data': stats})
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def _make_request(self, method: str, params: Dict, 
                          response_model: Optional[Type[BaseModel]] = None,
                          validate_response: bool = True) -> Any:
        """
        Улучшенный метод для выполнения HTTP запросов с повышенной безопасностью.
        """
        start_time = time.time()
        
        # Проверка лимита запросов
        await self.security_manager.wait_for_rate_limit()
        
        # Ограничение concurrent запросов
        async with self._semaphore:
            await self._ensure_session()
            
            # Генерация подписи запроса
            signature = self.security_manager.generate_request_signature(method, params)
            
            # Логирование запроса (без чувствительных данных)
            safe_params = {k: v for k, v in params.items() if k not in ['token', 'certificate']}
            self.logger.info(f"Making request to {method}", extra={
                'extra_data': {
                    'method': method,
                    'params_keys': list(safe_params.keys()),
                    'signature': signature[:8] + '...' if signature else None
                }
            })
            
            last_exception = None
            
            for attempt in range(self.max_retries):
                try:
                    async with self.circuit_breaker:
                        # Проверка размера запроса
                        request_size = len(json.dumps(params).encode())
                        if request_size > self.security_config.max_request_size:
                            raise SecurityError(f"Request size {request_size} exceeds limit")
                        
                        async with self._session.post(
                            f"{self.base_url}/{method}",
                            json=params,
                            headers={'X-Request-Signature': signature} if signature else {}
                        ) as response:
                            response_time = time.time() - start_time
                            response_text = await response.text()
                            
                            # Проверка размера ответа
                            if len(response_text) > self.security_config.max_request_size:
                                raise SecurityError("Response size exceeds limit")
                            
                            try:
                                response_data = json.loads(response_text)
                            except json.JSONDecodeError as e:
                                await self.analytics.record_request(method, False, response_time, "json_decode_error")
                                raise TelegramAPIError(f"Invalid JSON response: {e}")
                            
                            if not response_data.get("ok"):
                                error_code = response_data.get("error_code")
                                description = response_data.get("description", "Unknown error")
                                parameters = response_data.get("parameters", {})
                                
                                await self.analytics.record_request(method, False, response_time, f"api_error_{error_code}")
                                
                                # Создаем соответствующее исключение
                                exception_class = self._get_exception_class(error_code)
                                if error_code == 429:
                                    retry_after = parameters.get("retry_after", 1)
                                    raise exception_class(description, error_code, description, response_data, retry_after)
                                else:
                                    raise exception_class(description, error_code, description, response_data)
                            
                            # Успешный ответ
                            await self.analytics.record_request(method, True, response_time)
                            result = response_data.get("result")
                            
                            if not validate_response or response_model is None:
                                return result
                            
                            try:
                                return response_model.model_validate(result)
                            except ValidationError as e:
                                self.logger.error(f"Response validation failed for {method}", extra={
                                    'extra_data': {'validation_error': str(e)}
                                })
                                if validate_response:
                                    raise
                                return result
                
                except CircuitBreakerError as e:
                    await self.analytics.record_request(method, False, time.time() - start_time, "circuit_breaker")
                    raise TelegramAPIError(f"Circuit breaker open for {method}")
                
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    last_exception = e
                    response_time = time.time() - start_time
                    await self.analytics.record_request(method, False, response_time, type(e).__name__)
                    
                    if attempt == self.max_retries - 1:
                        break
                    
                    delay = self.retry_delay * (2 ** attempt) + secrets.randbelow(1000) / 1000
                    self.logger.warning(f"Request failed, retrying in {delay}s", extra={
                        'extra_data': {
                            'method': method,
                            'attempt': attempt + 1,
                            'error': str(e),
                            'delay': delay
                        }
                    })
                    await asyncio.sleep(delay)
                
                except TelegramTooManyRequestsError as e:
                    if attempt == self.max_retries - 1:
                        raise
                    
                    retry_after = e.retry_after or self.retry_delay * (2 ** attempt)
                    self.logger.warning(f"Rate limited, waiting {retry_after}s", extra={
                        'extra_data': {'method': method, 'retry_after': retry_after}
                    })
                    await asyncio.sleep(retry_after)
                
                except TelegramAPIError:
                    raise  # Пробрасываем API ошибки без повторов
                
                except Exception as e:
                    last_exception = e
                    response_time = time.time() - start_time
                    await self.analytics.record_request(method, False, response_time, "unexpected_error")
                    
                    self.logger.error(f"Unexpected error in {method}", extra={
                        'extra_data': {
                            'error': str(e),
                            'error_type': type(e).__name__,
                            'attempt': attempt + 1
                        }
                    })
                    
                    if attempt == self.max_retries - 1:
                        break
                    
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
            
            # Если дошли сюда, значит все попытки исчерпаны
            if last_exception:
                raise TelegramAPIError(f"All retry attempts failed for {method}: {last_exception}")
            else:
                raise TelegramAPIError(f"Unknown error in {method}")
    
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
        if force_refresh or "balance" not in self.star_balance_cache:
            response = await self._make_request("getStarBalance", {})
            balance = response.get("stars", 0)
            self.star_balance_cache["balance"] = balance
            self.logger.info("Star balance retrieved from API", extra={'extra_data': {'balance': balance}})
        else:
            balance = self.star_balance_cache["balance"]
            self.logger.info("Star balance retrieved from cache", extra={'extra_data': {'balance': balance}})
        
        await self._emit_event("balance_checked", {"balance": balance})
        return balance
    
    async def get_available_gifts(self, force_refresh: bool = False) -> List[AvailableGift]:
        """Получает список доступных подарков с улучшенным кэшированием."""
        if force_refresh or "gifts" not in self.available_gifts_cache:
            response = await self._make_request("getAvailableGifts", {})
            gifts = [AvailableGift.model_validate(g) for g in response.get("gifts", [])]
            self.available_gifts_cache["gifts"] = gifts
            self.logger.info("Available gifts retrieved from API", extra={'extra_data': {'count': len(gifts)}})
        else:
            gifts = self.available_gifts_cache["gifts"]
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
        if force_refresh or chat_id not in self.chat_cache:
            params = GetChatParams(chat_id=chat_id).model_dump(exclude_none=True)
            result = await self._make_request("getChat", params, response_model=Chat)
            self.chat_cache[chat_id] = result
            self.logger.info(f"Chat info retrieved from API", extra={'extra_data': {'chat_id': chat_id}})
        else:
            result = self.chat_cache[chat_id]
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
        
        async with self._session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise TelegramAPIError(f"Failed to download file: {response.status}")
    
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
    
    # --- Utility Methods ---
    def get_analytics(self) -> Dict:
        """Возвращает аналитику бота."""
        return self.analytics.get_stats()
    
    async def health_check(self) -> Dict:
        """Проверяет состояние бота."""
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
    
    async def bulk_send_message(self, chat_ids: List[Union[int, str]], text: str, 
                               delay: float = 0.1, **kwargs) -> List[Optional[Message]]:
        """Массовая отправка сообщений с контролем скорости."""
        results = []
        
        for chat_id in chat_ids:
            try:
                message = await self.send_message(chat_id, text, **kwargs)
                results.append(message)
            except Exception as e:
                self.logger.warning(f"Failed to send bulk message to {chat_id}: {e}")
                results.append(None)
            
            if delay > 0:
                await asyncio.sleep(delay)
        
        return results
    
    def add_webhook_validator(self, validator: Callable[[Dict], bool]):
        """Добавляет валидатор для webhook."""
        self._webhook_validators.append(validator)
    
    def validate_webhook_data(self, data: Dict) -> bool:
        """Проверяет данные webhook."""
        for validator in self._webhook_validators:
            if not validator(data):
                return False
        return True