import aiohttp
import configparser
import logging
import asyncio
from typing import Dict, Optional, Type, Any, Union, List
from pydantic import BaseModel, Field, ValidationError, root_validator

class TelegramAPIError(Exception):
    def __init__(self, message: str, error_code: Optional[int] = None, description: Optional[str] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.description = description
        self.response_data = response_data

class TelegramUnauthorizedError(TelegramAPIError):
    pass

class TelegramForbiddenError(TelegramAPIError):
    pass

class TelegramBadRequestError(TelegramAPIError):
    pass

class TelegramNotFoundError(TelegramAPIError):
    pass

class TelegramTooManyRequestsError(TelegramAPIError):
    def __init__(self, message: str, error_code: int, description: str, retry_after: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message, error_code, description, response_data)
        self.retry_after = retry_after

ERROR_CODE_TO_EXCEPTION: Dict[int, Type[TelegramAPIError]] = {
    400: TelegramBadRequestError,
    401: TelegramUnauthorizedError,
    403: TelegramForbiddenError,
    404: TelegramNotFoundError,
    429: TelegramTooManyRequestsError,
}

class TelegramMethodParams(BaseModel):
    class Config:
        extra = 'allow' 

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
    certificate: Optional[Any] = None 
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

class SendMessageParams(TelegramMethodParams):
    chat_id: Union[int, str]
    text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[Dict]] = None
    link_preview_options: Optional[Dict] = None 
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
    message_thread_id: Optional[int] = None 

class AnswerInlineQueryParams(TelegramMethodParams):
    inline_query_id: str
    results: List[Dict] 
    cache_time: Optional[int] = None
    is_personal: Optional[bool] = None
    next_offset: Optional[str] = None
    button: Optional[Dict] = None 
    
class GetChatParams(TelegramMethodParams):
    chat_id: Union[int, str]

class GetChatAdministratorsParams(TelegramMethodParams):
    chat_id: Union[int, str]

class KickChatMemberParams(TelegramMethodParams): 
    chat_id: Union[int, str]
    user_id: int
    until_date: Optional[int] = None
    revoke_messages: Optional[bool] = None

class UnbanChatMemberParams(TelegramMethodParams):
    chat_id: Union[int, str]
    user_id: int
    only_if_banned: Optional[bool] = None

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

class Chat(BaseModel):
    id: int
    type: str 
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None

class Message(BaseModel):
    message_id: int
    date: int
    chat: Chat
    from_user: Optional[User] = Field(None, alias='from') 
    text: Optional[str] = None

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

class ApiResponse(BaseModel):
    ok: bool
    result: Optional[Any] = None
    description: Optional[str] = None
    error_code: Optional[int] = None
    parameters: Optional[Dict] = None 

class CustomGiftSend:
    _MAX_RETRIES = 5
    _BASE_RETRY_DELAY = 1

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
        response_model: Optional[Type[BaseModel]] = None 
    ) -> Union[Dict, BaseModel]:
        session = await self._get_session()
        request_url = self.base_url + method
        try:
            self.logger.debug(f"Sending request to {request_url} with params: {params}")
            async with session.post(request_url, json=params) as response:
                response_json = await response.json()
                
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
                
                if response_model:
                    try:
                        return response_model.parse_obj(api_response.result)
                    except ValidationError as e:
                        self.logger.log(self.pydantic_logging_level, f"Failed to parse API response for method '{method}' into {response_model.__name__}: {e.errors()}")
                        raise
                return response_json.get("result") 

        except aiohttp.ClientError as e:
            self.logger.error(f"Network or Client error during {method}: {e}")
            if attempt < self._MAX_RETRIES:
                delay = self._BASE_RETRY_DELAY * (2 ** attempt)
                self.logger.warning(f"Network error for '{method}'. Retrying in {delay} seconds (attempt {attempt + 1}/{self._MAX_RETRIES}). Error: {e}")
                await asyncio.sleep(delay)
                return await self._make_request(method, params, attempt + 1, response_model)
            raise
        except ValidationError as e:
            self.logger.log(self.pydantic_logging_level, f"Input validation error for method '{method}': {e.errors()}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during {method}: {e}")
            raise

    async def send_gift(self, **kwargs) -> Dict:
        params = SendGiftParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("sendGift", params)

    async def gift_premium(self, **kwargs) -> Dict:
        params = GiftPremiumParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("giftPremium", params)

    async def get_star_balance(self) -> Dict:
        return await self._make_request("getStarBalance")

    async def get_available_gifts(self) -> Dict:
        return await self._make_request("getAvailableGifts")

    async def transfer_gift(self, **kwargs) -> Dict:
        params = TransferGiftParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("transferGift", params)

    async def get_updates(self, **kwargs) -> List[Dict]:
        params = GetUpdatesParams(**kwargs).dict(exclude_none=True)
        if "timeout" not in params:
            params["timeout"] = self.update_timeout
        return await self._make_request("getUpdates", params)

    async def get_user_chat_boosts(self, **kwargs) -> Dict:
        params = GetUserChatBoostsParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("getUserChatBoosts", params)

    async def refund_star_payment(self, **kwargs) -> Dict:
        params = RefundStarPaymentParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("refundStarPayment", params)

    async def set_webhook(self, **kwargs) -> Dict:
        params = SetWebhookParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("setWebhook", params)

    async def delete_webhook(self, **kwargs) -> Dict:
        params = DeleteWebhookParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("deleteWebhook", params)

    async def get_webhook_info(self) -> WebhookInfo: 
        return await self._make_request("getWebhookInfo", response_model=WebhookInfo)

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

    async def get_chat_administrators(self, **kwargs) -> List[Dict]:
        params = GetChatAdministratorsParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("getChatAdministrators", params)

    async def kick_chat_member(self, **kwargs) -> bool:
        params = KickChatMemberParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("kickChatMember", params) 

    async def unban_chat_member(self, **kwargs) -> bool:
        params = UnbanChatMemberParams(**kwargs).dict(exclude_none=True)
        return await self._make_request("unbanChatMember", params) 