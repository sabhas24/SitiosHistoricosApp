from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.favoritos import favorito_listar
from src.models.auth import user_show_id
from src.web.schemas.user import UserReadSchema

bp = Blueprint('me_api', __name__, url_prefix='/api/me')

@bp.get('/')
@jwt_required()
def get_current_user():
    """Obtener información del usuario actual desde el JWT."""
    user_id = get_jwt_identity()
    
    user = user_show_id(user_id)
    
    if not user:
        return jsonify(error="user_not_found"), 404
    
    user_data = UserReadSchema().dump(user)
    return jsonify(user_data), 200

@bp.get('/favoritos')
@jwt_required()
def list_favorites():
    """Lista los sitios favoritos del usuario autenticado con paginación."""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    if user_show_id(user_id) is None:
        return jsonify(error="usuario no encontrado"), 401
    
    list_favoritos = favorito_listar(user_id)

    return jsonify(list_favoritos), 200