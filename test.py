from data.loader import db
from parsing.parser import Parser
from pprint import pprint

# db.create_categories_table()
# db.create_products_table()
db.create_users_table()
db.create_carts_table()
db.create_cart_products_table()

# parser = Parser()
# data = parser.get_data()
# pprint(data)
#
# for category, products in data.items():
#     db.insert_into_categories(category)
#     category_id = db.get_category_id(category)
#     print(category, category_id)
#     for product in products:
#         product_name = product['product_title']
#         product_price = product['product_price']
#         product_link = product['product_link']
#         product_image_link = product['product_image_link']
#         product_characteristics = product['product_characteristics']
#         db.insert_into_product(product_name=product_name,
#                                price=product_price,
#                                link=product_link,
#                                image=product_image_link,
#                                characteristics=product_characteristics,
#                                category_id=category_id)


