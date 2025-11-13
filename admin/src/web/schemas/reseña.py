from marshmallow import Schema, fields, validate

class BaseSchema(Schema):
    """Schema base para ignorar campos extra."""
    class Meta:
        unknown = EXCLUDE
class ReseñaReadSchema(BaseSchema):
    """Schema para lectura de reseña."""
    id = fields.Int(dump_only=True)
    comentario = fields.Str(required=True)
    calificacion = fields.Int(required=True)
    estado = fields.Str(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_moderacion = fields.DateTime(dump_only=True)
    usuario_moderador_id = fields.Int(dump_only=True)
    motivo_rechazo = fields.Str(dump_only=True) 
class ReseñaCreateSchema(BaseSchema):
    """Schema para creación de reseña."""
    comentario = fields.Str(required=True, validate=validate.Length(min=1))
    calificacion = fields.Int(
        required=True, 
        validate=validate.Range(min=1, max=5)
    )
    sitio_id = fields.Int(required=True)
    email_usuario = fields.Email(required=True)
    nombre_usuario = fields.Str(required=True, validate=validate.Length(min=1, max=100))