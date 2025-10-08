from flask import render_template, request, redirect, url_for, flash, jsonify, Blueprint
from src.web.handlers.auth import check_permission
from src.models.propuestas.propuesta_services import (
    obtener_propuestas, 
    obtener_propuesta_por_id, 
    aprobar_propuesta, 
    rechazar_propuesta,
    obtener_estadisticas_propuestas
)
from flask import session

propuestas_bp = Blueprint("propuestas", __name__, url_prefix="/propuestas")


@propuestas_bp.route("/")
def index():
    """Listar todas las propuestas de sitios históricos"""
    
    # Verificar permisos
    if not check_permission("proposal_index"):
        from flask import abort
        abort(403)
    
    # Obtener parámetros de paginación y filtros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    estado = request.args.get('estado', '', type=str)
    ciudad = request.args.get('ciudad', '', type=str)
    provincia = request.args.get('provincia', '', type=str)
    proponente = request.args.get('proponente', '', type=str)
    fecha_desde = request.args.get('fecha_desde', '', type=str)
    fecha_hasta = request.args.get('fecha_hasta', '', type=str)
    
    # Preparar filtros
    filters = {}
    if estado:
        filters['estado'] = estado
    if ciudad:
        filters['ciudad'] = ciudad
    if provincia:
        filters['provincia'] = provincia
    if proponente:
        filters['proponente'] = proponente
    if fecha_desde:
        filters['fecha_desde'] = fecha_desde
    if fecha_hasta:
        filters['fecha_hasta'] = fecha_hasta
    
    # Obtener propuestas con filtros
    propuestas_data = obtener_propuestas(
        page=page,
        per_page=per_page,
        filters=filters if filters else None
    )
    
    # Obtener estadísticas
    estadisticas = obtener_estadisticas_propuestas()
    
    return render_template(
        "propuestas/index.html",
        propuestas_data=propuestas_data,
        estadisticas=estadisticas,
        filtros={
            'estado': estado,
            'ciudad': ciudad,
            'provincia': provincia,
            'proponente': proponente,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta
        }
    )


@propuestas_bp.route("/<int:propuesta_id>")
def detalle(propuesta_id):
    """Ver detalle de una propuesta específica"""
    
    # Verificar permisos
    if not check_permission("proposal_index"):
        from flask import abort
        abort(403)
    
    propuesta = obtener_propuesta_por_id(propuesta_id)
    if not propuesta:
        flash("Propuesta no encontrada", "error")
        return redirect(url_for('propuestas.index'))
    
    return render_template("propuestas/detalle.html", propuesta=propuesta)


@propuestas_bp.route("/<int:propuesta_id>/aprobar", methods=['POST'])
def aprobar(propuesta_id):
    """Aprobar una propuesta y crear el sitio histórico"""
    
    # Verificar permisos
    if not check_permission("proposal_validate"):
        from flask import abort
        abort(403)
    
    usuario_id = session.get('user_id')
    if not usuario_id:
        flash("Error de sesión", "error")
        return redirect(url_for('auth.login'))
    
    success, message = aprobar_propuesta(propuesta_id, usuario_id)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('propuestas.detalle', propuesta_id=propuesta_id))


@propuestas_bp.route("/<int:propuesta_id>/rechazar", methods=['POST'])
def rechazar(propuesta_id):
    """Rechazar una propuesta con motivo"""
    
    # Verificar permisos
    if not check_permission("proposal_validate"):
        from flask import abort
        abort(403)
    
    usuario_id = session.get('user_id')
    if not usuario_id:
        flash("Error de sesión", "error")
        return redirect(url_for('auth.login'))
    
    motivo_rechazo = request.form.get('motivo_rechazo', '').strip()
    if not motivo_rechazo:
        flash("Debe proporcionar un motivo para el rechazo", "error")
        return redirect(url_for('propuestas.detalle', propuesta_id=propuesta_id))
    
    success, message = rechazar_propuesta(propuesta_id, usuario_id, motivo_rechazo)
    
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('propuestas.detalle', propuesta_id=propuesta_id))


@propuestas_bp.route("/estadisticas")
def estadisticas():
    """API endpoint para obtener estadísticas de propuestas"""
    
    # Verificar permisos
    if not check_permission("proposal_index"):
        from flask import abort
        abort(403)
    
    stats = obtener_estadisticas_propuestas()
    return jsonify(stats)


@propuestas_bp.route("/json")
def json_list():
    """API endpoint para obtener propuestas en formato JSON"""
    
    # Verificar permisos
    if not check_permission("proposal_index"):
        from flask import abort
        abort(403)
    
    # Obtener parámetros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    propuestas_data = obtener_propuestas(page=page, per_page=per_page)
    
    # Convertir a formato JSON
    propuestas_json = []
    for propuesta in propuestas_data['propuestas']:
        propuesta_data = {
            'id': propuesta.id,
            'nombre': propuesta.nombre,
            'ciudad': propuesta.ciudad,
            'provincia': propuesta.provincia,
            'estado': propuesta.estado.value,
            'fecha_propuesta': propuesta.fecha_propuesta.isoformat(),
            'proponente': {
                'nombre': propuesta.nombre_proponente,
                'email': propuesta.email_proponente
            },
            'dias_desde_propuesta': propuesta.dias_desde_propuesta
        }
        propuestas_json.append(propuesta_data)
    
    return jsonify({
        'propuestas': propuestas_json,
        'pagination': {
            'page': propuestas_data['page'],
            'pages': propuestas_data['total_pages'],
            'per_page': propuestas_data['per_page'],
            'total': propuestas_data['total'],
            'has_prev': propuestas_data['has_prev'],
            'has_next': propuestas_data['has_next']
        }
    })
