from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.RolEntity import RolEntity
from model.entities.UserEntity import UserEntity
from model.dto.rolDTO import RolDTO
from mappers.RolMappers import RolMapper


class RolRepository:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger()


    def save(self, rol: RolDTO) -> tuple[RolDTO | None, str | None, int]:

        session = SessionLocal()
        try:
            entity = RolMapper.toEntity(rol)
            if not entity or not entity.rol:
                return None, "Datos inválidos: el rol está vacío.", 400

            existing = session.query(RolEntity).filter(
                RolEntity.rol == entity.rol
            ).first()

            if existing:
                self.log.warning(f"save - El rol '{entity.rol}' ya existe.")
                return None, f"El rol '{entity.rol}' ya existe.", 409

            session.add(entity)
            session.commit()
            return RolMapper.toDTO(entity), None, 201

        except Exception as ex:
            session.rollback()
            self.log.error(f"save - Error guardando rol: {str(ex)}")
            return None, f"Error guardando rol: {str(ex)}", 500
        finally:
            session.close()


    def findByName(self, rol: str) -> tuple[RolDTO | None, str | None, int]:

        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(RolEntity.rol == rol).first()
            if not entity:
                self.log.warning(f"findByName - Rol '{rol}' no encontrado.")
                return None, f"El rol '{rol}' no fue encontrado.", 404

            return RolMapper.toDTO(entity), None, 200

        except Exception as ex:
            self.log.error(f"findByName - Error: {str(ex)}")
            return None, f"Error buscando rol: {str(ex)}", 500
        finally:
            session.close()


    def getAll(self) -> tuple[list[RolDTO], str | None, int]:

        session = SessionLocal()
        try:
            entities = session.query(RolEntity).all()
            return RolMapper.toListDTO(entities), None, 200

        except Exception as ex:
            self.log.error(f"getAll - Error: {str(ex)}")
            return [], f"Error obteniendo roles: {str(ex)}", 500
        finally:
            session.close()

    def update(self, rolActual: str, rolNuevo: RolDTO) -> tuple[RolDTO | None, str | None, int]:
        
        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(
                RolEntity.rol == rolActual
            ).first()

            if not entity:
                self.log.warning(f"update - Rol '{rolActual}' no encontrado.")
                return None, f"El rol '{rolActual}' no fue encontrado.", 404

            if rolNuevo.rol and rolNuevo.rol != rolActual:
                duplicate = session.query(RolEntity).filter(
                    RolEntity.rol == rolNuevo.rol
                ).first()
                if duplicate:
                    self.log.warning(f"update - El nuevo nombre '{rolNuevo.rol}' ya existe.")
                    return None, f"El nuevo nombre '{rolNuevo.rol}' ya está en uso.", 409
                entity.rol = rolNuevo.rol

            session.commit()
            return RolMapper.toDTO(entity), None, 200

        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return None, f"Error actualizando rol: {str(ex)}", 500
        finally:
            session.close()


    def delete(self, rol: str) -> tuple[RolDTO | None, str | None, int]:

        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(RolEntity.rol == rol).first()
            if not entity:
                self.log.warning(f"delete - Rol '{rol}' no encontrado.")
                return None, f"El rol '{rol}' no fue encontrado.", 404

            user_in_use = session.query(UserEntity).filter(UserEntity.rol == rol).first()
            if user_in_use:
                self.log.warning(f"delete - El rol '{rol}' está en uso.")
                return None, f"No se puede eliminar el rol '{rol}' porque está asignado a usuarios.", 409

            dto = RolMapper.toDTO(entity)
            session.delete(entity)
            session.commit()
            return dto, None, 200

        except Exception as ex:
            session.rollback()
            self.log.error(f"delete - Error: {str(ex)}")
            return None, f"Error eliminando rol: {str(ex)}", 500
        finally:
            session.close()