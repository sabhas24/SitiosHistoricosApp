"""
Especificación OpenAPI para la API de Sitios Históricos.
Este archivo define manualmente los endpoints y sus esquemas.
"""


def get_openapi_spec():
    """Retorna la especificación OpenAPI completa."""
    return {
        "openapi": "3.0.2",
        "info": {
            "title": "API Sitios Históricos",
            "version": "1.0.0",
            "description": "API REST para gestión de sitios históricos, reseñas y favoritos",
            "contact": {
                "name": "Equipo de desarrollo"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Servidor de desarrollo"
            }
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Token JWT en formato: Bearer {token}"
                }
            },
            "schemas": get_schemas()
        },
        "paths": get_paths(),
        "tags": [
            {"name": "Usuarios", "description": "Endpoints de autenticación y usuarios"},
            {"name": "Sitios", "description": "Gestión de sitios históricos"},
            {"name": "Reseñas", "description": "Gestión de reseñas de sitios"},
            {"name": "Favoritos", "description": "Gestión de sitios favoritos"}
        ]
    }


def get_schemas():
    """Retorna los esquemas de datos."""
    return {
        "UserCreate": {
            "type": "object",
            "required": ["email", "name", "last_name", "password"],
            "properties": {
                "email": {"type": "string", "format": "email"},
                "name": {"type": "string", "minLength": 1, "maxLength": 80},
                "last_name": {"type": "string", "minLength": 1, "maxLength": 80},
                "password": {"type": "string", "minLength": 8, "maxLength": 128}
            }
        },
        "UserRead": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string", "format": "email"},
                "name": {"type": "string"},
                "last_name": {"type": "string"}
            }
        },
        "UserLogin": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "format": "email"},
                "password": {"type": "string"}
            }
        },
        "LoginResponse": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "Token JWT"},
                "expires_in": {"type": "integer", "description": "Tiempo de expiración en segundos"},
                "user": {"$ref": "#/components/schemas/UserRead"}
            },
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_in": 86400,
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "name": "Juan",
                    "last_name": "Pérez"
                }
            }
        },
        "SitioCreate": {
            "type": "object",
            "required": ["nombre", "descripcion_breve", "ciudad", "provincia", "estado_conservacion", "categoria", "latitud", "longitud"],
            "properties": {
                "nombre": {"type": "string", "maxLength": 255},
                "descripcion_breve": {"type": "string"},
                "descripcion_completa": {"type": "string"},
                "ciudad": {"type": "string", "maxLength": 100},
                "provincia": {"type": "string", "maxLength": 100},
                "estado_conservacion": {
                    "type": "string",
                    "enum": ["Bueno", "Regular", "Malo"]
                },
                "anio_inauguracion": {"type": "integer", "minimum": 1000, "maximum": 2100},
                "categoria": {
                    "type": "string",
                    "enum": ["Arquitectura", "Infraestructura", "Sitio arqueológico", "Monumento", "Edificio histórico", "Sitio natural"]
                },
                "latitud": {"type": "number", "minimum": -90, "maximum": 90},
                "longitud": {"type": "number", "minimum": -180, "maximum": 180},
                "visible": {"type": "boolean"},
                "tags": {"type": "array", "items": {"type": "string"}}
            }
        },
        "SitioRead": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "nombre": {"type": "string"},
                "descripcion_breve": {"type": "string"},
                "descripcion_completa": {"type": "string"},
                "ciudad": {"type": "string"},
                "provincia": {"type": "string"},
                "estado_conservacion": {"type": "string"},
                "anio_inauguracion": {"type": "integer"},
                "categoria": {"type": "string"},
                "latitud": {"type": "number"},
                "longitud": {"type": "number"},
                "visible": {"type": "boolean"},
                "fecha_registro": {"type": "string", "format": "date-time"},
                "fecha_ultima_modificacion": {"type": "string", "format": "date-time"},
                "tags": {"type": "array", "items": {"type": "string"}}
            }
        },
        "ReseñaCreate": {
            "type": "object",
            "required": ["comentario", "calificacion"],
            "properties": {
                "comentario": {"type": "string", "minLength": 1},
                "calificacion": {"type": "integer", "minimum": 1, "maximum": 5}
            }
        },
        "ReseñaRead": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "comentario": {"type": "string"},
                "calificacion": {"type": "integer"},
                "estado": {"type": "string", "enum": ["PENDIENTE", "APROBADA", "RECHAZADA"]},
                "fecha_creacion": {"type": "string", "format": "date-time"},
                "fecha_moderacion": {"type": "string", "format": "date-time"},
                "usuario_moderador_id": {"type": "integer"},
                "motivo_rechazo": {"type": "string"}
            }
        },
        "Review": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID único de la reseña"},
                "site_id": {"type": "integer", "description": "ID del sitio histórico"},
                "rating": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Calificación de 1 a 5"},
                "comment": {"type": "string", "description": "Comentario de la reseña"},
                "inserted_at": {"type": "string", "format": "date-time", "description": "Fecha de creación"},
                "updated_at": {"type": "string", "format": "date-time", "description": "Fecha de actualización"}
            },
            "required": ["id", "site_id", "rating", "inserted_at", "updated_at"]
        },
        "PaginationMeta": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Página actual"},
                "per_page": {"type": "integer", "description": "Elementos por página"},
                "total": {"type": "integer", "description": "Total de elementos"}
            },
            "required": ["page", "per_page", "total"]
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
                "details": {"type": "object"}
            }
        }
    }


def get_paths():
    """Retorna las rutas de la API."""
    return {
        "/api/user/register": {
            "post": {
                "tags": ["Usuarios"],
                "summary": "Registra un nuevo usuario",
                "description": "Crea una cuenta de usuario con rol 'user' por defecto",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Usuario creado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserRead"}
                            }
                        }
                    },
                    "400": {
                        "description": "Error de validación",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        },
        "/api/user/login": {
            "post": {
                "tags": ["Usuarios"],
                "summary": "Iniciar sesión",
                "description": "Autentica un usuario y devuelve un token JWT",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserLogin"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login exitoso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginResponse"}
                            }
                        }
                    },
                    "401": {
                        "description": "Credenciales inválidas",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        },
        "/api/sitios/": {
            "get": {
                "tags": ["Sitios"],
                "summary": "Listar sitios con filtros",
                "description": "Obtiene lista paginada de sitios con filtros de búsqueda y geográficos. Todos los parámetros son opcionales.",
                "parameters": [
                    {"name": "name", "in": "query", "required": False, "schema": {"type": "string"}, "description": "Buscar por nombre del sitio"},
                    {"name": "description", "in": "query", "required": False, "schema": {"type": "string"}, "description": "Buscar en la descripción"},
                    {"name": "city", "in": "query", "required": False, "schema": {"type": "string"}, "description": "Filtrar por ciudad"},
                    {"name": "province", "in": "query", "required": False, "schema": {"type": "string"}, "description": "Filtrar por provincia"},
                    {"name": "tags", "in": "query", "required": False, "schema": {"type": "array", "items": {"type": "string"}}, "description": "Filtrar por tags"},
                    {"name": "order_by", "in": "query", "required": False, "schema": {"type": "string", "enum": ["latest", "oldest"], "default": "latest"}, "description": "Ordenar por fecha"},
                    {"name": "lat", "in": "query", "required": False, "schema": {"type": "number", "minimum": -90, "maximum": 90}, "description": "Latitud del centro de búsqueda"},
                    {"name": "long", "in": "query", "required": False, "schema": {"type": "number", "minimum": -180, "maximum": 180}, "description": "Longitud del centro de búsqueda"},
                    {"name": "radius", "in": "query", "required": False, "schema": {"type": "number"}, "description": "Radio de búsqueda en metros"},
                    {"name": "page", "in": "query", "required": False, "schema": {"type": "integer", "default": 1, "minimum": 1}, "description": "Número de página"},
                    {"name": "per_page", "in": "query", "required": False, "schema": {"type": "integer", "default": 25, "minimum": 1, "maximum": 100}, "description": "Resultados por página"}
                ],
                "responses": {
                    "200": {
                        "description": "Lista de sitios con metadata de paginación",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "sitios": {"type": "array", "items": {"$ref": "#/components/schemas/SitioRead"}},
                                        "meta": {
                                            "type": "object",
                                            "properties": {
                                                "total": {"type": "integer"},
                                                "page": {"type": "integer"},
                                                "per_page": {"type": "integer"},
                                                "total_pages": {"type": "integer"},
                                                "has_prev": {"type": "boolean"},
                                                "has_next": {"type": "boolean"},
                                                "prev_num": {"type": "integer"},
                                                "next_num": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Parámetros inválidos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "type": "object",
                                            "properties": {
                                                "code": {"type": "string"},
                                                "message": {"type": "string"},
                                                "details": {"type": "object"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Sitios"],
                "summary": "Crear un nuevo sitio histórico",
                "description": "Requiere autenticación JWT y permisos de creación",
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SitioCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Sitio creado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SitioRead"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación"},
                    "403": {"description": "Sin permisos"},
                    "409": {"description": "Sitio ya existe"}
                }
            }
        },
        "/api/sitios/{id}": {
            "get": {
                "tags": ["Sitios"],
                "summary": "Obtener un sitio histórico",
                "description": "Endpoint público que retorna la información de un sitio",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del sitio histórico"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Sitio encontrado",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SitioRead"}
                            }
                        }
                    },
                    "404": {"description": "Sitio no encontrado"}
                }
            }
        },
        "/api/sites/{site_id}/reviews": {
            "get": {
                "tags": ["Reseñas"],
                "summary": "Listar reseñas de un sitio",
                "description": "Obtiene lista paginada de reseñas para un sitio histórico específico",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"},
                    {"name": "page", "in": "query", "required": False, "schema": {"type": "integer", "minimum": 1, "default": 1}, "description": "Número de página"},
                    {"name": "per_page", "in": "query", "required": False, "schema": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10}, "description": "Elementos por página"}
                ],
                "responses": {
                    "200": {
                        "description": "Lista de reseñas obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"type": "array", "items": {"$ref": "#/components/schemas/Review"}},
                                        "meta": {"$ref": "#/components/schemas/PaginationMeta"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Parámetros inválidos"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            },
            "post": {
                "tags": ["Reseñas"],
                "summary": "Crear reseña",
                "description": "Crea una nueva reseña para un sitio histórico específico",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "rating": {"type": "integer", "minimum": 1, "maximum": 5, "description": "Calificación de 1 a 5"},
                                    "site_id": {"type": "integer", "description": "ID del sitio (debe coincidir con URL)"},
                                    "comment": {"type": "string", "description": "Comentario opcional"}
                                },
                                "required": ["rating", "site_id"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Reseña creada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Review"}
                            }
                        }
                    },
                    "400": {"description": "Datos inválidos"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            }
        },
        "/api/sites/{site_id}/reviews/{review_id}": {
            "get": {
                "tags": ["Reseñas"],
                "summary": "Obtener reseña específica",
                "description": "Obtiene una reseña existente por su ID",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"},
                    {"name": "review_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reseña"}
                ],
                "responses": {
                    "200": {
                        "description": "Reseña obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Review"}
                            }
                        }
                    },
                    "400": {"description": "ID inválido"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio o reseña no encontrada"}
                }
            },
            "delete": {
                "tags": ["Reseñas"],
                "summary": "Eliminar reseña propia",
                "description": "Elimina una reseña existente por su ID (solo el autor)",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"},
                    {"name": "review_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reseña"}
                ],
                "responses": {
                    "204": {"description": "Reseña eliminada exitosamente"},
                    "401": {"description": "No autenticado"},
                    "403": {"description": "Sin permisos para eliminar"},
                    "404": {"description": "Sitio o reseña no encontrada"}
                }
            }
        },
        "/api/sites/{site_id}/favorite": {
            "put": {
                "tags": ["Favoritos"],
                "summary": "Marcar como favorito",
                "description": "Marca un sitio como favorito del usuario autenticado",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"}
                ],
                "responses": {
                    "204": {"description": "Sitio marcado como favorito"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            },
            "delete": {
                "tags": ["Favoritos"],
                "summary": "Desmarcar como favorito",
                "description": "Elimina un sitio de los favoritos del usuario autenticado",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "site_id", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del sitio histórico"}
                ],
                "responses": {
                    "204": {"description": "Sitio desmarcado como favorito"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            }
        },
        "/api/me/favoritos": {
            "get": {
                "tags": ["Favoritos"],
                "summary": "Listar mis favoritos",
                "description": "Retorna la lista de sitios favoritos del usuario autenticado",
                "security": [{"bearerAuth": []}],
                "responses": {
                    "200": {
                        "description": "Lista de favoritos del usuario",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/SitioRead"}
                                }
                            }
                        }
                    },
                    "401": {"description": "No autenticado"}
                }
            }
        }
    }
