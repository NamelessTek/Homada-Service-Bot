import os


class Config:
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
    TWILIO_ACCOUNT_SID = os.environ.get(
        "TWILIO_ACCOUNT_SID", 'ACd88e27bf758736e26c0ca47b9b949885')
    TWILIO_AUTH_TOKEN = os.environ.get(
        "TWILIO_AUTH_TOKEN", '674fe0bc1d80710bfcf19a3f8dc429cd')
    TWILIO_PHONE_NUMBER = os.environ.get(
        "TWILIO_PHONE_NUMBER", 'whatsapp:+14155238886')
    TWILIO_STUDIO_FLOW_SID = os.environ.get(
        "TWILIO_STUDIO_FLOW_SID", "FW032961632181dcbe427bd3a93961d6c2")

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        raise Exception(
            "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER must be set")
