from decimal import Decimal

from OrderFlow.masters.model.entities.ProductEntity import ProductEntity
from OrderFlow.masters.model.dtos.ProductDTO import ProductDTO

class ProductMapper:

    @staticmethod
    def toDTO(entity: ProductEntity) -> ProductDTO:

        if entity is None:
            return None

        return ProductDTO(
            internalCode=entity.codigoInterno,
            sku=entity.sku,
            barcode=entity.codigoBarras,
            description=entity.descripcion,
            unitMeasurements=entity.medidasUnidad,
            weight=entity.peso,
            dimensions=entity.dimensiones,
            minimumStock=Decimal(str(entity.stockMinimo)),
            maximumStock=Decimal(str(entity.stockMaximo)),
            reorderPoint=Decimal(str(entity.puntoReorden)),
            productCategoriesId=entity.productoCategoriasId,
            providerTaxId=entity.proveedorCuit
        )

    @staticmethod
    def toEntity(dto: ProductDTO) -> ProductEntity:
        
        if dto is None:
            return None

        return ProductEntity(
            codigoInterno=dto.internalCode,
            sku=dto.sku,
            codigoBarras=dto.barcode,
            descripcion=dto.description,
            medidasUnidad=dto.unitMeasurements,
            peso=dto.weight,
            dimensiones=dto.dimensions,
            stockMinimo=float(dto.minimumStock) if dto.minimumStock is not None else 0.0,
            stockMaximo=float(dto.maximumStock) if dto.maximumStock is not None else 0.0,
            puntoReorden=float(dto.reorderPoint) if dto.reorderPoint is not None else 0.0,
            productoCategoriasId=dto.productCategoriesId,
            proveedorCuit=dto.providerTaxId
        )

    @staticmethod
    def toListDTO(products: list[ProductEntity]) -> list[ProductDTO]:

        if not products:
            return []
        
        return [ProductMapper.toDTO(product) for product in products]