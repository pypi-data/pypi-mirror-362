import aiohttp
import configparser
import logging
import asyncio
from typing import Dict, Optional, Type, Any, Union, List, Literal
from pydantic import BaseModel, Field, ValidationError, root_validator, Extra

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
        self.retry_after = retry_after # Seconds after which the request can be retried

# Dictionary for mapping error codes to specific exceptions
ERROR_CODE_TO_EXCEPTION: Dict[int, Type[TelegramAPIError]] = {
    400: TelegramBadRequestError,
    401: TelegramUnauthorizedError,
    403: TelegramForbiddenError,
    404: TelegramNotFoundError,
    429: TelegramTooManyRequestsError,
}

# --- Pydantic Models for API Parameters ---
class TelegramMethodParams(BaseModel):
    """Base model for Telegram Bot API method parameters."""
    class Config:
        extra = Extra.allow # Allow extra fields if Telegram API changes

class SendGiftParams(TelegramMethodParams):
    chat_id: Union[int, str]
    gift_id: str
    pay_for_upgrade: Optional[bool] = None
    disable_notification: Optional[bool] = None
    text: Optional[str] = None
    parse_mode: Optional[str] = None
    entities: Optional[list] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None

class GiftPremiumParams(TelegramMethodParams):
    user_id: int
    months: int

class TransferGiftParams(TelegramMethodParams):
    owned_gift_id: str
    user_id: int
    chat_id: Optional[Union[int, str]] = None
    pay_for_transfer: Optional[bool] = None

class GetUpdatesParams(TelegramMethodParams):
    offset: Optional[int] = None
    limit: Optional[int] = Field(None, ge=1, le=100)
    timeout: Optional[int] = Field(None, ge=0)
    allowed_updates: Optional[List[str]] = None

class SetWebhookParams(TelegramMethodParams):
    url: str
    certificate: Optional[Any] = None # Binary data or file path
    ip_address: Optional[str] = None
    max_connections: Optional[int] = Field(None, ge=1, le=100)
    allowed_updates: Optional[List[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None

class DeleteWebhookParams(TelegramMethodParams):
    drop_pending_updates: Optional[bool] = None

class GetUserChatBoostsParams(TelegramMethodParams):
    user_id: int

class RefundStarPaymentParams(TelegramMethodParams):
    star_payment_charge_id: str

# --- Message Methods Params ---
class SendMessageParams(TelegramMethodParams):
    chat_id: Union[int, str]
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[Dict]] = None
    link_preview_options: Optional[Dict] = None # new in API 7.0
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    reply_parameters: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    business_connection_id: Optional[str] = None
    message_effect_id: Optional[str] = None

class EditMessageTextParams(TelegramMethodParams):
    chat_id: Optional[Union[int, str]] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[Dict]] = None
    link_preview_options: Optional[Dict] = None
    reply_markup: Optional[Dict] = None
    business_connection_id: Optional[str] = None

    @root_validator(pre=True)
    def check_ids(cls, values):
        if ('chat_id' not in values or 'message_id' not in values) and 'inline_message_id' not in values:
            raise ValueError('Either (chat_id and message_id) or inline_message_id must be provided')
        return values

class DeleteMessageParams(TelegramMethodParams):
    chat_id: Union[int, str]
    message_id: int

class ForwardMessageParams(TelegramMethodParams):
    chat_id: Union[int, str]
    from_chat_id: Union[int, str]
    message_id: int
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    message_thread_id: Optional[int] = None # for topics in groups

# --- Inline Mode Params ---
class AnswerInlineQueryParams(TelegramMethodParams):
    inline_query_id: str
    results: List[Dict] # Array of InlineQueryResult
    cache_time: Optional[int] = None
    is_personal: Optional[bool] = None
    next_offset: Optional[str] = None
    button: Optional[Dict] = None # InlineQueryResultsButton
    
# --- Chat Management Params ---
class GetChatParams(TelegramMethodParams):
    chat_id: Union[int, str]

class GetChatAdministratorsParams(TelegramMethodParams):
    chat_id: Union[int, str]

class KickChatMemberParams(TelegramMethodParams): # Renamed from banChatMember in API 6.2
    chat_id: Union[int, str]
    user_id: int
    until_date: Optional[int] = None
    revoke_messages: Optional[bool] = None

class UnbanChatMemberParams(TelegramMethodParams):
    chat_id: Union[int, str]
    user_id: int
    only_if_banned: Optional[bool] = None

# --- Pydantic Models for API Responses (Full Typification) ---
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
    
    class Config:
        populate_by_name = True # Allows using 'from_user' instead of 'from_field'
        allow_population_by_field_name = True # Alias for populate_by_name
        extra = Extra.allow # For future API changes

class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

class Chat(BaseModel):
    id: int
    type: str # 'private', 'group', 'supergroup', 'channel'
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    photo: Optional[ChatPhoto] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None # Forward reference
    # ... many more fields for Chat

    class Config:
        extra = Extra.allow

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
    date: int
    chat: Chat
    from_user: Optional[User] = Field(None, alias='from') # 'from' is a Python keyword, use alias
    text: Optional[str] = None
    
    # Media fields
    photo: Optional[List[PhotoSize]] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    video: Optional[Video] = None
    voice: Optional[Voice] = None
    # ... many more message content types (sticker, video_note, contact, location, venue, poll, dice, game, etc.)

    class Config:
        extra = Extra.allow # For future API changes

# Forward reference for Chat.pinned_message
Chat.update_forward_refs()

class ChatMember(BaseModel):
    user: User
    status: str # 'creator', 'administrator', 'member', 'restricted', 'left', 'kicked'

    class Config:
        extra = Extra.allow

# Specific ChatMember types (for more precise typing, though ChatMember is often enough)
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
    until_date: Optional[int] = None

class ChatMemberLeft(ChatMember):
    status: Literal['left']

class ChatMemberBanned(ChatMember):
    status: Literal['kicked']
    until_date: Optional[int] = None

# Union type for all possible ChatMember statuses
AnyChatMember = Union[
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned
]

class CallbackQuery(BaseModel):
    id: str
    from_user: User = Field(alias='from')
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: str
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow

class InlineQuery(BaseModel):
    id: str
    from_user: User = Field(alias='from')
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Dict] = None # Location model could be added

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow

class ChosenInlineResult(BaseModel):
    result_id: str
    from_user: User = Field(alias='from')
    query: str
    location: Optional[Dict] = None
    inline_message_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow

class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    # Add more update types as needed (shipping_query, pre_checkout_query, poll, poll_answer, my_chat_member, chat_member, chat_join_request, etc.)

    class Config:
        extra = Extra.allow

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
    
# --- New: AvailableGift Response Model ---
class AvailableGift(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    price_amount: int
    price_currency: str
    
    class Config:
        extra = Extra.allow

# Generic response model for API calls
class ApiResponse(BaseModel):
    ok: bool
    result: Optional[Any] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[Dict] = None # For error parameters like retry_after

# --- Main Client Class ---
class CustomGiftSend:
    _MAX_RETRIES = 5
    _BASE_RETRY_DELAY = 1

    # --- Mapping for simplified gift sending ---
    # This is a basic example. In a real scenario, you might load this from a config
    # or fetch dynamically and cache.
    _GIFT_ALIASES = {
        "premium_1_month": {"title_contains": "1 месяц Premium"},
        "premium_3_months": {"title_contains": "3 месяца Premium"},
        "premium_6_months": {"title_contains": "6 месяцев Premium"},
        "premium_12_months": {"title_contains": "12 месяцев Premium"},
        "star_pack_50_stars": {"title_contains": "50 Stars"},
        "star_pack_100_stars": {"title_contains": "100 Stars"},
        # Add more aliases as needed, matching parts of the gift title or description
    }

    def __init__(
        self, 
        logger: Optional[logging.Logger] = None, 
        pydantic_logging_level: int = logging.WARNING,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None
    ):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'Bot' not in config:
            raise ValueError("Секция [Bot] не найдена в config.ini")
        if 'token' not in config['Bot'] or not config['Bot']['token']:
            raise ValueError("Токен бота не указан в config.ini в секции [Bot]")

        self.token = config['Bot']['token']
        self.update_timeout = int(config['Bot'].get('update_timeout', 60))
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        
        self._session: Optional[aiohttp.ClientSession] = None
        self.logger = logger if logger is not None else self._setup_default_logger()
        self.pydantic_logging_level = pydantic_logging_level
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self._available_gifts_cache: Optional[List[AvailableGift]] = None # Cache for available gifts

    def _setup_default_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                proxy=self.proxy,
                proxy_auth=self.proxy_auth
            )
            self.logger.debug("Aiohttp client session created.")
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
            self.logger.info("Aiohttp client session closed.")

    async def __aenter__(self):
        await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _make_request(
        self, 
        method: str, 
        params: Optional[Dict] = None, 
        attempt: int = 0,
        response_model: Optional[Type[BaseModel]] = None # Parameter for response typification
    ) -> Union[Dict, BaseModel, bool, List[Any]]: # Return type can be Dict, BaseModel, bool, or List
        session = await self._get_session()
        request_url = self.base_url + method
        try:
            self.logger.debug(f"Sending request to {request_url} with params: {params}")
            async with session.post(request_url, json=params) as response:
                response_json = await response.json()
                
                # Validate the raw API response with ApiResponse model first
                api_response = ApiResponse(**response_json)

                if not api_response.ok:
                    error_code = api_response.error_code
                    description = api_response.description
                    
                    if error_code == 429 and attempt < self._MAX_RETRIES:
                        retry_after = api_response.parameters.get("retry_after", self._BASE_RETRY_DELAY * (2 ** attempt)) if api_response.parameters else self._BASE_RETRY_DELAY * (2 ** attempt)
                        self.logger.warning(f"Too many requests (429) for '{method}'. Retrying in {retry_after} seconds (attempt {attempt + 1}/{self._MAX_RETRIES}). Description: {description}")
                        await asyncio.sleep(retry_after)
                        return await self._make_request(method, params, attempt + 1, response_model)
                    
                    exception_class = ERROR_CODE_TO_EXCEPTION.get(error_code, TelegramAPIError)
                    
                    if exception_class == TelegramTooManyRequestsError and error_code == 429:
                        retry_after_final = api_response.parameters.get("retry_after") if api_response.parameters else None
                        raise exception_class(
                            message=f"Telegram API error for method '{method}': Too many requests after {self._MAX_RETRIES} attempts.",
                            error_code=error_code,
                            description=description,
                            retry_after=retry_after_final,
                            response_data=response_json
                        )
                    else:
                        raise exception_class(
                            message=f"Telegram API error for method '{method}': {description} (Code: {error_code})",
                            error_code=error_code,
                            description=description,
                            response_data=response_json
                        )
                
                self.logger.debug(f"Request to {method} successful.")
                
                # If a response_model is provided, try to parse the result into it
                if response_model:
                    try:
                        # Handle cases where result is a list of models (e.g., getUpdates, getChatAdministrators)
                        if isinstance(api_response.result, list):
                            return [response_model.parse_obj(item) for item in api_response.result]
                        else:
                            return response_model.parse_obj(api_response.result)
                    except ValidationError as e:
                        self.logger.log(self.pydantic_logging_level, f"Failed to parse API response for method '{method}' into {response_model.__name__}: {e.errors()}")
                        raise # Re-raise if parsing fails
                
                # For methods that return simple boolean or raw dict, return the result directly
                return api_response.result

        except aiohttp.ClientError as e:
            self.logger.error(f"Network or Client error during {method}: {e}")
            if attempt < self._MAX_RETRIES:
                delay = self._BASE_RETRY_DELAY * (2 ** attempt)
                self.logger.warning(f"Network error for '{method}'. Retrying in {delay} seconds (attempt {attempt + 1}/{self._MAX_RETRIES}). Error: {e}")
                await asyncio.sleep(delay)
                return await self._make_request(method, params, attempt + 1, response_model)
            raise
        except ValidationError as e:
            # More detailed logging for Pydantic validation errors
            self.logger.log(self.pydantic_logging_level, f"Input validation error for method '{method}': {e.errors()}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during {method}: {e}")
            raise

    # --- Existing Methods (Updated with response_model where applicable) ---
    async def send_gift(self, **kwargs) -> Dict: # Telegram API returns a raw dict for this
        params = SendGiftParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("sendGift", params)

    async def gift_premium(self, **kwargs) -> Dict: # Telegram API returns a raw dict for this
        params = GiftPremiumParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("giftPremium", params)

    async def get_star_balance(self) -> Dict: # Telegram API returns a raw dict for this
        return await self._make_request("getStarBalance")

    async def get_available_gifts(self) -> List[AvailableGift]: # Now returns a list of AvailableGift objects
        if self._available_gifts_cache is None:
            self.logger.debug("Fetching available gifts from API and caching.")
            gifts = await self._make_request("getAvailableGifts", response_model=AvailableGift)
            self._available_gifts_cache = gifts
        return self._available_gifts_cache

    async def transfer_gift(self, **kwargs) -> Dict: # Telegram API returns a raw dict for this
        params = TransferGiftParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("transferGift", params)

    async def get_updates(self, **kwargs) -> List[Update]: # Now returns a list of Update objects
        params = GetUpdatesParams(**kwargs).dict(exclude_none=True)
        if "timeout" not in params:
            params["timeout"] = self.update_timeout
        return await self._make_request("getUpdates", params, response_model=Update)

    async def get_user_chat_boosts(self, **kwargs) -> Dict: # Returns raw dict of ChatBoosts
        params = GetUserChatBoostsParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("getUserChatBoosts", params)

    async def refund_star_payment(self, **kwargs) -> Dict: # Returns raw dict
        params = RefundStarPaymentParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("refundStarPayment", params)

    async def set_webhook(self, **kwargs) -> bool: # Returns bool
        params = SetWebhookParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("setWebhook", params)

    async def delete_webhook(self, **kwargs) -> bool: # Returns bool
        params = DeleteWebhookParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("deleteWebhook", params)

    async def get_webhook_info(self) -> WebhookInfo: # Returns WebhookInfo object
        return await self._make_request("getWebhookInfo", response_model=WebhookInfo)

    # --- New Methods: Message Operations (Return typed objects) ---
    async def send_message(self, **kwargs) -> Message:
        params = SendMessageParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("sendMessage", params, response_model=Message)

    async def edit_message_text(self, **kwargs) -> Message:
        params = EditMessageTextParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("editMessageText", params, response_model=Message)

    async def delete_message(self, **kwargs) -> bool:
        params = DeleteMessageParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("deleteMessage", params)

    async def forward_message(self, **kwargs) -> Message:
        params = ForwardMessageParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("forwardMessage", params, response_model=Message)

    async def answer_inline_query(self, **kwargs) -> bool:
        params = AnswerInlineQueryParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("answerInlineQuery", params)

    async def get_chat(self, **kwargs) -> Chat:
        params = GetChatParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("getChat", params, response_model=Chat)

    async def get_chat_administrators(self, **kwargs) -> List[AnyChatMember]: 
        params = GetChatAdministratorsParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("getChatAdministrators", params, response_model=AnyChatMember)

    async def kick_chat_member(self, **kwargs) -> bool:
        params = KickChatMemberParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("kickChatMember", params)

    async def unban_chat_member(self, **kwargs) -> bool:
        params = UnbanChatMemberParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("unbanChatMember", params)

    async def send_simple_gift(self, chat_id: Union[int, str], gift_alias: str, **kwargs) -> Dict:
        available_gifts = await self.get_available_gifts()
        
        found_gift_id = None
        for gift in available_gifts:
            alias_criteria = self._GIFT_ALIASES.get(gift_alias)
            if alias_criteria:
                if "title_contains" in alias_criteria and alias_criteria["title_contains"].lower() in gift.title.lower():
                    found_gift_id = gift.id
                    break
            
        if not found_gift_id:
            raise ValueError(f"Псевдоним подарка '{gift_alias}' не найден среди доступных подарков или не соответствует критериям.")
        
        self.logger.info(f"Найден gift_id '{found_gift_id}' для псевдонима '{gift_alias}'. Отправка...")
        return await self.send_gift(chat_id=chat_id, gift_id=found_gift_id, **kwargs)

    async def get_formatted_available_gifts(self) -> List[Dict]:
        available_gifts = await self.get_available_gifts()
        formatted_list = []
        for gift in available_gifts:
            formatted_list.append({
                "id": gift.id,
                "title": gift.title,
                "description": gift.description if gift.description else "Нет описания",
                "price": f"{gift.price_amount / 100} {gift.price_currency}", 
                "type": "Premium" if "Premium" in gift.title else "Stars Pack"
            })
        return formatted_list