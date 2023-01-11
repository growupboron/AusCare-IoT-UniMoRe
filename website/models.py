from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))


class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    # photo is going to contain an image file
    photo = db.Column(db.LargeBinary)
    emotion = db.Column(db.String(150))
    emoji = db.Column(db.LargeBinary)
    supervisior = db.Column(db.String(150))
    admin = db.Column(db.String(150))
    evaluation = db.Column(db.String(150))
    face_id = db.Column(db.String(150))
