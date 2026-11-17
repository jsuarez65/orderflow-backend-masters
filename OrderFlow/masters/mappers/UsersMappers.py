from model.dto.userDTO import UserDTO
from model.entities.UserEntity import UserEntity


class UserMapper:

    @staticmethod
    def toDTO(entity: UserEntity | None) -> UserDTO | None:
        if entity is None:
            return None
        return UserDTO(
            username=entity.username,
            password=entity.password,
            rol=entity.rol
        )

    @staticmethod
    def toEntity(dto: UserDTO | None) -> UserEntity | None:
        if dto is None:
            return None
        if not dto.username or not dto.username.strip():
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
        return [
            UserMapper.toDTO(user)
            for user in users
            if user is not None
        ]
