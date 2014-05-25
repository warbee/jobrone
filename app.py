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
	return render_template('right-sidebar.html', first_search=first_search)

if __name__ == '__main__':
    app.run()