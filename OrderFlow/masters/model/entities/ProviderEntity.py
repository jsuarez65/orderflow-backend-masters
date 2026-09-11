from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class ProviderEntity(Base):
    __tablename__ = 'providers'

    cuit = Column(String(50), primary_key=True)
    razonSocial = Column(String(50), nullable=False)
    domicilio = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    telefono = Column(String(50), nullable=True)
    localidad_codigo_postal = Column(String(50), ForeignKey("localidades.codigo_postal"), nullable=True)
    provincia_nombre = Column(String(50), ForeignKey("provincias.nombre"), nullable=True)

    localidad = relationship("LocalityEntity")
    provincia = relationship("ProvinceEntity")
    