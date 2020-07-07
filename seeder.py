from app.model import *
from app import app, sql as db

def default_user(urole, rname, uname, passw):
    with app.app_context():
        role = Role.query.get(urole)
        user = User(role, rname, uname)
        user.secure_password(passw)
        db.session.add(user)
        db.session.commit()


def default_role(rname):
    with app.app_context():
        role = Role(rname)
        db.session.add(role)
        db.session.commit()

roles = ['administrator', 'user']
users = {
    1 : ['aku sayang kamu', 'sayang', 'sayang123'], # administrator
    2 : ['muhammad hekmen', 'hekmen', 'hekmen123'] # ordinary user
}

for role in roles:
    default_role(role)

for user_role in users.keys():
    default_user(user_role, users[user_role][0], users[user_role][1], users[user_role][2])

print('done.')
