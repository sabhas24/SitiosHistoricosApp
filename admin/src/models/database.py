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
    from src.models.sitios.sitio_historico import SitioHistorico
    from src.models.historial.historial import HistorialSitio
    from src.models.feature_flag.feature_flag import FeatureFlag
    print("⚠️ Resetting the database")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("✅ Database reset completed.")
