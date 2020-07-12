"""Сервер Telegram бота, запускаемый непосредственно"""
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
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

button_today = KeyboardButton('/today')
button_current_month = KeyboardButton('/currentMonth')
button_category = KeyboardButton('/categories')

markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_today).add(button_current_month).add(
    button_category)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта расходов\n\n"
        "Добавить расход: 250 такси\n"
        "За сегодня: /today\n"
        "За текущий месяц: /currentMonth\n"
        "Категории расходов: /categories",
        reply_markup = markup)


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


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    raw_message = message.text.lower().strip()
    if raw_message == 'январь':
        answer_message = expenses.get_month_statistics('01')
    elif raw_message == 'февраль':
         answer_message = expenses.get_month_statistics('02')
    elif raw_message == 'март':
         answer_message = expenses.get_month_statistics('03')
    elif raw_message == 'апрель':
         answer_message = expenses.get_month_statistics('04')
    elif raw_message == 'май':
         answer_message = expenses.get_month_statistics('05')
    elif raw_message == 'июнь':
         answer_message = expenses.get_month_statistics('06')
    elif raw_message == 'июль':
         answer_message = expenses.get_month_statistics('07')
    elif raw_message == 'август':
         answer_message = expenses.get_month_statistics('08')
    elif raw_message == 'сентябрь':
         answer_message = expenses.get_month_statistics('09')
    elif raw_message == 'октябрь':
         answer_message = expenses.get_month_statistics('10')
    elif raw_message == 'ноябрь':
         answer_message = expenses.get_month_statistics('11')
    elif raw_message == 'декабрь':
         answer_message = expenses.get_month_statistics('12')
    else:
        try:
            expense = expenses.add_expense(raw_message)
        except exceptions.NotCorrectMessage as e:
            await message.answer(str(e))
            return
        answer_message = (
            f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
            f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)