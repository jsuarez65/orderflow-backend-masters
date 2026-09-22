from repositories.RolRepository import RolRepository, DeleteResult
from configuration.LogConfiguration import LogConfiguration
from model.dto import rolDTO

rolRepository = RolRepository()


class RolService:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def createRol(self, rol: rolDTO) -> bool:
        self.log.info("createRol - Ingresa con rol: ", body=rol.rol)
        return rolRepository.save(rol) is not None

    def getRol(self, rol: str) -> rolDTO | None:
        self.log.info("getRol - Ingresa con nombre: ", body=rol)
        return rolRepository.findByName(rol)

    def updateRol(self, rolActual: str, rolNuevo: rolDTO) -> bool:
        self.log.info(f"updateRol - Actualizar rol '{rolActual}'")
        return rolRepository.update(rolActual, rolNuevo)

    def deleteRol(self, rol: str) -> DeleteResult:
        self.log.info("deleteRol - Eliminar rol: ", body=rol)
        return rolRepository.delete(rol)