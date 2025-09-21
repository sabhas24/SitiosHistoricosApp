from flacker_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()   

def init_app(app):
    db.init_app(app)
    return db

class BaseModel(DeclarativeBase):
    pass
