from datetime import datetime, timezone
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from src.models.database import db
from src.models.reseña import Reseña, EstadoReseña


def obtener_reseñas(page=1, per_page=25, filters=None):
    """Obtener lista paginada de reseñas con filtros opcionales"""
    query = db.session.query(Reseña).options(
        joinedload(Reseña.sitio),
        joinedload(Reseña.usuario_moderador)
    )
    
    # Aplicar filtros si existen
    if filters:
        # Filtro por estado
        if filters.get('estado'):
            try:
                estado_enum = EstadoReseña(filters['estado'])
                query = query.filter(Reseña.estado == estado_enum)
            except ValueError:
                pass
        
        # Filtro por calificación
        if filters.get('calificacion'):
            try:
                calificacion = int(filters['calificacion'])
                if 1 <= calificacion <= 5:
                    query = query.filter(Reseña.calificacion == calificacion)
            except (ValueError, TypeError):
                pass
        
        # Filtro por sitio
        if filters.get('sitio'):
            query = query.join(Reseña.sitio).filter(
                or_(
                    Reseña.sitio.has(nombre__ilike=f"%{filters['sitio']}%"),
                    Reseña.sitio.has(ciudad__ilike=f"%{filters['sitio']}%")
                )
            )
        
        # Filtro por usuario
        if filters.get('usuario'):
            query = query.filter(
                or_(
                    Reseña.nombre_usuario.ilike(f"%{filters['usuario']}%"),
                    Reseña.email_usuario.ilike(f"%{filters['usuario']}%")
                )
            )
        
        # Filtro por rango de fechas
        if filters.get('fecha_desde'):
            try:
                fecha_desde = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d')
                query = query.filter(Reseña.fecha_creacion >= fecha_desde)
            except ValueError:
                pass
        
        if filters.get('fecha_hasta'):
            try:
                fecha_hasta = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d')
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(Reseña.fecha_creacion <= fecha_hasta)
            except ValueError:
                pass
    
    # Orden por fecha de creación (más reciente primero)
    query = query.order_by(Reseña.fecha_creacion.desc())
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Obtener total de registros
    total = query.count()
    
    # Obtener registros paginados
    reseñas = query.offset(offset).limit(per_page).all()
    
    # Calcular información de paginación
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'reseñas': reseñas,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_num': page - 1 if has_prev else None,
        'next_num': page + 1 if has_next else None,
        'filters': filters or {}
    }


def obtener_reseña_por_id(reseña_id):
    """Obtener una reseña específica por ID"""
    return db.session.query(Reseña).options(
        joinedload(Reseña.sitio),
        joinedload(Reseña.usuario_moderador)
    ).filter(Reseña.id == reseña_id).first()


def aprobar_reseña(reseña_id, usuario_moderador_id):
    """Aprobar una reseña"""
    reseña = obtener_reseña_por_id(reseña_id)
    
    if not reseña or not reseña.puede_ser_moderada:
        return False, "Reseña no encontrada o ya procesada"
    
    try:
        reseña.estado = EstadoReseña.APROBADA
        reseña.fecha_moderacion = datetime.now(timezone.utc)
        reseña.usuario_moderador_id = usuario_moderador_id
        reseña.motivo_rechazo = None  # Limpiar motivo de rechazo si existía
        
        db.session.commit()
        
        return True, "Reseña aprobada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al aprobar reseña: {str(e)}"


def rechazar_reseña(reseña_id, usuario_moderador_id, motivo_rechazo):
    """Rechazar una reseña con motivo"""
    reseña = obtener_reseña_por_id(reseña_id)
    
    if not reseña or not reseña.puede_ser_moderada:
        return False, "Reseña no encontrada o ya procesada"
    
    try:
        reseña.estado = EstadoReseña.RECHAZADA
        reseña.fecha_moderacion = datetime.now(timezone.utc)
        reseña.usuario_moderador_id = usuario_moderador_id
        reseña.motivo_rechazo = motivo_rechazo
        
        db.session.commit()
        
        return True, "Reseña rechazada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al rechazar reseña: {str(e)}"


def obtener_estadisticas_reseñas():
    """Obtener estadísticas básicas de reseñas"""
    total = db.session.query(Reseña).count()
    pendientes = db.session.query(Reseña).filter(
        Reseña.estado == EstadoReseña.PENDIENTE
    ).count()
    aprobadas = db.session.query(Reseña).filter(
        Reseña.estado == EstadoReseña.APROBADA
    ).count()
    rechazadas = db.session.query(Reseña).filter(
        Reseña.estado == EstadoReseña.RECHAZADA
    ).count()
    
    # Promedio de calificaciones aprobadas
    from sqlalchemy import func
    promedio_calificacion = db.session.query(
        func.avg(Reseña.calificacion)
    ).filter(Reseña.estado == EstadoReseña.APROBADA).scalar()
    
    return {
        'total': total,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
        'rechazadas': rechazadas,
        'promedio_calificacion': round(promedio_calificacion, 2) if promedio_calificacion else 0
    }


def crear_reseña_ejemplo():
    """Crear una reseña de ejemplo para testing"""
    # Obtener el primer sitio disponible
    from src.models.sitio_historico import SitioHistorico
    sitio = db.session.query(SitioHistorico).first()
    
    if not sitio:
        return None
    
    reseña = Reseña(
        titulo="Excelente sitio histórico",
        comentario="Visité este lugar y quedé impresionado por su historia y conservación. Muy recomendable para aprender sobre nuestro patrimonio.",
        calificacion=5,
        sitio_id=sitio.id,
        email_usuario="visitante@example.com",
        nombre_usuario="María García"
    )
    
    db.session.add(reseña)
    db.session.commit()
    return reseña
