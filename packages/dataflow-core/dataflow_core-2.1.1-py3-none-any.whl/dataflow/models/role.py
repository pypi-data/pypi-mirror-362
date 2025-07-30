"""models.py"""
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from dataflow.db import Base

class Role(Base):
    """
    Table Role
    """

    __tablename__='ROLE'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    base_role = Column(Enum('admin', 'user', name='base_role_field'), default='user', nullable=False)

    users = relationship("User", back_populates="role_details", cascade="all, delete-orphan")
    role_server_assocs = relationship("RoleServer", back_populates="role")