from datetime import datetime , timezone
from typing import TYPE_CHECKING
from src.models.database import Base
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from sqlalchemy import DateTime, ForeignKey, String
if TYPE_CHECKING:
    from src.models.auth.role import Role
class user(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    is_super_admin: Mapped[bool] = mapped_column(default=False)
    inserted_at: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc)
    )
    favoritos = relationship('Favorito', back_populates='usuario', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}, {self.name}, {self.last_name} >'
