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
    localidadId = Column(String(50), ForeignKey("localidades.id"), nullable=True)
    provinciaNombre = Column(String(50), ForeignKey("provincias.nombre"), nullable=True)

    localidad = relationship("LocalityEntity")
    provincia = relationship("ProvinceEntity")

    