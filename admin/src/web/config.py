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

    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 5,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    
    MINIO_ENDPOINT = environ.get("MINIO_ENDPOINT", "minio.proyecto2025.linti.unlp.edu.ar")
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME", "grupo44")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "kKhBPfUYJHfyvaCdnNZT")
    MINIO_SECRET_KEY = environ.get(
        "MINIO_SECRET_KEY", "Tke5F7UZEP59mwkysJGRaWJYuCfLVlOypARR7fjx"
    )
    MINIO_SECURE = "minio.proyecto2025" in environ.get(
        "MINIO_ENDPOINT", "minio.proyecto2025.linti.unlp.edu.ar"
    )
    MINIO_SERVER = environ.get("MINIO_ENDPOINT", "minio.proyecto2025.linti.unlp.edu.ar")
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
    # Evitar SameSite=None sin secure durante el desarrollo en HTTP local
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_DOMAIN = None
    JWT_COOKIE_HTTPONLY = True
    FRONTEND_BASE_URL = "http://localhost:5173"
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False
    TESTING = False

    # Database Configuration
    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    BD_USER = environ.get("DATABASE_USERNAME")
    BD_PASSWORD = environ.get("DATABASE_PASSWORD")
    BD_HOST = environ.get("DATABASE_HOST")
    BD_PORT = environ.get("DATABASE_PORT")
    BD_NAME = environ.get("DATABASE_NAME")
    BD_URL = environ.get("DATABASE_URL")
    BD_SCHEME = environ.get("DATABASE_SCHEME")

    # MinIO Configuration
    MINIO_ENDPOINT = environ.get("MINIO_ENDPOINT")
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = True
    # Evitar SameSite=None sin secure durante el desarrollo en HTTP local
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_DOMAIN = ".proyecto2025.linti.unlp.edu.ar"
    JWT_COOKIE_HTTPONLY = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_CSRF_PROTECT = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_DOMAIN = ".proyecto2025.linti.unlp.edu.ar"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    FRONTEND_BASE_URL = environ.get("FRONTEND_BASE_URL")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
