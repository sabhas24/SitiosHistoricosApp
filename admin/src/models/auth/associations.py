from src.models.database import Base
from sqlalchemy import Table, Column, Integer, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.auth.role import Role
    from src.models.auth.permission import Permission

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)