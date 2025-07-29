import aiohttp
import configparser
import logging
from typing import Dict, Optional

# --- НОВОЕ: Класс исключения для ошибок Telegram API ---
class TelegramAPIError(Exception):
    """Custom exception for Telegram API errors."""
    def __init__(self, message: str, error_code: Optional[int] = None, description: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code
        self.description = description

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomGiftSend:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Проверка наличия секции 'Bot' и токена
        if 'Bot' not in config:
            raise ValueError("Секция [Bot] не найдена в config.ini")
        if 'token' not in config['Bot'] or not config['Bot']['token']:
            raise ValueError("Токен бота не указан в config.ini в секции [Bot]")

        self.token = config['Bot']['token']
        self.update_timeout = int(config['Bot'].get('update_timeout', 60)) # Увеличил дефолт до 60
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    async def _make_request(self, method: str, params: Dict = None) -> Dict:
        """
        Приватный метод для выполнения запросов к Telegram Bot API.
        Включает улучшенную обработку HTTP и API ошибок.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url + method, json=params) as response:
                    response.raise_for_status() # Вызывает исключение для HTTP ошибок (4xx, 5xx)
                    result = await response.json()
                    
                    if not result.get("ok"):
                        error_code = result.get("error_code")
                        description = result.get("description")
                        error_message = f"Telegram API error for method '{method}': {description} (Code: {error_code})"
                        logger.error(error_message)
                        raise TelegramAPIError(error_message, error_code, description)
                    
                    return result
            except aiohttp.ClientError as e:
                logger.error(f"Network or Client error during {method}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error during {method}: {e}")
                raise

    async def send_gift(self, chat_id: int, gift_id: str, **kwargs) -> Dict:
        """
        Используется для отправки подарка.
        https://core.telegram.org/bots/api#sendgift
        """
        params = {"chat_id": chat_id, "gift_id": gift_id, **kwargs}
        return await self._make_request("sendGift", params)

    async def gift_premium(self, user_id: int, months: int) -> Dict:
        """
        Используется для дарения подписки Telegram Premium.
        https://core.telegram.org/bots/api#giftpremium
        """
        params = {"user_id": user_id, "months": months}
        return await self._make_request("giftPremium", params)

    async def get_star_balance(self) -> Dict:
        """
        Используется для получения текущего баланса Telegram Stars бота.
        https://core.telegram.org/bots/api#getstarbalance
        """
        return await self._make_request("getStarBalance")

    async def get_available_gifts(self) -> Dict:
        """
        Используется для получения списка подарков, которые ваш бот может отправлять.
        https://core.telegram.org/bots/api#getavailablegifts
        """
        return await self._make_request("getAvailableGifts")

    async def transfer_gift(self, owned_gift_id: str, user_id: int, **kwargs) -> Dict:
        """
        Используется для передачи подаренного подарка другому пользователю.
        https://core.telegram.org/bots/api#transfergift
        """
        params = {"owned_gift_id": owned_gift_id, "user_id": user_id, **kwargs}
        return await self._make_request("transferGift", params)

    async def get_updates(self) -> list:
        """
        Используется для получения входящих обновлений с использованием долгого опроса.
        https://core.telegram.org/bots/api#getupdates
        """
        params = {"timeout": self.update_timeout}
        # getUpdates возвращает список, но _make_request возвращает Dict.
        # В данном случае, result['result'] будет списком обновлений.
        response = await self._make_request("getUpdates", params)
        return response.get("result", [])

    # --- НОВЫЕ ФУНКЦИИ API ---

    async def get_user_chat_boosts(self, user_id: int) -> Dict:
        """
        Используется для получения списка бустов чата, добавленных пользователем.
        https://core.telegram.org/bots/api#getuserchatboosts
        """
        params = {"user_id": user_id}
        return await self._make_request("getUserChatBoosts", params)

    async def refund_star_payment(self, star_payment_charge_id: str) -> Dict:
        """
        Используется для возврата средств за Star-платеж.
        https://core.telegram.org/bots/api#refundstarpayment
        """
        params = {"star_payment_charge_id": star_payment_charge_id}
        return await self._make_request("refundStarPayment", params)

    async def set_webhook(self, url: str, **kwargs) -> Dict:
        """
        Используется для указания URL и получения входящих обновлений через вебхук.
        https://core.telegram.org/bots/api#setwebhook
        """
        params = {"url": url, **kwargs}
        return await self._make_request("setWebhook", params)

    async def delete_webhook(self, drop_pending_updates: Optional[bool] = None) -> Dict:
        """
        Используется для удаления вебхука.
        https://core.telegram.org/bots/api#deletewebhook
        """
        params = {}
        if drop_pending_updates is not None:
            params["drop_pending_updates"] = drop_pending_updates
        return await self._make_request("deleteWebhook", params)

    async def get_webhook_info(self) -> Dict:
        """
        Используется для получения актуальной информации о вебхуке.
        https://core.telegram.org/bots/api#getwebhookinfo
        """
        return await self._make_request("getWebhookInfo")

    async def close(self):
        """
        Заглушка для будущего закрытия сессии aiohttp, если она будет инициализироваться здесь.
        В текущей реализации сессия создается и закрывается для каждого запроса.
        """
        logger.info("CustomGiftSend client closed (no persistent session to close).")