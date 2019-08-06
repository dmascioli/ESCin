from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

DEBUG = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'





