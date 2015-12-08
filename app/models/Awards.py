# coding=utf-8
from flask import current_app
from . import db, Contest


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
    u'待学院审批',
    u'待教务处审批',
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
                           db.ForeignKey('contest.contest_id', ondelete='CASCADE',
                                         onupdate='CASCADE'), nullable=False)
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

    def __repr__(self):
        return '<Awards %s>' % self.awards_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


def generate_next_awards_id(contest):
    ''' generate next awards id for the new awards '''
    last_awards = contest.awards.order_by(Awards.awards_id.desc())\
        .with_lockmode('update').first()
    contest_id = contest.contest_id
    if last_awards == None:
        return '%s%s' % (contest_id, '001')
    else:
        last_awards_id = int(last_awards.contest_id[8:])
        new_id = str(last_awards_id + 1)
        return '%s%s' % (contest_id, new_id.rjust(3, '0'))


def get_by_id(id):
    return Awards.query.filter(Awards.id == id).first()


def get_list_by_contest_id(cid):
    return Awards.query.filter(Awards.contest_id == cid).all()


def get_count():
    return Awards.query.count()


def get_list_pageable(page, per_page):
    return Awards.query.order_by(Awards.awards_id)\
        .paginate(page, per_page, error_out=False)


def create_awards(awards_form, contest_id):
    try:
        awards = Awards()
        contest = Contest.get_by_id(contest_id)
        awards.awards_id = generate_next_awards_id(contest)
        awards.level = awards_form.level.data
        awards.title = awards_form.title.data
        awards.type = awards_form.type.data
        awards.process = awards_form.process.data
        awards.contest = contest
        awards.save()
        current_app.logger.info(u'录入奖项 %s 成功', awards.awards_id)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'录入奖项 %s 失败', awards_form)
        current_app.logger.error(e)
        return 'FAIL'


def update_awards(awards, awards_form):
    try:
        awards.level = awards_form.level.data
        awards.title = awards_form.title.data
        awards.type = awards_form.type.data
        awards.process = awards_form.process.data
        awards.save()
        current_app.logger.info(u'更新奖项 %s 成功', awards.awards_id)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'更新奖项 %s 失败', awards_form)
        current_app.logger.error(e)
        return 'FAIL'
