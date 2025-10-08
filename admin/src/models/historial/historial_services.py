from src.models.database import db
from src.models.historial.historial import HistorialSitio, TipoAccion
from flask import session
from sqlalchemy import func, or_

def registrar_evento_historial(sitio_id, tipo_accion, detalles=None):
    """Registrar un evento en el historial de modificaciones"""
    try:
        # Obtener el usuario actual de la sesión
        email_usuario = session.get('user')
        if not email_usuario:
            return False
        
        # Buscar el usuario
        from src.models.auth.user import user
        usuario = db.session.query(user).filter_by(email=email_usuario).first()
        if not usuario:
            return False
        
        # Para eventos de eliminación, agregar información del sitio al detalle
        if tipo_accion == "Eliminación" and sitio_id:
            from src.models.sitios.sitio_historico import SitioHistorico
            sitio = db.session.get(SitioHistorico, sitio_id)
            if sitio and detalles:
                detalles += f" - ID: {sitio_id}, Ubicación: {sitio.ciudad}, {sitio.provincia}"
        
        # Crear registro del historial
        evento = HistorialSitio(
            sitio_id=sitio_id,
            user_id=usuario.id,
            tipo_accion=tipo_accion,
            detalles=detalles
        )
        
        db.session.add(evento)
        db.session.commit()
        
        print(f"✅ Evento registrado: {tipo_accion} en sitio {sitio_id} por usuario {usuario.email}")
        return True
        
    except Exception as e:
        print(f"❌ Error al registrar evento en historial: {str(e)}")
        db.session.rollback()
        return False

def obtener_historial_sitio(sitio_id, page=1, per_page=25, filters=None):
    """Obtener historial de un sitio con filtros y paginación"""
    query = db.session.query(HistorialSitio).filter(HistorialSitio.sitio_id == sitio_id)
    
    # Aplicar filtros si existen
    if filters:
        # Filtro por usuario
        if filters.get('usuario'):
            from src.models.auth.user import user
            query = query.join(user).filter(
                or_(
                    user.name.ilike(f"%{filters['usuario']}%"),
                    user.email.ilike(f"%{filters['usuario']}%")
                )
            )
        
        # Filtro por tipo de acción
        if filters.get('tipo_accion'):
            query = query.filter(HistorialSitio.tipo_accion == filters['tipo_accion'])
        
        # Filtro por rango de fechas
        if filters.get('fecha_desde'):
            try:
                from datetime import datetime
                fecha_desde = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d')
                query = query.filter(HistorialSitio.fecha_hora >= fecha_desde)
            except ValueError:
                pass
        
        if filters.get('fecha_hasta'):
            try:
                from datetime import datetime
                fecha_hasta = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d')
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(HistorialSitio.fecha_hora <= fecha_hasta)
            except ValueError:
                pass
    
    # Orden cronológico (más reciente primero)
    query = query.order_by(HistorialSitio.fecha_hora.desc())
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Obtener total de registros
    total = query.count()
    
    # Obtener registros paginados
    eventos = query.offset(offset).limit(per_page).all()
    
    # Calcular información de paginación
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'eventos': eventos,
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

def obtener_tipos_accion():
    """Obtener lista de tipos de acción disponibles"""
    return [tipo.value for tipo in TipoAccion]

def obtener_historial_completo(page=1, per_page=25, filters=None):
    """Obtener historial completo de todos los sitios (incluyendo eliminados)"""
    query = db.session.query(HistorialSitio)
    
    # Aplicar filtros si existen
    if filters:
        # Filtro por usuario
        if filters.get('usuario'):
            from src.models.auth.user import user
            query = query.join(user).filter(
                or_(
                    user.name.ilike(f"%{filters['usuario']}%"),
                    user.email.ilike(f"%{filters['usuario']}%")
                )
            )
        
        # Filtro por tipo de acción
        if filters.get('tipo_accion'):
            query = query.filter(HistorialSitio.tipo_accion == filters['tipo_accion'])
        
        # Filtro por rango de fechas
        if filters.get('fecha_desde'):
            try:
                from datetime import datetime
                fecha_desde = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d')
                query = query.filter(HistorialSitio.fecha_hora >= fecha_desde)
            except ValueError:
                pass
        
        if filters.get('fecha_hasta'):
            try:
                from datetime import datetime
                fecha_hasta = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d')
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(HistorialSitio.fecha_hora <= fecha_hasta)
            except ValueError:
                pass
    
    # Orden cronológico (más reciente primero)
    query = query.order_by(HistorialSitio.fecha_hora.desc())
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Obtener total de registros
    total = query.count()
    
    # Obtener registros paginados
    eventos = query.offset(offset).limit(per_page).all()
    
    # Calcular información de paginación
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'eventos': eventos,
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
