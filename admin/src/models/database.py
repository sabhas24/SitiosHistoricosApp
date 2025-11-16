from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()   

class Base(DeclarativeBase): 
    pass

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.models.auth.user import user
    from src.models.auth.role import Role
    from src.models.auth.permission import Permission
    from src.models.auth.associations import role_permissions
    from src.models.sitios.sitio_historico import SitioHistorico
    from src.models.sitios.imagen_sitio import ImagenSitio
    from src.models.tags.tag import Tag, sitio_tag  
    from src.models.reseñas.reseña import Reseña
    from src.models.favoritos.favoritos import Favorito
    from src.models.propuestas.propuesta_sitio import PropuestaSitio
    from src.models.historial.historial import HistorialSitio
    from src.models.feature_flag.feature_flag import FeatureFlag
    print("⚠️ Resetting the database")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("✅ Database reset completed.")
    
    # Ejecutar seeds automáticamente después del reset
    print("🌱 Running database seeds...")
    from src.models.seeds import run
    run()
    print("✅ Seeds executed successfully.")
