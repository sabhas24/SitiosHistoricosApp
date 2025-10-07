from src.models.database import db
from src.models.sitio_historico import SitioHistorico, EstadoConservacion, Categoria
from geoalchemy2.functions import ST_X, ST_Y, ST_GeomFromText
from sqlalchemy import func, or_

def sitio_create(**kwargs):
    """Crear un nuevo sitio histórico"""
    print(f"📝 Creating new sitio histórico: {kwargs.get('nombre')}")
    
    # Crear punto geográfico desde latitud y longitud
    if 'latitud' in kwargs and 'longitud' in kwargs:
        lat = float(kwargs.pop('latitud'))
        lng = float(kwargs.pop('longitud'))
        kwargs['ubicacion'] = f'POINT({lng} {lat})'
    
    # Convertir strings a enums
    if 'estado_conservacion' in kwargs:
        kwargs['estado_conservacion'] = EstadoConservacion(kwargs['estado_conservacion'])
    
    if 'categoria' in kwargs:
        kwargs['categoria'] = Categoria(kwargs['categoria'])
    
    sitio = SitioHistorico(**kwargs)
    db.session.add(sitio)
    db.session.commit()
    
    print(f"✅ Sitio histórico created with ID: {sitio.id}")
    return sitio

def sitio_index(page=1, per_page=25, filters=None):
    """Obtener sitios históricos con paginación y búsqueda avanzada"""
    query = db.session.query(SitioHistorico)
    
    # Aplicar filtros si existen
    if filters:
        # Búsqueda por texto (nombre o descripción breve)
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    SitioHistorico.nombre.ilike(search_term),
                    SitioHistorico.descripcion_breve.ilike(search_term)
                )
            )
        
        # Filtro por ciudad
        if filters.get('ciudad'):
            query = query.filter(SitioHistorico.ciudad.ilike(f"%{filters['ciudad']}%"))
        
        # Filtro por provincia
        if filters.get('provincia'):
            query = query.filter(SitioHistorico.provincia == filters['provincia'])
        
        # Filtro por categoría
        if filters.get('categoria'):
            query = query.filter(SitioHistorico.categoria == Categoria(filters['categoria']))
        
        # Filtro por estado de conservación
        if filters.get('estado_conservacion'):
            query = query.filter(SitioHistorico.estado_conservacion == EstadoConservacion(filters['estado_conservacion']))
        
        # Filtro por visibilidad
        if filters.get('visible') is not None:
            query = query.filter(SitioHistorico.visible == filters['visible'])
        
        # Filtro por rango de fechas
        if filters.get('fecha_desde'):
            try:
                from datetime import datetime
                fecha_desde = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d')
                query = query.filter(SitioHistorico.fecha_registro >= fecha_desde)
            except ValueError:
                pass
        
        if filters.get('fecha_hasta'):
            try:
                from datetime import datetime
                fecha_hasta = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d')
                # Agregar 23:59:59 para incluir todo el día
                fecha_hasta = fecha_hasta.replace(hour=23, minute=59, second=59)
                query = query.filter(SitioHistorico.fecha_registro <= fecha_hasta)
            except ValueError:
                pass
    
    # Aplicar orden
    order_by = filters.get('order_by', 'fecha_registro') if filters else 'fecha_registro'
    order_dir = filters.get('order_dir', 'desc') if filters else 'desc'
    
    if order_by == 'nombre':
        if order_dir == 'asc':
            query = query.order_by(SitioHistorico.nombre.asc())
        else:
            query = query.order_by(SitioHistorico.nombre.desc())
    elif order_by == 'ciudad':
        if order_dir == 'asc':
            query = query.order_by(SitioHistorico.ciudad.asc())
        else:
            query = query.order_by(SitioHistorico.ciudad.desc())
    else:  # fecha_registro por defecto
        if order_dir == 'asc':
            query = query.order_by(SitioHistorico.fecha_registro.asc())
        else:
            query = query.order_by(SitioHistorico.fecha_registro.desc())
    
    # Calcular offset
    offset = (page - 1) * per_page
    
    # Obtener total de registros (después de filtros)
    total = query.count()
    
    # Obtener sitios de la página actual
    sitios = query.offset(offset).limit(per_page).all()
    
    # Calcular información de paginación
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'sitios': sitios,
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

def sitio_show(id):
    """Obtener un sitio histórico por ID"""
    sitio = db.session.get(SitioHistorico, id)
    if not sitio:
        print(f"❌ Sitio histórico with ID {id} not found")
        return None
    return sitio

def sitio_update(id, **kwargs):
    """Actualizar un sitio histórico"""
    print(f"📝 Updating sitio histórico with ID: {id}")
    
    sitio = db.session.get(SitioHistorico, id)
    if not sitio:
        print(f"❌ Sitio histórico with ID {id} not found")
        return None
    
    # Actualizar coordenadas si se proporcionan
    if 'latitud' in kwargs and 'longitud' in kwargs:
        lat = float(kwargs.pop('latitud'))
        lng = float(kwargs.pop('longitud'))
        kwargs['ubicacion'] = f'POINT({lng} {lat})'
    
    # Convertir strings a enums
    if 'estado_conservacion' in kwargs:
        kwargs['estado_conservacion'] = EstadoConservacion(kwargs['estado_conservacion'])
    
    if 'categoria' in kwargs:
        kwargs['categoria'] = Categoria(kwargs['categoria'])
    
    # Actualizar campos
    for key, value in kwargs.items():
        if hasattr(sitio, key):
            setattr(sitio, key, value)
    db.session.commit()
    print(f"✅ Sitio histórico updated: {sitio.nombre}")
    return sitio

def sitio_delete(id):
    """Eliminar un sitio histórico"""
    print(f"📝 Deleting sitio histórico with ID: {id}")
    
    sitio = db.session.get(SitioHistorico, id)
    if not sitio:
        print(f"❌ Sitio histórico with ID {id} not found")
        return False
    
    db.session.delete(sitio)
    db.session.commit()
    print(f"✅ Sitio histórico deleted")
    return True

def sitio_get_coordinates(sitio):
    """Obtener las coordenadas de un sitio histórico"""
    if not sitio.ubicacion:
        return None, None
    
    # Obtener latitud y longitud desde el punto PostGIS
    result = db.session.query(
        ST_Y(sitio.ubicacion).label('latitud'),
        ST_X(sitio.ubicacion).label('longitud')
    ).filter(SitioHistorico.id == sitio.id).first()
    
    if result:
        return result.latitud, result.longitud
    return None, None

def sitio_count():
    """Contar total de sitios históricos"""
    return db.session.query(func.count(SitioHistorico.id)).scalar()

def sitio_count_by_estado():
    """Contar sitios por estado de conservación"""
    return db.session.query(
        SitioHistorico.estado_conservacion,
        func.count(SitioHistorico.id)
    ).group_by(SitioHistorico.estado_conservacion).all()

def sitio_count_visible():
    """Contar sitios visibles"""
    return db.session.query(func.count(SitioHistorico.id)).filter(
        SitioHistorico.visible == True
    ).scalar()

def get_search_options():
    """Obtener opciones para los filtros de búsqueda"""
    # Obtener provincias únicas
    provincias = db.session.query(SitioHistorico.provincia).distinct().order_by(SitioHistorico.provincia).all()
    provincias = [p[0] for p in provincias if p[0]]
    
    # Obtener ciudades únicas
    ciudades = db.session.query(SitioHistorico.ciudad).distinct().order_by(SitioHistorico.ciudad).all()
    ciudades = [c[0] for c in ciudades if c[0]]
    
    return {
        'provincias': provincias,
        'ciudades': ciudades,
        'categorias': [cat.value for cat in Categoria],
        'estados_conservacion': [estado.value for estado in EstadoConservacion]
    }