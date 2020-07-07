from app import app
from tool.home import home
from tool.auth import auth

app.register_blueprint(auth.auth_bp, url_prefix = '/')
app.register_blueprint(home.home_bp, url_prefix = '/recon')
