from app.model import *
from helper.user import *
from helper.general import *
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash
from .home import home_bp

@home_bp.route('/users')
@login_required
def users():
    if current_user.user_role.id == 1:
        page = request.args.get('page', 1, type = int)
        role = Role.query.all()
        user = User.query.paginate(page, 5, False)
        return render_template('home/user/list_user.html', users = user, roles = role)
    else:
        return redirect(url_for('home.index'))


@home_bp.route('/users/add', methods = ['GET', 'POST'])
@login_required
def add_user():
    if current_user.user_role.id == 1:
        if request.method == 'POST':
            realname = request.form.get('realname', '')
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            id_role  = request.form.get('id_role', type = int)

            if not filter_register_form(realname, username, password, id_role):
                return redirect(url_for('home.add_user'))

            try:
                role = Role.query.get(id_role)
                user = User(role, realname, username)
                user.secure_password(password)
                db.session.add(user)
                db.session.commit()
            except IntegrityError as Duplicated:
                flash('error', 'User is duplicated')
                return redirect(url_for('home.add_user'))

            flash('success', 'Successfully added new user.')
            return redirect(url_for('home.users'))
        else:
            roles = Role.query.all()
            return render_template('home/user/add_user.html', roles = roles)
    else:
        return redirect(url_for('home.index'))


@home_bp.route('/users/delete/<int:id>')
@login_required
def user_delete(id):
    if current_user.user_role.id == 1:
        user = User.query.get(id)
        if user != None:
            db.session.delete(user)
            db.session.commit()
            flash('success', 'Sucessfully delete user')
            return redirect(url_for('home.users'))
        else:
            flash('error', 'Cant find user with id {}'.format(str(id)))
            return redirect(url_for('home.users'))
    else:
        return redirect(url_for('home.index'))


@home_bp.route('/users/edit/<int:id>', methods = ['POST'])
@login_required
def user_edit(id):
    if current_user.user_role.id == 1:
        id_role  = request.form.get('id_role', type = int)
        realname = request.form.get('realname', '')
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if not filter_edit_form(realname, username, password, id_role):
            return secure_redirect(request.headers.get('referer'), url_for('home.users'))

        role = Role.query.get(id_role)
        user = User.query.get(id)
        user.user_role = role
        user.real_name = realname
        user.user_name = username
        if password != '':
            user.secure_password(password)

        db.session.add(user)
        db.session.commit()

        flash('success', 'Successfully edit user.')
        return secure_redirect(request.headers.get('referer'), url_for('home.users'))
    else:
        return redirect(url_for('home.index'))
