from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import jsonify


def create_apispec():
    """Crea la especificación OpenAPI."""
    spec = APISpec(
        title="API Sitios Históricos",
        version="1.0.0",
        openapi_version="3.0.2",
        info={
            "description": "API REST para gestión de sitios históricos, reseñas y favoritos",
            "contact": {
                "name": "Equipo de desarrollo",
                "url": "https://example.com"
            }
        },
        servers=[
            {"url": "http://localhost:5000", "description": "Servidor de desarrollo"},
        ],
        plugins=[MarshmallowPlugin()],
    )
    
    # Definir el esquema de seguridad JWT
    spec.components.security_scheme(
        "bearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Token JWT en formato: Bearer {token}"
        }
    )
    
    return spec


def register_schemas(spec):
    """Registra los schemas de Marshmallow en la especificación."""
    from src.web.schemas.user import UserCreateSchema, UserReadSchema, UserLoginSchema, UserUpdateSchema
    from src.web.schemas.sitios import SitioCreateSchema, SitioReadSchema, SitioUpdateSchema
    from src.web.schemas.reseña import ReseñaCreateSchema, ReseñaReadSchema
    
    # Registrar schemas de usuario
    spec.components.schema("UserCreate", schema=UserCreateSchema)
    spec.components.schema("UserRead", schema=UserReadSchema)
    spec.components.schema("UserLogin", schema=UserLoginSchema)
    spec.components.schema("UserUpdate", schema=UserUpdateSchema)
    
    # Registrar schemas de sitios
    spec.components.schema("SitioCreate", schema=SitioCreateSchema)
    spec.components.schema("SitioRead", schema=SitioReadSchema)
    spec.components.schema("SitioUpdate", schema=SitioUpdateSchema)
    
    # Registrar schemas de reseñas
    spec.components.schema("ReseñaCreate", schema=ReseñaCreateSchema)
    spec.components.schema("ReseñaRead", schema=ReseñaReadSchema)


def get_swagger_json(spec):
    """Retorna la especificación OpenAPI en formato JSON."""
    return jsonify(spec.to_dict())
