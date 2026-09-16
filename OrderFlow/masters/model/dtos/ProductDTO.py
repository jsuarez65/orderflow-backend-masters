from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ProductDTO:
    internalCode: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    unitMeasurements: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    minimumStock: Optional[Decimal] = None
    maximumStock: Optional[Decimal] = None
    reorderPoint: Optional[Decimal] = None
    productCategoriesId: Optional[int] = None
    providerTaxId: Optional[str] = None