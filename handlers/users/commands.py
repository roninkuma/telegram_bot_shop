from telebot.types import Message
from data.loader import bot, db
from .text_handlers import start_register

@bot.message_handler(commands=['start'], chat_types='private')
def command_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'''Здравствуйте, {message.from_user.full_name}
Вас приветствует бот интернет магазин''')
    start_register(message)