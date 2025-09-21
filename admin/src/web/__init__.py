from flask import Flask
from flask import render_template
from src.web.handlers import error
from flask import abort
from src.web.config import config

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/error401')
    def prueba_401():
        abort(401)  

    @app.route('/error500')
    def prueba_500():
        return 1 / 0 
    
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(500, error.internal_error)

    return app
