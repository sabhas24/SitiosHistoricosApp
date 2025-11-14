from flask import Blueprint, request, jsonify
from src.models.favoritos import favorito_listar
from src.models.auth import user_show_id
from src.web.utils.jwt_utils import jwt_required

bp = Blueprint('me_api', __name__, url_prefix='/api/me')

@bp.get('/favoritos')
@jwt_required
def list_favorites():
    """Lista los sitios favoritos del usuario autenticado con paginación."""
    user_id = request.current_user_id
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    if user_show_id(user_id) is None:
        return jsonify(error="usuario no encontrado"), 401
    
    list_favoritos = favorito_listar(user_id)

    return jsonify(list_favoritos), 200