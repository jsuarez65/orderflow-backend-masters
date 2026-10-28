from sqlalchemy import Column, String
from configuration.DatabaseConfiguration import Base

class CustomerEntity(Base):

    __tablename__ = 'clientes'
    __table_args__ = {'extend_existing': True}

    cuit = Column(String(50), primary_key=True)
    razonSocial = Column('razon_social', String(255), nullable=False) 
    telefono = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)