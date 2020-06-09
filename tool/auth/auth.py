from app import login
from app.model import *
from flask_login import login_user, logout_user, current_user
from flask import Blueprint, render_template, request, url_for, redirect, flash

auth_bp = Blueprint('auth', __name__, static_folder = 'assets', template_folder = 'views')

@login.user_loader
def user_loader(id):
    return User.query.get(id)


@auth_bp.route('/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated != True:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember = request.form.get('remember')

            user = User.query.filter_by(user_name = username).first()
            if user != None and user.check_password(password) == True:
                login_user(user, remember = bool(remember))
                return redirect(url_for('home.index'))
            else:
                return redirect(url_for('auth.login'))
        else:
            return render_template('auth/login.html')
    else:
        return redirect(url_for('home.index'))


@auth_bp.route('/logout')
def logout():
    if current_user.is_active == True:
        logout_user()
    return redirect(url_for('auth.login'))
