import os
from src.web import create_app
from src.web.config import config


app = create_app()

if __name__ == "__main__":
    app.run()
