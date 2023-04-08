from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tccs.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

# sorasutccs@gmail.com
# EC21DFA97E9C58523ECAADE2B1115D7F013C
# smtp.elasticemail.com
# 2525
# f4cbc274-c85c-47f7-a5c0-099ca3f19b88

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

user = "customer"
def change(x):
    global user
    user=x
def get():
    return user  


login_manager.login_view = "login_customer_page"
login_manager.login_message_category = "info"
from tccs import routes
