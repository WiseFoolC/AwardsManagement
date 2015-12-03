# coding=utf-8
from . import db
from datetime import date

ContestLevel = {
    'nation' : u'国家',
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


