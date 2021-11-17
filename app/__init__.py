from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
login_manager = LoginManager()
bootstap = Bootstrap()


def create_app(config_name):

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    db.init_app(app)
    bootstap.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "You must be logged in to access this page."

    

    #registering blueprints
    from .auth import auth as authentication_blueprint
    app.register_blueprint(authentication_blueprint)

    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)
    
    return app
