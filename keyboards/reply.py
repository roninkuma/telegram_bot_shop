from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db

def generate_contact_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Отправить свой номер', request_contact=True)
    markup.add(btn)
    return markup

def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text='Сделать заказ 🛍')
    card = KeyboardButton(text='Корзина 🛒')
    feedback = KeyboardButton(text='Написать отзыв ✨')
    settings = KeyboardButton(text='Настройки ⚙')
    info = KeyboardButton(text='Информация ⚠')
    markup.row(order)
    markup.row(card, feedback)
    markup.row(settings, info)
    return markup


def generate_categories():
    categories = db.get_categories()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for item in categories:
        btn = KeyboardButton(text=item[0])
        buttons.append(btn)
    markup.add(*buttons)
    return markup






