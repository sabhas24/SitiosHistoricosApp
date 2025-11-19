from datetime import datetime, timezone
from sqlalchemy import DateTime, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.database import Base, db


class ImagenSitio(Base):
    """Modelo para imágenes de sitios históricos"""
    __tablename__ = 'imagenes_sitios'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    sitio_id: Mapped[int] = mapped_column(ForeignKey("sitios_historicos.id"), nullable=False)
    
    url_publica: Mapped[str] = mapped_column(String(500), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    titulo_alt: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)

    orden: Mapped[int] = mapped_column(Integer, default=0)
    es_portada: Mapped[bool] = mapped_column(Boolean, default=False)
    
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    fecha_modificacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    sitio: Mapped["SitioHistorico"] = relationship("SitioHistorico", back_populates="imagenes")
    
    def __repr__(self):
        return f'<ImagenSitio id={self.id} - {self.titulo_alt}>'

    @property
    def es_eliminable(self):
        """Verifica si la imagen puede ser eliminada (no es portada)"""
        return not self.es_portada
