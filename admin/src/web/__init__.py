from flask import Flask, render_template
from src.web.config import config as app_config
from src.models import database
from flask_session import Session 
from src.web.controllers.auth import bp as auth_bp
from src.web.handlers.auth import is_authenticated

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    
    app.config.from_object(app_config[env])

    # Inicializar DB
    database.init_app(app)


    Session(app)

    @app.route("/")
    def home():
        return render_template("home.html")
    

    # Registrar blueprints
    app.register_blueprint(auth_bp)

    app.jinja_env.globals['is_authenticated'] = is_authenticated

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
