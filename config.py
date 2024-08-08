import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'daseg'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'mynindu'
    MYSQL_CURSORCLASS = 'DictCursor'
    SESSION_TYPE = 'filesystem'
