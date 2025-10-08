from flask import Flask, render_template
from src.web.config import config as app_config
from src.models import database
from flask_session import Session 
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.sitios import bp as sitios_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.admin.users import bp as admin_users_bp
from src.web.controllers.admin.feature_flags import feature_flags_bp
from src.web.controllers.historial import historial_bp
from src.web.controllers.profile import bp as profile_bp
from src.web.controllers.propuestas import propuestas_bp
from src.web.controllers.reseñas import reseñas_bp
from src.web.handlers.auth import is_authenticated, get_current_user, check_permission,check

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    
    app.config.from_object(app_config[env])

    # Inicializar DB
    database.init_app(app)

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

    app.jinja_env.globals['is_authenticated'] = is_authenticated
    app.jinja_env.globals['get_current_user'] = get_current_user
    app.jinja_env.globals['check_permission'] = check_permission
    app.jinja_env.globals['check'] = check
   
    # Filtros personalizados para Jinja2
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convierte saltos de línea en <br> tags"""
        if not text:
            return text
        return text.replace('\n', '<br>\n')

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
