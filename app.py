import flask_login
from flask import Flask, request, jsonify, json, render_template, flash, redirect, url_for, session

from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from pony.flask import Pony
from controllers.database import PonyDB
from flask_bcrypt import Bcrypt
import os
from flask_socketio import SocketIO
from controllers.treebot import  Chatbot

app = Flask(__name__)
app.config['TESTING'] = False
#app.debug = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

UPLOAD_FOLDER = os.path.abspath('static/products/')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app)


login_manager = LoginManager()

login_manager.init_app(app)

bcrypt = Bcrypt(app)

Pony(app)

ponyDB = PonyDB(bcrypt)

chatbot = Chatbot()




@app.before_request
def before_request():
    session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=15)

@login_manager.user_loader
def load_user(id):
    user = ponyDB.get_user_by_id(id)
    return user

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/')
@login_required
def home():
    products = ponyDB.get_products()
    categories = [product['category'] for product in products]
    print(set(categories))
    return render_template('index.html', products=products, categories=list(set(categories)))


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/validate_login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = ponyDB.get_user(username)

    if user is not None:
        if not bcrypt.check_password_hash(user.password, password):
            print(bcrypt.check_password_hash(user.password, password))
            flash('Please check your login details and try again.')
            return redirect(url_for('login_get'))
        login_user(user)

        return redirect(url_for('home'))
    flash('Please check your login details and try again.')
    return redirect(url_for('login_get'))

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/handlesignup', methods=['POST'])
def handle_signup():

    username = request.form.get('username')
    password = request.form.get('password')
    user = ponyDB.get_user(username)
    print('user', username)
    print('password', password)

    if user is not None:
        flash('username already exists.')
        return redirect(url_for('app.signup'))

    ponyDB.add_user(username, bcrypt.generate_password_hash(password))
    user = ponyDB.get_user(username)

    login_user(user)

    return render_template('userdetails.html')


def messageReceived(methods=['GET', 'POST']):

    print('message was received!!!')

subcategory = None
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print ('user id is ', current_user.gender)
    if 'data' in json.keys():
        print(str(json))
    response_data = {}

    if 'message' in json.keys():
        message = json['message']
        response = chatbot.get_answer(message)
        products = []
        degree = response[1]
        print('degree is', degree)
        name = response[2]
        print('in app', name)

        product_list = []
        print('degree', degree)

        if degree == 'category':
            products = ponyDB.get_product_by_category(product_category=name, user_gender=current_user.gender)
        elif degree == 'subcategory':
            products = ponyDB.get_product_by_subcategory(product_subcategory=name, user_gender=current_user.gender)
        elif degree == 'brand':
            subcategory = response[3]
            print('getting products by brand')
            products = ponyDB.get_product_by_brand(product_subcategory=subcategory, product_brand=name, user_gender=current_user.gender)
        elif degree == 'general_answer':
            print('len name', len(name))
            for n in name:
                print('n is '+n)
                products += ponyDB.get_product_by_subcategory(product_subcategory=str(n), user_gender=current_user.gender)
        elif degree == 'price_answer':
                products = ponyDB.get_product_by_price(price=name)

        else:
            products = ponyDB.get_products()

        if products is not None:
            product_list = products

        response_data['response'] = response[0]
        response_data['products'] = product_list

    socketio.emit('my response', response_data, callback=messageReceived)



@app.route('/get_products', methods=['POST', 'GET'])
@login_required
def get_products():
    #user_id = int(request.form.get('user_id'))
    message = str(request.form.get('message'))
    print('message ', message)
    response = chatbot.get_answer(message)

    return response[0]

@app.route('/questionaire', methods=['GET'])
def questionaire():

    age = request.form.get('age')
    gender = request.form.get('gender')
    user_id = 1

    #ponyDB.add_userdetails(user_id, age, gender, question1, question2, question3, question4)

    return render_template('userdetails.html')

@app.route('/postdetails', methods=['GET'])
def post_details():
    return "success"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_get'))


if __name__ == '__main__':
    app.run(port=5020)
    #app.run()
