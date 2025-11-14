from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from src.models.database import Base

class Favorito(Base):
    """Relación entre usuarios y sitios favoritos."""
    __tablename__ = 'favoritos'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sitio_id = Column(Integer, ForeignKey('sitios_historicos.id'), nullable=False)
    fecha_agregado = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    
    usuario = relationship('user', back_populates='favoritos')
    sitio = relationship('SitioHistorico', back_populates='favoritos')
    

    __table_args__ = (
        UniqueConstraint('user_id', 'sitio_id', name='_user_sitio_uc'),
    )
    
    def __repr__(self):
        return f'<Favorito user_id={self.user_id} sitio_id={self.sitio_id}>'