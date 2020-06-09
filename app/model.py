import bcrypt
from app import sql as db
from datetime import datetime
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'tb_role'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(13), nullable = False, unique = True)
    user = db.relationship('User', backref = 'user_role', lazy = 'dynamic')

    def __init__(self, name = None):
        self.name = name


class User(db.Model, UserMixin):
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key = True)
    id_role = db.Column(db.Integer, db.ForeignKey('tb_role.id'))
    real_name = db.Column(db.String(40), nullable = False, unique = True)
    user_name = db.Column(db.String(20), nullable = False, unique = True)
    pass_word = db.Column(db.String(63), nullable = False)

    def secure_password(self, plaintext):
        pass_salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(plaintext.encode('utf-8'), pass_salt)
        self.pass_word = pass_hash.decode('utf-8')

    def check_password(self, text_pass):
        return bcrypt.checkpw(text_pass.encode('utf-8'), self.pass_word.encode('utf-8'))

    def __init__(self, user_role, real_name, user_name):
        self.user_role = user_role
        self.real_name = real_name
        self.user_name = user_name


class Target(db.Model):
    __tablename__ = 'tb_target'

    id = db.Column(db.Integer, primary_key = True)
    target_url = db.Column(db.String(50), nullable = False)
    target_comment = db.Column(db.String(20), nullable = True)
    target_status_code = db.Column(db.String(3), default = '-')
    submited_at = db.Column(db.Date, default = datetime.utcnow)

    def __init__(self, url = None, comment = None):
        self.target_url = url
        self.target_comment = comment
