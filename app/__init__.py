from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate
#from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)


#toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'







