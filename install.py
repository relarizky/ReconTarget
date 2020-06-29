#!/usr/bin/python3

import os
import json
import getpass

if os.path.exists(os.getcwd() + '/config.json') != True:
    # Ask for credentials
    db_host = input('DB HOSTNAME\t: ')
    db_user = input('DB USERNAME\t: ')
    db_pass = getpass.getpass('DB PASSWORD\t: ')
    db_name = input('DB NAME\t\t: ')
    secret_key = input('SECRET KEY\t: ')

    # Create config file
    file_name = 'config.json'
    file_content = {
        'SECRET_KEY' : secret_key,
        'MYSQL_HOSTNAME' : db_host,
        'MYSQL_USERNAME' : db_user,
        'MYSQL_PASSWORD' : db_pass,
        'MYSQL_DB_NAME' : db_name
    }

    with open(file_name, 'w') as config:
        json.dump(file_content, config, indent = 4)

    # Create migration and run seeder.py for inserting default role and user
    os.system('flask db init; flask db migrate; flask db upgrade; python3 seeder.py')
