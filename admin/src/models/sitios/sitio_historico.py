from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, Float, event
from sqlalchemy.sql import func
from geoalchemy2.types import Geometry
from src.models.database import Base, db
from sqlalchemy.orm import relationship
from src.models.tags.tag import sitio_tag, Tag
import enum

class EstadoConservacion(enum.Enum):
    BUENO = "Bueno"
    REGULAR = "Regular"
    MALO = "Malo"

class Categoria(enum.Enum):
    ARQUITECTURA = "Arquitectura"
    INFRAESTRUCTURA = "Infraestructura"
    SITIO_ARQUEOLOGICO = "Sitio arqueológico"
    MONUMENTO = "Monumento"
    EDIFICIO_HISTORICO = "Edificio histórico"
    SITIO_NATURAL = "Sitio natural"

class SitioHistorico(Base):
    __tablename__ = 'sitios_historicos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion_breve = Column(Text, nullable=False)
    descripcion_completa = Column(Text, nullable=True)
    ciudad = Column(String(100), nullable=False)
    provincia = Column(String(100), nullable=False)
    
    ubicacion = Column(Geometry('POINT', 4326), nullable=False)
    
    estado_conservacion = Column(Enum(EstadoConservacion), nullable=False)
    anio_inauguracion = Column(Integer, nullable=True)
    categoria = Column(Enum(Categoria), nullable=False)
    
    # Campos para ranking
    calificacion_promedio = Column(Float, default=0.0, nullable=False)
    total_resenas = Column(Integer, default=0, nullable=False)
    
    # Campos de control
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    fecha_ultima_modificacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    visible = Column(Boolean, default=False, nullable=False)
    
    tags = relationship('Tag', secondary=sitio_tag, back_populates='sitios')
    reseñas = relationship('Reseña', back_populates='sitio', cascade='all, delete-orphan')
    favoritos = relationship('Favorito', back_populates='sitio', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SitioHistorico {self.nombre}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion_breve': self.descripcion_breve,
            'descripcion_completa': self.descripcion_completa,
            'ciudad': self.ciudad,
            'provincia': self.provincia,
            'latitud': self.ubicacion.y if self.ubicacion else None,
            'longitud': self.ubicacion.x if self.ubicacion else None,
            'estado_conservacion': self.estado_conservacion.value if self.estado_conservacion else None,
            'anio_inauguracion': self.anio_inauguracion,
            'categoria': self.categoria.value if self.categoria else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'fecha_ultima_modificacion': self.fecha_ultima_modificacion.isoformat() if self.fecha_ultima_modificacion else None,
            'visible': self.visible,
            'tags': [tag.nombre for tag in self.tags]
        }

#simula un trigger de base de datos para actualizar el ranking 
def actualizar_ranking_after_flush(session, flush_context):
    """Se ejecuta automáticamente después de cada flush (insert/update/delete)"""
    from src.models.reseñas.reseña import Reseña
    
   
    sitios_afectados = set()
    
    for obj in session.new | session.dirty | session.deleted:
        if isinstance(obj, Reseña):
            sitios_afectados.add(obj.sitio_id)
    
    for sitio_id in sitios_afectados:
        result = session.query(
            func.avg(Reseña.calificacion).label('promedio'),
            func.count(Reseña.id).label('total')
        ).filter(Reseña.sitio_id == sitio_id).first()
        
        sitio = session.get(SitioHistorico, sitio_id)
        if sitio:
            sitio.calificacion_promedio = float(result.promedio or 0)
            sitio.total_resenas = result.total or 0