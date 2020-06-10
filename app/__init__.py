from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from .configuration import Config
from helper.general import *

app = Flask(__name__)
app.config.from_object(Config)

sql = SQLAlchemy()
csrf = CSRFProtect()
login = LoginManager()
migrate = Migrate()

sql.init_app(app)
csrf.init_app(app)
login.init_app(app)
migrate.init_app(app, sql)

from .model import *
from .register import *

# route for file downloading
@app.route('/getflag/<country>')
def get_flag(country):
    return get_flag_image(country)

# error handler
@app.errorhandler(401)
def not_authorized(error):
    return redirect(url_for('auth.login'))

# template filter
@app.template_filter('pascal_case')
def convert_text(value):
    return pascal_case(value)


@app.template_filter('text_date')
def human_readable_date(value):
    return text_date(value)
