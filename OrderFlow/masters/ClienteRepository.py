from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

# CORRECCIÓN: Nombre de clase correcto para este archivo
class ClienteRepository:

    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    # 1. POST -> INSERT (El original del profe corregido)
    def insertClient(self, client):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("""
                INSERT INTO cliente (cuit, razon_social, telefono, email)
                VALUES (%s, %s, %s, %s)
            """, (
                client['cuit'],
                client['razon_social'],
                client['telefono'],
                client['email']
            ))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"createClient - Error al crear cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    # 2. GET -> SELECT ALL (Trae todos los clientes)
    def getAllClients(self):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()
            
            # Buscamos los campos reales de tu tabla. Incluyo el 'id' que seguro maneja la tabla.
            sqlCommand.execute("SELECT id, cuit, razon_social, telefono, email FROM cliente")
            
            resultados = sqlCommand.fetchall()
            return resultados

        except Exception as ex:
            self.log.error(f"getAllClients - Error al obtener clientes: {str(ex)}")
            return None

        finally:
            if sqlCommand:
                sqlCommand.close()

    # 3. PUT -> UPDATE (Actualiza los datos usando el id del cliente)
    def updateClient(self, client):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("""
                UPDATE cliente 
                SET cuit = %s, razon_social = %s, telefono = %s, email = %s
                WHERE id = %s
            """, (
                client['cuit'],
                client['razon_social'],
                client['telefono'],
                client['email'],
                client['id'] # Necesitamos el ID para saber a quién actualizar
            ))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"updateClient - Error al actualizar cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    # 4. DELETE -> DELETE (Borra al cliente usando su id)
    def deleteClient(self, id_client):
        sqlCommand = None
        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("DELETE FROM cliente WHERE id = %s", (id_client,))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            self.log.error(f"deleteClient - Error al eliminar cliente: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()