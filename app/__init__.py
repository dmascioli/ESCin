from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(Config)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)





