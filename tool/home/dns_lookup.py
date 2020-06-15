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
