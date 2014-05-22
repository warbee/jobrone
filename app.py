from flask import Flask, url_for, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
import os
import models

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()