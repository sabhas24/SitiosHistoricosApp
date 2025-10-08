from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from src.models.database import Base

class FeatureFlag(Base):
    __tablename__ = 'feature_flags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    is_enabled = Column(Boolean, default=False, nullable=False)
    maintenance_message = Column(Text, nullable=True)  # Mensaje para modos de mantenimiento
    last_modified_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    last_modified_by = Column(String(120), nullable=False)  # Email del usuario que modificó
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f'<FeatureFlag {self.name}: {"ON" if self.is_enabled else "OFF"}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_enabled': self.is_enabled,
            'maintenance_message': self.maintenance_message,
            'last_modified_at': self.last_modified_at.isoformat() if self.last_modified_at else None,
            'last_modified_by': self.last_modified_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
