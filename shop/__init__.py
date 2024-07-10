from flask import Flask,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_msearch import Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY']='karthi'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
search=Search()
#search.init_app(app)


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes
