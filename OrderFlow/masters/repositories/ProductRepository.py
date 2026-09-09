
from model.dtos import ProductDTO
from model.entities import ProductEntity


class ProductRepository:

    def __init__(self, log, session):
        self.session = session
        self.log = log

    def findAll(self) -> list[ProductEntity]:

        try:
            return self.session.query(ProductEntity).all()
        
        except Exception as ex:
            self.log.error(f"findAll - Error al recuperar productos: {str(ex)}")
            return []

    def save(self, product: ProductEntity) -> ProductEntity | None:

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

    def existsById(self, internalCode: str) -> bool:
        return self._findByInternalCode(internalCode) is not None

    def _findByInternalCode(self, internalCode: str) -> ProductEntity | None:

        try:
            return (
                self.session.query(ProductEntity)
                .filter(ProductEntity.codigoInterno == internalCode)
                .first()
            )

        except Exception as ex:
            self.log.error(
                f"_findByInternalCode - Error al buscar producto: {str(ex)}"
            )
            return None

    def _insert(self, product: ProductEntity) -> ProductEntity:

        self.session.add(product)
        self.session.commit()

        return product

    def _update(self, entityToUpdate: ProductEntity, entity: ProductEntity) -> ProductEntity:

        entityToUpdate.sku = entity.sku
        entityToUpdate.codigoBarras = entity.barcode
        entityToUpdate.descripcion = entity.description
        entityToUpdate.stockMinimo = entity.minimumStock
        entityToUpdate.stockMaximo = entity.maximumStock

        self.session.commit()

        return entityToUpdate