from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class RolRepository:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def _getConnection(self):
        return DatabaseConfiguration.getConnection()

    def insertRol(self, rol):
        sqlCommand = None
        try:
            db = self._getConnection()
            sqlCommand = db.cursor()

            # Todo en el mismo cursor, sin llamar a otros métodos
            sqlCommand.execute("SELECT * FROM rol WHERE rol = %s", (rol['rol'],))
            if sqlCommand.fetchone():
                self.log.warning("insertRol - El rol ya existe: ", body=rol)
                return False
            
            sqlCommand.execute("INSERT INTO rol (rol) VALUES (%s)", (rol['rol'],))
            db.commit()
            return True

        except Exception as ex:
            try:
                db.rollback()
            except:
                pass
            self.log.error(f"insertRol - Error al crear rol: {str(ex)}")
            return False

        finally:
            if sqlCommand:
                sqlCommand.close()
                
    def findByName(self, rol):
        sqlCommand = None
        try:
            db = self._getConnection()
            sqlCommand = db.cursor()
            sqlCommand.execute("SELECT * FROM rol WHERE rol = %s", (rol,))
            return sqlCommand.fetchone()
        
        except Exception as ex:
            self.log.error(f"findByName - Error al buscar rol: {str(ex)}")
            return None
        
        finally:
            if sqlCommand:
                sqlCommand.close()

    def updateRol(self, rolActual, rolNuevo):
        sqlCommand = None
        try:
            db = self._getConnection()
            sqlCommand = db.cursor()

            sqlCommand.execute("SELECT * FROM rol WHERE rol = %s", (rolActual,))
            if not sqlCommand.fetchone():
                self.log.warning(f"updateRol - El rol '{rolActual}' no existe")
                return False

            sqlCommand.execute("SELECT * FROM rol WHERE rol = %s", (rolNuevo,))
            if sqlCommand.fetchone():
                self.log.warning(f"updateRol - El rol '{rolNuevo}' ya existe")
                return False

            sqlCommand.execute("UPDATE rol SET rol = %s WHERE rol = %s", (rolNuevo, rolActual))
            db.commit()
            return True
        
        except Exception as ex:
            try:
                db.rollback()
            except:
                pass
            self.log.error(f"updateRol - Error al actualizar rol: {str(ex)}")
            return False
        
        finally:
            if sqlCommand:
                sqlCommand.close()

    def delete(self, rol):
        sqlCommand = None
        try:
            db = self._getConnection()
            sqlCommand = db.cursor()
            sqlCommand.execute("DELETE FROM rol WHERE rol = %s", (rol,))
            db.commit()
            return sqlCommand.rowcount > 0
        
        except Exception as ex:
            try:
                db.rollback()
            except:
                pass
            self.log.error(f"delete - Error al eliminar rol: {str(ex)}")
            return False
        
        finally:
            if sqlCommand:
                sqlCommand.close()