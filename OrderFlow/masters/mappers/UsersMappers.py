from model.entities.UserEntity import UserEntity
from model.dto.userDTO import userDTO

class UserMapper:
    
    @staticmethod
    def toDTO(entity: UserEntity) -> userDTO | None:

        if entity is None:
            return None

        return userDTO(
            username=entity.username,
            password=entity.password,
            rol=entity.rol
        )
        
    @staticmethod
    def toEntity(dto: userDTO) -> UserEntity | None:

        if dto is None:
            return None

        return UserEntity(
            username=dto.username,
            password=dto.password,
            rol=dto.rol
        )
    @staticmethod
    def toListDTO(users: list[UserEntity]) -> list[userDTO]:
        if not users:
            return []
        return [UserMapper.toDTO(u) for u in users]