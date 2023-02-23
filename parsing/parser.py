import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.url = 'https://texnomart.uz/ru/katalog/telefony'
        self.host = 'https://texnomart.uz'

    # Функция которая получает страницу по ссылке
    def get_html(self, url):
        html = requests.get(url).text
        return html
    # Функция. которая превращает страницу в спец объект суп
    def get_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    # Функция сбора данных
    def get_data(self):
        soup = self.get_soup(self.get_html(self.url))
        categories = soup.find_all('div', class_='category__content')
        data = {}
        for category in categories[:2]:
            title = category.find('a', class_='category__link').get_text(strip=True)
            category_link = self.host + category.find('a', class_='category__link').get('href')
            if title == 'Смартфоны':
                continue
            data[title] = []
            category_page = self.get_html(category_link)
            category_soup = self.get_soup(category_page)
            products = category_soup.find_all('div', class_='product-item-component')
            for product in products:
                product_title = product.find('a', class_='product-name').get_text(strip=True)
                product_price = product.find('div', class_='f-16').get_text(strip=True)
                product_price = int(product_price.replace(' ', '').replace('cум', ''))
                print(product_price)
                product_link = self.host + product.find('a', class_='product-name').get('href')
                product_image_link = product.find('img').get('src')
                product_page = self.get_html(product_link)
                product_soup = self.get_soup(product_page)
                block = product_soup.find('div', class_='characteristic-item')
                items = block.find_all('div', class_='list__item')
                text = ''
                for item in items:
                    string = f"""{item.find('span', class_='mr-6').get_text(strip=True)}: {item.find('div', class_='list__value').get_text(strip=True)}\n"""
                    text += string
                data[title].append({
                    'product_title': product_title,
                    'product_price': product_price,
                    'product_link': product_link,
                    'product_image_link': product_image_link,
                    'product_characteristics': text
                })
        return data
