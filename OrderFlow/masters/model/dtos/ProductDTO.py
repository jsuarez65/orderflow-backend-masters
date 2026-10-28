from decimal import Decimal
from pydantic import BaseModel


class ProductDTO(BaseModel):
    internalCode: str | None = None
    sku: str | None = None
    barcode: str | None = None
    description: str | None = None
    unitMeasurements: str | None = None
    weight: float | None = None
    dimensions: str | None = None
    minimumStock: Decimal | None = None
    maximumStock: Decimal | None = None
    reorderPoint: Decimal | None = None
    productCategoriesId: int | None = None
    providerTaxId: str | None = None

    @classmethod
    def of(cls, data: dict) -> "ProductDTO":
        return cls(
            internalCode=data.get("codigo_interno"),
            sku=data.get("sku"),
            barcode=data.get("codigo_barras"),
            description=data.get("descripcion"),
            unitMeasurements=data.get("medidas_unidad"),
            weight=data.get("peso"),
            dimensions=data.get("dimensiones"),
            minimumStock=data.get("stock_minimo"),
            maximumStock=data.get("stock_maximo"),
            reorderPoint=data.get("punto_reorden"),
            productCategoriesId=data.get("producto_categorias_id"),
            providerTaxId=data.get("proveedores_cuit")
        )