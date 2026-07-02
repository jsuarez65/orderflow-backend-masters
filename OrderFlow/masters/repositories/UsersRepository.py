from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class UsersRepository:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def _getConnection(self):
        return DatabaseConfiguration.getConnection()

    def insertUser(self, user):
        db = self._getConnection()
        cur = db.cursor()
        try:
            
            cur.execute("SELECT 1 FROM usuarios WHERE username = %s", (user['username'],))
            if cur.fetchone():
                self.log.warning("insertUser - El usuario ya existe: ", body=user)
                return False
            
            cur.execute("INSERT INTO usuarios (username, password, rol) VALUES (%s, %s, %s)", 
                        (user['username'], user['password'], user['rol']))
            db.commit()
            return True

        except Exception as ex:
            db.rollback()
            self.log.error(f"insertUser - Error al crear usuario: {str(ex)}")
            return False

        finally:
            cur.close()
                
    def findByUsername(self, username):
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            return cur.fetchone()
        
        except Exception as ex:
            self.log.error(f"findByUsername - Error al buscar usuario: {str(ex)}")
            return None
        
        finally:
            cur.close()

    def updateUser(self, usernameActual, userData):
        db = self._getConnection()
        cur = db.cursor()
        try:
            
            cur.execute("SELECT 1 FROM usuarios WHERE username = %s", (usernameActual,))
            if not cur.fetchone():
                self.log.warning(f"updateUser - El usuario '{usernameActual}' no existe")
                return False

            if usernameActual != userData['username']:
                cur.execute("SELECT 1 FROM usuarios WHERE username = %s", (userData['username'],))
                if cur.fetchone():
                    self.log.warning(f"updateUser - El nuevo nombre de usuario '{userData['username']}' ya existe")
                    return False


            cur.execute("""
                UPDATE usuarios 
                SET username = %s, password = %s, rol = %s 
                WHERE username = %s
            """, (userData['username'], userData['password'], userData['rol'], usernameActual))
            
            db.commit()
            return True
        
        except Exception as ex:
            db.rollback()
            self.log.error(f"updateUser - Error al actualizar usuario: {str(ex)}")
            return False
        
        finally:
            cur.close()

    def deleteUser(self, username):
        db = self._getConnection()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM usuarios WHERE username = %s", (username,))
            db.commit()
            return cur.rowcount > 0
        
        except Exception as ex:
            db.rollback()
            self.log.error(f"deleteUser - Error al eliminar usuario: {str(ex)}")
            return False
        
        finally:
            cur.close()