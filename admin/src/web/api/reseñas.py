from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.utils.jwt_utils import jwt_required
from src.models.auth import user_show_id
from src.models.reseñas.reseña_services import (
    obtener_reseña_por_id,
    eliminar_reseña,
    obtener_reseñas_por_sitio,
    create_reseña,
    obtener_reseña_por_usuario_y_sitio,
    actualizar_reseña
)
from src.models.sitios.sitios import get_sitio_by_id
from src.models.favoritos import favorito_agregar, favorito_eliminar
from src.web.schemas.reseña import ReseñaCreateSchema, ReseñaReadSchema

bp_reviews = Blueprint('reviews_api', __name__)


@bp_reviews.get('/sites/<int:site_id>/reviews/public')
def list_site_reviews_public(site_id):
    """Endpoint público para listar reseñas aprobadas de un sitio (sin autenticación)"""
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        errors = {}
        if page < 1:
            errors['page'] = ['Must be at least 1']
        if per_page < 1 or per_page > 100:
            errors['per_page'] = ['Must be between 1 and 100']
        
        if errors:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": errors
                }
            }), 400
        
        resultado = obtener_reseñas_por_sitio(sitio_id=site_id, page=page, per_page=per_page)
        
        reseñas_data = []
        for reseña in resultado['reseñas']:
            reseña_dict = {
                "id": reseña.id,
                "site_id": reseña.sitio_id,
                "rating": reseña.calificacion,
                "comment": reseña.comentario,
                "inserted_at": reseña.fecha_creacion.isoformat() + 'Z',
                "updated_at": reseña.fecha_creacion.isoformat() + 'Z',
                "author_name": reseña.nombre_usuario
            }
            reseñas_data.append(reseña_dict)
        
        return jsonify({
            "data": reseñas_data,
            "meta": {
                "page": resultado['page'],
                "per_page": resultado['per_page'],
                "total": resultado['total']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.get('/sites/<int:site_id>/reviews')
@jwt_required
def list_site_reviews(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        errors = {}
        if page < 1:
            errors['page'] = ['Must be at least 1']
        if per_page < 1 or per_page > 100:
            errors['per_page'] = ['Must be between 1 and 100']
        
        if errors:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": errors
                }
            }), 400
        
        resultado = obtener_reseñas_por_sitio(sitio_id=site_id, page=page, per_page=per_page)
        
        # Obtener información del usuario autenticado si está disponible
        usuario = user_show_id(request.current_user_id) if request.current_user_id else None
        user_review = None
        if usuario:
            user_review = obtener_reseña_por_usuario_y_sitio(usuario.email, site_id)
        
        reseñas_data = []
        for reseña in resultado['reseñas']:
            reseña_dict = {
                "id": reseña.id,
                "site_id": reseña.sitio_id,
                "rating": reseña.calificacion,
                "comment": reseña.comentario,
                "inserted_at": reseña.fecha_creacion.isoformat() + 'Z',
                "updated_at": reseña.fecha_creacion.isoformat() + 'Z',
                "author_name": reseña.nombre_usuario
            }
            reseñas_data.append(reseña_dict)
        
        response_data = {
            "data": reseñas_data,
            "meta": {
                "page": resultado['page'],
                "per_page": resultado['per_page'],
                "total": resultado['total']
            }
        }
        
        # Incluir información sobre la reseña del usuario si está autenticado
        if usuario:
            if user_review:
                from src.models.reseñas.reseña import EstadoReseña
                response_data["user_review"] = {
                    "id": user_review.id,
                    "rating": user_review.calificacion,
                    "comment": user_review.comentario,
                    "status": user_review.estado.value.lower(),
                    "can_edit": user_review.estado in [EstadoReseña.PENDIENTE, EstadoReseña.APROBADA],
                    "rejection_reason": user_review.motivo_rechazo if user_review.estado == EstadoReseña.RECHAZADA else None
                }
            else:
                response_data["user_review"] = None
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.post('/sites/<int:site_id>/reviews')
@jwt_required
def create_site_review(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        json_data = request.get_json(force=True)
        if not json_data:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": {"body": ["Request body is required"]}
                }
            }), 400
        
        errors = {}
        
        # Validar rating
        if 'rating' not in json_data:
            errors['rating'] = ['This field is required']
        elif not isinstance(json_data.get('rating'), (int, float)) or not (1 <= json_data.get('rating') <= 5):
            errors['rating'] = ['Must be between 1 and 5']
        
        # Validar site_id
        if 'site_id' not in json_data:
            errors['site_id'] = ['This field is required']
        elif json_data.get('site_id') != site_id:
            errors['site_id'] = ['Must match the site_id in the URL']
        
        # Validar comment (20-1000 caracteres)
        comment = json_data.get('comment', '').strip()
        if not comment:
            errors['comment'] = ['This field is required']
        elif len(comment) < 20:
            errors['comment'] = ['Must be at least 20 characters long']
        elif len(comment) > 1000:
            errors['comment'] = ['Must be at most 1000 characters long']
        
        if errors:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": errors
                }
            }), 400
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        # Verificar si ya existe una reseña del usuario para este sitio
        reseña_existente = obtener_reseña_por_usuario_y_sitio(usuario.email, site_id)
        if reseña_existente:
            return jsonify({
                "error": {
                    "code": "conflict",
                    "message": "You already have a review for this site",
                    "details": {
                        "existing_review_id": reseña_existente.id,
                        "suggestion": "Use PUT to update your existing review"
                    }
                }
            }), 409
        
        reseña = create_reseña(
            comentario=comment,
            calificacion=json_data['rating'],
            sitio_id=site_id,
            email_usuario=usuario.email,
            nombre_usuario=f"{usuario.name} {usuario.last_name}"
        )
        
        return jsonify({
            "id": reseña.id,
            "site_id": reseña.sitio_id,
            "rating": reseña.calificacion,
            "comment": reseña.comentario,
            "inserted_at": reseña.fecha_creacion.isoformat() + 'Z',
            "updated_at": reseña.fecha_creacion.isoformat() + 'Z',
            "status": "pending_moderation",
            "message": "Review created successfully and is pending moderation"
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.get('/sites/<int:site_id>/reviews/me')
@jwt_required
def get_my_review_for_site(site_id):
    """Obtiene la reseña del usuario autenticado para un sitio específico"""
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        reseña = obtener_reseña_por_usuario_y_sitio(usuario.email, site_id)
        if not reseña:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "You haven't reviewed this site yet"
                }
            }), 404
        
        from src.models.reseñas.reseña import EstadoReseña
        
        # Información adicional sobre el estado
        status_info = {
            "status": reseña.estado.value.lower(),
            "can_edit": reseña.estado in [EstadoReseña.PENDIENTE, EstadoReseña.APROBADA],
            "can_delete": True
        }
        
        if reseña.estado == EstadoReseña.RECHAZADA and reseña.motivo_rechazo:
            status_info["rejection_reason"] = reseña.motivo_rechazo
        
        return jsonify({
            "id": reseña.id,
            "site_id": reseña.sitio_id,
            "rating": reseña.calificacion,
            "comment": reseña.comentario,
            "inserted_at": reseña.fecha_creacion.isoformat() + 'Z',
            "updated_at": reseña.fecha_creacion.isoformat() + 'Z',
            **status_info
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.get('/sites/<int:site_id>/reviews/<int:review_id>')
@jwt_required
def get_site_review(site_id, review_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        if review_id <= 0:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": {
                        "review_id": ["Must be a positive integer"]
                    }
                }
            }), 400
        
        reseña = obtener_reseña_por_id(review_id)
        if not reseña:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        if reseña.sitio_id != site_id:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        from src.models.reseñas.reseña import EstadoReseña
        if reseña.estado != EstadoReseña.APROBADA:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        return jsonify({
            "id": reseña.id,
            "site_id": reseña.sitio_id,
            "rating": reseña.calificacion,
            "comment": reseña.comentario,
            "inserted_at": reseña.fecha_creacion.isoformat() + 'Z',
            "updated_at": reseña.fecha_creacion.isoformat() + 'Z'
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.put('/sites/<int:site_id>/reviews/<int:review_id>')
@jwt_required
def update_site_review(site_id, review_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        reseña = obtener_reseña_por_id(review_id)
        if not reseña:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        if reseña.sitio_id != site_id:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        if reseña.email_usuario != usuario.email:
            return jsonify({
                "error": {
                    "code": "forbidden",
                    "message": "You do not have permission to update this review"
                }
            }), 403
        
        json_data = request.get_json(force=True)
        if not json_data:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": {"body": ["Request body is required"]}
                }
            }), 400
        
        errors = {}
        
        # Validar rating si se proporciona
        if 'rating' in json_data:
            if not isinstance(json_data['rating'], (int, float)) or not (1 <= json_data['rating'] <= 5):
                errors['rating'] = ['Must be between 1 and 5']
        
        # Validar comment si se proporciona
        if 'comment' in json_data:
            comment = json_data['comment'].strip()
            if not comment:
                errors['comment'] = ['Comment cannot be empty']
            elif len(comment) < 20:
                errors['comment'] = ['Must be at least 20 characters long']
            elif len(comment) > 1000:
                errors['comment'] = ['Must be at most 1000 characters long']
        
        if errors:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": errors
                }
            }), 400
        
        # Actualizar reseña
        success, message = actualizar_reseña(
            review_id,
            usuario.email,
            comentario=json_data.get('comment'),
            calificacion=json_data.get('rating')
        )
        
        if not success:
            return jsonify({
                "error": {
                    "code": "server_error",
                    "message": message
                }
            }), 500
        
        # Obtener la reseña actualizada
        reseña_actualizada = obtener_reseña_por_id(review_id)
        
        return jsonify({
            "id": reseña_actualizada.id,
            "site_id": reseña_actualizada.sitio_id,
            "rating": reseña_actualizada.calificacion,
            "comment": reseña_actualizada.comentario,
            "inserted_at": reseña_actualizada.fecha_creacion.isoformat() + 'Z',
            "updated_at": reseña_actualizada.fecha_creacion.isoformat() + 'Z',
            "status": "pending_moderation",
            "message": message
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.delete('/sites/<int:site_id>/reviews/<int:review_id>')
@jwt_required
def delete_site_review(site_id, review_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        reseña = obtener_reseña_por_id(review_id)
        if not reseña:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        if reseña.sitio_id != site_id:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Review not found"
                }
            }), 404
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        if reseña.email_usuario != usuario.email:
            return jsonify({
                "error": {
                    "code": "forbidden",
                    "message": "You do not have permission to delete this review"
                }
            }), 403
        
        success, message = eliminar_reseña(review_id)
        if not success:
            return jsonify({
                "error": {
                    "code": "server_error",
                    "message": message
                }
            }), 500
        
        return jsonify({
            "message": "Review deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.put('/sites/<int:site_id>/favorite')
@jwt_required
def mark_site_as_favorite(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        try:
            favorito_agregar(usuario.id, site_id)
        except ValueError:
            pass
        
        return '', 204
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp_reviews.delete('/sites/<int:site_id>/favorite')
@jwt_required
def unmark_site_as_favorite(site_id):
    try:
        sitio = get_sitio_by_id(site_id)
        if not sitio:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        usuario = user_show_id(request.current_user_id)
        if not usuario:
            return jsonify({
                "error": {
                    "code": "unauthorized",
                    "message": "Authentication required"
                }
            }), 401
        
        favorito_eliminar(usuario.id, site_id)
        
        return '', 204
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500
