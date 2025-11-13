from src.models.database import db
from src.models.favoritos.favoritos import Favorito
from sqlalchemy.exc import IntegrityError

def favorito_agregar(user_id: int, sitio_id: int):
    """Agrega un sitio a favoritos del usuario."""
    favorito = Favorito(user_id=user_id, sitio_id=sitio_id)
    db.session.add(favorito)
    try:
        db.session.commit()
        print(f"✅ Sitio {sitio_id} agregado a favoritos de usuario {user_id}")
        return favorito
    except IntegrityError:
        db.session.rollback()
        print(f"⚠️ Sitio {sitio_id} ya está en favoritos de usuario {user_id}")
        raise ValueError("El sitio ya está en favoritos")

def favorito_eliminar(user_id: int, sitio_id: int):
    """Elimina un sitio de favoritos del usuario."""
    favorito = db.session.query(Favorito).filter_by(
        user_id=user_id,
        sitio_id=sitio_id
    ).first()
    
    if not favorito:
        print(f"❌ Favorito no encontrado: usuario {user_id}, sitio {sitio_id}")
        return False
    
    db.session.delete(favorito)
    db.session.commit()
    print(f"✅ Sitio {sitio_id} eliminado de favoritos de usuario {user_id}")
    return True

def favorito_listar(user_id: int):
    """Lista todos los favoritos de un usuario."""
    return db.session.query(Favorito).filter_by(user_id=user_id).all()

def favorito_existe(user_id: int, sitio_id: int) -> bool:
    """Verifica si un sitio está en favoritos del usuario."""
    return db.session.query(Favorito).filter_by(
        user_id=user_id,
        sitio_id=sitio_id
    ).first() is not None