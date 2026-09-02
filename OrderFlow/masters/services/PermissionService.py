from repositories.PermissionRepository import PermissionRepository
from configuration.LogConfiguration import LogConfiguration
from model.dto import permissionDTO

permisosRepository = PermissionRepository()

class PermissionService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createPermission(self, permiso : permissionDTO) -> bool:
        self.log.info("createPermission - Ingresa con permission: ", body=permiso)
        return permisosRepository.save(permiso)
    
    def getPermission(self, nombre : str) -> permissionDTO | None:
        self.log.info("getPermission - Ingresa con nombre: ", body=nombre)
        return permisosRepository.findByName(nombre)
    
    def updatePermission(self, nombreActual : str, permisoData : permissionDTO) -> bool:
        self.log.info(f"updatePermission - Actualizar permiso '{nombreActual}'")
        return permisosRepository.update(nombreActual, permisoData)
    
    def deletePermission(self, nombre):
        self.log.info("deletePermission - Eliminar permiso: ", body=nombre)
        return permisosRepository.delete(nombre)