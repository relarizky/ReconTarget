from app.model import *
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, url_for

home_bp = Blueprint('home', __name__, template_folder = 'views')

from .user import *

@home_bp.route('/')
@home_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type = int)
    return render_template('template.html')
