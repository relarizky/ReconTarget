from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from .configuration import Config

app = Flask(__name__)
app.config.from_object(Config)

sql = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

sql.init_app(app)
login.init_app(app)
migrate.init_app(app, sql)

from .model import *
from .register import *


# error handler
@app.errorhandler(401)
def not_authorized(error):
    return redirect(url_for('auth.login'))

# template filter
@app.template_filter('pascal_case')
def convert_text(value):
    convert = lambda text : text.capitalize()
    strings = value.split(' ')
    strings = list(map(convert, strings))
    return ' '.join(strings)
