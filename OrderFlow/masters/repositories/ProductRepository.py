
from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration
from model.dtos import ProductDTO


class ProductRepository:

    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def save(self, product : ProductDTO) -> ProductDTO | None:
                
        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()

            productFound = self.existsById(product.internalCode)

            if productFound:
                self.log.warning("save - El producto ya existe, se procederá a actualizarlo: ", body=product)
                productFound = self._update(sqlCommand, product)
            else:
                productFound = self._insert(sqlCommand, product)

            self.db.commit()
            return productFound

        except Exception as ex:
            self.db.rollback()

            self.log.error(f"createProduct - Error al crear producto: {str(ex)}")
            return None

        finally:
            if sqlCommand:
                sqlCommand.close()

    def existsById(self, codigoInterno : str) -> bool:

        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()
            sqlCommand.execute("SELECT * FROM Productos WHERE codigo_interno = %s", (codigoInterno,))
            result = sqlCommand.fetchone()
            return result is not None

        except Exception as ex:
            self.log.error(f"findById - Error al buscar producto por ID: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    def _insert(self, sqlCommand, product : ProductDTO) -> ProductDTO | None:
        
        sqlCommand.execute("""
            INSERT INTO Productos (codigo_interno, sku, codigo_barras, descripcion, 
            stock_minimo, stock_maximo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            product.internalCode,
            product.sku,
            product.barcode,
            product.description,
            product.minimumStock,
            product.maximumStock
        ))

        return product

    def _update(self, sqlCommand, product : ProductDTO) -> ProductDTO | None:
        
        sqlCommand.execute("""
            UPDATE Productos SET sku=%s, codigo_barras=%s, descripcion=%s, 
            stock_minimo=%s, stock_maximo=%s
            WHERE codigo_interno=%s""", (
                product.sku,
                product.barcode,
                product.description,
                product.minimumStock,
                product.maximumStock,
                product.internalCode
            ))

        return product