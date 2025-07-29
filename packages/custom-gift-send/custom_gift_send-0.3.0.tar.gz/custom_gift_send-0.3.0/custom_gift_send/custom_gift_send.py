import aiohttp
import configparser
import logging
import asyncio
from typing import Dict, Optional, Type, Any
from pydantic import BaseModel, Field, ValidationError

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
    chat_id: int
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
    chat_id: Optional[int] = None
    pay_for_transfer: Optional[bool] = None

class GetUpdatesParams(TelegramMethodParams):
    offset: Optional[int] = None
    limit: Optional[int] = Field(None, ge=1, le=100)
    timeout: Optional[int] = Field(None, ge=0)
    allowed_updates: Optional[list[str]] = None

class SetWebhookParams(TelegramMethodParams):
    url: str
    certificate: Optional[Any] = None
    ip_address: Optional[str] = None
    max_connections: Optional[int] = Field(None, ge=1, le=100)
    allowed_updates: Optional[list[str]] = None
    drop_pending_updates: Optional[bool] = None
    secret_token: Optional[str] = None

class DeleteWebhookParams(TelegramMethodParams):
    drop_pending_updates: Optional[bool] = None

class GetUserChatBoostsParams(TelegramMethodParams):
    user_id: int

class RefundStarPaymentParams(TelegramMethodParams):
    star_payment_charge_id: str

class CustomGiftSend:
    _MAX_RETRIES = 5
    _BASE_RETRY_DELAY = 1

    def __init__(self, logger: Optional[logging.Logger] = None):
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
            self._session = aiohttp.ClientSession()
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

    async def _make_request(self, method: str, params: Optional[Dict] = None, attempt: int = 0) -> Dict:
        session = await self._get_session()
        request_url = self.base_url + method
        try:
            self.logger.debug(f"Sending request to {request_url} with params: {params}")
            async with session.post(request_url, json=params) as response:
                response.raise_for_status()
                result = await response.json()
                
                if not result.get("ok"):
                    error_code = result.get("error_code")
                    description = result.get("description")
                    
                    if error_code == 429 and attempt < self._MAX_RETRIES:
                        retry_after = result.get("parameters", {}).get("retry_after", self._BASE_RETRY_DELAY * (2 ** attempt))
                        self.logger.warning(f"Too many requests (429) for '{method}'. Retrying in {retry_after} seconds (attempt {attempt + 1}/{self._MAX_RETRIES}). Description: {description}")
                        await asyncio.sleep(retry_after)
                        return await self._make_request(method, params, attempt + 1)
                    
                    exception_class = ERROR_CODE_TO_EXCEPTION.get(error_code, TelegramAPIError)
                    
                    if exception_class == TelegramTooManyRequestsError and error_code == 429:
                        retry_after_final = result.get("parameters", {}).get("retry_after")
                        raise exception_class(
                            message=f"Telegram API error for method '{method}': Too many requests after {self._MAX_RETRIES} attempts.",
                            error_code=error_code,
                            description=description,
                            retry_after=retry_after_final,
                            response_data=result
                        )
                    else:
                        raise exception_class(
                            message=f"Telegram API error for method '{method}': {description} (Code: {error_code})",
                            error_code=error_code,
                            description=description,
                            response_data=result
                        )
                
                self.logger.debug(f"Request to {method} successful.")
                return result
        except aiohttp.ClientError as e:
            self.logger.error(f"Network or Client error during {method}: {e}")
            if attempt < self._MAX_RETRIES:
                delay = self._BASE_RETRY_DELAY * (2 ** attempt)
                self.logger.warning(f"Network error for '{method}'. Retrying in {delay} seconds (attempt {attempt + 1}/{self._MAX_RETRIES}). Error: {e}")
                await asyncio.sleep(delay)
                return await self._make_request(method, params, attempt + 1)
            raise
        except ValidationError as e:
            self.logger.error(f"Input validation error for method '{method}': {e}")
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

    async def get_updates(self, **kwargs) -> list:
        params = GetUpdatesParams(**kwargs).dict(exclude_none=True)
        if "timeout" not in params:
            params["timeout"] = self.update_timeout
        
        response = await self._make_request("getUpdates", params)
        return response.get("result", [])

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

    async def get_webhook_info(self) -> Dict:
        return await self._make_request("getWebhookInfo")