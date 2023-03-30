from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tccs.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_customer_page"
login_manager.login_message_category = "info"

user = "customer"
def change(x):
    global user
    user=x
def get():
    return user    
from tccs import routes
