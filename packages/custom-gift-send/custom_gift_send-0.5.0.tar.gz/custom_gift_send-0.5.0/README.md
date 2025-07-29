Custom Gift Send - Асинхронный Telegram Bot API Клиент для Подарков и Stars 🎁✨
Custom Gift Send — это мощный и надёжный асинхронный Python-клиент для взаимодействия с Telegram Bot API, специально разработанный для работы с функциями подарков и Telegram Stars. Этот модуль предоставляет удобный интерфейс для отправки подарков, управления подписками Telegram Premium, отслеживания баланса Stars и работы с вебхуками, а также включает продвинутую валидацию входных данных и гибкое логирование.

Особенности 🌟
Асинхронные операции: Полностью асинхронный дизайн, использующий aiohttp для высокоэффективных сетевых запросов.

Управление сессией: Эффективное управление HTTP-сессиями с использованием асинхронного контекстного менеджера, обеспечивающее правильное открытие и закрытие соединений.

Гибкое логирование: Позволяет настраивать логгер модуля или передавать собственный экземпляр logging.Logger для более тонкого контроля над выводом информации.

Строгая валидация параметров: Использует Pydantic для автоматической валидации типов и значений входных параметров API-методов, предотвращая ошибки на ранней стадии и делая API более типобезопасным.

Надёжная обработка ошибок:

Гранулированные исключения: Предоставляет специфичные классы исключений для различных ошибок Telegram API (например, TelegramBadRequestError, TelegramTooManyRequestsError), упрощая обработку ошибок.

Автоматические повторные попытки: Встроенная логика повторных попыток с экспоненциальной задержкой для сетевых ошибок и ошибок 429 Too Many Requests, повышая устойчивость к временным сбоям.

Полная поддержка API для подарков и Stars: Включает методы для отправки подарков, дарения Premium, проверки баланса Stars, получения доступных подарков и передачи подарков другим пользователям.

Функции вебхуков: Поддержка установки, удаления и получения информации о вебхуках.

Работа с сообщениями: Методы для отправки, редактирования, удаления и пересылки сообщений.

Инлайн-режим: Методы для обработки инлайн-запросов и ответов.

Управление чатами: Методы для получения информации о чатах, администраторах, а также для блокировки/разблокировки участников.

Поддержка прокси: Возможность настройки HTTP/SOCKS прокси для всех запросов.

Типизация ответов API: Некоторые методы теперь возвращают типизированные объекты Pydantic (например, Message, Chat, User), улучшая автодополнение и читаемость кода.

Установка 🚀
Клонируйте репозиторий (или скачайте файлы custom_gift_send.py, __init__.py, config.ini, example.py):

git clone https://github.com/Ваш_Профиль/CustomSendGift.git
cd CustomSendGift

(Замените Ваш_Профиль на ваш реальный профиль GitHub)

Установите зависимости:

pip install aiohttp pydantic

Если вы используете setup.py, то зависимости будут установлены автоматически при установке пакета:

pip install .

Конфигурация ⚙️
Перед использованием модуля вам необходимо настроить ваш токен бота Telegram в файле config.ini:

# config.ini
[Bot]
token = ВАШ_ТОКЕН_БОТА_ЗДЕСЬ
update_timeout = 60

token: Токен вашего бота, полученный от BotFather. Обязательно для работы модуля.

update_timeout: Время ожидания (в секундах) для запросов getUpdates. Используется, если не передан в метод get_updates.

Использование 🧑‍💻
Модуль предназначен для асинхронного использования. Рекомендуется использовать его как асинхронный контекстный менеджер для корректного управления сессиями aiohttp.

Инициализация, логирование и прокси
Вы можете инициализировать CustomGiftSend с логгером по умолчанию или передать свой собственный экземпляр logging.Logger для интеграции с вашей системой логирования. Также можно настроить прокси.

import asyncio
import logging
import aiohttp # Для aiohttp.BasicAuth
from custom_gift_send import CustomGiftSend, TelegramAPIError, ValidationError

# 1. Пример настройки собственного логгера
my_custom_logger = logging.getLogger("MyBotLogger")
my_custom_logger.setLevel(logging.DEBUG) # Уровень DEBUG для подробных логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
my_custom_logger.addHandler(console_handler)

# 2. Пример настройки прокси (если требуется)
# proxy_url = "http://user:password@proxy.example.com:8080"
# proxy_auth = aiohttp.BasicAuth("user", "password")

async def main():
    # Использование модуля как контекстного менеджера с пользовательским логгером и прокси
    async with CustomGiftSend(
        logger=my_custom_logger,
        pydantic_logging_level=logging.INFO, # Уровень логирования для ошибок Pydantic
        # proxy=proxy_url,
        # proxy_auth=proxy_auth
    ) as gift_bot:
        my_custom_logger.info("Бот запущен и готов к работе!")
        # ... ваш код ...

    # Или без пользовательского логгера и прокси
    # async with CustomGiftSend() as gift_bot:
    #     logging.info("Бот запущен с логгером по умолчанию!")
    #     # ... ваш код ...

if __name__ == "__main__":
    asyncio.run(main())

Примеры вызовов методов
Все методы API теперь принимают параметры в виде ключевых слов (**kwargs). Pydantic будет автоматически валидировать эти параметры. Если параметры не соответствуют ожидаемой схеме, будет выброшено исключение pydantic.ValidationError.

import asyncio
import logging
from custom_gift_send import (
    CustomGiftSend,
    TelegramAPIError,
    TelegramBadRequestError,
    TelegramForbiddenError,
    TelegramTooManyRequestsError,
    ValidationError,
    Message, # Импортируем типизированные ответы
    Chat,
    WebhookInfo
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_examples():
    async with CustomGiftSend(logger=logger) as gift_bot:
        chat_id = -1001234567890 # Пример ID группы/канала (замените на реальный)
        user_id = 123456789      # Пример User ID (замените на реальный)
        
        try:
            # Получение баланса Telegram Stars
            balance_info = await gift_bot.get_star_balance()
            logger.info(f"Баланс Telegram Stars: {balance_info}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка при получении баланса Stars: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")

        try:
            # Получение доступных подарков
            available_gifts = await gift_bot.get_available_gifts()
            logger.info(f"Доступные подарки: {available_gifts}")
            first_gift_id = None
            if available_gifts.get("ok") and available_gifts["result"]:
                first_gift_id = available_gifts["result"][0].get("id")
                logger.info(f"Первый доступный Gift ID: {first_gift_id}")
            else:
                logger.warning("Нет доступных подарков для демонстрации send_gift.")

            if first_gift_id:
                # Отправка подарка (пример использования Pydantic-валидации через kwargs)
                send_gift_result = await gift_bot.send_gift(
                    chat_id=chat_id,
                    gift_id=first_gift_id,
                    pay_for_upgrade=False,
                    disable_notification=True,
                    text="Поздравляю с улучшением модуля!"
                )
                logger.info(f"Результат отправки подарка: {send_gift_result}")

        except TelegramBadRequestError as e:
            logger.error(f"Ошибка 400 Bad Request при отправке подарка: {e.description}")
        except ValidationError as e:
            logger.error(f"Ошибка валидации параметров send_gift: {e}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API при работе с подарками: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")

        try:
            # Отправка подписки Telegram Premium
            gift_premium_result = await gift_bot.gift_premium(user_id=user_id, months=1)
            logger.info(f"Результат дарения Premium: {gift_premium_result}")
        except TelegramForbiddenError as e:
            logger.error(f"Ошибка 403 Forbidden при дарении Premium: {e.description}")
        except ValidationError as e:
            logger.error(f"Ошибка валидации параметров gift_premium: {e}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API при дарении Premium: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")

        try:
            # Получение обновлений (с использованием Pydantic-валидации для limit и timeout)
            updates = await gift_bot.get_updates(limit=5, timeout=10)
            logger.info(f"Получено обновлений: {len(updates)}")
            for update in updates:
                logger.debug(f"Обновление: {update}")
        except TelegramTooManyRequestsError as e:
            logger.warning(f"Слишком много запросов. Повтор через {e.retry_after} секунд.")
        except ValidationError as e:
            logger.error(f"Ошибка валидации параметров get_updates: {e}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API при получении обновлений: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")

        # Пример установки вебхука (закомментировано, так как требует реального URL)
        # try:
        #     webhook_url = "https://your.domain/webhook_path"
        #     set_webhook_result = await gift_bot.set_webhook(url=webhook_url, max_connections=40, drop_pending_updates=True)
        #     logger.info(f"Установка вебхука: {set_webhook_result}")
        # except TelegramAPIError as e:
        #     logger.error(f"Ошибка при установке вебхука: {e.description}")
        # except ValidationError as e:
        #     logger.error(f"Ошибка валидации параметров set_webhook: {e}")

        try:
            # Получение информации о вебхуке (теперь возвращает типизированный объект WebhookInfo)
            webhook_info: WebhookInfo = await gift_bot.get_webhook_info()
            logger.info(f"Информация о вебхуке: URL={webhook_info.url}, Pending Updates={webhook_info.pending_update_count}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка при получении информации о вебхуке: {e.description}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")

        # --- Примеры новых методов ---
        print("\n--- Демонстрация новых методов ---")

        try:
            # Отправка сообщения (возвращает типизированный объект Message)
            sent_message: Message = await gift_bot.send_message(
                chat_id=chat_id,
                text="Привет от обновленного бота!"
            )
            logger.info(f"Сообщение отправлено. ID: {sent_message.message_id}, Текст: {sent_message.text}")

            # Редактирование сообщения (возвращает типизированный объект Message)
            edited_message: Message = await gift_bot.edit_message_text(
                chat_id=chat_id,
                message_id=sent_message.message_id,
                text="Привет от обновленного бота! (Отредактировано)"
            )
            logger.info(f"Сообщение отредактировано. Новый текст: {edited_message.text}")

            # Удаление сообщения (возвращает bool)
            deleted_status: bool = await gift_bot.delete_message(
                chat_id=chat_id,
                message_id=sent_message.message_id
            )
            logger.info(f"Сообщение удалено: {deleted_status}")

            # Пересылка сообщения (возвращает типизированный объект Message)
            # Для этого нужно, чтобы sent_message.message_id существовал и был доступен
            # forward_result: Message = await gift_bot.forward_message(
            #     chat_id=chat_id,
            #     from_chat_id=chat_id,
            #     message_id=sent_message.message_id # Используйте ID существующего сообщения
            # )
            # logger.info(f"Сообщение переслано. ID: {forward_result.message_id}")

        except ValidationError as e:
            logger.error(f"Ошибка валидации Pydantic для методов сообщений: {e}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API для методов сообщений: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка для методов сообщений: {e}")

        try:
            # Получение информации о чате (возвращает типизированный объект Chat)
            chat_info: Chat = await gift_bot.get_chat(chat_id=chat_id)
            logger.info(f"Информация о чате: {chat_info.title} (Тип: {chat_info.type})")
        except ValidationError as e:
            logger.error(f"Ошибка валидации Pydantic для get_chat: {e}")
        except TelegramAPIError as e:
            logger.error(f"Ошибка Telegram API для get_chat: {e.description} (Код: {e.error_code})")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка для get_chat: {e}")

        # Примеры для kick_chat_member, unban_chat_member, answer_inline_query, refund_star_payment
        # требуют специфических условий или данных для работы.
        # Например, для kick_chat_member бот должен быть админом с соответствующими правами.
        # Для answer_inline_query нужно обрабатывать inline_query обновления.
        # Для refund_star_payment нужен реальный star_payment_charge_id.


API Справочник 📚
Ниже приведён список ключевых методов класса CustomGiftSend с кратким описанием и указанием их параметров.

class CustomGiftSend(logger: Optional[logging.Logger] = None, pydantic_logging_level: int = logging.WARNING, proxy: Optional[str] = None, proxy_auth: Optional[aiohttp.BasicAuth] = None)
Назначение: Инициализирует клиент Telegram Bot API.

Параметры:

logger (Optional[logging.Logger]): Опциональный экземпляр логгера Python. Если не предоставлен, будет создан логгер по умолчанию.

pydantic_logging_level (int): Уровень логирования (например, logging.INFO, logging.WARNING) для ошибок валидации Pydantic. По умолчанию logging.WARNING.

proxy (Optional[str]): URL HTTP/SOCKS прокси (например, "http://user:pass@host:port").

proxy_auth (Optional[aiohttp.BasicAuth]): Объект aiohttp.BasicAuth для аутентификации на прокси.

async send_gift(**kwargs) -> Dict
Назначение: Отправляет подарок от имени бота в указанный чат.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): Уникальный идентификатор целевого чата.

gift_id (str, обязательно): Уникальный идентификатор подарка (можно получить с помощью get_available_gifts).

pay_for_upgrade (Optional[bool]): Оплатить ли повышение уровня для Premium-подарков.

disable_notification (Optional[bool]): Отправлять ли сообщение без звука.

text (Optional[str]): Дополнительный текст для подарка.

parse_mode (Optional[str]): Режим разбора для текста (например, 'MarkdownV2', 'HTML').

entities (Optional[list]): Массив специальных объектов-сущностей, которые появляются в тексте сообщения.

reply_parameters (Optional[Dict]): Параметры для ответа на сообщение.

reply_markup (Optional[Dict]): Объект кастомной клавиатуры.

Возвращает: Dict (результат операции Telegram API).

Исключения: TelegramBadRequestError, ValidationError.

async gift_premium(**kwargs) -> Dict
Назначение: Дарит подписку Telegram Premium указанному пользователю.

Параметры Pydantic (через kwargs):

user_id (int, обязательно): Уникальный идентификатор пользователя.

months (int, обязательно): Количество месяцев подписки (1, 3, 6 или 12).

Возвращает: Dict.

Исключения: TelegramForbiddenError, ValidationError.

async get_star_balance() -> Dict
Назначение: Получает текущий баланс Telegram Stars бота.

Параметры: Нет.

Возвращает: Dict (информация о балансе Stars).

async get_available_gifts() -> Dict
Назначение: Получает список подарков, которые ваш бот может отправлять.

Параметры: Нет.

Возвращает: Dict (список доступных подарков).

async transfer_gift(**kwargs) -> Dict
Назначение: Передает подаренный подарок другому пользователю.

Параметры Pydantic (через kwargs):

owned_gift_id (str, обязательно): Уникальный идентификатор подарка, который принадлежит боту.

user_id (int, обязательно): ID пользователя, которому передаётся подарок.

chat_id (Optional[Union[int, str]]): ID чата, если бот не имеет прямого доступа к user_id.

pay_for_transfer (Optional[bool]): Оплатить ли комиссию за передачу.

Возвращает: Dict.

Исключения: TelegramNotFoundError, ValidationError.

async get_updates(**kwargs) -> list
Назначение: Получает входящие обновления с использованием долгого опроса.

Параметры Pydantic (через kwargs):

offset (Optional[int]): ID первого обновления, которое нужно получить.

limit (Optional[int]): Максимальное количество обновлений для получения (1-100).

timeout (Optional[int]): Время ожидания в секундах для долгого опроса (0-60). По умолчанию используется update_timeout из config.ini.

allowed_updates (Optional[List[str]]): Список типов обновлений, которые бот хочет получать.

Возвращает: list (список объектов Update).

async get_user_chat_boosts(**kwargs) -> Dict
Назначение: Получает список бустов чата, добавленных пользователем.

Параметры Pydantic (через kwargs):

user_id (int, обязательно): ID пользователя, чьи бусты нужно получить.

Возвращает: Dict.

async refund_star_payment(**kwargs) -> Dict
Назначение: Возвращает средства за Star-платеж.

Параметры Pydantic (через kwargs):

star_payment_charge_id (str, обязательно): ID платежа Stars, который нужно вернуть.

Возвращает: Dict.

async set_webhook(**kwargs) -> Dict
Назначение: Указывает URL для получения входящих обновлений через вебхук.

Параметры Pydantic (через kwargs):

url (str, обязательно): URL для вебхука.

certificate (Optional[Any]): Открытый ключ SSL-сертификата.

ip_address (Optional[str]): IP-адрес для использования вместо URL.

max_connections (Optional[int]): Максимальное количество одновременных подключений (1-100).

allowed_updates (Optional[List[str]]): Список типов обновлений, которые бот хочет получать.

drop_pending_updates (Optional[bool]): Удалять ли ожидающие обновления.

secret_token (Optional[str]): Секретный токен для заголовка X-Telegram-Bot-Api-Secret-Token.

Возвращает: Dict.

async delete_webhook(**kwargs) -> Dict
Назначение: Удаляет вебхук.

Параметры Pydantic (через kwargs):

drop_pending_updates (Optional[bool]): Удалять ли ожидающие обновления.

Возвращает: Dict.

async get_webhook_info() -> WebhookInfo
Назначение: Получает актуальную информацию о вебхуке бота.

Параметры: Нет.

Возвращает: WebhookInfo (типизированный объект Pydantic).

async send_message(**kwargs) -> Message
Назначение: Отправляет текстовое сообщение.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID целевого чата.

text (str, обязательно): Текст сообщения.

parse_mode (Optional[str]): Режим разбора для текста.

entities (Optional[List[Dict]]): Массив сущностей.

link_preview_options (Optional[Dict]): Опции предпросмотра ссылок.

disable_notification (Optional[bool]): Отправлять ли без звука.

protect_content (Optional[bool]): Защищать ли контент от пересылки и сохранения.

reply_parameters (Optional[Dict]): Параметры для ответа.

reply_markup (Optional[Dict]): Объект кастомной клавиатуры.

business_connection_id (Optional[str]): ID бизнес-соединения.

message_effect_id (Optional[str]): ID эффекта сообщения.

Возвращает: Message (типизированный объект Pydantic).

async edit_message_text(**kwargs) -> Message
Назначение: Редактирует текст существующего сообщения.

Параметры Pydantic (через kwargs):

text (str, обязательно): Новый текст сообщения.

chat_id (Optional[Union[int, str]]): ID чата, если сообщение в чате.

message_id (Optional[int]): ID сообщения, если сообщение в чате.

inline_message_id (Optional[str]): ID инлайн-сообщения, если сообщение инлайн.

(Требуется либо (chat_id и message_id), либо inline_message_id)

parse_mode, entities, link_preview_options, reply_markup, business_connection_id (как в send_message).

Возвращает: Message (типизированный объект Pydantic).

async delete_message(**kwargs) -> bool
Назначение: Удаляет сообщение в чате.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID чата.

message_id (int, обязательно): ID сообщения для удаления.

Возвращает: bool (True в случае успеха).

async forward_message(**kwargs) -> Message
Назначение: Пересылает сообщение.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID целевого чата.

from_chat_id (Union[int, str], обязательно): ID исходного чата.

message_id (int, обязательно): ID сообщения для пересылки.

disable_notification (Optional[bool]): Отправлять ли без звука.

protect_content (Optional[bool]): Защищать ли контент.

message_thread_id (Optional[int]): ID темы сообщения (для форумов).

Возвращает: Message (типизированный объект Pydantic).

async answer_inline_query(**kwargs) -> bool
Назначение: Отвечает на инлайн-запрос.

Параметры Pydantic (через kwargs):

inline_query_id (str, обязательно): ID инлайн-запроса.

results (List[Dict], обязательно): Массив результатов инлайн-запроса.

cache_time (Optional[int]): Время кэширования результата.

is_personal (Optional[bool]): Является ли результат персональным.

next_offset (Optional[str]): Смещение для следующего запроса.

button (Optional[Dict]): Кнопка для отображения под результатами.

Возвращает: bool (True в случае успеха).

async get_chat(**kwargs) -> Chat
Назначение: Получает информацию о чате.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID чата.

Возвращает: Chat (типизированный объект Pydantic).

async get_chat_administrators(**kwargs) -> List[Dict]
Назначение: Получает список администраторов чата.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID чата.

Возвращает: List[Dict] (список объектов ChatMember).

async kick_chat_member(**kwargs) -> bool
Назначение: Блокирует пользователя в группе, супергруппе или канале.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID чата.

user_id (int, обязательно): ID пользователя.

until_date (Optional[int]): Дата разблокировки в формате Unix-времени.

revoke_messages (Optional[bool]): Удалять ли сообщения пользователя.

Возвращает: bool (True в случае успеха).

async unban_chat_member(**kwargs) -> bool
Назначение: Разблокирует пользователя в супергруппе или канале.

Параметры Pydantic (через kwargs):

chat_id (Union[int, str], обязательно): ID чата.

user_id (int, обязательно): ID пользователя.

only_if_banned (Optional[bool]): Разблокировать только если пользователь был заблокирован.

Возвращает: bool (True в случае успеха).

Обработка Ошибок 🚦
Модуль предоставляет специфичные исключения для разных типов ошибок Telegram API:

TelegramAPIError: Базовый класс для всех ошибок API.

TelegramUnauthorizedError (HTTP 401): Неверный токен бота.

TelegramForbiddenError (HTTP 403): Бот заблокирован пользователем или не имеет доступа к ресурсу.

TelegramBadRequestError (HTTP 400): Некорректные параметры запроса.

TelegramNotFoundError (HTTP 404): Ресурс не найден.

TelegramTooManyRequestsError (HTTP 429): Превышен лимит запросов. Содержит атрибут retry_after, указывающий, через сколько секунд можно повторить запрос.

pydantic.ValidationError: Выбрасывается, если входные параметры не соответствуют ожидаемой Pydantic-модели.

Пример обработки ошибок:

import asyncio
from custom_gift_send import (
    CustomGiftSend,
    TelegramAPIError,
    TelegramBadRequestError,
    TelegramTooManyRequestsError,
    ValidationError
)

async def handle_errors():
    async with CustomGiftSend() as gift_bot:
        try:
            # Попытка вызвать метод с некорректным параметром
            await gift_bot.send_gift(chat_id="not_an_int", gift_id="invalid")
        except ValidationError as e:
            print(f"Ошибка валидации Pydantic: {e}")
        except TelegramBadRequestError as e:
            print(f"Ошибка Bad Request: {e.description} (Код: {e.error_code})")
        except TelegramTooManyRequestsError as e:
            print(f"Ошибка Too Many Requests: Попробуйте снова через {e.retry_after} секунд.")
        except TelegramAPIError as e:
            print(f"Общая ошибка Telegram API: {e.description} (Код: {e.error_code})")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(handle_errors())