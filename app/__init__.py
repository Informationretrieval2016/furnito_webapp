from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from app import views, models
