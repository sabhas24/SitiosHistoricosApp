"""Convenient access to ORM models.

Usamos importación diferida (lazy) para evitar problemas de dependencias
cíclicas durante inicialización de la app.
"""
from importlib import import_module
from typing import TYPE_CHECKING

def __getattr__(name: str):  # pragma: no cover
    mapping = {
        'SitioHistorico': ('src.models.sitios.sitio_historico', 'SitioHistorico'),
        'Tag': ('src.models.tags.tag', 'Tag'),
        'user': ('src.models.auth.user', 'user'),
        'Role': ('src.models.auth.role', 'Role'),
        'Permission': ('src.models.auth.permission', 'Permission'),
        'FeatureFlag': ('src.models.feature_flag.feature_flag', 'FeatureFlag'),
        'HistorialSitio': ('src.models.historial.historial', 'HistorialSitio'),
        'PropuestaSitio': ('src.models.propuestas.propuesta_sitio', 'PropuestaSitio'),
        'Reseña': ('src.models.reseñas.reseña', 'Reseña'),
    }
    if name in mapping:
        module_name, attr = mapping[name]
        module = import_module(module_name)
        return getattr(module, attr)
    raise AttributeError(name)

if TYPE_CHECKING:  # Para autocompletado / type checkers
    from src.models.sitios.sitio_historico import SitioHistorico  # noqa: F401
    from src.models.tags.tag import Tag  # noqa: F401
    from src.models.auth.user import user  # noqa: F401
    from src.models.auth.role import Role  # noqa: F401
    from src.models.auth.permission import Permission  # noqa: F401
    from src.models.feature_flag.feature_flag import FeatureFlag  # noqa: F401
    from src.models.historial.historial import HistorialSitio  # noqa: F401
    from src.models.propuestas.propuesta_sitio import PropuestaSitio  # noqa: F401
    from src.models.reseñas.reseña import Reseña  # noqa: F401

__all__ = [
    'SitioHistorico', 'Tag', 'user', 'Role', 'Permission', 'FeatureFlag',
    'HistorialSitio', 'PropuestaSitio', 'Reseña'
]