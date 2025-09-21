from os import environ


class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    BD_USER="postgres"
    BD_PASSWORD="admin"
    BD_HOST="localhost"
    BD_PORT="5432"
    BD_NAME="grupo44"
    BD_SCHEME="postgresql+psycopg2"
    SQLALCHEMY_ENGINE = {"default": f"{BD_SCHEME}://{BD_USER}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}"}

    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_ENGINE={"default": environ.get("DATABASE_URL")}
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}