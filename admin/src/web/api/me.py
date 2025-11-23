from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.favoritos import favorito_listar
from src.models.auth import user_show_id
from src.web.schemas.user import UserReadSchema
from src.web.schemas.favorito import FavoritoReadSchema
from src.web.schemas.reseña import ReseñaReadSchema
from src.models.reseñas.reseña_services import obtener_reseñas_por_usuario
from src.web.config import ProductionConfig

bp = Blueprint("me_api", __name__)


@bp.get("/")
@jwt_required()
def get_current_user():
    """Obtener información del usuario actual desde el JWT."""
    try:
        user_id = get_jwt_identity()

        user = user_show_id(user_id)

        if not user:
            return jsonify(error="user_not_found"), 404

        user_data = UserReadSchema().dump(user)
        return jsonify(user_data), 200
    except Exception as e:
        return (
            jsonify(
                error="internal_error",
                message=f"Error al obtener información del usuario: {str(e)}",
            ),
            500,
        )


@bp.get("/favoritos")
@jwt_required()
def list_favorites():
    """Lista los sitios favoritos del usuario autenticado con paginación."""
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    order = request.args.get("order", "latest", type=str)

    if user_show_id(user_id) is None:
        return jsonify(error="usuario no encontrado"), 401

    list_favoritos = favorito_listar(user_id, page=page, per_page=per_page, order=order)

    schema = FavoritoReadSchema(many=True)
    list_favoritos["favoritos"] = schema.dump(list_favoritos["favoritos"])

    return jsonify(list_favoritos), 200


@bp.get("/reviews")
@jwt_required()
def get_my_reviews():
    """Obtener todas las reseñas del usuario autenticado."""
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 25, type=int)
    order = request.args.get("order", "latest", type=str)
    user = user_show_id(user_id)
    if user is None:
        return jsonify(error="usuario no encontrado"), 401
    reviews = obtener_reseñas_por_usuario(
        user.email, page=page, per_page=per_page, order=order
    )

    schema = ReseñaReadSchema(many=True)
    reviews["reseñas"] = schema.dump(reviews["reseñas"])

    return jsonify(reviews), 200
