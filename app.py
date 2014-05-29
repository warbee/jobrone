from flask import Flask, url_for, render_template, flash, request, session
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

@app.route('/wizard', methods=['POST'])
def getStarted():
	#email = request.args.get('email')
	#first_search = request.args.get('first_search')
	email = request.form['email']
	first_search = request.form['first_search']
	screen = request.form['screen']

	if int(screen) == 1:
		global jobs
		jobs = 0		

		data = indeed.getTree(first_search, jobs)
		results = indeed.getResults(data)

		global skill
		global user

		user = models.User
		skill = models.Skills
		db = models.db

		global visitor
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

	elif int(screen) == 2 and jobs < 10:

		first_selection = request.form['first_selection']
		if first_selection == 'None':
			jobs += 5
			data = indeed.getTree(first_search, jobs)
			results = indeed.getResults(data)

			return render_template('joblist.html', first_search=first_search,
												   results=results,
												   email=email,
												   skill_check=0,
												   visitor_id=visitor.id,
												   screen=screen)
		else:
			second_search = request.form['second_skill']
			#this should probably checked via js...
			if second_search == first_search:
				return 'cannot be the same skill'
			else:
				jobs = 0
				screen += 1
				
				data = indeed.getTree(second_search, jobs)
				results = indeed.getResults(data)

				db = models.db
				try:
					second_skill = skill(user_id=visitor.id, skill=second_search, skill_num=2, created=None)
					db.session.add(second_skill)
					db.session.commit()
				except Exception as e:
					db.session.rollback()
					second_skill = db.update(user).where(and_(user.id==visitor.id, skill.skill_num==2)).values(skill=second_search)
					db.session.commit()

				return render_template('joblist.html', first_search=first_search,
													   second_search=second_search,
													   results=results,
													   email=email,
													   skill_check=0,
													   visitor_id=visitor.id,
													   screen=screen)

	elif jobs > 10:
		return 'Why didn\'t you like those jobs?'

	else:
		return 'screen value: ' + str(screen)

if __name__ == '__main__':
    app.run()