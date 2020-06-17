import os
import tempfile

from app.model import *
from helper.whois import *
from helper.general import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/whois')
@login_required
def whois_index():
    page = request.args.get('page', 1, type = int)
    target = Target.query.filter_by(id_user = current_user.id).paginate(page, 5, False)
    return render_template('home/whois/list_target.html', targets = target)
