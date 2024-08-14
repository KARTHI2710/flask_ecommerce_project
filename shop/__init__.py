from flask import Flask,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY']='karthi'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
search=Search()
#search.init_app(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message='Please login first'


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes
