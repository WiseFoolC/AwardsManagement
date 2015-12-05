# coding=utf-8
from flask import current_app
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from app import login_manager


class Permission:
    NORMAL = u'录入信息'
    COLLEGE = u'学院审批'
    DEAN = u'教务处审批'

PermissionList = [u'录入信息', u'学院审批', u'教务处审批']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(128), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(512))
    department = db.Column(db.Unicode(128))
    permission = db.Column(db.Unicode(32), default=Permission.NORMAL)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %s>' % (self.username)

    @property
    def password(self):
        raise AttributeError(u'密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_by_id(id):
    return User.query.filter(User.id == id).first()


def get_by_username(username):
    return User.query.filter(User.username == username).first()


def get_list_with_page(page, per_page):
    pagination = User.query.order_by(User.id).paginate(page, per_page, False)
    return pagination


def get_count():
    return User.query.count()


def create_user(user_form):
    try:
        has_user = get_by_username(user_form.username.data)
        if has_user:
            current_app.logger.error(u'用户 %s 已存在' % has_user.username)
            return u"该用户名已经存在"
        user = User(user_form.username.data)
        user.password = user_form.password.data
        user.department = user_form.department.data
        user.permission = user_form.permission.data
        user.save()
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'添加用户 %s 失败' % user_form.username.data)
        return 'FAIL'


def update_user(user, user_form):
    try:
        user.username = user_form.username.data
        user.department = user_form.department.data
        user.permission = user_form.permission.data
        user.save()
        return 'OK'
    except Exception, e:
        return 'FAIL'


def delete_by_id(id):
    try:
        user = get_by_id(id)
        user.remove()
        return 'OK'
    except Exception, e:
        return 'FAIL'
