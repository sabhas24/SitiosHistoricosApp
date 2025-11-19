from marshmallow import Schema, fields, validate, EXCLUDE


class BaseSchema(Schema):
    """Schema base para ignorar campos extra."""

    class Meta:
        unknown = EXCLUDE


class ImagenSitioSchema(BaseSchema):
    """Schema para imágenes de sitios históricos."""

    id = fields.Int(dump_only=True)
    url_publica = fields.Str(required=True)
    nombre_archivo = fields.Str(dump_only=True)
    titulo_alt = fields.Str(required=True)
    descripcion = fields.Str(required=False)
    orden = fields.Int(dump_only=True)
    es_portada = fields.Bool(dump_only=True)


class SitioReadSchema(BaseSchema):
    """Schema para lectura de sitio histórico."""

    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    descripcion_breve = fields.Str(required=False)
    descripcion_completa = fields.Str(required=False)
    ciudad = fields.Str(required=True)
    provincia = fields.Str(required=True)
    estado_conservacion = fields.Method("get_estado_conservacion")
    anio_inauguracion = fields.Int(required=False)
    categoria = fields.Method("get_categoria")
    latitud = fields.Method("get_latitud")
    longitud = fields.Method("get_longitud")
    visible = fields.Bool(dump_only=True)
    fecha_registro = fields.DateTime(dump_only=True)
    fecha_ultima_modificacion = fields.DateTime(dump_only=True)
    tags = fields.Method("get_tags")
    imagenes = fields.Nested(ImagenSitioSchema, many=True, dump_only=True)
    imagen_principal = fields.Method("get_imagen_principal")

    def get_latitud(self, obj):
        """Obtener latitud desde la ubicación PostGIS."""
        if hasattr(obj, "ubicacion") and obj.ubicacion:
            from geoalchemy2.functions import ST_Y
            from src.models.database import db

            result = db.session.query(ST_Y(obj.ubicacion)).scalar()
            return float(result) if result else None
        return None

    def get_longitud(self, obj):
        """Obtener longitud desde la ubicación PostGIS."""
        if hasattr(obj, "ubicacion") and obj.ubicacion:
            from geoalchemy2.functions import ST_X
            from src.models.database import db

            result = db.session.query(ST_X(obj.ubicacion)).scalar()
            return float(result) if result else None
        return None

    def get_imagen_principal(self, obj):
        """Obtener la URL de la imagen principal (portada)."""
        if hasattr(obj, "imagen_portada") and obj.imagen_portada:
            return obj.imagen_portada.url_publica
        # Si no hay portada, usar la primera imagen
        if hasattr(obj, "imagenes") and obj.imagenes:
            return obj.imagenes[0].url_publica
        return None

    def get_tags(self, obj):
        """Obtener los nombres de los tags."""
        if hasattr(obj, "tags") and obj.tags:
            return [tag.nombre for tag in obj.tags]
        return []

    def get_estado_conservacion(self, obj):
        """Obtener el valor del estado de conservación."""
        if hasattr(obj, "estado_conservacion") and obj.estado_conservacion:
            return obj.estado_conservacion.value
        return None

    def get_categoria(self, obj):
        """Obtener el valor de la categoría."""
        if hasattr(obj, "categoria") and obj.categoria:
            return obj.categoria.value
        return None


class SitioCreateSchema(BaseSchema):
    """Schema para creación de sitio histórico."""

    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    descripcion_breve = fields.Str(required=True)
    descripcion_completa = fields.Str(required=False)
    ciudad = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    provincia = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    estado_conservacion = fields.Str(
        required=True, validate=validate.OneOf(["Bueno", "Regular", "Malo"])
    )
    anio_inauguracion = fields.Int(
        required=False, validate=validate.Range(min=1000, max=2100)
    )
    categoria = fields.Str(
        required=True,
        validate=validate.OneOf(
            [
                "Arquitectura",
                "Infraestructura",
                "Sitio arqueológico",
                "Monumento",
                "Edificio histórico",
                "Sitio natural",
            ]
        ),
    )
    latitud = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitud = fields.Float(required=True, validate=validate.Range(min=-180, max=180))
    visible = fields.Bool(required=False, load_default=False)
    tags = fields.List(fields.Str(), required=False)


class SitioUpdateSchema(BaseSchema):
    """Schema para actualización parcial de sitio histórico."""

    nombre = fields.Str(validate=validate.Length(min=1, max=255))
    descripcion_breve = fields.Str()
    descripcion_completa = fields.Str()
    ciudad = fields.Str(validate=validate.Length(min=1, max=100))
    provincia = fields.Str(validate=validate.Length(min=1, max=100))
    estado_conservacion = fields.Str(
        validate=validate.OneOf(["Bueno", "Regular", "Malo"])
    )
    anio_inauguracion = fields.Int(validate=validate.Range(min=1000, max=2100))
    categoria = fields.Str(
        validate=validate.OneOf(
            [
                "Arquitectura",
                "Infraestructura",
                "Sitio arqueológico",
                "Monumento",
                "Edificio histórico",
                "Sitio natural",
            ]
        )
    )
    latitud = fields.Float(validate=validate.Range(min=-90, max=90))
    longitud = fields.Float(validate=validate.Range(min=-180, max=180))
    visible = fields.Bool()
    tags = fields.List(fields.Str())
