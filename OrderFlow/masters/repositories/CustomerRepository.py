from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class CustomerRepository:

    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def insertCustomer(self, Customer):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("""
                INSERT INTO clientes (cuit, razon_social, telefono, email)
                VALUES (%s, %s, %s, %s)
            """, (
                Customer.cuit,
                Customer.razon_social,
                Customer.telefono,
                Customer.email
            ))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"createCustomer - Error al crear cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    def getAllCustomers(self):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()
            
            sqlCommand.execute("SELECT cuit, razon_social, telefono, email FROM clientes")
            
            resultados = sqlCommand.fetchall()
            
            # Lo convertimos a una lista de diccionarios para que Flask lo pueda mandar como JSON
            clientes_lista = []
            for row in resultados:
                clientes_lista.append({
                    "cuit": row[0],
                    "razon_social": row[1],
                    "telefono": row[2],
                    "email": row[3]
                })
            
            return clientes_lista

        except Exception as ex:
            self.log.error(f"getAllCustomers - Error al obtener clientes: {str(ex)}")
            return None

        finally:
            if sqlCommand:
                sqlCommand.close()

    def updateCustomer(self, Customer):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("""
                UPDATE clientes 
                SET razon_social = %s, telefono = %s, email = %s
                WHERE cuit = %s
            """, (
                Customer.razon_social,
                Customer.telefono,
                Customer.email,
                Customer.cuit # Necesitamos el CUIT para saber a quién actualizar
            ))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"updateCustomer - Error al actualizar cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    def deleteCustomer(self, idCustomer):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("DELETE FROM clientes WHERE cuit = %s", (idCustomer,))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"deleteCustomer - Error al eliminar cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()