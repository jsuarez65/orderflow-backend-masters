from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class CityEntity(Base):

    __tablename__ = 'localidades'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    provinciaId = Column(
        Integer,
        ForeignKey("provincias.id"),
        nullable=False
    )

    #provincia = relationship("ProvinceEntity")