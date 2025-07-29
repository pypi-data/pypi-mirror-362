Custom Gift Send - Асинхронный Telegram Bot API Клиент 🎁✨
custom-gift-send — это мощный асинхронный Python-клиент для Telegram Bot API, предназначенный для работы с подарками, Telegram Stars, списками задач и управлением сообщениями/чатами. Модуль использует aiohttp для эффективных запросов, Pydantic для строгой валидации и предоставляет типизированные ответы для удобства разработки.
Основные возможности

Асинхронные операции: Быстрые запросы с использованием aiohttp.
Подарки и Stars: Отправка подарков, дарение Premium, управление балансом Stars.
Списки задач: Поддержка новых методов send_checklist и edit_message_checklist (требуется бизнес-аккаунт).
Управление сообщениями: Отправка, редактирование, удаление и пересылка сообщений.
Вебхуки и чаты: Установка вебхуков, получение информации о чатах и администраторах.
Кэширование: Оптимизированное кэширование для подарков, баланса Stars и информации о чатах.
Надежность: Автоматические повторные попытки при ошибках и детализированное логирование.

Установка
Клонируйте репозиторий или установите через PyPI:
pip install custom-gift-send

Зависимости (aiohttp, pydantic, cachetools) устанавливаются автоматически.
Конфигурация
Создайте файл config.ini в корневой директории:
[Bot]
token = ВАШ_ТОКЕН_БОТА
update_timeout = 60

Получите токен у BotFather.
Использование
Модуль предназначен для асинхронного использования с контекстным менеджером:
import asyncio
import logging
from custom_gift_send import CustomGiftSend, Checklist, ChecklistTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    async with CustomGiftSend(logger=logger) as bot:
        # Отправка подарка
        gifts = await bot.get_available_gifts()
        if gifts:
            await bot.send_gift(chat_id=123456, gift_id=gifts[0].id, text="Поздравляю!")

        # Отправка списка задач
        checklist = Checklist(title="Задачи", tasks=[ChecklistTask(id=1, text="Задача 1")])
        message = await bot.send_checklist(chat_id=123456, checklist=checklist)
        logger.info(f"Отправлен список задач: {message.message_id}")

        # Получение баланса Stars
        balance = await bot.get_star_balance()
        logger.info(f"Баланс Stars: {balance}")

if __name__ == "__main__":
    asyncio.run(main())

API-справочник

send_gift(chat_id, gift_id, **kwargs): Отправляет подарок.
send_checklist(chat_id, checklist, **kwargs): Отправляет список задач.
edit_message_checklist(chat_id, message_id, checklist, **kwargs): Редактирует список задач.
get_star_balance(): Получает баланс Telegram Stars.
get_available_gifts(): Возвращает список доступных подарков.
send_message(chat_id, text, **kwargs): Отправляет сообщение.
Полный список методов в документации Telegram.

Обработка ошибок
Модуль предоставляет специфичные исключения:

TelegramBadRequestError: Некорректные параметры.
TelegramTooManyRequestsError: Превышен лимит запросов.
ValidationError: Ошибки валидации Pydantic.

try:
    await bot.send_gift(chat_id="invalid", gift_id="123")
except ValidationError as e:
    logger.error(f"Ошибка валидации: {e}")
except TelegramBadRequestError as e:
    logger.error(f"Ошибка API: {e.description}")

Лицензия
MIT License. Подробности в файле LICENSE.