
from model.dtos import ProductDTO
from model.entities import ProductEntity


class ProductRepository:

    def __init__(self, log, session):
        self.session = session
        self.log = log

    def save(self, product: ProductDTO) -> ProductDTO | None:

        try:
            productFound = self.findByInternalCode(product.internalCode)

            if productFound:
                self.log.warning(
                    f"save - El producto ya existe, se procederá a actualizarlo: {product}"
                )
                return self._update(productFound, product)

            return self._insert(product)

        except Exception as ex:
            self.log.error(f"save - Error al guardar producto: {str(ex)}")
            self.session.rollback()
            return None

    def findByInternalCode(self, internalCode: str) -> ProductEntity | None:

        try:
            return (
                self.session.query(ProductEntity)
                .filter(ProductEntity.codigoInterno == internalCode)
                .first()
            )

        except Exception as ex:
            self.log.error(
                f"findByInternalCode - Error al buscar producto: {str(ex)}"
            )
            return None

    def existsById(self, internalCode: str) -> bool:
        return self.findByInternalCode(internalCode) is not None

    def _insert(self, product: ProductDTO) -> None:

        productEntity = ProductEntity(
            codigoInterno=product.internalCode,
            sku=product.sku,
            codigoBarras=product.barcode,
            descripcion=product.description,
            stockMinimo=product.minimumStock,
            stockMaximo=product.maximumStock
        )

        self.session.add(productEntity)
        self.session.commit()

        return None

    def _update(self, entity: ProductEntity, dto: ProductDTO) -> None:

        entity.sku = dto.sku
        entity.codigoBarras = dto.barcode
        entity.descripcion = dto.description
        entity.stockMinimo = dto.minimumStock
        entity.stockMaximo = dto.maximumStock

        self.session.commit()

        return entity