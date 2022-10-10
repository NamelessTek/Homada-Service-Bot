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
