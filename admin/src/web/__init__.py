from flask import Flask, render_template
from src.web.config import config as app_config
from src.models import database
from flask_session import Session
from flask_cors import CORS
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.sitios import (
    bp as sitios_bp,
)  # re-exported in controllers/sitios/__init__.py
from src.web.controllers.tagsfolder.tags import bp as tags_bp
from src.web.controllers.admin.users import bp as admin_users_bp
from src.web.controllers.admin.feature_flags import feature_flags_bp
from src.web.controllers.historial import (
    historial_bp,
)  # re-exported in controllers/historial/__init__.py
from src.web.controllers.perfil.profile import bp as profile_bp
from src.web.controllers.propuestas import propuestas_bp
from src.web.controllers.reseñas import reseñas_bp
from src.web.handlers.auth import (
    is_authenticated,
    get_current_user,
    check_permission,
    check,
    get_session_info,
)
from src.web.api import api_bp
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from os import environ
from flask_jwt_extended import JWTManager


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(app_config[env])

    # Configurar CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:*",
                    "http://127.0.0.1:*",
                    "https://grupo44.proyecto2025.linti.unlp.edu.ar"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            }
        },
    )

    # Inicializar DB
    database.init_app(app)

    # Cargar variables de entorno
    load_dotenv()

    # Inicializar OAuth
    CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
    oauth = OAuth(app)
    oauth.register(
        name="google",
        client_id=environ.get("GOOGLE_CLIENT_ID"),
        client_secret=environ.get("GOOGLE_CLIENT_SECRET"),
        server_metadata_url=CONF_URL,
        client_kwargs={
            "scope": "openid email profile",
        },
    )
    # Inicializar JWT
    jwt = JWTManager(app)

    # Inicializar sesión
    Session(app)

    # Middleware para verificar modo de mantenimiento
    @app.before_request
    def before_request():
        from src.web.handlers.maintenance import check_maintenance_mode

        maintenance_response = check_maintenance_mode()
        if maintenance_response:
            return maintenance_response

    @app.route("/")
    def home():
        return render_template("home.html")

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(sitios_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(feature_flags_bp)
    app.register_blueprint(historial_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(propuestas_bp)
    app.register_blueprint(reseñas_bp)

    # Registrar blueprint de la API REST
    app.register_blueprint(api_bp, url_prefix="/api")

    app.jinja_env.globals["is_authenticated"] = is_authenticated
    app.jinja_env.globals["get_current_user"] = get_current_user
    app.jinja_env.globals["check_permission"] = check_permission
    app.jinja_env.globals["check"] = check
    app.jinja_env.globals["get_session_info"] = get_session_info

    @app.template_filter("nl2br")
    def nl2br_filter(text):
        if not text:
            return text
        return text.replace("\n", "<br>\n")

    @app.cli.command("reset-db")
    def reset_db_command():
        database.reset_db()
        print("✅ Database reset completed.")

    @app.cli.command("seed-db")
    def seed_db_command():
        from src.models.seeds import run

        run()
        print("✅ Seeding completed.")

    return app
