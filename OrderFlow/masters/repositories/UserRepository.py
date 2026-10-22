from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.UserEntity import UserEntity
from model.dto.userDTO import UserDTO
from mappers.UsersMappers import UserMapper


class UserRepository:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger() # el logger debe inyectarse


    def save(self, user: UserDTO) -> tuple[UserDTO | None, str | None, int]:

        #  El repositorio solo debe encargarse de las tareas de persistencia, y en el caso
        # del save puede devolver la entidad persistida, pero no debe controlar si el usuario existe,
        # si hay datos invalidos, etc, todo eso es tarea del service que es quien debe manejar la logica de
        # negocio. 


        session = SessionLocal() # la sesion debe inyectarse desde el service
        try:
            entity = UserMapper.toEntity(user)
            if not entity or not entity.username:
                # Esto es parte del service no del repositorio
                return None, "Datos inválidos: el username está vacío.", 400

            existing = session.query(UserEntity).filter(
                UserEntity.username == entity.username
            ).first()

            if existing:
                # Esto es parte del service no del repositorio
                self.log.warning(f"save - El usuario '{entity.username}' ya existe.")
                return None, f"El usuario '{entity.username}' ya existe.", 409

            session.add(entity)
            session.commit()  # el commit lo debe hacer el servicio, al igual que el rollback
            return UserMapper.toDTO(entity), None, 201

        except Exception as ex:
            session.rollback()  #las excepcionjes manejarlas ddesde el service
            self.log.error(f"save - Error guardando usuario: {str(ex)}")
            return None, f"Error guardando usuario: {str(ex)}", 500
        finally:
            session.close() # la sesion no se cierra, eso lo maneja el controller quien es el que arranca la transaccion

    def findByUsername(self, username: str) -> tuple[UserDTO | None, str | None, int]:

        session = SessionLocal() # la sesion se inyecta desde el service

        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == username
            ).first()

            if not entity:
                # que logica se sigue si no se encuentra se define en el service, tener en cuenta que la descripcion de un 
                # mensaje de error es logica de negocio, no del repositorio, el repositorio solo debe devolver None si no encuentra la entidad
                self.log.warning(f"findByUsername - Usuario '{username}' no encontrado.")
                return None, f"El usuario '{username}' no fue encontrado.", 404

            return UserMapper.toDTO(entity), None, 200

        except Exception as ex:
            self.log.error(f"findByUsername - Error: {str(ex)}")  # No catchear excepciones, dejar que las mismas se propaguen
            # y el service las tome y determine la logica a seguir
            return None, f"Error buscando usuario: {str(ex)}", 500
        finally:
            session.close() # la sesion no se cierra, eso lo maneja el controller quien es el que arranca la transaccion


    def getAll(self) -> tuple[list[UserDTO], str | None, int]:

        session = SessionLocal()
        try:
            entities = session.query(UserEntity).all()
            return UserMapper.toListDTO(entities), None, 200

        except Exception as ex:
            self.log.error(f"getAll - Error: {str(ex)}")
            return [], f"Error obteniendo usuarios: {str(ex)}", 500
        finally:
            session.close()


    def update(self, usernameActual: str, user: UserDTO) -> tuple[UserDTO | None, str | None, int]:
        
        session = SessionLocal()
        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == usernameActual
            ).first()

            if not entity:
                self.log.warning(f"update - Usuario '{usernameActual}' no encontrado.")
                return None, f"El usuario '{usernameActual}' no fue encontrado.", 404

            if user.username and user.username != usernameActual:
                duplicate = session.query(UserEntity).filter(
                    UserEntity.username == user.username
                ).first()
                if duplicate:
                    self.log.warning(f"update - El username '{user.username}' ya existe.")
                    return None, f"El username '{user.username}' ya está en uso.", 409
                entity.username = user.username

            if user.password:
                entity.password = user.password
            if user.rol:
                entity.rol = user.rol

            session.commit()
            return UserMapper.toDTO(entity), None, 200

        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return None, f"Error actualizando usuario: {str(ex)}", 500
        finally:
            session.close()


    def delete(self, username: str) -> tuple[UserDTO | None, str | None, int]:

        session = SessionLocal()
        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == username
            ).first()

            if not entity:
                self.log.warning(f"delete - Usuario '{username}' no encontrado.")
                return None, f"El usuario '{username}' no fue encontrado.", 404

            dto = UserMapper.toDTO(entity)
            session.delete(entity)
            session.commit()
            return dto, None, 200

        except Exception as ex:
            session.rollback()
            self.log.error(f"delete - Error: {str(ex)}")
            return None, f"Error eliminando usuario: {str(ex)}", 500
        finally:
            session.close()