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
                "expires_in": {"type": "integer", "description": "Segundos hasta expiración"},
                "user": {"$ref": "#/components/schemas/UserRead"}
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
        "/api/sitios/{sitio_id}/reseñas": {
            "post": {
                "tags": ["Reseñas"],
                "summary": "Crear una reseña",
                "description": "Crea una nueva reseña para un sitio. Requiere JWT",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "sitio_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ReseñaCreate"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Reseña creada",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ReseñaRead"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            }
        },
        "/api/sitios/{sitio_id}/favoritos": {
            "put": {
                "tags": ["Favoritos"],
                "summary": "Agregar a favoritos",
                "description": "Agrega un sitio a los favoritos del usuario autenticado",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "sitio_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {"description": "Sitio agregado a favoritos"},
                    "401": {"description": "No autenticado"},
                    "404": {"description": "Sitio no encontrado"}
                }
            },
            "delete": {
                "tags": ["Favoritos"],
                "summary": "Eliminar de favoritos",
                "description": "Elimina un sitio de los favoritos del usuario autenticado",
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {
                        "name": "sitio_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {"description": "Sitio eliminado de favoritos"},
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
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "schema": {"type": "integer", "default": 25}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de favoritos",
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
