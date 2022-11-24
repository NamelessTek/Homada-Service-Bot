import os


class Config:
    # SQL Credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    MYSQL_HOST = os.environ.get("MYSQL_HOST", 'db')
    MYSQL_USER = os.environ.get("MYSQL_USER", 'generic_operator')
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", 'homada')
    MYSQL_DB = os.environ.get("MYSQL_DB", 'Homada_DB')
    MYSQL_PORT = os.environ.get("MYSQL_PORT", '3306')
    SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + \
        MYSQL_PASSWORD+"@"+MYSQL_HOST+"/"+MYSQL_DB+"?charset=utf8mb4"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Twilio Token and SID
    TWILIO_ACCOUNT_SID = os.environ.get(
        "TWILIO_ACCOUNT_SID", 'ACd88e27bf758736e26c0ca47b9b949885')
    TWILIO_AUTH_TOKEN = os.environ.get(
        "TWILIO_AUTH_TOKEN", '674fe0bc1d80710bfcf19a3f8dc429cd')
    TWILIO_PHONE_NUMBER = os.environ.get(
        "TWILIO_PHONE_NUMBER", 'whatsapp:+14155238886')

    # URL for uploading pdfs
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", 'App/homada/static/uploads')
    # check if the folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER", 'smtp.@gmail.com')
    MAIL_PORT = os.environ.get("MAIL_PORT", '465')
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", 'True')
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", 'True')
    MAIL_EMAIL = os.environ.get(
        "MAIL_EMAIL", 'namelessnoreply25@gmail.com')
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", 'dpivkcsjblqscusq')

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        raise Exception(
            "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER must be set")
