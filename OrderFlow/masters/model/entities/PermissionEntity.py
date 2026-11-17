from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from configuration.DatabaseConfiguration import Base


class PermissionEntity(Base):
    __tablename__ = 'permisos'
    __table_args__ = {"extend_existing": True}
    
    nombre = Column(String(100), primary_key=True, nullable=False)
    descripcion = Column(Text, nullable=False)