from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration
from model.dto import rolDTO

class RolRepository:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def _getConnection(self):
        return DatabaseConfiguration.getConnection()
    
    def save(self, rol : rolDTO) -> rolDTO | None:
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("SELECT 1 FROM rol WHERE rol = %s", (rol.rol,))
            if cur.fetchone():
                self.log.warning("save - El rol ya existe: ", body=rol)
                return False
            
            cur.execute("INSERT INTO rol (rol) VALUES (%s)", (rol.rol,))
            db.commit()
            return True

        except Exception as ex:
            db.rollback()
            self.log.error(f"save - Error al crear rol: {str(ex)}")
            return False

        finally:
            cur.close()

    def insertRol(self, rol : rolDTO) -> rolDTO | None:
        sqlCommand = None
        try:
            db = self._getConnection()
            sqlCommand = db.cursor()

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
                
    def existById(self, rol : str) -> bool:
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

    def updateRol(self, rolActual, rolNuevo : rolDTO) -> rolDTO | None:
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

    def delete(self, rol : rolDTO) -> rolDTO | None:
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