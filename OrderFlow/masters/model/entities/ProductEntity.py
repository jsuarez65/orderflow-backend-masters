from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class ProductEntity(Base):

    __tablename__ = "productos"
    __table_args__ = {"extend_existing": True}

    codigoInterno = Column("codigo_interno", String(50), primary_key=True)
    sku = Column("sku", String(50), nullable=True)
    codigoBarras = Column("codigo_barras", String(50), nullable=True)
    descripcion = Column("descripcion", String(255), nullable=True)
    medidasUnidad = Column("medidas_unidad", String(50), nullable=True)
    peso = Column("peso", Float, nullable=True)
    dimensiones = Column("dimensiones", String(50), nullable=True)
    stockMinimo = Column("stock_minimo", Float, nullable=True)
    stockMaximo = Column("stock_maximo", Float, nullable=True)
    puntoReorden = Column("punto_reorden", Float, nullable=True)

    productoCategoriasId = Column(
        "producto_categorias_id",
        Integer,
        ForeignKey("producto_categorias.id"),
        nullable=True
    )

    proveedorCuit = Column(
        "proveedores_cuit",
        String(50),
        ForeignKey("proveedores.cuit"),
        nullable=True
    )

    #productoCategoria = relationship("ProductCategoryEntity")
    #relationshipproveedor = relationship("ProviderEntity")