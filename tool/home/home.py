from app.model import *
from helper.general import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, flash

home_bp = Blueprint('home', __name__, template_folder = 'views')

from .user import *
from .reverse_ip import *
from .wp_user_finder import *

@home_bp.route('/')
@home_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type = int)
    target = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/index.html', targets = target)


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


@home_bp.route('/add', methods = ['POST'])
@login_required
def add_target():
    target_url  = request.form.get('target_url', '')

    if not filter_target_form(target_url):
        return redirect(url_for('home.index'))

    check_conn = check_connection(target_url)

    target = Target(current_user, target_url)
    target.target_url = check_conn.get('url')
    target.target_server = check_conn.get('server')
    target.target_country = get_country(target_url)
    target.target_status_code = check_conn.get('code')

    db.session.add(target)
    db.session.commit()

    flash('success', 'Successfully add target.')
    return redirect(url_for('home.index'))


@home_bp.route('/delete/<int:id>')
@login_required
def delete_target(id):
    target = Target.query.get(id)
    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.index'))
        else:
            db.session.delete(target)
            db.session.commit()
            flash('success', 'Successfully delete target.')
            return redirect(url_for('home.index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.index'))


@home_bp.route('/check/<int:id>')
@login_required
def check_target_connection(id):
    target = Target.query.get(id)

    if target != None:
        check_conn = check_connection(target.target_url)
        target.target_url = check_conn.get('url')
        target.target_status_code = check_conn.get('code')

        db.session.add(target)
        db.session.commit()
        return redirect(url_for('home.index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.index'))
