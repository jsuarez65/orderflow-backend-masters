from configuration.LogConfiguration import LogConfiguration
from model.dto.userDTO import UserDTO
from repositories.RolRepository import RolRepository
from repositories.UserRepository import UserRepository


class UsersService:

    def __init__(self, log=None):
        #aca debe llegar el session inyectado desde el controller 
        self.log = log or LogConfiguration.getLogger()
        self.usersRepository = UserRepository(self.log)
        self.rolRepository = RolRepository(self.log)

    def createUser(self, user: UserDTO) -> tuple[UserDTO | None, str | None, int]:
        if user is None:
            return None, "DTO nulo recibido.", 400  # lo ideal es lanzar una excepcion (raise InvalidUserException) y que el
        # controller la capture y devuelva el codigo de error que corresponda.

        self.log.info(f"createUser - Creando usuario: {user.username}")

        if user.rol:
            rolDto, rolError, _ = self.rolRepository.findByName(user.rol) # aca debe devolver el rolEntity o None.. si hubo un error
            # todo este codigo debe encerrarse bajo un try y catch y eso seria considerado un error y se lanzaria una exception
            # de error que la toma el controller y este ultimo mandaria el 500
            if rolError or rolDto is None:
                self.log.warning(f"createUser - El rol '{user.rol}' no existe.")  #idem aca mandar exception
                return None, f"El rol '{user.rol}' no existe en el sistema.", 400

        return self.usersRepository.save(user)

    def getUser(self, username: str) -> tuple[UserDTO | None, str | None, int]:
        self.log.info(f"getUser - Buscando usuario: {username}")
        return self.usersRepository.findByUsername(username)

    def getAllUsers(self) -> tuple[list[UserDTO], str | None, int]:
        self.log.info("getAllUsers - Obteniendo todos los usuarios")
        return self.usersRepository.getAll()

    def updateUser(self, usernameActual: str, user: UserDTO) -> tuple[UserDTO | None, str | None, int]:
        if user is None:
            return None, "DTO nulo recibido.", 400

        self.log.info(f"updateUser - Actualizando usuario '{usernameActual}'")

        if user.rol:
            rolDto, rolError, _ = self.rolRepository.findByName(user.rol)
            if rolError or rolDto is None:
                self.log.warning(f"updateUser - El rol '{user.rol}' no existe.")
                return None, f"El rol '{user.rol}' no existe en el sistema.", 400

        return self.usersRepository.update(usernameActual, user)

    def deleteUser(self, username: str) -> tuple[UserDTO | None, str | None, int]:
        self.log.info(f"deleteUser - Eliminando usuario: {username}")
        return self.usersRepository.delete(username)