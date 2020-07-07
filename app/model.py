import bcrypt, json
from app import sql as db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import JSON

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
    target = db.relationship('Target', backref = 'user', lazy = 'dynamic', cascade = 'all, delete')

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
    id_user = db.Column(db.Integer, db.ForeignKey('tb_user.id'))
    target_url = db.Column(db.String(50), nullable = False)
    target_server = db.Column(db.String(20))
    target_country = db.Column(db.String(7))
    target_status_code = db.Column(db.String(4))
    submited_at = db.Column(db.Date, default = datetime.utcnow)

    revip = db.relationship('RevIP', backref = 'target', lazy = 'dynamic', cascade = 'all, delete')
    whois = db.relationship('Whois', backref = 'target', lazy = 'dynamic', cascade = 'all, delete')
    wpuser = db.relationship('WPUser', backref = 'target', lazy = 'dynamic', cascade = 'all, delete')
    foundlink = db.relationship('FoundLink', backref = 'target', lazy = 'dynamic', cascade = 'all, delete')
    dnslookup = db.relationship('DNSLookup', backref = 'target', lazy = 'dynamic', cascade = 'all, delete')

    def __init__(self, user, url = None):
        self.user = user
        self.target_url = url


class RevIP(db.Model):
    __tablename__ = 'tb_revip'

    id = db.Column(db.Integer, primary_key = True)
    id_target = db.Column(db.Integer, db.ForeignKey('tb_target.id'))
    list_domain = db.Column(JSON)

    def __init__(self, target, domains = []):
        self.target = target
        self.list_domain = domains


class WPUser(db.Model):
    __tablename__ = 'tb_wpuser'

    id = db.Column(db.Integer, primary_key = True)
    id_target = db.Column(db.Integer, db.ForeignKey('tb_target.id'))
    list_username = db.Column(JSON)

    def __init__(self, target, usernames = []):
        self.target = target
        self.list_username = usernames


class DNSLookup(db.Model):
    __tablename__ = 'tb_dnslookup'

    id = db.Column(db.Integer, primary_key = True)
    id_target = db.Column(db.Integer, db.ForeignKey('tb_target.id'))
    has_scanned = db.Column(db.Boolean, default = False)
    dnslookup_result = db.Column(db.Text)

    def __init__(self, target, has_scanned = False, result = None):
        self.target = target
        self.has_scanned = has_scanned
        self.dnslookup_result = result


class Whois(db.Model):
    __tablename__ = 'tb_whois'

    id = db.Column(db.Integer, primary_key = True)
    id_target = db.Column(db.Integer, db.ForeignKey('tb_target.id'))
    has_scanned = db.Column(db.Boolean, default = False)
    whois_result = db.Column(db.Text)

    def __init__(self, target, has_scanned = False, result = None):
        self.target = target
        self.has_scanned = has_scanned
        self.whois_result = result


class FoundLink(db.Model):
    __tablename__ = 'tb_link'

    id = db.Column(db.Integer, primary_key = True)
    id_target = db.Column(db.Integer, db.ForeignKey('tb_target.id'))
    found_link = db.Column(JSON)

    def __init__(self, target, found_link = None):
        self.target = target
        self.found_link = found_link
