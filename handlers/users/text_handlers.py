from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.reply import generate_contact_button, \
    generate_main_menu, generate_categories
from keyboards.inline import generate_products_pagination


def start_register(message: Message):
    chat_id = message.chat.id
    '''Спросить у базы есть пользователь
    Если его нет - начать регистрацию, если он есть показать главное меню'''
    user = db.get_user_by_id(chat_id)
    if user:
        '''Показать главное меню'''
        show_main_menu(message)
    else:
        msg = bot.send_message(chat_id, 'Отправьте свои имя и фамилию')
        bot.register_next_step_handler(msg, get_name_ask_phone)


def get_name_ask_phone(message: Message):
    full_name = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Отправьте номер телефона, нажав на кнопку',
                           reply_markup=generate_contact_button())
    bot.register_next_step_handler(msg, finish_register, full_name)


def finish_register(message:Message, full_name):
    chat_id = message.chat.id
    contact = message.contact.phone_number
    db.register_user(chat_id, full_name, contact)
    db.create_cart(telegram_id=chat_id)
    bot.send_message(chat_id, 'Регистрация прошла успешно')
    show_main_menu(message)

def show_main_menu(message: Message):
    chat_id = message.chat.id
    text = '''Что хотите сделать?'''
    bot.send_message(chat_id, text, reply_markup=generate_main_menu())


@bot.message_handler(regexp='Сделать заказ 🛍')
def reaction_to_order(message: Message):
    chat_id = message.chat.id
    text = 'Выберите категорию товаров'
    bot.send_message(chat_id, text, reply_markup=generate_categories())


categories = db.get_categories()
categories = [item[0] for item in categories]


@bot.message_handler(func=lambda message: message.text in categories)
def reaction_to_category(message: Message):
    chat_id = message.chat.id
    text = 'Выберите товар: '
    your_choice = f'Вы выбрали категорию: {message.text}'
    bot.send_message(chat_id, your_choice, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text, reply_markup=generate_products_pagination(message.text))


@bot.message_handler(regexp='Информация ⚠')
def information(message: Message):
    chat_id = message.chat.id
    text = '''Наш бот самый лучший. У нас самые низкие цены. Зовите друзей'''
    bot.send_message(chat_id, text)
