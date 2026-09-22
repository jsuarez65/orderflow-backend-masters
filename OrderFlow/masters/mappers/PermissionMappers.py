from model.entities.PermissionEntity import PermissionEntity
from model.dto.permissionDTO import permissionDTO

class PermissionMapper:

    @staticmethod
    def toDTO(entity: PermissionEntity) -> permissionDTO:

        if entity is None:
            return None

        return permissionDTO(
            nombre=entity.nombre,
            descripcion=entity.descripcion
        )

    @staticmethod
    def toEntity(dto: permissionDTO) -> PermissionEntity:

        if dto is None:
            return None

        return PermissionEntity(
            nombre=dto.nombre,
            descripcion=dto.descripcion
        )

    @staticmethod
    def toListDTO(permissions: list[PermissionEntity]) -> list[permissionDTO]:

        if not permissions:
            return []
        
        return [PermissionMapper.toDTO(permission) for permission in permissions]