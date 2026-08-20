
from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration


class ProviderRepository:
   
    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def save(self, provider):
        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()

            providerFound = self.findById(provider['cuit'])

            if providerFound:
                self.log.warning("save - El proveedor ya existe, se procederá a actualizarlo: ", body=provider)
                providerFound = self._update(sqlCommand, provider)
            else:
                providerFound = self._insert(sqlCommand, provider)

            self.db.commit()
            return providerFound

        except Exception as ex:
            self.db.rollback()

            self.log.error(f"save - Error al guardar/actualizar proveedor: {str(ex)}")
            return None

        finally:
            if sqlCommand:
                sqlCommand.close()

    def findById(self, cuit):

        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()
            sqlCommand.execute("SELECT * FROM Proveedores WHERE cuit = %s", (cuit,))
            result = sqlCommand.fetchone()
            return result is not None

        except Exception as ex:
            self.log.error(f"findById - Error al buscar proveedor por CUIT: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()

    def _insert(self, sqlCommand, provider):
        
        sqlCommand.execute("""
            INSERT INTO Proveedores (cuit, razon_social, domicilio, email, telefono, localidad_codigo_postal, provincia_nombre)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            provider['cuit'],
            provider['razon_social'],
            provider['domicilio'],
            provider['email'],
            provider['telefono'],
            provider['localidad_codigo_postal'],
            provider['provincia_nombre']
        ))
        return provider

    def _update(self, sqlCommand, provider):
        
        sqlCommand.execute("""
            UPDATE Proveedores SET razon_social=%s, domicilio=%s, telefono=%s, email=%s
            WHERE cuit=%s""", (
                provider['cuit'],
                provider['razon_social'],
                provider['domicilio'],
                provider['email'],
                provider['telefono'],
                provider['localidad_codigo_postal'],
                provider['provincia_nombre'],
                
            ))
        return provider
           