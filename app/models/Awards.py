# coding=utf-8
import traceback
from flask import current_app
from . import db, Contest, Resource


awards_teacher = db.Table('awards_teacher',
    db.Column('awards', db.String(128), db.ForeignKey('awards.awards_id', ondelete="CASCADE")),
    db.Column('teacher', db.Integer, db.ForeignKey('teacher.id', ondelete="CASCADE"))
)

awards_student = db.Table('awards_student',
    db.Column('awards', db.String(128), db.ForeignKey('awards.awards_id', ondelete="CASCADE")),
    db.Column('student', db.String(64), db.ForeignKey('student.stu_no', ondelete="CASCADE"))
)

AwardsLevel = [
    u'省级一等奖',
    u'省级二等奖',
    u'省级三等奖',
    u'国家级一等奖',
    u'国家级二等奖',
    u'国家级三等奖',
]

AwardsType = [
    u'个人',
    u'团体'
]

AwardsProcess = [
    u'已录入',
    u'学院审批通过',
    u'教务处审批通过'
]

AwardsResult = [
    u'一档',
    u'二档',
    u'三档',
    u'四档'
]

class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    awards_id = db.Column(db.String(128), nullable=False,
                          unique=True, index=True)
    honor = db.Column(db.Unicode(128))
    level = db.Column(db.Unicode(128))
    title = db.Column(db.Unicode(512))
    type = db.Column(db.Unicode(32))
    process = db.Column(db.Unicode(64), default=AwardsProcess[0])
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
        db.session.delete(self)
        db.session.commit()


def generate_next_awards_id(contest):
    ''' generate next awards id for the new awards '''
    last_awards = contest.awards.order_by(Awards.awards_id.desc())\
        .with_lockmode('update').first()
    contest_id = contest.contest_id
    if last_awards == None:
        return '%s%s' % (contest_id, '001')
    else:
        last_awards_id = int(last_awards.awards_id[8:])
        new_id = str(last_awards_id + 1)
        return '%s%s' % (contest_id, new_id.rjust(3, '0'))


def get_by_id(id):
    return Awards.query.filter(Awards.id == id).first()


def get_list_by_contest_id(cid):
    return Awards.query.filter(Awards.contest_id == cid).all()


def get_count(contest_id = -1, level = -1):
    query = Awards.query
    if contest_id != -1:
        query = query.filter(Awards.contest_id == contest_id)
    if level != -1:
        query = query.filter(Awards.process == AwardsProcess[level - 2])
    return query.count()


def get_list_pageable(page, per_page, contest_id = -1, level = -1):
    query = Awards.query
    if contest_id != -1:
        query = query.filter(Awards.contest_id == contest_id)
    if level != -1:
        query = query.filter(Awards.process == AwardsProcess[level - 2])
    return query.order_by(Awards.awards_id)\
        .paginate(page, per_page, error_out=False)


def create_awards(awards_form, contest, files):
    try:
        awards = Awards()
        awards.awards_id = generate_next_awards_id(contest)
        awards.level = awards_form.level.data
        if awards_form.honor.data == '':
            awards.honor = awards_form.level.data
        awards.title = awards_form.title.data
        awards.type = awards_form.type.data
        awards.contest = contest
        awards.teachers = awards_form.get_teacher_list()
        awards.students = awards_form.get_student_list()
        awards.save()
        current_app.logger.info(u'录入奖项 %s 成功', awards.awards_id)
        for name, file in files.items(multi=True):
            Resource.save_res(file, awards)
        current_app.logger.info(u'上传奖项附件成功')
        return 'OK'
    except Exception:
        current_app.logger.error(u'录入奖项 %r 失败', awards_form)
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'


def update_awards(awards, awards_form, files):
    try:
        awards.level = awards_form.level.data
        if awards_form.honor.data == '':
            awards.honor = awards_form.level.data
        awards.title = awards_form.title.data
        awards.type = awards_form.type.data
        awards.teachers = awards_form.get_teacher_list()
        awards.students = awards_form.get_student_list()
        awards.save()
        current_app.logger.info(u'更新奖项 %s 成功', awards.awards_id)
        for name, file in files.items(multi=True):
            Resource.save_res(file, awards)
        current_app.logger.info(u'上传奖项附件成功')
        return 'OK'
    except Exception:
        current_app.logger.error(u'更新奖项 %r 失败', awards_form)
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'


def delete_awards(awards):
    try:
        awards.remove()
        current_app.logger.info(u'删除奖项成功')
        return 'OK'
    except Exception:
        current_app.logger.error(u'删除奖项失败')
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'


def pass_awards(awards, opt, result):
    try:
        if opt == 1:
            awards.process = AwardsProcess[opt]
            awards.save()
            current_app.logger.info(u'审核奖项成功')
            return 'OK'
        elif opt == 2:
            if not (0 <= result < 4):
                return u'非法操作'
            awards.process = AwardsProcess[opt]
            awards.result = AwardsResult[result]
            awards.save()
            current_app.logger.info(u'审核奖项成功')
            return 'OK'
        else:
            return u'非法操作'
    except Exception:
        current_app.logger.error(u'审核奖项错误')
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'