
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app_config
import os

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

def create_app(config_name):
    if(os.getenv('FLASK_CONFIG')=='production') :
        app = Flask(__name__)  # pragma: no cover 
        app.config.update(  # pragma: no cover 
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    migrate = Migrate(app, db)
    from app import models
    from .operations import operations as ops_blueprint
    app.register_blueprint(ops_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app