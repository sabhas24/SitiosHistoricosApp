from src.web import create_app
from src.models.database import reset_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        reset_db()
    app.run(debug=True)