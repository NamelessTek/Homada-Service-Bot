from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask
from homada.config import Config
from flask_cors import CORS
from twilio.rest import Client
from flask_admin.contrib.sqla import ModelView
from flask_session import Session


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
mail = Mail()


@login_manager.user_loader
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config.from_object(Config)
    Session(app)
    CORS(app)

    #CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.app_context().push()

    from homada.ubicacion.routes import location
    from homada.twilio.routes import twilio
    from homada.clientes.routes import cliente
    from homada.reservaciones.routes import reservacion
    from homada.admin.routes import admin_homada

    app.config.from_object(Config)
    app.register_blueprint(location)
    app.register_blueprint(twilio)
    app.register_blueprint(cliente)
    app.register_blueprint(reservacion)
    app.register_blueprint(admin_homada)

    return app
