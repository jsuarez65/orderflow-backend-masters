from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class CityEntity(Base):

    __tablename__ = 'localidades'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    codigo_postal = Column(String(10), nullable=False)
    nombre_localidad = Column(String(50), nullable=False)
    