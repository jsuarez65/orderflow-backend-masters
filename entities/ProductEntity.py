from sqlalchemy import Column, Integer, String, Float
from  sqlalchemy import declarativeBase

class ProductEntity(base):
    __tablename__ = 'productos'

    codigoInterno = Column (String(50), primary_key=True)
    sku = Column