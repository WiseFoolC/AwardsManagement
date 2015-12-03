from flask import Flask
from config import config
from app.models import db
from app.models import ContestSeries, Contest, Awards, \
    Student, Teacher, User, Resource

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()