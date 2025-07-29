from setuptools import setup, find_packages

setup(
    name="custom-gift-send",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    author="Your Name",
    description="A Python library for sending Telegram gifts and premium subscriptions",
    url="https://github.com/Nsvl/custom-gift-send",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)