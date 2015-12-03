# coding=utf-8
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from app import login_manager


class Permisson:
    NORMAL = 0
    COLLEGE = 1
    DEAN = 2


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(512))
    department = db.Column(db.Unicode(128))
    permission = db.Column(db.Integer, default=Permisson.NORMAL)

    @property
    def password(self):
        raise AttributeError(u'密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % (self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_by_id(id):
    return User.query.filter(User.id == id).first()

def get_by_username(username):
    return User.query.filter(User.username == username).first()