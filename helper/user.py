from flask import flash
from flask_login import current_user

def filter_register_form(realname, username, password, id_role):
    error = 0

    if len(realname) == 0 or len(username) == 0 or len(password) == 0 or id_role == None:
        flash('error', 'You need to fill all the fields.')
        error += 1
    else:
        if len(username) < 5 or len(username) > 40:
            flash('error', 'Username cant be less than 5 and cant be more than 40.')
            error += 1
        if len(password) < 8:
            flash('error', 'Password cant be less than 8 characters.')
            error += 1
        if id_role not in [1, 2]:
            flash('error', 'Invalid id role.')
            error += 1

    return error == 0


def filter_edit_form(realname, username, new_password, id_role = None):
    error = 0

    if len(realname) == 0 or len(username) == 0:
        flash('error', 'You need to fill all the required fields.')
        error += 1
    else:
        if len(username) < 5 or len(username) > 40:
            flash('error', 'Username cant be less than 5 and cant be more than 40.')
            error += 1
        if len(new_password) != 0 and len(new_password) < 8:
            flash('error', 'Password cant be less than 8 characters.')
            error += 1
        if id_role != None and id_role not in [1, 2]:
            flash('error', 'Invalid id role.')
            error += 1

    return error == 0
