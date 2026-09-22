from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.PermissionEntity import PermissionEntity
from model.dto import permissionDTO
from mappers.PermissionMappers import PermissionMapper


class PermissionRepository:

    def __init__(self, log=None, session=None):
        self.log = log or LogConfiguration.getLogger()

    def save(self, permission: permissionDTO) -> permissionDTO | None:
        session = SessionLocal()
        try:
            entity = PermissionMapper.toEntity(permission)
            session.merge(entity)
            session.commit()
            return PermissionMapper.toDTO(entity)
        except Exception as ex:
            session.rollback()
            self.log.error(f"save - Error guardando permiso: {str(ex)}")
            return None
        finally:
            session.close()

    def findByName(self, name: str) -> permissionDTO | None:
        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == name
            ).first()
            return PermissionMapper.toDTO(entity)
        except Exception as ex:
            self.log.error(f"findByName - Error: {str(ex)}")
            return None
        finally:
            session.close()

    def getAllPermissions(self) -> list[permissionDTO]:
        session = SessionLocal()
        try:
            entities = session.query(PermissionEntity).all()
            return PermissionMapper.toListDTO(entities)
        except Exception as ex:
            self.log.error(f"getAllPermissions - Error: {str(ex)}")
            return []
        finally:
            session.close()

    def update(self, nombreActual: str, permission: permissionDTO) -> bool:
        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == nombreActual
            ).first()
            if not entity:
                return False
            entity.descripcion = permission.descripcion
            if permission.nombre and permission.nombre != nombreActual:
                entity.nombre = permission.nombre
            session.commit()
            return True
        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return False
        finally:
            session.close()

    def deletePermission(self, name: str) -> bool:
        session = SessionLocal()
        try:
            entity = session.query(PermissionEntity).filter(
                PermissionEntity.nombre == name
            ).first()
            if entity:
                session.delete(entity)
                session.commit()
                return True
            return False
        except Exception as ex:
            session.rollback()
            self.log.error(f"deletePermission - Error: {str(ex)}")
            return False
        finally:
            session.close()