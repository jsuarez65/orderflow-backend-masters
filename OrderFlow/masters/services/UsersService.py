
from mappers.UsersMappers import UserMapper

from exceptions.users_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserCreationException,
    UserUpdateException
)
from model.dto.userDTO import UserDTO
from repositories.UserRepository import UserRepository



class UsersService:

    def __init__(self, log=None, session=None):
        
        self.log = log
        self.session = session
        self.usersRepository = UserRepository(log, session)

    def createUser(self, user: UserDTO) -> UserDTO:
        self.log.info(f"createUser - Creando usuario: {user}")

        if user is None or not user.validate():
            raise UserCreationException(
                "Todos los campos (username, password, rol) son obligatorios."
            )
        if not self.rolRepository.existsByRol(user.rol):
            raise UserCreationException(
                f"El rol '{user.rol}' no existe en el sistema."
            )
        if self.usersRepository.existsByUsername(user.username):
            raise UserAlreadyExistsException(
                f"El usuario '{user.username}' ya existe."
            )

        try:
            userEntity = UserMapper.toEntity(user)
            createdUser = self.usersRepository.create(userEntity)
            self.session.commit()
            return UserMapper.toDTO(createdUser)
        except Exception as e:
            self.session.rollback()
            self.log.error(f"createUser - Error al crear el usuario: {e}")
            raise UserCreationException(
                "Error inesperado al crear el usuario."
            ) from e

    def getAllUser(self) -> list[UserDTO]:
        self.log.info("getAllUser - Buscando todos los usuarios")
        userEntity = self.usersRepository.getAllUser()
        return UserMapper.entityListToDTOList(userEntity)
    
        

    def getAllUsers(self) -> list[UserDTO]:
        self.log.info("getAllUsers - Obteniendo todos los usuarios")
        try:
            users = self.usersRepository.findAll()
            return UserMapper.toListDTO(users)
        except Exception as e:
            self.log.exception(f"getAllUsers - Error al obtener los usuarios: {e}")
            raise (
                "Error inesperado al obtener los usuarios."
            ) from e

    def updateUser(self, usernameActual: str, user: UserDTO) -> UserDTO:
        self.log.info(f"updateUser - Actualizando usuario '{usernameActual}'")

        if user is None or not user.validate():
            raise UserUpdateException("Todos los campos son obligatorios.")
        if not self.rolRepository.existsByRol(user.rol):
            raise UserUpdateException(
                f"El rol '{user.rol}' no existe en el sistema."
            )
        if (
            user.username != usernameActual
            and self.usersRepository.existsByUsername(user.username)
        ):
            raise UserAlreadyExistsException(
                f"El usuario '{user.username}' ya existe."
            )

        try:
            userEntity = UserMapper.toEntity(user)
            if userEntity is None:
                raise UserUpdateException("Los datos del usuario son inválidos.")

            updatedUser = self.usersRepository.update(usernameActual, userEntity)
            if updatedUser is None:
                raise UserNotFoundException(
                    f"El usuario '{usernameActual}' no existe."
                )

            self.session.commit()
            return UserMapper.toDTO(updatedUser)
        except Exception as e:
            self.session.rollback()
            self.log.exception(f"updateUser - Error al actualizar el usuario: {e}")
            if isinstance(e, ):
                raise
            raise (
                "Error inesperado al actualizar el usuario."
            ) from e

    def deleteUser(self, username: str) -> UserDTO:
        self.log.info(f"deleteUser - Eliminando usuario: {username}")
        try:
            deletedUser = self.usersRepository.delete(username)
            if deletedUser is None:
                raise UserNotFoundException(f"El usuario '{username}' no existe.")

            deletedUserDTO = UserMapper.toDTO(deletedUser)
            self.session.commit()
            return deletedUserDTO
        except Exception as e:
            self.session.rollback()
            self.log.exception(f"deleteUser - Error al eliminar el usuario: {e}")
            if isinstance(e, ):
                raise
            raise (
                "Error inesperado al eliminar el usuario."
            ) from e
