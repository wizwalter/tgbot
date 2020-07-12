"""Сервер Telegram бота, запускаемый непосредственно"""
import logging

from aiogram import Bot, Dispatcher, executor, types
import datetime
import os

import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.environ.get('API_TOKEN')
ACCESS_ID = os.environ.get('ACCESS_ID')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта расходов\n\n"
        "Добавить расход: 250 такси\n"
        "За сегодня: /today\n"
        "За текущий месяц: /currentMonth\n"
        "Категории расходов: /categories")


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет статистику расходов за сегодня"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['currentMonth'])
async def month_statistics(message: types.Message):
    """Отправляет статистику расходов за текущий месяц в текущем году"""
    now = expenses._get_now_datetime()
    current_month = f"{now.month:02d}"
    answer_message = expenses.get_month_statistics(current_month)
    await message.answer(answer_message)

@dp.message_handler(commands=['january'])
async def january_statistics(message: types.Message):
    """Отправляет статистику расходов за январь месяц в текущем году"""
    answer_message = expenses.get_month_statistics('01')
    await message.answer(answer_message)


@dp.message_handler(commands=['february'])
async def february_statistics(message: types.Message):
    """Отправляет статистику расходов за февраль месяц в текущем году"""
    answer_message = expenses.get_month_statistics('02')
    await message.answer(answer_message)


@dp.message_handler(commands=['march'])
async def march_statistics(message: types.Message):
    """Отправляет статистику расходов за март месяц в текущем году"""
    answer_message = expenses.get_month_statistics('03')
    await message.answer(answer_message)


@dp.message_handler(commands=['april'])
async def april_statistics(message: types.Message):
    """Отправляет статистику расходов за апрель месяц в текущем году"""
    answer_message = expenses.get_month_statistics('04')
    await message.answer(answer_message)


@dp.message_handler(commands=['may'])
async def may_statistics(message: types.Message):
    """Отправляет статистику расходов за май месяц в текущем году"""
    answer_message = expenses.get_month_statistics('05')
    await message.answer(answer_message)


@dp.message_handler(commands=['june'])
async def june_statistics(message: types.Message):
    """Отправляет статистику расходов за июня месяц в текущем году"""
    answer_message = expenses.get_month_statistics('06')
    await message.answer(answer_message)


@dp.message_handler(commands=['july'])
async def july_statistics(message: types.Message):
    """Отправляет статистику расходов за июль месяц в текущем году"""
    answer_message = expenses.get_month_statistics('07')
    await message.answer(answer_message)


@dp.message_handler(commands=['august'])
async def august_statistics(message: types.Message):
    """Отправляет статистику расходов за август месяц в текущем году"""
    answer_message = expenses.get_month_statistics('08')
    await message.answer(answer_message)


@dp.message_handler(commands=['september'])
async def september_statistics(message: types.Message):
    """Отправляет статистику расходов за сентябрь месяц в текущем году"""
    answer_message = expenses.get_month_statistics('09')
    await message.answer(answer_message)


@dp.message_handler(commands=['october'])
async def october_statistics(message: types.Message):
    """Отправляет статистику расходов за октябрь месяц в текущем году"""
    answer_message = expenses.get_month_statistics('10')
    await message.answer(answer_message)


@dp.message_handler(commands=['november'])
async def november_statistics(message: types.Message):
    """Отправляет статистику расходов за ноябрь месяц в текущем году"""
    answer_message = expenses.get_month_statistics('11')
    await message.answer(answer_message)


@dp.message_handler(commands=['december'])
async def december_statistics(message: types.Message):
    """Отправляет статистику расходов за декабрь месяц в текущем году"""
    answer_message = expenses.get_month_statistics('12')
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""   
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)