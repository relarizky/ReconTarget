from app.model import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for
from .home import home_bp

@home_bp.route('/users')
@login_required
def users():
    if current_user.user_role.id == 1:
        page = request.args.get('page', 1, type = int)
        user = User.query.paginate(page, 10, False)
        return render_template('home/user.html', users = user)
    else:
        return redirect(url_for('home.index'))


@home_bp.route('/users/edit/<int:id>')
@login_required
def user_edit(id):
    if current_user.user_role.id == 1:
        user = User.query.get(id)
        return 'konto'
    else:
        return redirect(url_for('home.index'))
