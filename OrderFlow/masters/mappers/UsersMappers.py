from model.entities.UserEntity import UserEntity
from model.dto.userDTO import UserDTO

class UserMapper:
    
    @staticmethod
    def toDTO(entity: UserEntity) -> UserDTO | None:

        if entity is None:
            return None

        return UserDTO(
            username=entity.username,
            password=entity.password,
            rol=entity.rol
        )
        
    @staticmethod
    def toEntity(dto: UserDTO) -> UserEntity | None:

        if dto is None:
            return None

        return UserEntity(
            username=dto.username,
            password=dto.password,
            rol=dto.rol
        )
    @staticmethod
    def toListDTO(users: list[UserEntity]) -> list[UserDTO]:
        if not users:
            return []
        return [UserMapper.toDTO(u) for u in users if u is not None]