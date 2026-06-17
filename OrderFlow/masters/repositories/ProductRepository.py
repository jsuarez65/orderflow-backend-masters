
from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class ProductRepository:

    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def insertProduct(self, product):
        
        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()

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

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()

            self.log.error(f"createProduct - Error al crear producto: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()