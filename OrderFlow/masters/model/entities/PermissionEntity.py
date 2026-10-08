from sqlalchemy import Column, String, Text
from configuration.DatabaseConfiguration import Base


from sqlalchemy import Column, String, Text

class PermissionEntity(Base):
    __tablename__ = 'permisos'
    nombre = Column(String(100), primary_key=True, nullable=False)
    descripcion = Column(Text, nullable=False)