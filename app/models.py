from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    qr_code = db.Column(db.String(140))
    checkins = db.relationship('Checkin', lazy=True)

    def __repr__(self):
        return '<Event {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(140))
    last = db.Column(db.String(140))
    pittid = db.Column(db.String(140))
    event = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<Checkin: {}>'.format(self.pittid)
