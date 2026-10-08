from repositories.RolRepository import RolRepository
from configuration.LogConfiguration import LogConfiguration
from model.dto.rolDTO import RolDTO


class RolService:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger()
        self.rolRepository = RolRepository(self.log)

    def createRol(self, rol: RolDTO) -> tuple[RolDTO | None, str | None, int]:
        if rol is None:
            return None, "DTO nulo recibido.", 400
        self.log.info(f"createRol - Ingresa con rol: {rol.rol}")
        return self.rolRepository.save(rol)

    def getRol(self, rol: str) -> tuple[RolDTO | None, str | None, int]:
        self.log.info(f"getRol - Ingresa con nombre: {rol}")
        return self.rolRepository.findByName(rol)

    def getAllRoles(self) -> tuple[list[RolDTO], str | None, int]:
        self.log.info("getAllRoles - Obteniendo todos los roles")
        return self.rolRepository.getAll()

    def updateRol(self, rolActual: str, rolNuevo: RolDTO) -> tuple[RolDTO | None, str | None, int]:
        if rolNuevo is None:
            return None, "DTO nulo recibido.", 400
        self.log.info(f"updateRol - Actualizar rol '{rolActual}'")
        return self.rolRepository.update(rolActual, rolNuevo)

    def deleteRol(self, rol: str) -> tuple[RolDTO | None, str | None, int]:
        self.log.info(f"deleteRol - Eliminar rol: {rol}")
        return self.rolRepository.delete(rol)