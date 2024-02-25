import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN = '7023815986:AAGqZLAIqYsFG30fsN2FLvVka8EPGK6mCNY'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# кол-во попыток
ATTEMPTS = 6

# словарь для хранения данных пользователя
users = {}


# Функция возвращающая случайное число
def get_random_number() -> int:
    return random.randint(1, 100)


'''
# Объявляем пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0,
        'loss': 0}
'''

# хендлер для /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )
    # если нов.пользов., то добавим в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0,
            'loss': 0

        }


# хендлер для /help
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# хендлер для /stat
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}\n'
        f'Игр проиграно: {users[message.from_user.id]['loss']}'
        # f'Вас зовут: {users[message.from_user.first_name]}'
    )


# хендлер для /cansel
@dp.message(Command(commands='cansel'))
async def process_cansel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await  message.answer(
            'А мы итак с вами не играем. '
            'Может, сыграем разок?'
        )


# хендлер согласие начать игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            f'Ура!\n\nЯ загадал число от 1 до 100, '
            f'попробуй угадать!\n\n'
            f'У Вас осталось {users[message.from_user.id]['attempts']} попыток'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# хендлер отказ начать игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# хендлер реагирует на числа от 1 до 100
# (реагирует на попытку пользователя угадать число)
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id][
            'secret_number']:  # если введенное число равно загаданному системой
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Мое число меньше\n'
                                 f'У Вас осталось {users[message.from_user.id]['attempts']} попыток')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше\n'
                                 f'У Вас осталось {users[message.from_user.id]['attempts']} попыток')
        if users[message.from_user.id]['attempts'] == 0:  # если кончились попытки
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['loss'] += 1
            await message.answer(
                f'К сожалению, у Вас больше не осталось попыток.\n'
                f'Вы проиграли :(\n\n'
                f'Мое число было {users[message.from_user.id]["secret_number"]}\n\n'
                f'Давайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# хендлер на остальные сообщения
@dp.message()
async def process_other_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
