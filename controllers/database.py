from pony.orm import *
from flask_login import UserMixin
import json
import random
class PonyDB:
    db = Database()

    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
        self.seed = False

        self.db.bind(provider='sqlite', filename='shop', create_db=True)

        self.db.generate_mapping(create_tables=True)

        if self.seed:
            self.seed_database('controllers/seed.json')

    class Product(db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str)
        category = Optional(str)
        subcategory = Optional(str)
        price = Optional(int)
        description = Optional(str)
        image = Optional(str)
        brand = Optional(str)
        gender = Optional(str)


    class User(UserMixin, db.Entity):
        id = PrimaryKey(int, auto=True)
        username = Required(str, unique=True)
        password = Required(bytes, unique=True)
        age = Optional(int)
        gender = Optional(str)
        occupation = Optional(str)
        question_1 = Optional(str)
        question_2 = Optional(str)

    @db_session
    def add_user(self, username, password):
        PonyDB.User(username=username, password=password)

    @db_session
    def add_product(self, title ,category,subcategory, price, description, image):
        PonyDB.User(title=title, category=category, subcategory=subcategory, price=price,  description=description, image=image )

    @db_session
    def add_user_details(self, id, age, gender, question1):
        PonyDB.UserDetails(user_id=id, age=age, gender=gender, question_1=question1)

    @db_session
    def get_products(self):
        #result = PonyDB.Product.select()
        result =  PonyDB.Product.select_by_sql("SELECT * FROM Product ORDER BY RANDOM()")

        if len(result) > 0:
            return self.serialize_result(result)
        else:
            return None

    @db_session
    def get_product_by_id(self, product_id):
        result = PonyDB.Product.select(lambda p: p.id == product_id).page(1)
        if len(result) > 0:
            result = result[0]
            return result
        else:
            return None

    @db_session
    def get_product_by_category(self, product_category='', user_gender='neutral'):
        result = PonyDB.Product.select_by_sql("SELECT * FROM Product WHERE  category like '%"+str(product_category).lower() +"%' and (gender='"+user_gender+"' or gender='neutral')")

        if len(result) > 0:
            return self.serialize_result(result)
        else:
            return None

    @db_session
    def get_product_by_subcategory(self, product_subcategory='',  user_gender='neutral'):
        print("inside query", product_subcategory, user_gender)
        result = PonyDB.Product.select_by_sql("SELECT * FROM Product WHERE  subcategory like '%"+product_subcategory +"%'" )# and (gender='"+user_gender+"'  or gender='neutral')")

        if len(result) > 0:
            return self.serialize_result(result)
        else:
            return None

    @db_session
    def get_product_by_brand(self, product_subcategory='', product_brand='',  user_gender='neutral'):
        result = PonyDB.Product.select_by_sql("SELECT * FROM Product WHERE  subcategory like '%"+product_subcategory + "%' and brand like '%"+ product_brand+"%' and (gender='"+user_gender+"' or gender='neutral')")

        if len(result) > 0:
            return self.serialize_result(result)
        else:
            return None

    @db_session
    def get_product_by_price(self,product_subcategory='', product_brand='', price='',   user_gender='neutral'):
        print('price is', price, "type", type(price))
        price = price * 100

        #result = PonyDB.Product.select_by_sql("SELECT * FROM Product WHERE  subcategory like '%"+str(product_subcategory).lower() + "%' and brand like '%"+ product_brand+"%' and (gender='"+user_gender+"' or gender='neutral') and price <=" + price)
        result = PonyDB.Product.select_by_sql("SELECT * FROM Product WHERE  (gender='"+user_gender+"' or gender='neutral') and price <=" + str(price) +" ORDER BY price DESC ")

        if len(result) > 0:
            return self.serialize_result(result)
        else:
            return None

    @db_session
    def get_random_products(self, size):
        result = PonyDB.Product.select_by_sql("SELECT * FROM Product ORDER BY RANDOM()")
        if len(result) > 0:
            return self.serialize_result(result, size)
        else:
            return None

    @db_session
    def get_user(self, username):
        result = PonyDB.User.select(lambda s: s.username == username).page(1)
        if len(result) > 0:
            result = result[0]
            return result
        else:
            return None

    @db_session
    def get_user_by_id(self, userid):
        result = PonyDB.User.select(lambda s: s.id == userid).page(1)
        if len(result) > 0:
            result = result[0]
            return result
        else:
            return None

    @db_session
    def seed_database(self, dump_filename):

        data = json.load(open(dump_filename, 'r'))
        for record in data['Users']:
            print(record['username'])
            user = PonyDB.User(username=record['username'], password=self.bcrypt.generate_password_hash(record['password']))

    @db_session
    def serialize_result(self, products, size_=30):
        product_list = []
        for row in products:

            row_dict = {}
            row_dict['id'] = row.id
            row_dict['title'] = row.title
            row_dict['image'] = row.image
            row_dict['price'] ='€ '+str(float(row.price/100))
            row_dict['category'] = row.category
            row_dict['subcategory'] = row.subcategory
            row_dict['description'] = row.description
            product_list.append(row_dict)
        print(product_list)

        return product_list[:size_]
