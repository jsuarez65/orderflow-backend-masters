from mappers.PermissionMappers import PermissionMapper
from exceptions.permission_exceptions import (
    PermissionNotFoundException,
    PermissionAlreadyExistsException,
    PermissionCreationException,
    PermissionUpdateException
)
from model.dto.permissionDTO import PermissionDTO
from repositories.PermissionRepository import PermissionRepository



class PermissionService:

    def __init__(self, log=None, session=None):
        
        self.log = log 
        self.session = session
        self.permissionRepository = PermissionRepository(log, session)

    
    def createPermission(self, permission: PermissionDTO) -> PermissionDTO | None:
        
        self.log.info(f"createPermission - Ingresa con permission: ", body=permission)

        if self.permissionRepository.findByName(permission.nombre) is not None:
                raise PermissionAlreadyExistsException(
                    f"El permiso '{permission.nombre}' ya existe."
                )
        try:
            permissionToCreate = PermissionMapper.dtoToEntity(permission)
            createdPermission = self.permissionRepository.create(permissionToCreate)
            self.session.commit()
            return createdPermission
        except Exception as e:
            self.session.rollback()
            self.log.error(f"createPermission - Excepción inesperada: {e}")
            raise PermissionCreationException(
                "Error inesperado al crear el permiso."
            ) from e

        

    def getAllPermissions(self) -> list[PermissionDTO]:
        
            self.log.info("getAllPermissions - Obteniendo todos los permisos")
            permissionEntity= self.permissionRepository.getAllPermissions()
            return PermissionMapper.entityListToDTOList(permissionEntity)
        

    def updatePermission(
        self, permission: PermissionDTO) -> PermissionDTO | None:
        
        self.log.info(f"updatePermission - Actualizar permiso ", body=permission)
        
        if not self.permissionRepository.findById(permission.id):
            raise PermissionNotFoundException(
                f"El permiso con ID '{permission.id}' no existe."
            )
        try:
            permissionToUpdate = PermissionMapper.dtoToEntity(permission)
            updatedPermission = self.permissionRepository.update(permissionToUpdate)
            self.session.commit()
            return updatedPermission
        except Exception as e:
            self.session.rollback()
            self.log.error(f"updatePermission - Excepción inesperada: {e}")
            raise PermissionUpdateException(
                "Error inesperado al actualizar el permiso."
            ) from e

            