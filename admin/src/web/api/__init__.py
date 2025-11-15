from flask import Blueprint
from src.web.api.user import bp as user_bp
from src.web.api.sitios import bp as sitios_bp
from src.web.api.me import bp as me_bp
from src.web.api.reseñas import bp_reviews


api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(user_bp, url_prefix='/user')
api_bp.register_blueprint(sitios_bp, url_prefix='/sitios')
api_bp.register_blueprint(me_bp, url_prefix='/me')
api_bp.register_blueprint(bp_reviews)
