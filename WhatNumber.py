import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN = '7023815986:AAGqZLAIqYsFG30fsN2FLvVka8EPGK6mCNY'

def get_random_number() -> int:
    return random.randint(1, 100)


# Объявляем пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}
