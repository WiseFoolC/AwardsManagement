# coding=utf-8
from flask import Flask
from config import config
from app.models import db
from app.models import ContestSeries, Contest, Awards, \
    Student, Teacher, User, Resource

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(config['deploy'])
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User.User(u'admin')
        user.password = '123456'
        user.department = u'教务处'
        user.permission = User.Permission.DEAN
        user.save()
        '''
        for i in range(10):
            u = User.User(u'user' + unicode(i))
            u.password = '123456'
            u.save()
        '''