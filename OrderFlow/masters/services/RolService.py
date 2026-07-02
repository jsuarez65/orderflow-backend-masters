        
from repositories.RolRepository import RolRepository
from configuration.LogConfiguration import LogConfiguration

rolRepository = RolRepository()

class RolService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createRol(self, rol):
        self.log.info("createRol - Ingresa con rol: ", body=rol)
        return rolRepository.insertRol(rol)
    
    def getRol(self, rol):
        self.log.info("getRol - Ingresa con nombre: ", body=rol)
        return rolRepository.findByName(rol)
    
    def updateRol(self, rolActual, rolNuevo):
        self.log.info(f"updateRol - Actualizar rol '{rolActual}' a '{rolNuevo}'")
        return rolRepository.updateRol(rolActual, rolNuevo)
    
    def deleteRol(self, rol):
        self.log.info("deleteRol - Eliminar rol: ", body=rol)
        return rolRepository.delete(rol)
    
    