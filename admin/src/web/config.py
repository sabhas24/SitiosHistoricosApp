from os import environ



class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = environ.get("SECRET_KEY", "c413c4db1b08e3ef4e296c8d9643d378")
    SESSION_TYPE="filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
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

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}