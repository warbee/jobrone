from flask import Flask, url_for, render_template, flash, request, session, redirect, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import os
import indeed

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

import models

@app.route('/')
def index():
	return render_template('index.html') 

@app.route('/one', methods=['GET'])
def getStarted():
	email = request.args.get('email')
	first_search = request.args.get('first_search')
	screen = 1

	try:
		joblist = request.args.get('joblist')
		g.jobs = joblist
	except:
		g.jobs = 0	

	data = indeed.getTree(first_search, g.jobs)
	results = indeed.getResults(data)

	user = models.User
	skill = models.Skills
	db = models.db

	try:
		visitor = user(email=email, created=None)
		db.session.add(visitor)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		visitor = user.query.filter_by(email=email).first()

	try:
		first_skill = skill(user_id=visitor.id, skill=first_search, skill_num=1, created=None)
		db.session.add(first_skill)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		first_skill = db.update(user).where(and_(user.id==visitor.id, skill.skill_num==1)).values(skill=first_search)
		db.session.commit()


	return render_template('joblist.html', first_search=first_search,
										   results=results,
										   email=email,
										   skill_check=0,
										   visitor_id=visitor.id,
										   screen=screen)


@app.route('/two', methods=['GET'])
def secondScreen():
	email = request.args.get('email')
	first_search = request.args.get('first_search')
	first_selection = request.args.get('first_selection')

	if first_selection == 'None':
		jobs = 5
		return redirect(url_for('getStarted', email=email,
											  first_search=first_search,
											  joblist=jobs))
	else:
		return 'second_screen'


if __name__ == '__main__':
    app.run()