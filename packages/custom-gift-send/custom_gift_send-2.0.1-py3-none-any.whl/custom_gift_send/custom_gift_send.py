import aiohttp
import configparser
import logging
import asyncio
import os
import json
from logging import Formatter
from enum import Enum
from pybreaker import CircuitBreaker, CircuitBreakerError
from pybreaker.storage import CircuitBreakerStorage
from pybreaker.storage.memory import CircuitBreakerMemoryStorage
from typing import Dict, Optional, Type, Any, Union, List, Literal, AsyncIterator
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict
from datetime import datetime
from cachetools import TTLCache


# --- Custom Exceptions for Telegram API Errors ---
class TelegramAPIError(Exception):
    """Base exception for Telegram API errors."""
    def __init__(self, message: str, error_code: Optional[int] = None, description: Optional[str] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.response_data = response_data

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
    def __init__(self, message: str, error_code: int, description: str, retry_after: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message, error_code, description, response_data)
        self.retry_after = retry_after


# --- Enums ---
class GiftAlias(str, Enum):
    """
    Enum для псевдонимов подарков, упрощающий выбор gift_id.
    """
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


# --- Pydantic Models for Telegram API types ---
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

class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

class Chat(BaseModel):
    id: int
    type: str
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

    model_config = ConfigDict(populate_by_name=True)

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

AnyChatMember = Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned]

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

class SendGiftParams(BaseModel):
    chat_id: Union[int, str]
    gift_id: str
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class GiftPremiumParams(BaseModel):
    user_id: int
    months: int
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class TransferGiftParams(BaseModel):
    recipient_user_id: int
    message_thread_id: Optional[int] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class GetUpdatesParams(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None
    timeout: Optional[int] = None
    allowed_updates: Optional[List[str]] = None

class SetWebhookParams(BaseModel):
    url: str
    certificate: Optional[Any] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None

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
    text: str
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
    text: str
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


# --- Main CustomGiftSend Class ---
class CustomGiftSend:
    """
    Асинхронный клиент для Telegram Bot API с поддержкой подарков, Stars,
    списков задач и других функций версии 9.1.
    """
    def __init__(self, token: str, config_path: Optional[str] = None,
                 base_url: str = "https://api.telegram.org/bot",
                 max_retries: int = 5, retry_delay: int = 2,
                 conn_timeout: int = 10, request_timeout: int = 60):
        """
        Инициализирует клиент Telegram Bot API.

        Args:
            token (str): Токен вашего бота Telegram.
            config_path (Optional[str]): Путь к файлу конфигурации INI.
            base_url (str): Базовый URL для запросов к Telegram API.
            max_retries (int): Максимальное количество попыток повторной отправки.
            retry_delay (int): Начальная задержка (в секундах) между попытками.
            conn_timeout (int): Таймаут соединения aiohttp в секундах.
            request_timeout (int): Общий таймаут запроса aiohttp в секундах.
        """
        self.token = self._load_token(token, config_path)
        self.base_url = f"{base_url}{self.token}"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.conn_timeout = conn_timeout
        self.request_timeout = request_timeout
        self._session: Optional[aiohttp.ClientSession] = None

        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Создаем стандартный форматтер
        log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
        formatter = Formatter(log_format)

        # Проверяем, есть ли уже обработчики, чтобы избежать дублирования
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # Дополнительно: настроить логирование для aiohttp
        aiohttp_logger = logging.getLogger('aiohttp.client')
        if not aiohttp_logger.handlers:
            aiohttp_logger.setLevel(logging.WARNING)
            aiohttp_logger.addHandler(ch)

        # Настройка Circuit Breaker
        fail_exceptions = (
            TelegramBadRequestError,
            TelegramForbiddenError,
            TelegramNotFoundError,
            aiohttp.ClientError
        )
        self.breaker_storage: CircuitBreakerStorage = CircuitBreakerMemoryStorage()
        self.circuit_breaker = CircuitBreaker(
            fail_max=5,
            reset_timeout=60,
            exclude=TelegramTooManyRequestsError,
            fail_exceptions=fail_exceptions,
            storage=self.breaker_storage
        )
        self.circuit_breaker.add_listener(self._circuit_breaker_listener)

        self.available_gifts_cache = TTLCache(maxsize=1, ttl=3600)
        self.star_balance_cache = TTLCache(maxsize=1, ttl=300)

    def _circuit_breaker_listener(self, *args, **kwargs):
        """Слушатель для логирования событий Circuit Breaker."""
        event_name = kwargs.get('event_name')
        if event_name == 'state_change':
            old_state = kwargs.get('old_state')
            new_state = kwargs.get('new_state')
            self.logger.warning(f"Circuit Breaker: Изменение состояния с {old_state} на {new_state}")
        elif event_name == 'failure':
            exc = kwargs.get('exception')
            self.logger.warning(f"Circuit Breaker: Отказ операции - {exc}")
        elif event_name == 'success':
            self.logger.info("Circuit Breaker: Успешная операция")

    def _load_token(self, token: str, config_path: Optional[str]) -> str:
        """
        Загружает токен бота из файла конфигурации или использует переданный.
        """
        if config_path:
            try:
                config = configparser.ConfigParser()
                config.read(config_path)
                return config['telegram']['bot_token']
            except (configparser.Error, KeyError):
                self.logger.error("Не удалось прочитать токен из файла конфигурации.")
                raise ValueError("Ошибка: Неверный путь к файлу конфигурации или отсутствует секция [telegram] с bot_token.")
        elif token:
            return token
        else:
            raise ValueError("Токен бота не предоставлен. Укажите его напрямую или через config_path.")

    async def _ensure_session(self):
        """
        Гарантирует, что сессия aiohttp активна.
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close(self):
        """
        Закрывает сессию aiohttp.
        """
        if self._session:
            await self._session.close()
            self.logger.info("Сессия aiohttp закрыта.")

    async def _make_request(self, method: str, params: Dict, response_model: Optional[Type[BaseModel]] = None) -> Any:
        """
        Выполняет HTTP POST запрос к Telegram Bot API.

        Args:
            method (str): Метод API Telegram (например, 'sendMessage').
            params (Dict): Словарь параметров для запроса.
            response_model (Optional[Type[BaseModel]]): Модель Pydantic для валидации ответа.

        Returns:
            Any: Распарсенный ответ от API, либо валидированный объект модели.

        Raises:
            TelegramAPIError: В случае ошибок Telegram API или сетевых ошибок.
            ValidationError: Если ответ API не соответствует Pydantic модели.
        """
        await self._ensure_session()
        self.logger.info(f"Отправка запроса: {method}, params: {list(params.keys())}")

        for attempt in range(self.max_retries):
            try:
                async with self.circuit_breaker:
                    async with self._session.post(
                        f"{self.base_url}/{method}",
                        json=params,
                        timeout=aiohttp.ClientTimeout(
                            connect=self.conn_timeout,
                            total=self.request_timeout
                        )
                    ) as response:
                        response_text = await response.text()
                        try:
                            response_data = json.loads(response_text)
                        except json.JSONDecodeError:
                            self.logger.error(f"Не удалось декодировать JSON ответ от {method}: {response_text[:500]}")
                            raise TelegramAPIError(f"Неверный JSON ответ от API: {response_text}", response_data=response_text)

                        if not response_data.get("ok"):
                            error_code = response_data.get("error_code")
                            description = response_data.get("description", "Неизвестная ошибка")
                            parameters = response_data.get("parameters", {})

                            if error_code == 401:
                                raise TelegramUnauthorizedError(f"Ошибка: {description}", error_code, description, response_data)
                            elif error_code == 403:
                                raise TelegramForbiddenError(f"Ошибка: {description}", error_code, description, response_data)
                            elif error_code == 404:
                                raise TelegramNotFoundError(f"Ошибка: {description}", error_code, description, response_data)
                            elif error_code == 429:
                                retry_after = parameters.get("retry_after")
                                raise TelegramTooManyRequestsError(f"Ошибка: {description}. Повтор через {retry_after} секунд.", error_code, description, retry_after, response_data)
                            elif error_code == 400:
                                self.logger.warning(f"Bad Request: {description}. Parameters: {parameters}")
                                raise TelegramBadRequestError(f"Ошибка: {description}. Параметры: {parameters}", error_code, description, response_data)
                            else:
                                raise TelegramAPIError(f"Неизвестная ошибка Telegram API: {description} (Код: {error_code})", error_code, description, response_data)
                        else:
                            self.logger.info(f"Получен ответ от {method}: status={response.status}, ok={response_data.get('ok')}")
                            result = response_data.get("result")
                            if response_model is None:
                                return result
                            try:
                                return response_model.model_validate(result)
                            except ValidationError as e:
                                self.logger.error(f"Ошибка валидации Pydantic для {method}: {e}")
                                raise ValidationError(f"Ошибка валидации ответа API для {method}: {e}") from e

            except CircuitBreakerError as e:
                self.logger.warning(f"Circuit Breaker разомкнут для {method}: {e}")
                raise TelegramAPIError(f"Запрос отклонён Circuit Breaker: {method}. Цепь разомкнута.", response_data=None) from e
            except aiohttp.ClientError as e:
                self.logger.warning(f"Ошибка HTTP клиента для {method}, попытка {attempt + 1}/{self.max_retries}: {e}")
                if attempt == self.max_retries - 1:
                    raise TelegramAPIError(f"Не удалось выполнить запрос после {self.max_retries} попыток: {method} - {e}", response_data=None) from e
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
            except asyncio.TimeoutError:
                self.logger.warning(f"Таймаут запроса для {method}, попытка {attempt + 1}/{self.max_retries}")
                if attempt == self.max_retries - 1:
                    raise TelegramAPIError(f"Запрос {method} превысил таймаут после {self.max_retries} попыток.", response_data=None)
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
            except TelegramAPIError as e:
                if not isinstance(e, TelegramTooManyRequestsError):
                    self.logger.error(f"Telegram API ошибка для {method}: {e.description} (Код: {e.error_code})")
                if not isinstance(e, TelegramTooManyRequestsError) or attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(e.retry_after if e.retry_after else self.retry_delay * (2 ** attempt))
            except Exception as e:
                self.logger.critical(f"Неизвестная критическая ошибка при запросе {method}: {e}")
                raise

        raise TelegramAPIError(f"Неизвестная ошибка: _make_request для {method} не вернул результат.", response_data=None)

    # --- Gift Methods ---
    async def send_gift(self, chat_id: Union[int, str], gift_id: str, **kwargs) -> Message:
        """
        Отправляет подарок по его ID.
        """
        params = SendGiftParams(chat_id=chat_id, gift_id=gift_id, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("sendGift", params, response_model=Message)

    async def send_simple_gift(self, chat_id: Union[int, str], gift_id: Union[GiftAlias, str], **kwargs) -> Message:
        """
        Отправляет простой подарок, используя либо Enum-псевдоним, либо фактический ID подарка.
        """
        if isinstance(gift_id, GiftAlias):
            gift_id_str = gift_id.value
        elif isinstance(gift_id, str):
            gift_id_str = gift_id
        else:
            raise ValueError(f"Недопустимый тип для gift_id. Ожидается GiftAlias или str, получено: {type(gift_id)}")
        params = SendGiftParams(chat_id=chat_id, gift_id=gift_id_str, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("sendGift", params, response_model=Message)

    async def gift_premium_subscription(self, user_id: int, months: int, **kwargs) -> Message:
        """
        Дарит Premium-подписку пользователю.
        """
        params = GiftPremiumParams(user_id=user_id, months=months, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("giftPremiumSubscription", params, response_model=Message)

    async def transfer_gift(self, recipient_user_id: int, **kwargs) -> bool:
        """
        Переводит подарок другому пользователю.
        """
        params = TransferGiftParams(recipient_user_id=recipient_user_id, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("transferGift", params)

    async def get_star_balance(self) -> int:
        """
        Получает баланс Telegram Stars бота. Результат кэшируется.
        """
        if "balance" not in self.star_balance_cache:
            response = await self._make_request("getStarBalance", {})
            balance = response.get("stars", 0)
            self.star_balance_cache["balance"] = balance
            self.logger.info(f"Получен баланс Stars (из API): {balance}")
        else:
            balance = self.star_balance_cache["balance"]
            self.logger.info(f"Получен баланс Stars (из кэша): {balance}")
        return balance

    async def get_available_gifts(self) -> List[AvailableGift]:
        """
        Получает список доступных подарков. Результат кэшируется.
        """
        if "gifts" not in self.available_gifts_cache:
            response = await self._make_request("getAvailableGifts", {})
            gifts = [AvailableGift.model_validate(g) for g in response.get("gifts", [])]
            self.available_gifts_cache["gifts"] = gifts
            self.logger.info(f"Получены доступные подарки (из API): count={len(gifts)}")
        else:
            gifts = self.available_gifts_cache["gifts"]
            self.logger.info(f"Получены доступные подарки (из кэша): count={len(gifts)}")
        return gifts

    async def get_revenue_withdrawal_state(self) -> RevenueWithdrawalState:
        """
        Returns the current state of a revenue withdrawal operation.
        """
        result = await self._make_request("getRevenueWithdrawalState", {}, response_model=RevenueWithdrawalState)
        return result

    async def refund_star_payment(self, user_id: int, telegram_payment_charge_id: str) -> bool:
        """
        Refunds a successful star payment.
        """
        params = RefundStarPaymentParams(
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id
        ).model_dump(exclude_none=True)
        return await self._make_request("refundStarPayment", params)

    # --- Message Methods ---
    async def send_message(self, chat_id: Union[int, str], text: str, **kwargs) -> Message:
        """
        Отправляет текстовое сообщение.
        """
        params = SendMessageParams(chat_id=chat_id, text=text, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("sendMessage", params, response_model=Message)

    async def edit_message_text(self, text: str, **kwargs) -> Union[Message, bool]:
        """
        Редактирует текстовое сообщение.
        """
        params = EditMessageTextParams(text=text, **kwargs).model_dump(exclude_none=True)
        result = await self._make_request("editMessageText", params, response_model=Message)
        return result

    async def delete_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """
        Удаляет сообщение.
        """
        params = DeleteMessageParams(chat_id=chat_id, message_id=message_id).model_dump(exclude_none=True)
        return await self._make_request("deleteMessage", params)

    async def forward_message(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_id: int, **kwargs) -> Message:
        """
        Пересылает сообщение.
        """
        params = ForwardMessageParams(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("forwardMessage", params, response_model=Message)

    async def answer_inline_query(self, inline_query_id: str, results: List[Dict], **kwargs) -> bool:
        """
        Отвечает на inline-запрос.
        """
        params = AnswerInlineQueryParams(inline_query_id=inline_query_id, results=results, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("answerInlineQuery", params)

    # --- Updates and Webhook Methods ---
    async def get_updates(self, offset: Optional[int] = None, limit: Optional[int] = None,
                          timeout: Optional[int] = None, allowed_updates: Optional[List[str]] = None) -> List[Update]:
        """
        Используйте этот метод для получения входящих обновлений с помощью long polling.
        """
        params = GetUpdatesParams(
            offset=offset,
            limit=limit,
            timeout=timeout if timeout is not None else 60,
            allowed_updates=allowed_updates
        ).model_dump(exclude_none=True)
        result = await self._make_request("getUpdates", params)
        return [Update.model_validate(upd) for upd in result]

    async def updates_stream(self, timeout: int = 60, limit: int = 100,
                             allowed_updates: Optional[List[str]] = None) -> AsyncIterator[Update]:
        """
        Асинхронный итератор для непрерывного получения обновлений от Telegram API.
        """
        offset = None
        self.logger.info(f"Запущен поток получения обновлений: timeout={timeout}, limit={limit}")
        while True:
            try:
                updates = await self.get_updates(
                    offset=offset,
                    limit=limit,
                    timeout=timeout,
                    allowed_updates=allowed_updates
                )
                if updates:
                    for update in updates:
                        yield update
                        if offset is None or update.update_id >= offset:
                            offset = update.update_id + 1
                else:
                    self.logger.debug("Нет новых обновлений, ожидание...")
            except TelegramTooManyRequestsError as e:
                self.logger.warning(f"Превышен лимит запросов: {e.description}. Ожидание {e.retry_after} сек.")
                await asyncio.sleep(e.retry_after if e.retry_after else 10)
            except TelegramAPIError as e:
                self.logger.error(f"Ошибка при получении обновлений: {e.description} (Код: {e.error_code})")
                await asyncio.sleep(5)
            except Exception as e:
                self.logger.critical(f"Непредвиденная ошибка в потоке обновлений: {e}")
                await asyncio.sleep(10)

    async def set_webhook(self, url: str, **kwargs) -> bool:
        """
        Устанавливает вебхук.
        """
        params = SetWebhookParams(url=url, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("setWebhook", params)

    async def delete_webhook(self, **kwargs) -> bool:
        """
        Удаляет вебхук.
        """
        params = DeleteWebhookParams(**kwargs).model_dump(exclude_none=True)
        return await self._make_request("deleteWebhook", params)

    async def get_webhook_info(self) -> WebhookInfo:
        """
        Получает информацию о текущем статусе вебхука.
        """
        return await self._make_request("getWebhookInfo", {}, response_model=WebhookInfo)

    # --- Chat Methods ---
    async def get_chat(self, chat_id: Union[int, str]) -> Chat:
        """
        Получает информацию о чате. Результат кэшируется.
        """
        if not hasattr(self, '_chat_cache'):
            self._chat_cache = TTLCache(maxsize=100, ttl=3600)

        if chat_id not in self._chat_cache:
            params = GetChatParams(chat_id=chat_id).model_dump(exclude_none=True)
            result = await self._make_request("getChat", params, response_model=Chat)
            self._chat_cache[chat_id] = result
            self.logger.info(f"Получена информация о чате {chat_id} (из API)")
        else:
            result = self._chat_cache[chat_id]
            self.logger.info(f"Получена информация о чате {chat_id} (из кэша)")
        return result

    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[AnyChatMember]:
        """
        Получает список администраторов чата.
        """
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
        """
        Запрещает пользователю участвовать в чате до указанного момента.
        """
        params = KickChatMemberParams(chat_id=chat_id, user_id=user_id, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("kickChatMember", params)

    async def unban_chat_member(self, chat_id: Union[int, str], user_id: int, **kwargs) -> bool:
        """
        Разбанивает пользователя в чате.
        """
        params = UnbanChatMemberParams(chat_id=chat_id, user_id=user_id, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("unbanChatMember", params)

    # --- Checklist Methods ---
    async def send_checklist(self, chat_id: Union[int, str], checklist: InputChecklist, **kwargs) -> Message:
        """
        Отправляет список задач (чеклист).
        """
        params = SendChecklistParams(chat_id=chat_id, checklist=checklist, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("sendChecklist", params, response_model=Message)

    async def edit_message_checklist(self, checklist: InputChecklist, **kwargs) -> Message:
        """
        Редактирует существующий список задач (чеклист) в сообщении.
        """
        params = EditMessageChecklistParams(checklist=checklist, **kwargs).model_dump(exclude_none=True)
        return await self._make_request("editMessageChecklist", params, response_model=Message)

    # --- Business Connection Methods ---
    async def get_business_connection(self, business_connection_id: str) -> Dict:
        """
        Get information about a business connection.
        """
        params = {"business_connection_id": business_connection_id}
        return await self._make_request("getBusinessConnection", params)

    async def hide_keyboard(self, **kwargs) -> bool:
        """
        Hide the keyboard in a Web App.
        """
        params = HideKeyboardParams(**kwargs).model_dump(exclude_none=True)
        return await self._make_request("hideKeyboard", params)