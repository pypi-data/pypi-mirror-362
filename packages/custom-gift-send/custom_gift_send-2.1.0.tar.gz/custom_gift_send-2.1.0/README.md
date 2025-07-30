# Custom Gift Send - Улучшенный Асинхронный Telegram Bot API Клиент 🎁✨🔒

**custom-gift-send v2.1.0** — мощный и безопасный асинхронный Python-клиент для Telegram Bot API версии 9.1 с повышенной безопасностью, аналитикой и расширенными возможностями. Предназначен для работы с подарками, Telegram Stars, списками задач, бизнес-аккаунтами и мини-приложениями.

## 🚀 Новые возможности v2.1.0

### 🔒 Повышенная безопасность
- **Rate Limiting**: Интеллектуальное ограничение скорости запросов
- **Request Signing**: Подписывание запросов для защиты от подделки
- **IP Filtering**: Фильтрация по разрешенным IP-адресам
- **Data Encryption**: Шифрование чувствительных данных
- **SSL/TLS**: Усиленная проверка сертификатов
- **Request Size Limits**: Ограничения на размер запросов и ответов

### 📊 Аналитика и мониторинг
- **Real-time Analytics**: Статистика запросов в реальном времени
- **Performance Metrics**: Метрики производительности и времени ответа
- **Error Tracking**: Отслеживание и категоризация ошибок
- **Health Checks**: Проверка состояния бота
- **Structured Logging**: JSON-логирование для лучшего анализа

### 🎯 Система событий
- **Event Handlers**: Обработчики событий для различных действий
- **Webhook Validation**: Валидация входящих webhook-данных
- **Custom Events**: Возможность создания собственных событий

### 🔧 Улучшенная функциональность
- **Bulk Operations**: Массовые операции с контролем скорости
- **Enhanced Caching**: Улучшенное кэширование с принудительным обновлением
- **File Operations**: Загрузка и скачивание файлов
- **Chat Management**: Расширенное управление чатами
- **Safe Methods**: Безопасные методы, не вызывающие исключения

## 📦 Установка

```bash
pip install custom-gift-send
```

### Дополнительные зависимости для разработки:
```bash
pip install custom-gift-send[dev]  # Для разработки
pip install custom-gift-send[docs] # Для документации
```

## ⚙️ Конфигурация

### Базовая конфигурация
```python
from custom_gift_send import CustomGiftSend, SecurityConfig

# Конфигурация безопасности
security_config = SecurityConfig(
    max_request_size=50 * 1024 * 1024,  # 50MB
    rate_limit_requests=30,              # 30 запросов
    rate_limit_window=60,                # за 60 секунд
    allowed_ips={'127.0.0.1', '192.168.1.0/24'},  # Разрешенные IP
    encrypt_sensitive_data=True,         # Шифрование данных
    max_concurrent_requests=100,         # Максимум concurrent запросов
    enable_request_signing=True          # Подписывание запросов
)
```

### Файл конфигурации config.ini
```ini
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

[security]
max_request_size = 52428800
rate_limit_requests = 30
rate_limit_window = 60
encrypt_sensitive_data = true
max_concurrent_requests = 100
enable_request_signing = true
```

## 🎯 Использование

### Базовое использование с улучшенной безопасностью
```python
import asyncio
import logging
from custom_gift_send import CustomGiftSend, GiftAlias, SecurityConfig, InputChecklist, InputChecklistTask

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Конфигурация безопасности
    security_config = SecurityConfig(
        rate_limit_requests=30,
        rate_limit_window=60,
        encrypt_sensitive_data=True,
        enable_request_signing=True
    )
    
    async with CustomGiftSend(
        token="ВАШ_ТОКЕН_БОТА",
        security_config=security_config,
        logger=logger
    ) as bot:
        
        # Проверка состояния бота
        health = await bot.health_check()
        logger.info(f"Bot health: {health['status']}")
        
        # Отправка подарка с использованием GiftAlias
        await bot.send_simple_gift(
            chat_id=123456, 
            gift_id=GiftAlias.PREMIUM_3_MONTHS, 
            text="Поздравляю! 🎉"
        )
        
        # Дарение Premium-подписки
        await bot.gift_premium_subscription(user_id=123456, months=3)
        
        # Отправка списка задач
        checklist = InputChecklist(
            title="Мои задачи на сегодня",
            tasks=[
                InputChecklistTask(text="Проверить почту", is_checked=False),
                InputChecklistTask(text="Обновить код", is_checked=True),
                InputChecklistTask(text="Написать документацию", is_checked=False)
            ]
        )
        message = await bot.send_checklist(chat_id=123456, checklist=checklist)
        logger.info(f"Checklist sent: {message.message_id}")
        
        # Получение баланса Stars с принудительным обновлением
        balance = await bot.get_star_balance(force_refresh=True)
        logger.info(f"Star balance: {balance}")
        
        # Массовая отправка сообщений
        chat_ids = [123456, 789012, 345678]
        results = await bot.bulk_send_message(
            chat_ids=chat_ids,
            text="Привет всем! 👋",
            delay=0.5  # Задержка между отправками
        )
        
        # Получение аналитики
        analytics = bot.get_analytics()
        logger.info(f"Bot analytics: {analytics}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Система событий
```python
async def on_gift_sent(data):
    print(f"Gift sent to chat {data['chat_id']}: {data['gift_id']}")

async def on_message_sent(data):
    print(f"Message {data['message_id']} sent to chat {data['chat_id']}")

async def main():
    async with CustomGiftSend(token="ВАШ_ТОКЕН") as bot:
        # Добавление обработчиков событий
        bot.add_event_handler("gift_sent", on_gift_sent)
        bot.add_event_handler("message_sent", on_message_sent)
        
        # Ваш код...
```

### Улучшенный поток обновлений с обработкой ошибок
```python
async def error_handler(error):
    logger.error(f"Error in updates stream: {error}")
    # Здесь можно добавить логику восстановления

async def main():
    async with CustomGiftSend(token="ВАШ_ТОКЕН") as bot:
        async for update in bot.updates_stream(
            timeout=60,
            error_handler=error_handler
        ):
            if update.message:
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"Получено: {update.message.text}"
                )
```

### Работа с файлами
```python
async def main():
    async with CustomGiftSend(token="ВАШ_ТОКЕН") as bot:
        # Отправка фото
        with open("photo.jpg", "rb") as photo:
            await bot.send_photo(
                chat_id=123456,
                photo=photo.read(),
                caption="Красивое фото! 📸"
            )
        
        # Получение информации о файле
        file_info = await bot.get_file("BAADBAADrwADBREAAYdaAAE...")
        
        # Скачивание файла
        file_data = await bot.download_file(file_info["file_path"])
        with open("downloaded_file", "wb") as f:
            f.write(file_data)
```

## 🔧 API-справочник

### Основные методы подарков
- `send_gift(chat_id, gift_id, **kwargs)` - Отправка подарка по ID
- `send_simple_gift(chat_id, gift_id, **kwargs)` - Отправка подарка с GiftAlias
- `gift_premium_subscription(user_id, months, **kwargs)` - Дарение Premium
- `transfer_gift(recipient_user_id, **kwargs)` - Перевод подарка
- `get_star_balance(force_refresh=False)` - Получение баланса Stars
- `get_available_gifts(force_refresh=False)` - Список доступных подарков
- `refund_star_payment(user_id, charge_id)` - Возврат платежа Stars

### Методы сообщений
- `send_message(chat_id, text, **kwargs)` - Отправка сообщения
- `send_message_safe(chat_id, text, **kwargs)` - Безопасная отправка
- `edit_message_text(text, **kwargs)` - Редактирование сообщения
- `delete_message(chat_id, message_id)` - Удаление сообщения
- `forward_message(chat_id, from_chat_id, message_id, **kwargs)` - Пересылка
- `bulk_send_message(chat_ids, text, delay=0.1, **kwargs)` - Массовая отправка

### Методы чатов
- `get_chat(chat_id, force_refresh=False)` - Информация о чате
- `get_chat_administrators(chat_id)` - Администраторы чата
- `get_chat_member_count(chat_id)` - Количество участников
- `set_chat_title(chat_id, title)` - Установка названия
- `set_chat_description(chat_id, description)` - Установка описания
- `pin_chat_message(chat_id, message_id)` - Закрепление сообщения
- `leave_chat(chat_id)` - Покидание чата

### Методы чеклистов
- `send_checklist(chat_id, checklist, **kwargs)` - Отправка чеклиста
- `edit_message_checklist(checklist, **kwargs)` - Редактирование чеклиста

### Методы файлов
- `send_photo(chat_id, photo, **kwargs)` - Отправка фото
- `send_document(chat_id, document, **kwargs)` - Отправка документа
- `get_file(file_id)` - Информация о файле
- `download_file(file_path)` - Скачивание файла

### Утилиты и аналитика
- `get_bot_info()` - Информация о боте
- `health_check()` - Проверка состояния
- `get_analytics()` - Получение аналитики
- `updates_stream(timeout, limit, error_handler)` - Поток обновлений

## 🛡️ Безопасность

### Конфигурация SecurityConfig
```python
@dataclass
class SecurityConfig:
    max_request_size: int = 50 * 1024 * 1024  # Максимальный размер запроса
    rate_limit_requests: int = 30              # Лимит запросов
    rate_limit_window: int = 60                # Окно лимита (секунды)
    allowed_ips: Optional[Set[str]] = None     # Разрешенные IP
    webhook_secret_token: Optional[str] = None # Секретный токен webhook
    encrypt_sensitive_data: bool = True        # Шифрование данных
    max_concurrent_requests: int = 100         # Максимум concurrent запросов
    request_timeout_multiplier: float = 1.5    # Множитель таймаута
    enable_request_signing: bool = True        # Подписывание запросов
```

### Валидация webhook
```python
def custom_webhook_validator(data: dict) -> bool:
    # Ваша логика валидации
    return "update_id" in data

bot.add_webhook_validator(custom_webhook_validator)
```

## 📊 Аналитика

Модуль предоставляет подробную аналитику:
- Общее количество запросов
- Успешные и неудачные запросы
- Время ответа (среднее и распределение)
- Ошибки по типам
- Отправленные сообщения и подарки
- Время работы бота
- Процент успешности

## ⚠️ Обработка ошибок

```python
from custom_gift_send import (
    TelegramBadRequestError,
    TelegramTooManyRequestsError,
    SecurityError,
    RateLimitError,
    ValidationError
)

try:
    await bot.send_simple_gift(
        chat_id="invalid", 
        gift_id=GiftAlias.PREMIUM_1_MONTH
    )
except ValidationError as e:
    logger.error(f"Validation error: {e}")
except TelegramBadRequestError as e:
    logger.error(f"API error: {e.description}")
except SecurityError as e:
    logger.error(f"Security error: {e}")
except RateLimitError as e:
    logger.error(f"Rate limit exceeded: {e}")
```

## 🔄 Миграция с версии 2.0.x

1. Обновите зависимости:
```bash
pip install custom-gift-send>=2.1.0
```

2. Добавьте конфигурацию безопасности:
```python
from custom_gift_send import SecurityConfig

security_config = SecurityConfig()
bot = CustomGiftSend(token="TOKEN", security_config=security_config)
```

3. Используйте новые методы:
```python
# Старый способ
balance = await bot.get_star_balance()

# Новый способ с принудительным обновлением
balance = await bot.get_star_balance(force_refresh=True)
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Добавьте тесты для новой функциональности
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

### Разработка
```bash
git clone https://github.com/Nsvl/custom-gift-send.git
cd custom-gift-send
pip install -e .[dev]
pytest
```

## 📞 Поддержка

- **Telegram канал**: [@GifterChannel](https://t.me/GifterChannel)
- **Issues**: [GitHub Issues](https://github.com/Nsvl/custom-gift-send/issues)
- **Email**: huff-outer-siding@duck.com

## 📄 Лицензия

MIT License. Подробности в файле [LICENSE](LICENSE).

## 🎉 Благодарности

Спасибо всем, кто использует и развивает этот проект! Ваши отзывы и предложения делают модуль лучше.

---

**Custom Gift Send v2.1.0** - Ваш надежный и безопасный спутник в мире Telegram Bot API! 🚀🔒