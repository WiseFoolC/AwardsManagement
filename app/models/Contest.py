# coding=utf-8
from flask import current_app
from . import db, ContestSeries
from datetime import date

ContestLevel = {
    'nation' : u'国家级',
    'province' : u'省级'
}


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.String(128), unique=True, nullable=False)
    name_cn = db.Column(db.Unicode(512))
    name_en = db.Column(db.String(512))
    level = db.Column(db.Unicode())
    organizer = db.Column(db.Unicode(512))
    co_organizer = db.Column(db.Unicode(512))
    year = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    place = db.Column(db.Unicode(1024))


    series_name = db.Column(db.Unicode(256),
                            db.ForeignKey('contest_series.name', ondelete="CASCADE"),
                            nullable=False)
    series = db.relationship('ContestSeries',
                             backref=db.backref('contests',
                                                cascade="all, delete-orphan",
                                                passive_deletes=True,
                                                lazy='dynamic'))

    def __repr__(self):
        return '<Contest %s %s>' % (self.contest_id, self.name_cn)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


def generate_next_contest_id(year):
    ''' generate next contest id for the new contest's year '''
    last_contest = Contest.query.filter(Contest.year == year)\
        .order_by(Contest.contest_id.desc())\
        .with_lockmode('update').first()
    if last_contest == None:
        return 'W%d%s' % (year, '001')
    else:
        last_contest_id = int(last_contest.contest_id[6:])
        new_id = str(last_contest_id + 1)
        return 'W%d%s' % (year, new_id.rjust(3, '0'))


def get_by_id(id):
    return Contest.query.filter(Contest.id == id).first()


def get_count():
    return Contest.query.count()


def get_list_pageable(page, per_page):
    return Contest.query.order_by(Contest.id)\
        .paginate(page, per_page, error_out=False)


def create_contest(contest_form):
    try:
        contest = Contest()
        contest.contest_id = generate_next_contest_id(contest_form.year.data)
        contest.name_cn = contest_form.name_cn.data
        contest.name_en = contest_form.name_en.data
        contest.level = contest_form.level.data
        contest.organizer = contest_form.organizer.data
        contest.co_organizer = contest_form.co_organizer.data
        contest.year = contest_form.year.data
        contest.start_date = contest_form.date_range.data[0]
        contest.end_date = contest_form.date_range.data[1]
        contest.place = contest_form.place.data
        contest.series = ContestSeries.get_by_id(contest_form.series_id.data)
        contest.save()
        current_app.logger.info(u'录入竞赛 %s 成功', contest.name_cn)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'录入竞赛 %s 失败', contest_form.name_cn.data)
        current_app.logger.error(e)
        return 'FAIL'


def update_contest(contest, contest_form):
    try:
        contest.name_cn = contest_form.name_cn.data
        contest.name_en = contest_form.name_en.data
        contest.level = contest_form.level.data
        contest.organizer = contest_form.organizer.data
        contest.co_organizer = contest_form.co_organizer.data
        contest.year = contest_form.year.data
        contest.start_date = contest_form.date_range.data[0]
        contest.end_date = contest_form.date_range.data[1]
        contest.place = contest_form.place.data
        contest.series = ContestSeries.get_by_id(contest_form.series_id.data)
        contest.save()
        current_app.logger.info(u'更新竞赛 %s 成功', contest.name_cn)
        return 'OK'
    except Exception, e:
        current_app.logger.error(u'更新竞赛 %s 失败', contest_form.name_cn.data)
        current_app.logger.error(e)
        return 'FAIL'

