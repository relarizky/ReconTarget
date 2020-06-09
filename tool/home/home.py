from app.model import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, flash

home_bp = Blueprint('home', __name__, template_folder = 'views')

from .user import *

@home_bp.route('/')
@home_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type = int)
    return render_template('template.html')


@home_bp.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        realname = request.form.get('realname', '')
        username = request.form.get('username', '')
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')

        if not filter_edit_form(realname, username, new_password):
            return redirect(url_for('home.edit_profile'))

        current_user.real_name = realname
        current_user.user_name = username

        if old_password != '' and new_password != '':
            if current_user.check_password(old_password) == True:
                current_user.secure_password(new_password)
            else:
                flash('error', 'Old password is incorrect.')
                return redirect(url_for('home.edit_profile'))

        db.session.add(current_user)
        db.session.commit()

        flash('success', 'Successfully update profile.')
        return redirect(url_for('home.edit_profile'))
    else:
        roles = Role.query.all()
        return render_template('home/edit_profile.html', user = current_user, roles = roles)
