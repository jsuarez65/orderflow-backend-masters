from model.entities.RolEntity import RolEntity
from model.dto.rolDTO import RolDTO

class RolMapper:

    @staticmethod
    def toDTO(entity: RolEntity) -> RolDTO | None:

        if entity is None:
            return None

        return RolDTO(
            rol=entity.rol
        )

    @staticmethod
    def toEntity(dto: RolDTO) -> RolEntity | None:

        if dto is None:
            return None

        return RolEntity(
            rol=dto.rol
        )

    @staticmethod
    def toListDTO(roles: list[RolEntity]) -> list[RolDTO]:

        if not roles:
            return []
        
        return [RolMapper.toDTO(role) for role in roles]