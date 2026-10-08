from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.PermissionEntity import PermissionEntity
from model.dto.permissionDTO import PermissionDTO
from mappers.PermissionMappers import PermissionMapper


class PermissionRepository:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger()

    def save(self, permission: PermissionDTO) -> tuple[PermissionDTO | None, str | None]:

        session = SessionLocal()
        try:
            entity = PermissionMapper.toEntity(permission)
            if not entity:
                return None,

            existing = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == entity.nombre
            ).first()

            if existing:
                self.log.warning(f"save - El permiso '{entity.nombre}' ya existe.")
                return None, f"El permiso '{entity.nombre}' ya existe."

            session.add(entity)
            session.commit()
            return PermissionMapper.toDTO(entity), None

        except Exception as ex:
            session.rollback()
            self.log.error(f"save - Error guardando permiso: {str(ex)}")
            return None, f"Error guardando permiso: {str(ex)}"
        finally:
            session.close()

    def findByName(self, name: str) -> tuple[PermissionDTO | None, str | None]:

        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == name
            ).first()

            if not entity:
                self.log.warning(f"findByName - Permiso '{name}' no encontrado.")
                return None, f"El permiso '{name}' no fue encontrado."

            return PermissionMapper.toDTO(entity), None

        except Exception as ex:
            self.log.error(f"findByName - Error: {str(ex)}")
            return None, f"Error buscando permiso: {str(ex)}"
        finally:
            session.close()

    def getAllPermissions(self) -> tuple[list[PermissionDTO], str | None]:

        session = SessionLocal()
        try:
            entities = session.query(PermissionEntity).all()
            return PermissionMapper.toListDTO(entities), None

        except Exception as ex:
            self.log.error(f"getAllPermissions - Error: {str(ex)}")
            return [], f"Error obteniendo permisos: {str(ex)}"
        finally:
            session.close()

    def update(self, nombreActual: str, permission: PermissionDTO) -> tuple[PermissionDTO | None, str | None]:

        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == nombreActual
            ).first()

            if not entity:
                self.log.warning(f"update - Permiso '{nombreActual}' no encontrado.")
                return None, f"El permiso '{nombreActual}' no fue encontrado."

            if permission.descripcion is not None:
                entity.descripcion = permission.descripcion

            if permission.nombre and permission.nombre != nombreActual:
                duplicate = session.query(PermissionEntity).filter(
                    PermissionEntity.nombre == permission.nombre
                ).first()
                if duplicate:
                    self.log.warning(f"update - El nuevo nombre '{permission.nombre}' ya existe.")
                    return None, f"El nuevo nombre '{permission.nombre}' ya está en uso."
                entity.nombre = permission.nombre

            session.commit()
            return PermissionMapper.toDTO(entity), None

        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return None, f"Error actualizando permiso: {str(ex)}"
        finally:
            session.close()


    def delete(self, name: str) -> tuple[PermissionDTO | None, str | None]:

        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == name
            ).first()

            if not entity:
                self.log.warning(f"delete - Permiso '{name}' no encontrado.")
                return None, f"El permiso '{name}' no fue encontrado."

            dto = PermissionMapper.toDTO(entity)   # guardamos el DTO antes de borrar
            session.delete(entity)
            session.commit()
            return dto, None

        except Exception as ex:
            session.rollback()
            self.log.error(f"delete - Error: {str(ex)}")
            return None, f"Error eliminando permiso: {str(ex)}"
        finally:
            session.close()