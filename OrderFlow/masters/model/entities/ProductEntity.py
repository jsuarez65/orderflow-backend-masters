from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class ProductEntity(Base):

    __tablename__ = 'productos'

    codigoInterno = Column(String(50), primary_key=True)
    sku = Column(String(50), nullable=False)
    codigoBarras = Column(String(50), nullable=True)
    descripcion = Column(String(255), nullable=False)
    medidasUnidad = Column(String(50), nullable=True)
    peso = Column(Float, nullable=False)
    dimensiones = Column(String(50), nullable=True)
    stockMinimo = Column(Float, nullable=False)
    stockMaximo = Column(Float, nullable=False)
    puntoReorden = Column(Float, nullable=False)

    productoCategoriasId = Column(
        Integer,
        ForeignKey("producto_categorias.id"),
        nullable=False
    )

    proveedorCuit = Column(
        String(50),
        ForeignKey("proveedores.cuit"),
        nullable=False
    )

    productoCategoria = relationship("ProductCategoryEntity")
    proveedor = relationship("ProviderEntity")
