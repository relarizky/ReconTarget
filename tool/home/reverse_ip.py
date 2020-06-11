from app.model import *
from helper.user import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash
from .home import home_bp

@home_bp.route('/revip')
@login_required
def reverse_ip_index():
    page = request.args.get('page', 1, type = int)
    revip = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/revip/list_target.html', revips = revip)


@home_bp.route('/revip/scan/<int:id>')
@login_required
def reverse_ip_scan(id):
    pass
