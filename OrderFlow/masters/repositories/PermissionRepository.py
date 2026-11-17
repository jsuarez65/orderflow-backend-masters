from model.entities.PermissionEntity import PermissionEntity



class PermissionRepository:

    def __init__(self, log, session):
        self.session = session
        self.log = log

    def findAll(self) -> list[PermissionEntity]:
        return self.session.query(PermissionEntity).all()

    def save(self, permission: PermissionEntity) -> PermissionEntity:
        permissionFound = self._findByPermission(permission.permiso)

        if permissionFound:
            self.log.warning(
                f"save - El permiso ya existe, se procederá a actualizarlo: {permission}"
            )
            return self._update(permissionFound, permission)

        return self._insert(permission)

    def existsById(self, permission: str) -> bool:
        return self._findByPermission(permission) is not None

    def _findByPermission(self, permission: str) -> PermissionEntity | None:
        return (
            self.session.query(PermissionEntity)
            .filter(PermissionEntity.permission == permission)
            .first()
        )


    def _insert(self, permission: PermissionEntity) -> PermissionEntity:
        self.session.add(permission)
        return permission

    def _update(self, entityToUpdate: PermissionEntity, entity: PermissionEntity) -> PermissionEntity:
        entityToUpdate.nombre = entity.nombre
        entityToUpdate.descripcion = entity.descripcion

        return entityToUpdate