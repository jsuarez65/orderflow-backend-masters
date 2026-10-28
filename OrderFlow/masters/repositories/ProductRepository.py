
from model.entities import ProductEntity


class ProductRepository:

    def __init__(self, log, session):
        self.session = session
        self.log = log

    def findAll(self) -> list[ProductEntity]:
        return self.session.query(ProductEntity).all()

    def save(self, product: ProductEntity) -> ProductEntity:
        productFound = self._findByInternalCode(product.codigoInterno)

        if productFound:
            self.log.warning(
                f"save - El producto ya existe, se procederá a actualizarlo: {product}"
            )
            return self._update(productFound, product)

        return self._insert(product)

    def existsById(self, internalCode: str) -> bool:
        return self._findByInternalCode(internalCode) is not None

    def _findByInternalCode(self, internalCode: str) -> ProductEntity | None:
        return (
            self.session.query(ProductEntity)
            .filter(ProductEntity.codigoInterno == internalCode)
            .first()
        )


    def _insert(self, product: ProductEntity) -> ProductEntity:
        self.session.add(product)
        return product

    def _update(self, entityToUpdate: ProductEntity, entity: ProductEntity) -> ProductEntity:
        entityToUpdate.sku = entity.sku
        entityToUpdate.codigoBarras = entity.barcode
        entityToUpdate.descripcion = entity.description
        entityToUpdate.stockMinimo = entity.minimumStock
        entityToUpdate.stockMaximo = entity.maximumStock

        return entityToUpdate