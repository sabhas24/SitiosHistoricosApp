from flask import Flask, render_template
from src.web.config import config as app_config
from src.models import database


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    # Cargar configuración antes de init DB
    app.config.from_object(app_config[env])

    # Inicializar DB
    database.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")

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
