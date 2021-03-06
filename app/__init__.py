from flask import Flask
from . import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
import os

photos = UploadSet('photos', IMAGES)
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

    # configure UploadSet
    configure_uploads(app, photos)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    # Initializing
    login_manager.init_app(app)
    db.init_app(app)
    bootstrap = Bootstrap(app)
    mail.init_app(app)

    return app
