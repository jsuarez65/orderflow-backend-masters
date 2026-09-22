from model.entities.RolEntity import RolEntity
from model.dto.rolDTO import rolDTO

class RolMapper:

    @staticmethod
    def toDTO(entity: RolEntity) -> rolDTO:

        if entity is None:
            return None

        return rolDTO(
            rol=entity.rol
        )

    @staticmethod
    def toEntity(dto: rolDTO) -> RolEntity:

        if dto is None:
            return None

        return RolEntity(
            rol=dto.rol
        )

    @staticmethod
    def toListDTO(roles: list[RolEntity]) -> list[rolDTO]:

        if not roles:
            return []
        
        return [RolMapper.toDTO(role) for role in roles]