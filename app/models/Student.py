from flask import current_app
from . import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stu_no = db.Column(db.String(32), nullable=False, unique=True)
    name = db.Column(db.Unicode(128))
    department = db.Column(db.Unicode(128))
    major = db.Column(db.Unicode(128))
    grade = db.Column(db.String(32))

    def __repr__(self):
        return '<Student %s %s>' % (self.stu_no, self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def get_by_id(id):
    return Student.query.filter(Student.id == id).first()


def get_all():
    return Student.query.all()
