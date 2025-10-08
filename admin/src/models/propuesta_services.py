from datetime import datetime, timezone
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from src.models.database import db
from src.models.propuesta_sitio import PropuestaSitio, EstadoPropuesta
from src.models.sitios import sitio_create
from src.models.sitio_historico import EstadoConservacion, Categoria


def obtener_propuestas(page=1, per_page=25, filters=None):
    """Obtener lista paginada de propuestas con filtros opcionales"""
    query = db.session.query(PropuestaSitio).options(
        joinedload(PropuestaSitio.usuario_validador),
        joinedload(PropuestaSitio.sitio_creado)
    )
    
    # Aplicar filtros si existen
    if filters:
        # Filtro por estado
        if filters.get('estado'):
            try:
                estado_enum = EstadoPropuesta(filters['estado'])
                query = query.filter(PropuestaSitio.estado == estado_enum)
            except ValueError:
                pass
        
        # Filtro por ciudad
        if filters.get('ciudad'):
            query = query.filter(PropuestaSitio.ciudad.ilike(f"%{filters['ciudad']}%"))
        
        # Filtro por provincia
        if filters.get('provincia'):
            query = query.filter(PropuestaSitio.provincia.ilike(f"%{filters['provincia']}%"))
        
        # Filtro por nombre del proponente
        if filters.get('proponente'):
            query = query.filter(
                or_(
                    PropuestaSitio.nombre_proponente.ilike(f"%{filters['proponente']}%"),
                    PropuestaSitio.email_proponente.ilike(f"%{filters['proponente']}%")
                )
            )
        
        # Filtro por rango de fechas
        if filters.get('fecha_desde'):
            try:
                fecha_desde = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d')
                query = query.filter(PropuestaSitio.fecha_propuesta >= fecha_desde)
            except ValueError:
                pass
        
        if filters.get('fecha_hasta'):
            try:
                fecha_hasta = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d')
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(PropuestaSitio.fecha_propuesta <= fecha_hasta)
            except ValueError:
                pass
    
    # Orden por fecha de propuesta (más reciente primero)
    query = query.order_by(PropuestaSitio.fecha_propuesta.desc())
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Obtener total de registros
    total = query.count()
    
    # Obtener registros paginados
    propuestas = query.offset(offset).limit(per_page).all()
    
    # Calcular información de paginación
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'propuestas': propuestas,
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


def obtener_propuesta_por_id(propuesta_id):
    """Obtener una propuesta específica por ID"""
    return db.session.query(PropuestaSitio).options(
        joinedload(PropuestaSitio.usuario_validador),
        joinedload(PropuestaSitio.sitio_creado)
    ).filter(PropuestaSitio.id == propuesta_id).first()


def aprobar_propuesta(propuesta_id, usuario_validador_id):
    """Aprobar una propuesta y crear el sitio histórico correspondiente"""
    propuesta = obtener_propuesta_por_id(propuesta_id)
    
    if not propuesta or not propuesta.puede_ser_validada:
        return False, "Propuesta no encontrada o ya procesada"
    
    try:
        # Mapear estado de conservación
        estado_conservacion_map = {
            'Bueno': EstadoConservacion.BUENO,
            'Regular': EstadoConservacion.REGULAR,
            'Malo': EstadoConservacion.MALO
        }
        estado_conservacion = estado_conservacion_map.get(propuesta.estado_conservacion.value)
        
        # Mapear categoría (simplificado)
        categoria_map = {
            'Arquitectura': Categoria.ARQUITECTURA,
            'Infraestructura': Categoria.INFRAESTRUCTURA,
            'Sitio arqueológico': Categoria.SITIO_ARQUEOLOGICO,
            'Monumento': Categoria.MONUMENTO,
            'Edificio histórico': Categoria.EDIFICIO_HISTORICO,
            'Sitio natural': Categoria.SITIO_NATURAL
        }
        categoria = categoria_map.get(propuesta.categoria, Categoria.MONUMENTO)
        
        # Crear el sitio histórico
        sitio = sitio_create(
            nombre=propuesta.nombre,
            descripcion_breve=propuesta.descripcion_breve,
            descripcion_completa=propuesta.descripcion_completa or propuesta.descripcion_breve,
            ciudad=propuesta.ciudad,
            provincia=propuesta.provincia,
            latitud=propuesta.latitud,
            longitud=propuesta.longitud,
            estado_conservacion=estado_conservacion.value,  # Pasar como string
            anio_inauguracion=propuesta.año_inauguracion,
            categoria=categoria.value,  # Pasar como string
            visible=False,  # Inicialmente no visible hasta revisión adicional
            tags=[]  # Sin tags inicialmente
        )
        
        # Actualizar la propuesta
        propuesta.estado = EstadoPropuesta.APROBADA
        propuesta.fecha_validacion = datetime.now(timezone.utc)
        propuesta.usuario_validador_id = usuario_validador_id
        propuesta.sitio_creado_id = sitio.id
        
        db.session.commit()
        
        return True, f"Propuesta aprobada y sitio histórico creado con ID: {sitio.id}"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al aprobar propuesta: {str(e)}"


def rechazar_propuesta(propuesta_id, usuario_validador_id, motivo_rechazo):
    """Rechazar una propuesta con motivo"""
    propuesta = obtener_propuesta_por_id(propuesta_id)
    
    if not propuesta or not propuesta.puede_ser_validada:
        return False, "Propuesta no encontrada o ya procesada"
    
    try:
        propuesta.estado = EstadoPropuesta.RECHAZADA
        propuesta.fecha_validacion = datetime.now(timezone.utc)
        propuesta.usuario_validador_id = usuario_validador_id
        propuesta.motivo_rechazo = motivo_rechazo
        
        db.session.commit()
        
        return True, "Propuesta rechazada exitosamente"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error al rechazar propuesta: {str(e)}"


def obtener_estadisticas_propuestas():
    """Obtener estadísticas básicas de propuestas"""
    total = db.session.query(PropuestaSitio).count()
    pendientes = db.session.query(PropuestaSitio).filter(
        PropuestaSitio.estado == EstadoPropuesta.PENDIENTE
    ).count()
    aprobadas = db.session.query(PropuestaSitio).filter(
        PropuestaSitio.estado == EstadoPropuesta.APROBADA
    ).count()
    rechazadas = db.session.query(PropuestaSitio).filter(
        PropuestaSitio.estado == EstadoPropuesta.RECHAZADA
    ).count()
    
    return {
        'total': total,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
        'rechazadas': rechazadas
    }


def crear_propuesta_ejemplo():
    """Crear una propuesta de ejemplo para testing"""
    propuesta = PropuestaSitio(
        nombre="Casa Histórica de San Martín (Propuesta)",
        descripcion_breve="Propuesta de casa histórica donde vivió el General San Martín",
        descripcion_completa="Una propuesta detallada de sitio histórico con valor cultural",
        ciudad="Buenos Aires",
        provincia="Buenos Aires",
        latitud=-34.6118,
        longitud=-58.3960,
        estado_conservacion=EstadoConservacionPropuesta.BUENO,
        año_inauguracion=1820,
        categoria="Edificio histórico",
        email_proponente="ciudadano@example.com",
        nombre_proponente="Juan Pérez"
    )
    
    db.session.add(propuesta)
    db.session.commit()
    return propuesta
