from . import db


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128))
    department = db.Column(db.Unicode(128))

    def __repr__(self):
        return '<Teacher %s>' % self.name