from marshmallow import Schema, fields
from src.web.schemas.sitios import SitioReadSchema

class FavoritoReadSchema(Schema):
    """Schema para leer favoritos."""
    id = fields.Integer()
    user_id = fields.Integer()
    sitio_id = fields.Integer()
    fecha_agregado = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ')
    sitio = fields.Nested(SitioReadSchema)
    
    class Meta:
        load_instance = True
        
class FavoritoCreateSchema(Schema):
    """Schema para crear favoritos."""
    sitio_id = fields.Integer(required=True)
    
    class Meta:
        load_instance = True
