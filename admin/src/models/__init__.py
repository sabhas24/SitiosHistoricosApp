# Importar todos los modelos para que SQLAlchemy los reconozca
from .sitio_historico import SitioHistorico
from .tag import Tag
from .auth.user import user
from .auth.role import Role
from .auth.permission import Permission
from .feature_flag import FeatureFlag
from .historial import HistorialSitio
from .propuesta_sitio import PropuestaSitio
from .reseña import Reseña

# Exportar para facilitar importaciones
__all__ = [
    'SitioHistorico',
    'Tag', 
    'user',
    'Role',
    'Permission',
    'FeatureFlag',
    'HistorialSitio',
    'PropuestaSitio',
    'Reseña'
]