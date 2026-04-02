from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint
from src.web.handlers.auth import check
from src.models.reseñas.reseña_services import (
    obtener_reseñas, 
    obtener_reseña_por_id, 
    aprobar_reseña, 
    rechazar_reseña,
    eliminar_reseña,
    obtener_estadisticas_reseñas
)
from flask import session

reseñas_bp = Blueprint("reseñas", __name__, url_prefix="/resenas")


@reseñas_bp.route("/")
@check("review_index")
def index():
    """Listar todas las reseñas para moderación"""
    
    # Obtener parámetros de paginación y filtros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    estado = request.args.get('estado', '', type=str)
    calificacion = request.args.get('calificacion', '', type=str)
    sitio = request.args.get('sitio', '', type=str)
    usuario = request.args.get('usuario', '', type=str)
    fecha_desde = request.args.get('fecha_desde', '', type=str)
    fecha_hasta = request.args.get('fecha_hasta', '', type=str)
    orden_campo = request.args.get('orden_campo', 'fecha', type=str)
    orden_direccion = request.args.get('orden_direccion', 'desc', type=str)
    
    # Preparar filtros
    filters = {}
    if estado:
        filters['estado'] = estado
    if calificacion:
        filters['calificacion'] = calificacion
    if sitio:
        filters['sitio'] = sitio
    if usuario:
        filters['usuario'] = usuario
    if fecha_desde:
        filters['fecha_desde'] = fecha_desde
    if fecha_hasta:
        filters['fecha_hasta'] = fecha_hasta
    if orden_campo:
        filters['orden_campo'] = orden_campo
    if orden_direccion:
        filters['orden_direccion'] = orden_direccion
    
    # Obtener reseñas con filtros
    reseñas_data = obtener_reseñas(
        page=page,
        per_page=per_page,
        filters=filters if filters else None
    )
    
    # Obtener estadísticas
    estadisticas = obtener_estadisticas_reseñas()
    
    return render_template(
        "reseñas/index.html",
        reseñas_data=reseñas_data,
        estadisticas=estadisticas,
        filtros={
            'estado': estado,
            'calificacion': calificacion,
            'sitio': sitio,
            'usuario': usuario,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'orden_campo': orden_campo,
            'orden_direccion': orden_direccion
        }
    )


@reseñas_bp.route("/<int:resena_id>")
@check("review_index")
def detalle(resena_id):
    """Ver detalle de una reseña específica"""
    
    reseña = obtener_reseña_por_id(resena_id)
    if not reseña:
        flash("Reseña no encontrada", "error")
        return redirect(url_for('reseñas.index'))
    
    return render_template("reseñas/detalle.html", reseña=reseña)


@reseñas_bp.route("/<int:resena_id>/aprobar", methods=['POST'])
@check("review_moderate")
def aprobar(resena_id):
    """Aprobar una reseña"""
    
    from src.web.handlers.auth import get_current_user
    current_user = get_current_user()
    if not current_user:
        flash("Error de sesión", "error")
        return redirect(url_for('auth.login'))
    
    success, message = aprobar_reseña(resena_id, current_user.id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('reseñas.detalle', resena_id=resena_id))


@reseñas_bp.route("/<int:resena_id>/rechazar", methods=['POST'])
@check("review_moderate")
def rechazar(resena_id):
    """Rechazar una reseña con motivo"""
    
    from src.web.handlers.auth import get_current_user
    current_user = get_current_user()
    if not current_user:
        flash("Error de sesión", "error")
        return redirect(url_for('auth.login'))
    
    motivo_rechazo = request.form.get('motivo_rechazo', '').strip()
    if not motivo_rechazo:
        flash("Debe proporcionar un motivo para el rechazo", "error")
        return redirect(url_for('reseñas.detalle', resena_id=resena_id))
    
    success, message = rechazar_reseña(resena_id, current_user.id, motivo_rechazo)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('reseñas.detalle', resena_id=resena_id))


@reseñas_bp.route("/estadisticas")
@check("review_index")
def estadisticas():
    """API endpoint para obtener estadísticas de reseñas"""
    
    stats = obtener_estadisticas_reseñas()
    return jsonify(stats)


@reseñas_bp.route("/json")
@check("review_index")
def json_list():
    """API endpoint para obtener reseñas en formato JSON"""
    
    # Obtener parámetros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    reseñas_data = obtener_reseñas(page=page, per_page=per_page)
    
    # Convertir a formato JSON
    reseñas_json = []
    for reseña in reseñas_data['reseñas']:
        reseña_data = {
            'id': reseña.id,
            'titulo': reseña.titulo,
            'calificacion': reseña.calificacion,
            'estado': reseña.estado.value,
            'fecha_creacion': reseña.fecha_creacion.isoformat(),
            'sitio': {
                'id': reseña.sitio.id,
                'nombre': reseña.sitio.nombre,
                'ciudad': reseña.sitio.ciudad
            },
            'usuario': {
                'nombre': reseña.nombre_usuario,
                'email': reseña.email_usuario
            },
            'dias_desde_creacion': reseña.dias_desde_creacion
        }
        reseñas_json.append(reseña_data)
    
    return jsonify({
        'reseñas': reseñas_json,
        'pagination': {
            'page': reseñas_data['page'],
            'pages': reseñas_data['total_pages'],
            'per_page': reseñas_data['per_page'],
            'total': reseñas_data['total'],
            'has_prev': reseñas_data['has_prev'],
            'has_next': reseñas_data['has_next']
        }
    })


@reseñas_bp.route("/<int:resena_id>/eliminar", methods=['POST'])
@check("review_moderate")
def eliminar(resena_id):
    """Eliminar una reseña con confirmación"""
    
    confirmacion = request.form.get('confirmacion')
    if confirmacion != 'ELIMINAR':
        flash("Debe escribir 'ELIMINAR' para confirmar la eliminación", "error")
        return redirect(url_for('reseñas.detalle', resena_id=resena_id))
    
    success, message = eliminar_reseña(resena_id)
    
    if success:
        flash(message, "success")
        return redirect(url_for('reseñas.index'))
    else:
        flash(message, "error")
        return redirect(url_for('reseñas.detalle', resena_id=resena_id))
