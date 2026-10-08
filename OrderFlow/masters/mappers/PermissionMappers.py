from model.entities.PermissionEntity import PermissionEntity
from model.dto.permissionDTO import PermissionDTO


class PermissionMapper:

    @staticmethod
    def toDTO(entity: PermissionEntity | None) -> PermissionDTO | None:
        if entity is None:
            return None
        return PermissionDTO(
            nombre=entity.nombre,
            descripcion=entity.descripcion
        )

    @staticmethod
    def toEntity(dto: PermissionDTO | None) -> PermissionEntity | None:
        if dto is None:
            return None
        if not dto.nombre or not dto.nombre.strip():
            return None
        return PermissionEntity(
            nombre=dto.nombre,
            descripcion=dto.descripcion
        )

    @staticmethod
    def toListDTO(permissions: list[PermissionEntity]) -> list[PermissionDTO]:
        if not permissions:
            return []
        return [
            PermissionMapper.toDTO(p)
            for p in permissions
            if p is not None
        ]