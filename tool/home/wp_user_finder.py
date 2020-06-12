import os
import tempfile

from app.model import *
from helper.user import *
from helper.reverse_ip import *

from .home import home_bp
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file

@home_bp.route('/wpuserfinder')
@login_required
def wp_user_finder_index():
    pass
