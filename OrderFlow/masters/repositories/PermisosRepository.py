from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class PermisosRepository:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def _getConnection(self):
        return DatabaseConfiguration.getConnection()

    def save(self, permiso):
        db = self._getConnection()
        cur = db.cursor()
        try:
            # Verificamos si existe (todo en el mismo cursor)
            cur.execute("SELECT 1 FROM permisos WHERE nombre = %s", (permiso['nombre'],))
            if cur.fetchone():
                self.log.warning("save - El permiso ya existe: ", body=permiso)
                return False
            
            cur.execute("INSERT INTO permisos (nombre, descripcion) VALUES (%s, %s)", 
                        (permiso['nombre'], permiso['descripcion']))
            db.commit()
            return True

        except Exception as ex:
            db.rollback()
            self.log.error(f"save - Error al crear permiso: {str(ex)}")
            return False

        finally:
            cur.close()
                
    def findByName(self, nombre):
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM permisos WHERE nombre = %s", (nombre,))
            return cur.fetchone()
        
        except Exception as ex:
            self.log.error(f"findByName - Error al buscar permiso: {str(ex)}")
            return None
        
        finally:
            cur.close()

    def update(self, nombreActual, permisoData):
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("SELECT 1 FROM permisos WHERE nombre = %s", (nombreActual,))
            if not cur.fetchone():
                self.log.warning(f"update - El permiso '{nombreActual}' no existe")
                return False

            if nombreActual != permisoData['nombre']:
                cur.execute("SELECT 1 FROM permisos WHERE nombre = %s", (permisoData['nombre'],))
                if cur.fetchone():
                    self.log.warning(f"update - El permiso '{permisoData['nombre']}' ya existe")
                    return False

            cur.execute("""
                UPDATE permisos 
                SET nombre = %s, descripcion = %s 
                WHERE nombre = %s
            """, (permisoData['nombre'], permisoData['descripcion'], nombreActual))
            
            db.commit()
            return True
        
        except Exception as ex:
            db.rollback()
            self.log.error(f"update - Error al actualizar permiso: {str(ex)}")
            return False
        
        finally:
            cur.close()

    def delete(self, nombre):
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM permisos WHERE nombre = %s", (nombre,))
            db.commit()
            return cur.rowcount > 0
        
        except Exception as ex:
            db.rollback()
            self.log.error(f"delete - Error al eliminar permiso: {str(ex)}")
            return False
        
        finally:
            cur.close()