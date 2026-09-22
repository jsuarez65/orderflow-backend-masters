from repositories.PermissionRepository import PermissionRepository
from configuration.LogConfiguration import LogConfiguration
from model.dto import permissionDTO


class PermissionService:

    def __init__(self, log=None, session=None):
        self.log = log or LogConfiguration.getLogger()
        self.permissionRepository = PermissionRepository(self.log, session)

    def createPermission(self, permiso: permissionDTO) -> bool:
        self.log.info("createPermission - Ingresa con permission: ", body=permiso)
        return self.permissionRepository.save(permiso) is not None

    def getPermission(self, nombre: str) -> permissionDTO | None:
        self.log.info("getPermission - Ingresa con nombre: ", body=nombre)
        return self.permissionRepository.findByName(nombre)

    def updatePermission(self, nombreActual: str, permisoData: permissionDTO) -> bool:
        self.log.info(f"updatePermission - Actualizar permiso '{nombreActual}'")
        return self.permissionRepository.update(nombreActual, permisoData)

    def deletePermission(self, nombre: str) -> bool:
        self.log.info("deletePermission - Eliminar permiso: ", body=nombre)
        return self.permissionRepository.deletePermission(nombre)