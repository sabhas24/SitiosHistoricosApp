from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.utils.jwt_utils import jwt_required
from src.models.auth import user_show_id
from src.models.reseñas.reseña_services import (
    obtener_reseña_por_id,
    eliminar_reseña,
    obtener_reseñas_por_sitio,
    create_reseña,
)
from src.models.sitios.sitios import get_sitio_by_id
from src.models.favoritos import favorito_agregar, favorito_eliminar
from src.web.schemas.reseña import ReseñaCreateSchema, ReseñaReadSchema

bp_reviews = Blueprint("reviews_api", __name__)


@bp_reviews.get("/sites/<int:site_id>/reviews/public")
def list_public_site_reviews(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        errors = {}
        if page < 1:
            errors["page"] = ["Must be at least 1"]
        if per_page < 1 or per_page > 100:
            errors["per_page"] = ["Must be between 1 and 100"]

        if errors:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": errors,
                        }
                    }
                ),
                400,
            )

        resultado = obtener_reseñas_por_sitio(
            sitio_id=site_id, page=page, per_page=per_page
        )

        reseñas_data = []
        for reseña in resultado["reseñas"]:
            reseña_dict = {
                "id": reseña.id,
                "site_id": reseña.sitio_id,
                "rating": reseña.calificacion,
                "comment": reseña.comentario,
                "author_name": reseña.nombre_usuario,
                "inserted_at": reseña.fecha_creacion.isoformat() + "Z",
                "updated_at": reseña.fecha_creacion.isoformat() + "Z",
            }
            reseñas_data.append(reseña_dict)

        return (
            jsonify(
                {
                    "data": reseñas_data,
                    "meta": {
                        "page": resultado["page"],
                        "per_page": resultado["per_page"],
                        "total": resultado["total"],
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.get("/sites/<int:site_id>/reviews")
@jwt_required
def list_site_reviews(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        errors = {}
        if page < 1:
            errors["page"] = ["Must be at least 1"]
        if per_page < 1 or per_page > 100:
            errors["per_page"] = ["Must be between 1 and 100"]

        if errors:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": errors,
                        }
                    }
                ),
                400,
            )

        resultado = obtener_reseñas_por_sitio(
            sitio_id=site_id, page=page, per_page=per_page
        )

        reseñas_data = []
        for reseña in resultado["reseñas"]:
            reseña_dict = {
                "id": reseña.id,
                "site_id": reseña.sitio_id,
                "rating": reseña.calificacion,
                "comment": reseña.comentario,
                "inserted_at": reseña.fecha_creacion.isoformat() + "Z",
                "updated_at": reseña.fecha_creacion.isoformat() + "Z",
            }
            reseñas_data.append(reseña_dict)

        return (
            jsonify(
                {
                    "data": reseñas_data,
                    "meta": {
                        "page": resultado["page"],
                        "per_page": resultado["per_page"],
                        "total": resultado["total"],
                    },
                }
            ),
            200,
        )

        return (
            jsonify(
                {
                    "data": reseñas_data,
                    "meta": {
                        "page": resultado["page"],
                        "per_page": resultado["per_page"],
                        "total": resultado["total"],
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.get("/sites/<int:site_id>/reviews/me")
@jwt_required
def get_my_site_review(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Authentication required",
                        }
                    }
                ),
                401,
            )

       
        from src.models.reseñas.reseña_services import obtener_reseñas_por_usuario
        
        #
        from src.models.reseñas.reseña_services import obtener_reseñas
        
        filters = {
            'sitio': str(site_id), 
            'usuario': usuario.email 
        }
     
        
        from src.models.reseñas.reseña import Reseñ
        from src.models.database import db
        
        reseña = db.session.query(Reseña).filter(
            Reseña.sitio_id == site_id,
            Reseña.email_usuario == usuario.email
        ).first()
        
        if not reseña:
             return (
                jsonify({"error": {"code": "not_found", "message": "Review not found"}}),
                404,
            )
            
        return (
            jsonify(
                {
                    "id": reseña.id,
                    "site_id": reseña.sitio_id,
                    "rating": reseña.calificacion,
                    "comment": reseña.comentario,
                    "status": reseña.estado.value, # Importante para el frontend
                    "inserted_at": reseña.fecha_creacion.isoformat() + "Z",
                    "updated_at": reseña.fecha_creacion.isoformat() + "Z",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                        "details": str(e)
                    }
                }
            ),
            500,
        )


from src.models.feature_flag.feature_flag_services import are_reviews_enabled

@bp_reviews.post("/sites/<int:site_id>/reviews")
@jwt_required
def create_site_review(site_id):
    try:
       
        if not are_reviews_enabled():
            return (
                jsonify(
                    {
                        "error": {
                            "code": "service_unavailable",
                            "message": "Reviews are currently disabled",
                        }
                    }
                ),
                503,
            )

        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        json_data = request.get_json(force=True)
        if not json_data:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": {"body": ["Request body is required"]},
                        }
                    }
                ),
                400,
            )

        errors = {}

        if "rating" not in json_data:
            errors["rating"] = ["This field is required"]
        elif not isinstance(json_data.get("rating"), (int, float)) or not (
            1 <= json_data.get("rating") <= 5
        ):
            errors["rating"] = ["Must be between 1 and 5"]

        if "site_id" not in json_data:
            errors["site_id"] = ["This field is required"]
        elif json_data.get("site_id") != site_id:
            errors["site_id"] = ["Must match the site_id in the URL"]

        if errors:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": errors,
                        }
                    }
                ),
                400,
            )

        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Authentication required",
                        }
                    }
                ),
                401,
            )

        reseña = create_reseña(
            comentario=json_data.get("comment", ""),
            calificacion=json_data["rating"],
            sitio_id=site_id,
            email_usuario=usuario.email,
            nombre_usuario=f"{usuario.name} {usuario.last_name}",
        )

        return (
            jsonify(
                {
                    "id": reseña.id,
                    "site_id": reseña.sitio_id,
                    "rating": reseña.calificacion,
                    "comment": reseña.comentario,
                    "inserted_at": reseña.fecha_creacion.isoformat() + "Z",
                    "updated_at": reseña.fecha_creacion.isoformat() + "Z",
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.get("/sites/<int:site_id>/reviews/<int:review_id>")
@jwt_required
def get_site_review(site_id, review_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        if review_id <= 0:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": {"review_id": ["Must be a positive integer"]},
                        }
                    }
                ),
                400,
            )

        reseña = obtener_reseña_por_id(review_id)
        if not reseña:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        if reseña.sitio_id != site_id:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        from src.models.reseñas.reseña import EstadoReseña

        if reseña.estado != EstadoReseña.APROBADA:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        return (
            jsonify(
                {
                    "id": reseña.id,
                    "site_id": reseña.sitio_id,
                    "rating": reseña.calificacion,
                    "comment": reseña.comentario,
                    "inserted_at": reseña.fecha_creacion.isoformat() + "Z",
                    "updated_at": reseña.fecha_creacion.isoformat() + "Z",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.delete("/sites/<int:site_id>/reviews/<int:review_id>")
@jwt_required
def delete_site_review(site_id, review_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        reseña = obtener_reseña_por_id(review_id)
        if not reseña:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        if reseña.sitio_id != site_id:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Authentication required",
                        }
                    }
                ),
                401,
            )

        if reseña.email_usuario != usuario.email:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "forbidden",
                            "message": "You do not have permission to delete this review",
                        }
                    }
                ),
                403,
            )

        if not eliminar_reseña(review_id):
            return (
                jsonify(
                    {
                        "error": {
                            "code": "server_error",
                            "message": "An unexpected error occurred",
                        }
                    }
                ),
                500,
            )

        return "", 204

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.put("/sites/<int:site_id>/favorite")
@jwt_required
def mark_site_as_favorite(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Authentication required",
                        }
                    }
                ),
                401,
            )

        try:
            favorito_agregar(usuario.id, site_id)
        except ValueError:
            pass

        return "", 204

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp_reviews.delete("/sites/<int:site_id>/favorite")
@jwt_required
def unmark_site_as_favorite(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Authentication required",
                        }
                    }
                ),
                401,
            )

        favorito_eliminar(usuario.id, site_id)

        return "", 204

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )
