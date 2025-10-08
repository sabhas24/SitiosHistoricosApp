# Importar todos los controladores para que estén disponibles
from .auth import bp as auth_bp
# Explicit import from subpackage sitios.sitios where blueprint is defined
from .sitios.sitios import bp as sitios_bp
from .tagsfolder.tags import bp as tags_bp
from .perfil.profile import bp as profile_bp
from .historial.historial import historial_bp
from .propuestas import propuestas_bp
from .reseñas import reseñas_bp

# Lista de todos los blueprints para registrar en la aplicación
blueprints = [
    auth_bp,
    sitios_bp, 
    tags_bp,
    profile_bp,
    historial_bp,
    propuestas_bp,
    reseñas_bp
]