import os
import tempfile

from app.model import *
from helper.user import *
from helper.reverse_ip import *
from helper.wp_user_finder import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/wpuserfinder')
@login_required
def wp_user_finder_index():
    page = request.args.get('page', 1, type = int)
    wpuser = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/wpuser/list_target.html', wpusers = wpuser)


@home_bp.route('/wpuserfinder/scan/<int:id>')
@login_required
def wp_user_finder_scan(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.dns_lookup_index'))
        if target.target_status_code == 'dead':
            flash('error', 'The site seems to be dead')
            return redirect(url_for('home.wp_user_finder_index'))
        try:
            wp_users = WPUserFinder(target.target_url)
            wp_users = set(wp_users.find_from_wp_json() + wp_users.find_from_author_page())
            wp_users = list(wp_users)

            if len(wp_users) != 0:
                if target.wpuser.first() == None:
                    wp_user = WPUser(target, wp_users)
                    db.session.add(wp_user)
                    db.session.commit()
                else:
                    wp_user = WPUser.query.get(target.wpuser.first().id)
                    wp_user.list_username = wp_users
                    db.session.add(wp_user)
                    db.session.commit()
            else:
                flash('error', 'No username found in target {}'.format(target.target_url))
                return redirect(url_for('home.wp_user_finder_index'))
        except Exception as Error:
            flash('error', 'Failed to fetch username bcz, {}'.format(Error))
            return redirect(url_for('home.wp_user_finder_index'))
        else:
            flash('success', 'Found {} usernames in {}'.format(str(len(wp_users)), target.target_url))
            return redirect(url_for('home.wp_user_finder_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.wp_user_finder_index'))


@home_bp.route('/wpuserfinder/download/<int:id>')
@login_required
def wp_user_finder_download(id):
    tempfile.tempdir = os.getcwd()
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.wp_user_finder_index'))

        if target.wpuser.first() == None:
            flash('error', 'You have not done any scan this target')
            return redirect(url_for('home.wp_user_finder_index'))

        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile.tempdir = temp_dir
            file_name = 'wpuser_' + get_info(target.target_url, info = 'domain') + '.txt'
            file_object = tempfile.NamedTemporaryFile(mode = 'w+t')
            file_content = target.wpuser.first().list_username

            try:
                file_object.writelines('\n'.join(file_content))
                file_object.seek(0)
                response = send_file(file_object.name,
                    mimetype='text/plain',
                    as_attachment = True,
                    attachment_filename = file_name)
                response.headers['Content-Length'] = os.path.getsize(file_object.name)
                response.headers['Cache-Control'] = 'no-cache'
            finally:
                file_object.close()

            return response
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.wp_user_finder_index'))


@home_bp.route('/wpuserfinder/view_raw/<int:id>')
@login_required
def wp_user_finder_view_raw(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.wp_user_finder_index'))
        elif target.wpuser.first() == None:
            flash('error', 'You have not done any scan to this target')
            return redirect(url_for('home.wp_user_finder_index'))
        else:
            return '<br>'.join(target.wpuser.first().list_username)
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.wp_user_finder_index'))
