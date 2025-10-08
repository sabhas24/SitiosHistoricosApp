from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.database import Base

# Tabla muchos a muchos
sitio_tag = Table(
    'sitio_tag',
    Base.metadata,
    Column('sitio_id', Integer, ForeignKey('sitios_historicos.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    slug = Column(String(60), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    sitios = relationship('SitioHistorico', secondary=sitio_tag, back_populates='tags')

    __table_args__ = (
        UniqueConstraint('nombre', name='uq_tag_nombre'),
        UniqueConstraint('slug', name='uq_tag_slug'),
    )

    def __init__(self, nombre):
        self.nombre = nombre
        self.slug = self.generate_slug(nombre)

    @staticmethod
    def generate_slug(nombre):
        import unicodedata
        import re
        nombre = nombre.lower()
        nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('ascii')
        nombre = re.sub(r'\s+', '-', nombre)
        nombre = re.sub(r'[^a-z0-9-]', '', nombre)
        nombre = re.sub(r'-+', '-', nombre)
        return nombre
