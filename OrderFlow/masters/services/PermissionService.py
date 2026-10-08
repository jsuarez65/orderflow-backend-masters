from repositories.PermissionRepository import PermissionRepository
from configuration.LogConfiguration import LogConfiguration
from model.dto.permissionDTO import PermissionDTO


class PermissionService:

    def __init__(self, log=None,):
        self.log = log or LogConfiguration.getLogger()
        self.permissionRepository = PermissionRepository(self.log)

    def createPermission(self, permission: PermissionDTO) -> tuple[PermissionDTO | None, str | None]:
        if permission is None:
            return None, "DTO nulo recibido."
        self.log.info(f"createPermission - Ingresa con permission: {permission.nombre}")
        return self.permissionRepository.save(permission)

    def getPermission(self, nombre: str) -> tuple[PermissionDTO | None, str | None]:
        self.log.info(f"getPermission - Ingresa con nombre: {nombre}")
        return self.permissionRepository.findByName(nombre)

    def getAllPermissions(self) -> tuple[list[PermissionDTO], str | None]:
        self.log.info("getAllPermissions - Obteniendo todos los permisos")
        return self.permissionRepository.getAllPermissions()

    def updatePermission(self, nombreActual: str, permission: PermissionDTO) -> tuple[PermissionDTO | None, str | None]:
        if permission is None:
            return None, "DTO nulo recibido."
        self.log.info(f"updatePermission - Actualizar permiso '{nombreActual}'")
        return self.permissionRepository.update(nombreActual, permission)

    def deletePermission(self, nombre: str) -> tuple[PermissionDTO | None, str | None]:
        self.log.info(f"deletePermission - Eliminar permiso: {nombre}")
        return self.permissionRepository.delete(nombre)