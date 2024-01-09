from flask import Flask
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from urllib.parse import quote
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"]="hsfjrgfjwnfgwejkfnjwegnwj"
app.secret_key="sacfasfgwgwgwgwgwegehehehehru5hrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/privateclinicdb?charset=utf8mb4" % quote(
    "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE']=8
#mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] ='nguyenthikimlyts99@gmail.com'
app.config['MAIL_PASSWORD'] =os.environ.get('0335557963Aa')
#
db = SQLAlchemy(app=app)
admin= Admin(app=app, name='Quản Trị NWA', template_mode='bootstrap4')
login = LoginManager(app=app)
mail = Mail(app)
