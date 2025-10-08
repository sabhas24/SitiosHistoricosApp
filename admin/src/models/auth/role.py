from src.models.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
from src.models.auth.associations import role_permissions

if TYPE_CHECKING:
    from src.models.auth.user import user
    from src.models.auth.permission import Permission

class Role(Base):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Relaciones
    users: Mapped[list["user"]] = relationship("user", back_populates="role")
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", 
        secondary=role_permissions, 
        back_populates="roles"
    )
    
    def __repr__(self):
        return f'<Role {self.name}>'