from src.models.database import db
from src.models.sitio_historico import SitioHistorico, EstadoConservacion, Categoria
from geoalchemy2.functions import ST_X, ST_Y, ST_GeomFromText
from sqlalchemy import func

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

def sitio_index():
    """Obtener todos los sitios históricos"""
    return db.session.query(SitioHistorico).all()

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