""" Работа с расходами — их добавление, удаление, статистики"""
import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    inserted_row_id = db.insert("expense", {
        "amount": parsed_message.amount,
        "created": str(_get_now_datetime()),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def get_today_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    now = str(_get_now_datetime().date())
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   f"from expense where date(created)=date('{now}')")
    result = cursor.fetchone()
    cursor.close()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    return (f"Расходы сегодня:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"За текущий месяц: /currentMonth")


def get_month_statistics(current_month: str) -> str:
    """Возвращает строкой статистику расходов за указанный месяц в текущем году"""
    now = _get_now_datetime()
    current_year = f"{now.year:04d}"
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense where extract(month FROM created) = {current_month} "
                   f"and extract(year from created) = {current_year}")
    result = cursor.fetchone()
    cursor.close()
    if not result[0]:
        return "В этом месяце нет расходов"
    all_month_expenses = result[0]
    return (f"Расходы в текущем месяце:\n"
            f"всего — {all_month_expenses} руб.\n")


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if regexp_result == None:
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")
    amount = regexp_result.group(1)
    category_text = regexp_result.group(2)
    return Message(amount=amount, category_text=category_text)


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now