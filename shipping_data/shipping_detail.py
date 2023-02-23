from telebot.types import ShippingOption, LabeledPrice
from .shipping_product import Product


def generate_product_invoice(product_data):
    query = Product(
        title='Лучший бот телеграм магазин',
        description='\n'.join([title for title in product_data]),
        start_parameter='create_invoice_products',
        currency='UZS',
        prices=[LabeledPrice(
            label=f"{product_data[title]['quantity']} x {title}",
            amount=int(product_data[title]['quantity']) * int(product_data[title]['price']) * 100
        )
            for title in product_data],
        need_name=True
    )
    return query