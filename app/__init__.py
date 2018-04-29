# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://contact_app_admin:bk9106@localhost/contact_app_db'
app.secret_key = 'sshh'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "you must be logged-in to access this api"
ma = Marshmallow(app)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')

from flask_migrate import Migrate
migrate = Migrate(app, db)

from app import models

