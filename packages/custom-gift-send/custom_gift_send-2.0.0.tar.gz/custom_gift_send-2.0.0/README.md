Custom Gift Send - Асинхронный Telegram Bot API Клиент 🎁✨
custom-gift-send — мощный асинхронный Python-клиент для Telegram Bot API версии 9.1, предназначенный для работы с подарками, Telegram Stars, списками задач, бизнес-аккаунтами и мини-приложениями. Использует aiohttp для эффективных запросов, pydantic для строгой валидации, cachetools для кэширования, pythonjsonlogger для структурированного логирования и pybreaker для надежности с помощью CircuitBreaker.
Основные возможности

Асинхронные операции: Быстрые запросы с использованием aiohttp.
Подарки и Stars: Отправка подарков (с поддержкой GiftAlias), дарение Premium, управление балансом Stars, возврат платежей, получение состояния вывода средств.
Списки задач (чеклисты): Поддержка методов sendChecklist, editMessageChecklist и обработка событий ChecklistTasksDone, ChecklistTasksAdded (требуется бизнес-аккаунт).
Управление сообщениями: Отправка, редактирование, удаление, пересылка сообщений, включая медиа с новыми параметрами.
Вебхуки и чаты: Установка вебхуков, получение обновлений через updates_stream, информация о чатах и администраторах.
Мини-приложения: Поддержка методов, таких как hideKeyboard, для Web Apps.
Кэширование: Настраиваемое кэширование для подарков, баланса Stars и информации о чатах.
Надежность: Автоматические повторные попытки с экспоненциальным backoff, CircuitBreaker для защиты от сбоев, структурированное JSON-логирование.

Установка
Установите через PyPI:
pip install custom-gift-send

Зависимости (aiohttp>=3.8.4, pydantic>=2.0.3, cachetools>=5.3.1, pythonjsonlogger>=2.0.7, pybreaker>=1.1.0) устанавливаются автоматически.
Конфигурация
Создайте файл config.ini в корневой директории:
[telegram]
bot_token = ВАШ_ТОКЕН_БОТА
update_timeout = 60
cache_ttl_gifts = 3600
cache_ttl_balance = 300
cache_ttl_chats = 3600
max_retries = 5
retry_delay = 2
conn_timeout = 10
request_timeout = 60

Или задайте токен через переменную окружения TELEGRAM_BOT_TOKEN. Получите токен у BotFather.
Использование
Модуль предназначен для асинхронного использования:
import asyncio
import logging
from custom_gift_send import CustomGiftSend, GiftAlias, InputChecklist, InputChecklistTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    async with CustomGiftSend(token="ВАШ_ТОКЕН_БОТА", logger=logger) as bot:
        # Отправка подарка с использованием GiftAlias
        await bot.send_simple_gift(chat_id=123456, gift_id=GiftAlias.PREMIUM_3_MONTHS, text="Поздравляю!")

        # Дарение Premium-подписки
        await bot.gift_premium_subscription(user_id=123456, months=3)

        # Отправка списка задач
        checklist = InputChecklist(title="Задачи", tasks=[InputChecklistTask(text="Задача 1")])
        message = await bot.send_checklist(chat_id=123456, checklist=checklist)
        logger.info(f"Отправлен список задач: {message.message_id}")

        # Получение баланса Stars
        balance = await bot.get_star_balance()
        logger.info(f"Баланс Stars: {balance}")

        # Скрытие клавиатуры в Web App
        await bot.hide_keyboard(chat_id=123456, message_id=123)

        # Поток обновлений
        async for update in bot.updates_stream(timeout=60):
            logger.info(f"Получено обновление: {update.update_id}")

if __name__ == "__main__":
    asyncio.run(main())

API-справочник

send_simple_gift(chat_id, gift_id, **kwargs): Отправляет подарок, используя GiftAlias или ID.
gift_premium_subscription(user_id, months, **kwargs): Дарит Premium-подписку.
send_checklist(chat_id, checklist, **kwargs): Отправляет список задач.
edit_message_checklist(checklist, **kwargs): Редактирует список задач.
get_star_balance(): Получает баланс Telegram Stars.
get_available_gifts(): Возвращает список доступных подарков.
get_revenue_withdrawal_state(): Получает состояние вывода средств.
send_message(chat_id, text, **kwargs): Отправляет сообщение.
hide_keyboard(chat_id, message_id, **kwargs): Скрывает клавиатуру в Web App.
updates_stream(timeout, limit, allowed_updates): Асинхронный итератор для получения обновлений.
Полный список методов в документации Telegram.

Обработка ошибок
Модуль предоставляет специфичные исключения:

TelegramBadRequestError: Некорректные параметры.
TelegramTooManyRequestsError: Превышен лимит запросов.
ValidationError: Ошибки валидации Pydantic.
CircuitBreakerError: Ошибка при разомкнутой цепи CircuitBreaker.

try:
    await bot.send_simple_gift(chat_id="invalid", gift_id=GiftAlias.PREMIUM_1_MONTH)
except ValidationError as e:
    logger.error(f"Ошибка валидации: {e}")
except TelegramBadRequestError as e:
    logger.error(f"Ошибка API: {e.description}")
except CircuitBreakerError as e:
    logger.error(f"Цепь разомкнута: {e}")

Лицензия
MIT License. Подробности в файле LICENSE.