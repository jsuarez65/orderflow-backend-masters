from mappers.RolMappers import RolMapper
from exceptions.rol_exceptions import (
    RolNotFoundException,
    RolAlreadyExistsException,
    RolCreationException,
    RolUpdateException)

from model.dto.rolDTO import RolDTO
from repositories.RolRepository import RolRepository



class RolService:

    def __init__(self, log=None, session=None):
        
        self.log = log 
        self.session = session
        self.rolRepository = RolRepository(log, session)

    def createRol(self, rol: RolDTO) -> RolDTO | None:
        self.log.info(f"createRol - Ingresa con rol: ", body=rol)
        
        if self.rolRepository.findByName(rol.nombre) is not None:
                raise RolAlreadyExistsException(
                    f"El rol '{rol.nombre}' ya existe."
                )
        try:
            rolToCreate = RolMapper.dtoToEntity(rol)
            createdRol = self.rolRepository.create(rolToCreate)
            self.session.commit()
            return createdRol
        except Exception as e:
            self.session.rollback()
            self.log.error(f"createRol - Excepción inesperada: {e}")
            raise RolCreationException(
                "Error inesperado al crear el rol."
            ) from e
def getAllRoles(self) -> list[RolDTO]:
        
            self.log.info("getAllRoles - Obteniendo todos los roles")
            rolEntity= self.rolRepository.getAllRoles()
            return RolMapper.entityListToDTOList(rolEntity)
        