from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.favoritos import favorito_listar
from src.models.auth import user_show_id
from src.web.schemas.user import UserReadSchema
from src.web.schemas.favorito import FavoritoReadSchema
from src.models.reseñas.reseña_services import obtener_reseñas_por_usuario

bp = Blueprint("me_api", __name__, url_prefix="/api/me")


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
    
    # Serializar los favoritos usando el schema
    favorito_schema = FavoritoReadSchema(many=True)
    favoritos_serialized = favorito_schema.dump(list_favoritos["favoritos"])
    
    # Crear la respuesta con los favoritos serializados
    response_data = {
        **{k: v for k, v in list_favoritos.items() if k != 'favoritos'},
        'favoritos': favoritos_serialized
    }

    return jsonify(response_data), 200


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

    # Convert ORM Reseña objects to plain dicts for JSON serialization
    reseñas_data = []
    for r in reviews.get('reseñas', []):
        try:
            sitio_nombre = r.sitio.nombre if getattr(r, 'sitio', None) else None
        except Exception:
            sitio_nombre = None
        reseña_dict = {
            "id": r.id,
            "site_id": r.sitio_id,
            "sitio_nombre": sitio_nombre,
            "calificacion": r.calificacion,
            "resena": r.comentario,
            "comentario": r.comentario,
            "fecha": r.fecha_creacion.isoformat() + 'Z' if getattr(r, 'fecha_creacion', None) else None,
            "inserted_at": r.fecha_creacion.isoformat() + 'Z' if getattr(r, 'fecha_creacion', None) else None,
            "updated_at": (r.fecha_moderacion.isoformat() + 'Z') if getattr(r, 'fecha_moderacion', None) else (r.fecha_creacion.isoformat() + 'Z' if getattr(r, 'fecha_creacion', None) else None),
            "estado": r.estado.value.lower() if getattr(r, 'estado', None) else None
        }
        reseñas_data.append(reseña_dict)

    response_payload = {
        **{k: v for k, v in reviews.items() if k != 'reseñas'},
        'reseñas': reseñas_data
    }

    return jsonify(response_payload), 200
