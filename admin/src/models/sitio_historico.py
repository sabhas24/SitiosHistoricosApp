from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from geoalchemy2.types import Geometry
from src.models.database import Base
from sqlalchemy.orm import relationship
from src.models.tag import sitio_tag, Tag
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
    
    # Coordenadas geográficas usando PostGIS
    ubicacion = Column(Geometry('POINT'), nullable=False)
    
    estado_conservacion = Column(Enum(EstadoConservacion), nullable=False)
    anio_inauguracion = Column(Integer, nullable=True)
    categoria = Column(Enum(Categoria), nullable=False)
    
    # Campos de control
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    visible = Column(Boolean, default=False, nullable=False)
    tags = relationship('Tag', secondary=sitio_tag, back_populates='sitios')
    reseñas = relationship('Reseña', back_populates='sitio', cascade='all, delete-orphan')
    
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
            'estado_conservacion': self.estado_conservacion.value if self.estado_conservacion else None,
            'anio_inauguracion': self.anio_inauguracion,
            'categoria': self.categoria.value if self.categoria else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'visible': self.visible,
            'tags': [tag.nombre for tag in self.tags]
        }