
import DatabaseConfiguration
import LogConfiguration

class ProviderRepository:
    def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

    def insertProvider(provider):

        sqlCommand = None

        try:
            sqlCommand = self.db.cursor()

            sqlCommand.execute("""INSERT INTO provider (cuil, razon_social,
             domicilio, email, telefono, localidad_codigo_postal, provincia_nombre)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                provider['cuil'],
                provider['razon_social'],
                provider['domicilio'],
                provider['email'],
                provider['telefono'],
                provider['localidad_codigo_postal'],
                provider['provincia_nombre']
            ))

            self.db.commit()
            return True

        except Exception as ex:
            self.db.rollback()
            
            self.log.error(f"createProvider: - Eror al insertar el proveedor: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()   