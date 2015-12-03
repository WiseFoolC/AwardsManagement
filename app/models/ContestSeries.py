from . import db


class ContestSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), unique=True, nullable=False)

    def __repr__(self):
        return '<ContestSeries %s>' % self.name