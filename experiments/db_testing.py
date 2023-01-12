import os.path
import sqlite3

from flask import Flask
from flask_security import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, insert, update, delete, select
from sqlalchemy.testing import db
import base64

db = SQLAlchemy()


class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    # photo is going to contain an image file
    photo = db.Column(db.LargeBinary)
    emotion = db.Column(db.String(150))
    emoji = db.Column(db.LargeBinary)
    Supervisior = db.Column(db.String(150))
    admin = db.Column(db.String(150))
    evaluation = db.Column(db.String(150))


DBNAME = 'Test.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DBNAME}'
db.init_app(app)

if os.path.exists(os.path.join(os.path.curdir, DBNAME)):
    # create the db
    with app.app_context():
        db.create_all()
        print('Created Database!')

# Create a connection to the database


# try to add an element to the database

@app.route('/')
def home():
    image = open('/Users/miche/PycharmProjects/AusCare_IoT/images/how-to-be-happy.jpg', 'rb')
    emoji = open('/Users/miche/PycharmProjects/AusCare_IoT/website/static/emojis/happy.png', 'rb')
    stm = insert(Patient).values(name='Micheal', photo=base64.b64encode(image.read()), emotion='happy',
                                 emoji=base64.b64encode(emoji.read()), Supervisior='Micheal', admin='Micheal',
                                 evaluation='good')
    db.session.execute(stm)
    db.session.commit()
    image.close()
    emoji.close()
    return 'HELLO'


# read the database

with app.app_context():
    photo = db.session.query(Patient.photo).filter(Patient.name == 'Micheal').first()
    file = open('/Users/miche/PycharmProjects/AusCare_IoT/images/test.jpg', 'wb')
    file.write(base64.b64decode(photo[0]))
    file.close()
app.run(debug=True, port=5000)
