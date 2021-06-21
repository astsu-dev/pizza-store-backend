from pizza_store.db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


class RolePermission(Base):
    __tablename__ = "roles_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
