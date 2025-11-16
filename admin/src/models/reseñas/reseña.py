from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.database import Base
from src.models.sitios.sitio_historico import SitioHistorico
from src.models.auth.user import user

class EstadoReseña(Enum):
    """Estados posibles de una reseña"""
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"


class Reseña(Base):
    """Modelo para reseñas de sitios históricos enviadas por usuarios públicos"""
    __tablename__ = 'reseñas'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Información de la reseña
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    comentario: Mapped[str] = mapped_column(Text, nullable=False)
    calificacion: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 estrellas
    
    # Sitio al que pertenece la reseña
    sitio_id: Mapped[int] = mapped_column(ForeignKey("sitios_historicos.id"), nullable=False)
    
    # Usuario que escribió la reseña (para futuro uso en Etapa 2)
    email_usuario: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Estado de moderación
    estado: Mapped[EstadoReseña] = mapped_column(default=EstadoReseña.PENDIENTE)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    # Moderación
    fecha_moderacion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    usuario_moderador_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    motivo_rechazo: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relaciones
    sitio: Mapped["SitioHistorico"] = relationship("SitioHistorico", back_populates="reseñas")
    usuario_moderador: Mapped["user"] = relationship("user", foreign_keys=[usuario_moderador_id])
    
    def __repr__(self):
        return f'<Reseña {self.titulo} - {self.estado.value}>'

    @property
    def puede_ser_moderada(self):
        """Verifica si la reseña puede ser moderada"""
        return self.estado == EstadoReseña.PENDIENTE

    @property
    def dias_desde_creacion(self):
        """Calcula los días transcurridos desde la creación"""
        if self.fecha_creacion:
            return (datetime.now(timezone.utc) - self.fecha_creacion).days
        return 0

    @property
    def calificacion_estrellas(self):
        """Devuelve la calificación en formato de estrellas"""
        estrellas_llenas = "★" * self.calificacion
        estrellas_vacias = "☆" * (5 - self.calificacion)
        return estrellas_llenas + estrellas_vacias
