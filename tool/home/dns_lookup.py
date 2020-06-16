import os
import tempfile

from app.model import *
from helper.user import *
from helper.reverse_ip import *
from helper.wp_user_finder import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/dnslookup')
@login_required
def dns_lookup_index():
    page = request.args.get('page', 1, type = int)
    dnslookup = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/dnslookup/list_target.html', dnslookups = dnslookup)


@home_bp.route('/dnslookup/scan/<int:id>')
@login_required
def dns_lookup_scan(id):
    target = Target.query.get(id)

    if target != None:
        if target.id_user != current_user.id:
            flash('error', 'You are not allowed to do that!')
            return redirect(url_for('home.dns_lookup_index'))
        if target.target_status_code == 'dead':
            flash('error', 'The site seems to be dead')
            return redirect(url_for('home.dns_lookup_index'))
    else:
        flash('error', 'Cant find target with id {}'.format(str(id)))
        return redirect(url_for('home.dns_lookup_index'))
