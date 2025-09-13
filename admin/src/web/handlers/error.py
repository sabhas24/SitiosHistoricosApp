from dataclasses import dataclass
from flask import render_template

@dataclass
class HTTPError:
    code: int
    message: str
    description: str

def not_found(e):
    error = HTTPError(
        code=404,
        message="Pagina no encontrada",
        description="lo sentimos, la pagina que estás buscando no existe."
    )
    return render_template('error.html', error=error), 404

def unauthorized(e):
    error = HTTPError(
        code=401,
        message="Acceso no autorizado",
        description="No tenés permiso para acceder a esta página."
    )
    return render_template('error.html', error=error), 401

def internal_error(e):
    error = HTTPError(
        code=500,
        message="Error del servidor",
        description="Ocurrió un error inesperado. Estamos trabajando en ello."
    )
    return render_template('error.html', error=error), 500
