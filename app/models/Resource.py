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
                             backref=db.backref('resource',
                                                cascade="all, delete-orphan",
                                                passive_deletes=True,
                                                lazy='dynamic'))