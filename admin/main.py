from src.web import create_app
from src.models.database import reset_db
from src.models.seeds import run as run_seeds

app = create_app()

if __name__ == '__main__':
    with app.app_context():
       reset_db()
       run_seeds()

    app.run(debug=True)