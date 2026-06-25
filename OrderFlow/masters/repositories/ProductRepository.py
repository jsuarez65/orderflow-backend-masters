
from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class ProductRepository:

    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def save(self, product):
                
        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()

            productFound = self.findById(product['codigo_interno'])

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

    def findById(self, codigoInterno):

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

    def _insert(self, sqlCommand, product):
        
        sqlCommand.execute("""
            INSERT INTO Productos (codigo_interno, sku, codigo_barras, descripcion, 
            stock_minimo, stock_maximo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            product['codigo_interno'],
            product['sku'],
            product['codigo_barras'],
            product['descripcion'],
            product['stock_minimo'],
            product['stock_maximo']
        ))

        return product

    def _update(self, sqlCommand, product):
        
        sqlCommand.execute("""
            UPDATE Productos SET sku=%s, codigo_barras=%s, descripcion=%s, 
            stock_minimo=%s, stock_maximo=%s
            WHERE codigo_interno=%s""", (
                product['sku'],
                product['codigo_barras'],
                product['descripcion'],
                product['stock_minimo'],
                product['stock_maximo'],
                product['codigo_interno']
            ))

        return product