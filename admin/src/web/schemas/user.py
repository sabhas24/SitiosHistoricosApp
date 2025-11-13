from marshmallow import Schema, fields, validate, EXCLUDE

class BaseSchema(Schema):
    """Schema base para ignorar campos extra."""
    class Meta:
        unknown = EXCLUDE   


class UserReadSchema(BaseSchema):
    """Schema para lectura de usuario."""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)

class UserCreateSchema(BaseSchema):
    """Schema para creación de usuario público."""
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=128))


class UserLoginSchema(BaseSchema):
    """Schema para login de usuario."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=128))

class UserUpdateSchema(BaseSchema):
    """Schema para actualización parcial de usuario."""
    name = fields.Str(validate=validate.Length(min=1, max=80))
    last_name = fields.Str(validate=validate.Length(min=1, max=80))
    password = fields.Str(load_only=True, validate=validate.Length(min=8, max=128))
