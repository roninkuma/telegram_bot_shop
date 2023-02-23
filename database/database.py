import sqlite3

class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)
    # Основной менеджер подключения и управления базой
    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result
    # Создаем таблицу категорий товаров
    def create_categories_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) UNIQUE
        )'''
        self.manager(sql, commit=True)

    # Закидывам данные в таблицу
    def insert_into_categories(self, category_name):
        sql = '''INSERT OR IGNORE INTO categories(category_name)
        VALUES (?)'''
        self.manager(sql, category_name, commit=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT UNIQUE,
            price INTEGER,
            image TEXT,
            link TEXT,
            characteristics TEXT, 
            category_id INTEGER REFERENCES categories(category_id)
        )
        '''
        self.manager(sql, commit=True)

    def get_category_id(self, category_name):
        sql = '''
        SELECT category_id FROM categories WHERE category_name = ?
        '''
        return self.manager(sql, category_name, fetchone=True)[0]

    def insert_into_product(self, product_name, price, image, link, characteristics, category_id):
        sql = '''
        INSERT OR IGNORE INTO products(product_name, price, image, link, characteristics, category_id)
        VALUES (?,?,?,?,?,?)
        '''
        self.manager(sql, product_name, price, image, link, characteristics, category_id, commit=True)

    # INT - INTEGER -2147483648 до 2147483647
    # BIGINT -9223372036854775808 до 9223372036854775808
    # TINYINT -128 до 127

    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            contact VARCHAR(20) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def create_carts_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS carts(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            total_products INTEGER DEFAULT 0,
            total_price DECIMAL(12, 2) DEFAULT 0
        )'''
        self.manager(sql, commit=True)

    def create_cart_products_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES carts(cart_id),
            product_name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            final_price DECIMAL(12,2) NOT NULL,
            UNIQUE(cart_id, product_name)
        )'''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.manager(sql, telegram_id, fetchone=True)

    def register_user(self, telegram_id, full_name, contact):
        sql = '''INSERT INTO users(telegram_id, full_name, contact)
        VALUES (?,?,?)'''
        self.manager(sql, telegram_id, full_name, contact, commit=True)

    def create_cart(self, telegram_id):
        sql = '''INSERT INTO carts(telegram_id) VALUES (?)'''
        self.manager(sql, telegram_id, commit=True)

    def get_categories(self):
        sql = '''SELECT category_name FROM categories'''
        return self.manager(sql, fetchall=True)  # [('asd', ), ('asd', )]

    def get_count_product_in_category(self, category_name):
        sql = '''
        SELECT COUNT(product_id) FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        '''
        return self.manager(sql, category_name, fetchone=True)[0]  # (5, )

    def get_products_to_page(self, category_name, offset, limit):
        sql = '''SELECT * FROM products
        WHERE category_id = (
            SELECT category_id FROM categories WHERE category_name = ?
        )
        LIMIT ?
        OFFSET ?
        '''
        return self.manager(sql, category_name, limit, offset, fetchall=True)

    def get_product_detail(self, product_id):
        sql = '''
        SELECT * FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def get_category_name_by_id(self, category_id):
        sql = '''
        SELECT category_name FROM categories WHERE category_id = ?
        '''
        return self.manager(sql, category_id, fetchone=True)[0]  # ('Кнопочные',)
