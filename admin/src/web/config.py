import os
from dotenv import load_dotenv

# --- DEBUG PRINTS ---
print("--- GEMINI CLI DEBUG PRINTS ---")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')}")
print(f"GOOGLE_CLIENT_SECRET: {os.getenv('GOOGLE_CLIENT_SECRET')}")
print("--- END GEMINI CLI DEBUG PRINTS ---")


from os import environ
from datetime import timedelta


load_dotenv()

# --- DEBUG PRINTS ---
print("--- Loading Environment Variables ---")
print(f"DB_URL: {os.environ.get('DB_URL')}")
print(f"GOOGLE_CLIENT_ID: {os.environ.get('GOOGLE_CLIENT_ID')}")
print(
    f"GOOGLE_CLIENT_SECRET: {'*' * 10 if os.environ.get('GOOGLE_CLIENT_SECRET') else None}"
)  # Avoid printing secrets
print("------------------------------------")


class Config:
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
        "pool_size": 10,
        "pool_pre_ping": True,
        "pool_recycle": 60,
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):

    MINIO_ENDPOINT = environ.get("MINIO_ENDPOINT", "127.0.0.1:9000")
    MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME", "grupo44")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY", "minioadmin")
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
    FRONTEND_BASE_URL = "http://localhost:5173"


class ProductionConfig(Config):

    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    DEBUG = False

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")

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
