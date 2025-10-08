from os import environ
from datetime import timedelta



class Config(object):
    SECRET_KEY = "c413c4db1b08e3ef4e296c8d9643d378"
    SESSION_TYPE="filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poll_size": 10,
        "pool_pre_ping": True,
        "pool_recycle": 60
    }
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    BD_USER = "postgres"
    BD_PASSWORD = "admin"
    BD_HOST = "localhost"
    BD_PORT = "5432"
    BD_NAME = "grupo44"
    BD_SCHEME = "postgresql"
    
    SQLALCHEMY_ENGINES = {
        "default": f"{BD_SCHEME}://{BD_USER}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}?client_encoding=utf8"
    }


class ProductionConfig(Config):
    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    DEBUG = False
    
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}