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
        wp_users = WPUserFinder(target.target_url)
        wp_users = set(wp_users.find_from_wp_json() + wp_users.find_from_author_page())
        wp_users = list(wp_users)

        if target.wpuser.first() == None:
            wp_user = WPUser(target, wp_users)
            db.session.add(wp_user)
            db.session.commit()
        else:
            wp_user = WPUser.query.get(target.wpuser.first().id)
            wp_user.list_username = wp_users
            db.session.add(wp_user)
            db.session.commit()

        flash('success', 'Found {} usernames in {}'.format(str(len(wp_users)), target.target_url))
        return redirect(url_for('home.wp_user_finder_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.wp_user_finder_index'))
