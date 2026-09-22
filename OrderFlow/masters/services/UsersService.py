from repositories.UsersRepository import UsersRepository
from configuration.LogConfiguration import LogConfiguration
from model.dto import userDTO
from werkzeug.security import generate_password_hash

usersRepository = UsersRepository()


class UsersService:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def createUser(self, user: userDTO) -> bool:
        self.log.info("createUser - Ingresa con usuario: ", body=user.username)
        user.password = generate_password_hash(user.password)
        return usersRepository.save(user) is not None

    def getUser(self, username: str) -> userDTO | None:
        self.log.info("getUser - Ingresa con nombre: ", body=username)
        return usersRepository.findByUsername(username)

    def updateUser(self, usernameActual: str, userData: userDTO) -> bool:
        self.log.info(f"updateUser - Actualizar usuario '{usernameActual}'")
        userData.password = generate_password_hash(userData.password)
        return usersRepository.update(usernameActual, userData)

    def deleteUser(self, username: str) -> bool:
        self.log.info("deleteUser - Eliminar usuario: ", body=username)
        return usersRepository.delete(username)