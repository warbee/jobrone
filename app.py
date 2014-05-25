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
	first_search = request.args.get('first_search')
	
	data = indeed.getTree(first_search)
	results = indeed.getResults(data)

	global skill
	skill = models.Skills


	skill(user_id=0, skill=first_search, created=None)
	
	return render_template('joblist.html', first_search=first_search,
										   results=results,
										   skill_check=skill.id)

if __name__ == '__main__':
    app.run()