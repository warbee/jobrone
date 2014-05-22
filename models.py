from app import db
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, email, created):
        self.email = email
        self.created = created

    def __repr__(self):
        return '<id %r>' % self.id


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    first_job = db.Column(db.String(1000))
    second_job = db.Column(db.String(1000))
    third_job = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, user_id, first_job, second_job, third_job, created):
        self.user_id = user_id
        self.first_job = first_job
        self.second_job = second_job
        self.third_job = third_job
        self.created = created

    def __repr__(self):
        return '<id %r>' % self.id