import os
from dotenv import load_dotenv
from os import environ
from datetime import timedelta

load_dotenv()


class Config:
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    CORS_ORIGINS = ["*"]
    SECRET_KEY = environ.get("SECRET_KEY", "c413c4db1b08e3ef4e296c8d9643d378")
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_pre_ping": True,
        "pool_recycle": 60,
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    MINIO_ENDPOINT = environ.get("MINIO_ENDPOINT", "127.0.0.1:9000")
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME", "grupo44")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "hajqpfzuadiMb4aIqDPz")
    MINIO_SECRET_KEY = environ.get(
        "MINIO_SECRET_KEY", "YoTbnJTYnaVXovWm93GJpYLj9LsPs3tMluHzJe57"
    )
    MINIO_SECURE = False
    MINIO_SERVER = "127.0.0.1:9000"
    DEBUG = True
    BD_USER = environ.get("DB_USER", "postgres")
    BD_PASSWORD = environ.get("DB_PASSWORD", "admin")
    BD_HOST = environ.get("DB_HOST", "localhost")
    BD_PORT = environ.get("DB_PORT", "5432")
    BD_NAME = environ.get("DB_NAME", "grupo44")
    BD_SCHEME = environ.get("DB_SCHEME", "postgresql")
    SQLALCHEMY_ENGINES = {
        "default": environ.get("DATABASE_URL")
        or f"{BD_SCHEME}://{BD_USER}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}?client_encoding=utf8"
    }
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "cambiar-en-produccion")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_DOMAIN = None
    JWT_COOKIE_HTTPONLY = True
    FRONTEND_BASE_URL = "http://localhost:5173"
    SESSION_COOKIE_DOMAIN = None


class ProductionConfig(Config):
    BD_USER = environ.get("DB_USER")
    BD_PASSWORD = environ.get("DB_PASSWORD")
    BD_HOST = environ.get("DB_HOST")
    BD_PORT = environ.get("DB_PORT")
    BD_NAME = environ.get("DB_NAME")
    BD_SCHEME = environ.get("DB_SCHEME")
    MINIO_ENDPOINT = environ.get(
        "MINIO_ENDPOINT", "minio.proyecto2025.linti.unlp.edu.ar"
    )
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME", "grupo44")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "hajqpfzuadiMb4aIqDPz")
    MINIO_SECRET_KEY = environ.get(
        "MINIO_SECRET_KEY", "YoTbnJTYnaVXovWm93GJpYLj9LsPs3tMluHzJe57"
    )
    MINIO_SECURE = True
    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_DOMAIN = ".grupo44.proyecto2025.linti.unlp.edu.ar"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    JWT_COOKIE_DOMAIN = ".grupo44.proyecto2025.linti.unlp.edu.ar"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    FRONTEND_BASE_URL = environ.get(
        "FRONTEND_BASE_URL", "https://grupo44.proyecto2025.linti.unlp.edu.ar"
    )
    CORS_ORIGINS = ["https://grupo44.proyecto2025.linti.unlp.edu.ar"]


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
