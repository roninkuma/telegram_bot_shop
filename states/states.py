from telebot.handler_backends import State, StatesGroup


class CartState(StatesGroup):
    cart = State()
