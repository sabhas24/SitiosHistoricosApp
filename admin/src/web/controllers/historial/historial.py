from flask import render_template, request, jsonify, Blueprint
from src.web.handlers.auth import check_permission
from src.models.historial.historial_services import obtener_historial_sitio
from src.models.sitios import get_sitio_by_id

historial_bp = Blueprint("historial", __name__, url_prefix="/historial")


@historial_bp.route("/sitio/<int:sitio_id>")
def historial_sitio(sitio_id):
    """Ver historial de un sitio histórico específico"""
    
    # Aplicar verificación de permisos
    if not check_permission("site_history"):
        from flask import abort
        abort(403)
    
    # Verificar que el sitio existe
    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return render_template("error.html", error="Sitio histórico no encontrado"), 404
    
    # Obtener parámetros de paginación y filtros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tipo_accion = request.args.get('tipo_accion', '', type=str)
    fecha_desde = request.args.get('fecha_desde', '', type=str)
    fecha_hasta = request.args.get('fecha_hasta', '', type=str)
    
    # Preparar filtros
    filters = {}
    if tipo_accion:
        filters['tipo_accion'] = tipo_accion
    if fecha_desde:
        filters['fecha_desde'] = fecha_desde
    if fecha_hasta:
        filters['fecha_hasta'] = fecha_hasta
    
    # Obtener historial con filtros
    historial_data = obtener_historial_sitio(
        sitio_id=sitio_id,
        page=page,
        per_page=per_page,
        filters=filters if filters else None
    )
    
    return render_template(
        "sitios/historial.html",
        sitio=sitio,
        historial_data=historial_data,
        filtros={
            'tipo_accion': tipo_accion,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta
        }
    )


@historial_bp.route("/sitio/<int:sitio_id>/json")
def historial_sitio_json(sitio_id):
    """API endpoint para obtener historial en formato JSON"""
    
    # Aplicar verificación de permisos
    if not check_permission("site_history"):
        from flask import abort
        abort(403)
    
    # Verificar que el sitio existe
    sitio = get_sitio_by_id(sitio_id)
    if not sitio:
        return jsonify({"error": "Sitio histórico no encontrado"}), 404
    
    # Obtener parámetros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tipo_accion = request.args.get('tipo_accion', '', type=str)
    fecha_desde = request.args.get('fecha_desde', '', type=str)
    fecha_hasta = request.args.get('fecha_hasta', '', type=str)
    
    # Preparar filtros
    filters = {}
    if tipo_accion:
        filters['tipo_accion'] = tipo_accion
    if fecha_desde:
        filters['fecha_desde'] = fecha_desde
    if fecha_hasta:
        filters['fecha_hasta'] = fecha_hasta
    
    # Obtener historial
    historial_data = obtener_historial_sitio(
        sitio_id=sitio_id,
        page=page,
        per_page=per_page,
        filters=filters if filters else None
    )
    
    # Convertir a formato JSON
    historial_data_json = []
    for evento in historial_data['eventos']:
        evento_data = {
            'id': evento.id,
            'tipo_accion': evento.tipo_accion,
            'fecha': evento.fecha_hora.isoformat(),
            'detalles': evento.detalles,
            'usuario': {
                'id': evento.usuario.id if evento.usuario else None,
                'username': evento.usuario.name if evento.usuario else 'Sistema',
                'email': evento.usuario.email if evento.usuario else None
            }
        }
        historial_data_json.append(evento_data)
    
    return jsonify({
        'historial': historial_data_json,
        'pagination': {
            'page': historial_data['page'],
            'pages': historial_data['total_pages'],
            'per_page': historial_data['per_page'],
            'total': historial_data['total'],
            'has_prev': historial_data['has_prev'],
            'has_next': historial_data['has_next']
        }
    })
