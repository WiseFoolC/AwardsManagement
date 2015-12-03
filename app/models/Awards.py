# coding=utf-8
from . import db


awards_teacher = db.Table('awards_teacher',
    db.Column('awards_id', db.Integer, db.ForeignKey('awards.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'))
)

awards_student = db.Table('awards_student',
    db.Column('awards_id', db.Integer, db.ForeignKey('awards.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)

AwardsLevel = {
    '1' : u'一等奖',
    '2' : u'二等奖',
    '3' : u'三等奖'
}

AwardsType = {
    'personal' : u'个人',
    'group' : u'团体'
}

AwardsProcess = [
    u'学院审批',
    u'教务处审批',
    u'正式定档'
]

AwardsResult = {
    '1' : u'一档',
    '2' : u'二档',
    '3' : u'三档',
    '4' : u'四档'
}

class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    awards_id = db.Column(db.String(128), nullable=False, unique=True)
    level = db.Column(db.Unicode(128))
    title = db.Column(db.Unicode(512))
    type = db.Column(db.Unicode(32))
    process = db.Column(db.Unicode(64))
    result = db.Column(db.Unicode(64))

    contest_id = db.Column(db.String(128),
                           db.ForeignKey('contest.contest_id', ondelete='CASCADE'),
                           nullable=False)
    contest = db.relationship('Contest',
                             backref=db.backref('awards',
                                                cascade="all, delete-orphan",
                                                passive_deletes=True,
                                                lazy='dynamic'))

    teachers = db.relationship('Teacher',
                               secondary=awards_teacher,
                               backref=db.backref('awards', lazy='dynamic'))

    students = db.relationship('Student',
                               secondary=awards_student,
                               backref=db.backref('awards', lazy='dynamic'))

