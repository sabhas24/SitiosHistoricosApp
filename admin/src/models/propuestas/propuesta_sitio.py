from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, String, Text, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.database import Base


class EstadoPropuesta(Enum):
    """Estados posibles de una propuesta de sitio histórico"""
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"


class EstadoConservacionPropuesta(Enum):
    """Estados de conservación para propuestas"""
    BUENO = "Bueno"
    REGULAR = "Regular"
    MALO = "Malo"


class PropuestaSitio(Base):
    """Modelo para propuestas de sitios históricos enviadas por usuarios públicos"""
    __tablename__ = 'propuestas_sitios'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Información del sitio propuesto
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion_breve: Mapped[str] = mapped_column(Text, nullable=False)
    descripcion_completa: Mapped[str] = mapped_column(Text, nullable=True)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False)
    latitud: Mapped[float] = mapped_column(Float, nullable=False)
    longitud: Mapped[float] = mapped_column(Float, nullable=False)
    estado_conservacion: Mapped[EstadoConservacionPropuesta] = mapped_column(nullable=False)
    año_inauguracion: Mapped[int] = mapped_column(Integer, nullable=True)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Información de la propuesta
    estado: Mapped[EstadoPropuesta] = mapped_column(default=EstadoPropuesta.PENDIENTE)
    fecha_propuesta: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    # Usuario que propuso (para futuro uso en Etapa 2)
    email_proponente: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre_proponente: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Validación/rechazo
    fecha_validacion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    usuario_validador_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    motivo_rechazo: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Sitio creado (si fue aprobada)
    sitio_creado_id: Mapped[int] = mapped_column(ForeignKey("sitios_historicos.id"), nullable=True)
    
    # Relaciones
    usuario_validador: Mapped["user"] = relationship("user", foreign_keys=[usuario_validador_id])
    sitio_creado: Mapped["SitioHistorico"] = relationship("SitioHistorico", foreign_keys=[sitio_creado_id])
    
    def __repr__(self):
        return f'<PropuestaSitio {self.nombre} - {self.estado.value}>'

    @property
    def puede_ser_validada(self):
        """Verifica si la propuesta puede ser validada"""
        return self.estado == EstadoPropuesta.PENDIENTE

    @property
    def dias_desde_propuesta(self):
        """Calcula los días transcurridos desde la propuesta"""
        if self.fecha_propuesta:
            return (datetime.now(timezone.utc) - self.fecha_propuesta).days
        return 0
