from sqlalchemy import Column, String
from configuration.DatabaseConfiguration import Base

class CustomerEntity(Base):

    __tablename__ = 'clientes'
    __table_args__ = {'extend_existing': True}

    cuit = Column(String(50), primary_key=True)
    # Aca le decimos: "Mi variable de Python es razonSocial, pero en la DB buscá 'razon_social'"
    razonSocial = Column('razon_social', String(255), nullable=False) 
    telefono = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)