from os import environ
from datetime import timedelta



class Config(object):
    CORS_ORIGINS = ["*"]
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
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "cambiar-en-produccion")
    JWT_EXPIRATION= 3600 
class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_SECURE = False
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
    CORS_ORIGINS = ["https://grupo44.proyecto2025.linti.unlp.edu.ar/"]
    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    DEBUG = False
    
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}