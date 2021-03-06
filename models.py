from app import db
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, email, created):
        self.email = email
        self.created = created

    def __repr__(self):
        return '<id %r>' % self.id


class Skills(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    skill = db.Column(db.String(1000))
    skill_num = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, user_id, skill, skill_num, created):
        self.user_id = user_id
        self.skill = skill
        self.skill_num = skill_num
        self.created = created

    def __repr__(self):
        return '<id %r>' % self.id


class Chosen(db.Model):
    __tablename__ = 'chosen_jobs'

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


class Ignored(db.Model):
    __tablename__ = 'ignored_jobs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    job = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, user_id, job, created):
        self.user_id = user_id
        self.job = job
        self.created = created

    def __repr__(self):
        return '<id %r>' % self.id


class Pages(db.Model):
    __tablename__ = 'paging'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    screen = db.Column(db.Integer)
    page = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __init__(self, user_id, screen, page, created, modified):
        self.user_id = user_id
        self.screen = screen
        self.page = page
        self.created = created
        self.modified = modified

    def __repr__(self):
        return '<id %r>' % self.id