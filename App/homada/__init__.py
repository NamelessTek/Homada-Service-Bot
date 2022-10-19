from http import client
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask
from homada.config import Config
from flask_cors import CORS
from twilio.rest import Client

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    #CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.app_context().push()

    from homada.ubicacion.routes import location
    from homada.twilio.routes import twilio
    from homada.clientes.routes import client

    app.config.from_object(Config)
    app.register_blueprint(location)
    app.register_blueprint(twilio)
    app.register_blueprint(client)

    return app
