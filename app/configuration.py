import os
from helper.general import get_config

class Config(object):

    # General Configuration
    #DEBUG = True
    CONFIG = os.getcwd() + '/config.json'
    SECRET_KEY = get_config('SECRET_KEY')

    # Database Credentials
    MYSQL_HOSTNAME = get_config('MYSQL_HOSTNAME')
    MYSQL_USERNAME = get_config('MYSQL_USERNAME')
    MYSQL_PASSWORD = get_config('MYSQL_PASSWORD')
    MYSQL_DB_NAME  = get_config('MYSQL_DB_NAME')

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
