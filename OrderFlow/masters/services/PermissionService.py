"""from OrderFlow.masters.repositories.PermisosRepository import PermissionRepository
from configuration.LogConfiguration import LogConfiguration

permissionRepository = PermissionRepository()

class PermissionService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createPermission(self, permission):
        
        self.log.info("createPermission - Ingresa con permission: ", body=permission)
        return permissionRepository.save(permission)
    
    def getPermisos(self, nombre):
        self.log.info("getPermisos - Ingresa con nombre: ", body=nombre)
        return permissionRepository.findByName(nombre)
    
    def deletePermission(self, nombre):
        self.log.info("deletePermission - Eliminar permiso: ", body=nombre)
        return permissionRepository.delete(nombre)"""
    
"""def updatePermission (self,permission):
        self.log.info("updatePermission - Ingresa con permission: ", body=permission)
        return permissionRepository.save(permission)"""
        
from repositories.PermisosRepository import PermisosRepository
from configuration.LogConfiguration import LogConfiguration

permisosRepository = PermisosRepository()

class PermissionService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createPermission(self, permiso):
        self.log.info("createPermission - Ingresa con permission: ", body=permiso)
        return permisosRepository.save(permiso)
    
    def getPermission(self, nombre):
        self.log.info("getPermission - Ingresa con nombre: ", body=nombre)
        return permisosRepository.findByName(nombre)
    
    def updatePermission(self, nombreActual, permisoData):
        self.log.info(f"updatePermission - Actualizar permiso '{nombreActual}'")
        return permisosRepository.update(nombreActual, permisoData)
    
    def deletePermission(self, nombre):
        self.log.info("deletePermission - Eliminar permiso: ", body=nombre)
        return permisosRepository.delete(nombre)