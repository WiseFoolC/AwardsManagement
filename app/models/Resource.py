from flask import current_app
from . import db

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Unicode(1024), nullable=False, unique=True)
    name = db.Column(db.Unicode(1024), unique=True, default=u'UNTITLED')
    upload_time = db.Column(db.DateTime)

    awards_id = db.Column(db.String(128),
                          db.ForeignKey('awards.awards_id', ondelete='CASCADE'),
                          nullable=False)

    awards = db.relationship('Awards',
                             backref=db.backref('resources',
                                                cascade="all, delete-orphan",
                                                passive_deletes=True,
                                                lazy='dynamic'))

    def __repr__(self):
        return '<Resource %s>' % self.filename

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()