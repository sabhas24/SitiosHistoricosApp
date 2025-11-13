from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sitios import SitioCreateSchema, SitioReadSchema
from src.web.schemas.reseña import ReseñaCreateSchema, ReseñaReadSchema
from src.web.utils.jwt_utils import jwt_required
from src.web.handlers.auth import check_permission
from src.models.sitios.sitios import sitio_exists, sitio_new, get_sitio_by_id
from src.models.reseñas.reseña_services import create_reseña, obtener_reseña_por_id, eliminar_reseña, obtener_reseñas
from src.models.auth import user_show_id
from src.models.favoritos import favorito_agregar, favorito_eliminar


bp = Blueprint('sitios_api', __name__, url_prefix='/api/sitios')

@bp.post('/')
@jwt_required
def create_sitio():
    """Crear un nuevo sitio histórico."""
    try: 
        sitio_data = SitioCreateSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400
    
   
    if not check_permission('create_sitio'):
        return jsonify(error="forbidden", message="No tienes permiso para crear sitios"), 403
    
   
    if sitio_exists(sitio_data["nombre"], sitio_data["ciudad"]):
        return jsonify(error="Ya existe un sitio con ese nombre en esta ciudad"), 409
    

    sitio = sitio_new(**sitio_data)
    sitio_read = SitioReadSchema().dump(sitio)
    return jsonify(sitio_read), 201

@bp.get('/<int:id>')
def get_sitio(id):
    """Obtener un sitio histórico por ID."""
    sitio = get_sitio_by_id(id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    sitio_read = SitioReadSchema().dump(sitio)
    return jsonify(sitio_read), 200


@bp.post('/<int:sitio_id>/reseñas')
@jwt_required
def new_review(sitio_id):
    """Crear una nueva reseña para un sitio."""
   
    try:
        reseña_data = ReseñaCreateSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400

    
    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    
    user_id = request.current_user_id
    user = user_show_id(user_id)
    if not user:
        return jsonify(error="usuario no encontrado"), 401

    if reseña_data["calificacion"] < 1 or reseña_data["calificacion"] > 5:
        return jsonify(error="validacion", message="La calificación debe estar entre 1 y 5"), 400       
   
    reseña = create_reseña(
        comentario=reseña_data["comentario"],
        calificacion=reseña_data["calificacion"],
        sitio_id=sitio_id,
        email_usuario=user.email,      
        nombre_usuario=user.name        
    )
    
    return jsonify(ReseñaReadSchema().dump(reseña)), 201

@bp.get('/<int:sitio_id>/reseñas')
@jwt_required
def list_sitio_reviews(sitio_id):
    """Lista las reseñas de un sitio con paginación."""
    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    if not check_permission('review_index', request.current_user_id):
        return jsonify(error="forbidden", message="No tienes permiso para ver reseñas"), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
   reseñas_pagination = obtener_reseñas(sitio_id=sitio_id, page=page, per_page=per_page)
    
    return jsonify({
        'reseñas': reseñas,
        'total': reseñas_pagination.total,
        'page': reseñas_pagination.page,
        'per_page': reseñas_pagination.per_page,
        'pages': reseñas_pagination.pages
    }), 200
@bp.get('/<int:sitio_id>/reseñas/<int:reseña_id>')
@jwt_required
def get_sitio_review(sitio_id, reseña_id):
    """Obtiene una reseña específica de un sitio."""
   
    sitio = get_sitio_by_id(sitio_id)
    if not ceck_permission('review_index', request.current_user_id):
        return jsonify(error="forbidden", message="No tienes permiso para ver reseñas"), 403
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    
    reseña = obtener_reseña_por_id(reseña_id)
    if not reseña:
        return jsonify(error="not_found", message="Reseña no encontrada"), 404
    
   
    if reseña.sitio_id != sitio_id:
        return jsonify(error="not_found", message="Reseña no pertenece a este sitio"), 404
    
    return jsonify(ReseñaReadSchema().dump(reseña)), 200



@bp.delete('/<int:sitio_id>/reseñas/<int:reseña_id>')
@jwt_required
def delete_sitio_review(sitio_id, reseña_id):
    """Elimina una reseña específica de un sitio."""
    user_id = request.current_user_id
    if not check_permission('review_destroy', user_id):
        return jsonify(error="forbidden", message="No tienes permiso para eliminar reseñas"), 403
   
    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    
    reseña = obtener_reseña_por_id(reseña_id)
    if not reseña:
        return jsonify(error="not_found", message="Reseña no encontrada"), 404
    
   
    if reseña.sitio_id != sitio_id:
        return jsonify(error="not_found", message="Reseña no pertenece a este sitio"), 404

    if not eliminar_reseña(reseña_id):
        return jsonify(error="internal_error", message="Error al eliminar reseña"), 500
    
return jsonify(message="Reseña eliminada exitosamente"), 200


@bp.put('/<int:sitio_id>/favoritos')
@jwt_required
def add_favorite_sitio(sitio_id):
    """Agrega un sitio a los favoritos del usuario."""
    user_id = request.current_user_id

    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    user = user_show_id(user_id)
    if not user:
        return jsonify(error="usuario no encontrado"), 401
    
    favorito = favorito_agregar(user_id, sitio_id)
    return jsonify(message="Sitio agregado a favoritos exitosamente"), 200



@bp.delete('/<int:sitio_id>/favoritos')
@jwt_required
def remove_favorite_sitio(sitio_id):
    """Elimina un sitio de los favoritos del usuario."""
    user_id = request.current_user_id

    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify(error="not_found", message="Sitio no encontrado"), 404
    
    user = user_show_id(user_id)
    if not user:
        return jsonify(error="usuario no encontrado"), 401
    
    try:
        favoritos= favorito_eliminar(user_id, sitio_id)
        return jsonify(message="Sitio eliminado de favoritos exitosamente"), 200
    except Exception as e:
        return jsonify(error="internal_error", message=f"Error al eliminar sitio de favoritos: {str(e)}"), 500