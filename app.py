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

	#update this to write to the paging metadata table
	paging = request.args.get('paging')
	if not paging:
		paging = 0

	data = indeed.getTree(first_search, paging*5)
	results = indeed.getResults(data)

	user = models.User
	skill = models.Skills
	db = models.db
	page = models.Pages

	#next try to add the visitor to get an email
	visitor = user.query.filter_by(email=email).first()
	if visitor is None:
		try:
			visitor = user(email=email, created=None)
			db.session.add(visitor)
			db.session.commit()
		except Exception as e:
			db.session.rollback()

	first_page = page.query.filter(page.user_id==visitor.id).filter(page.screen==1).first()
	try:
		first_page = page(user_id=visitor.id, screen=screen, page=1, created=None, modified=None)
		db.session.add(first_page)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
	
	#finally, add the skill
	first_skill = skill.query.filter(skill.user_id==visitor.id).filter(skill.skill_num==1).first()
	if first_skill is None:
		try:
			first_skill = skill(user_id=visitor.id, skill=first_search, skill_num=1, created=None)
			db.session.add(first_skill)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
	else:
		first_skill.skill = first_search
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

	user = models.User
	skill = models.Skills
	db = models.db
	page = models.Pages

	#update this to read/update the paging table, and pass the new number
	if first_selection == 'None':

		visitor = user.query.filter_by(email=email).first()
		first_page = page.query.filter(page.user_id==visitor.id).filter(page.screen==1).first()

		if first_page.page <= 2:
			first_page.page = int(first_page.page) + 1
			db.session.commit()

			return redirect(url_for('getStarted', email=email,
												  first_search=first_search,
												  paging=first_page.page))
		else:
			first_page.page = int(first_page.page) + 1
			db.session.commit()

			return redirect(url_for('explain'))
	else:
		return 'second_screen'


@app.route('/explain')
def explain():
	return 'Explain why screen'

if __name__ == '__main__':
    app.run()