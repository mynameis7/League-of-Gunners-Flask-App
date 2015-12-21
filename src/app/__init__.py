import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from flask_turbolinks import turbolinks
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "1qaz@WSX"
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

#turbolinks(app)

from app import views, models
