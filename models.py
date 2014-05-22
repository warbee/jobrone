from app import db
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<id %r>' % self.id

