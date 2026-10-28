from sqlalchemy import Column, String, Integer, UniqueConstraint
from configuration.DatabaseConfiguration import Base

class CityEntity(Base):

    __tablename__ = 'localidades'
    __table_args__ = (
        UniqueConstraint('codigo_postal', 'nombre_localidad', name='uq_localidades_cp_nombre'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True)
    
    postalCode = Column('codigo_postal', String(50), nullable=False)
    cityName = Column('nombre_localidad', String(255), nullable=False)