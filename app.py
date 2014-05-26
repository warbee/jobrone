from flask import Flask, url_for, render_template, flash, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import indeed

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

import models

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/start', methods=['GET'])
def getStarted():
	email = request.args.get('email')
	first_search = request.args.get('first_search')
	
	data = indeed.getTree(first_search)
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
		visitor = user.query.filter_by(email=email).first()

	first_skill = skill(user_id=visitor.id, skill=first_search, created=None)
	db.session.add(first_skill)
	db.session.commit()
	
	return render_template('joblist.html', first_search=first_search,
										   results=results,
										   email=email,
										   skill_check=skill.id,
										   visitor_id=visitor.id)

if __name__ == '__main__':
    app.run()