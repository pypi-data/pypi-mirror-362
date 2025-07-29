from setuptools import setup, find_packages
import os

# Чтение README.md для long_description
# Проверяем, существует ли README.md, чтобы избежать ошибок при сборке без него
current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='custom-gift-send',
    version='0.3.0', # <-- Установите здесь желаемую версию!
    author='Nsvl', # <-- Укажите ваше имя
    author_email='testtelegasms2@gmail.com', # <-- Укажите ваш email
    description='Асинхронный Python-модуль для взаимодействия с Telegram Bot API (подарки и Stars).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nsvl/custom-gift-send', # <-- Опционально: ссылка на ваш репозиторий GitHub
    packages=find_packages(), # Автоматически находит пакеты (в данном случае 'custom_gift_send')
    install_requires=[
        'aiohttp>=3.0.0', # Указываем минимальную версию aiohttp
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    keywords='telegram bot api stars gift premium', # Ключевые слова для поиска на PyPI
)