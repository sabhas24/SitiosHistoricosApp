from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from src.models.database import Base
import enum

class TipoAccion(enum.Enum):
    CREACION = "Creación"
    EDICION = "Edición" 
    ELIMINACION = "Eliminación"
    CAMBIO_ESTADO = "Cambio de estado"
    CAMBIO_TAGS = "Cambio de tags"
    CAMBIO_VISIBILIDAD = "Cambio de visibilidad"

class HistorialSitio(Base):
    __tablename__ = 'historial_sitios'
    
    id = Column(Integer, primary_key=True)
    sitio_id = Column(Integer, ForeignKey('sitios_historicos.id', ondelete='SET NULL'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    fecha_hora = Column(DateTime, default=func.now(), nullable=False)
    tipo_accion = Column(String(50), nullable=False)
    detalles = Column(Text, nullable=True)  # Para almacenar información adicional del cambio
    
    # Relaciones
    sitio = relationship('SitioHistorico', backref='historial')
    usuario = relationship('user', backref='historial_modificaciones')
    
    def __repr__(self):
        return f'<HistorialSitio {self.tipo_accion} - {self.fecha_hora}>'
