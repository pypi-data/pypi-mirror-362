from setuptools import setup, find_packages
import os

# Чтение README.md для long_description
current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='custom-gift-send',
    version='1.5.0',
    author='NSvl',
    author_email='huff-outer-siding@duck.com',
    description='Асинхронный Python-модуль для Telegram Bot API (подарки, Stars, списки задач, бизнес-аккаунты).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nsvl/custom-gift-send',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.0.0',
        'pydantic>=1.10.0',
        'cachetools>=5.0.0',
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
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.7',
    keywords='telegram bot api stars gift premium checklist business account',
)