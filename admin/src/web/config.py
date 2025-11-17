from os import environ
from datetime import timedelta


class Config(object):
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    CORS_ORIGINS = ["*"]

    SECRET_KEY = "c413c4db1b08e3ef4e296c8d9643d378"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None

    SQLALCHEMY_ENGINE_OPTIONS = {
        "poll_size": 10,
        "pool_pre_ping": True,
        "pool_recycle": 60,
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    # Configuración MinIO
    MINIO_ENDPOINT = environ.get("MINIO_ENDPOINT", "192.168.100.219:9000")
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME", "grupo44")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE = False

    # Legacy config
    MINIO_SERVER = "localhost:9000"

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

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "cambiar-en-produccion")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_DOMAIN = None

    FRONTEND_BASE_URL = "http://localhost:5173"


class ProductionConfig(Config):
    CORS_ORIGINS = ["https://grupo44.proyecto2025.linti.unlp.edu.ar/"]

    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    DEBUG = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    FRONTEND_BASE_URL = "https://grupo44.proyecto2025.linti.unlp.edu.ar"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
