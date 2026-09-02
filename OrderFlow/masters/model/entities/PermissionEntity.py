from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PermissionEntity(Base):
    __tablename__ = 'permisos'

    nombre = Column(String(100), primary_key=True)
    descripcion = Column(String(200))