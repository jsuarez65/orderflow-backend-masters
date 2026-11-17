from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.dto.OperationResultDTO import OperationResultDTO
from model.dto.userDTO import UserDTO
from services.UsersService import (
    InternalErrorException,
    InvalidRolException,
    InvalidUserException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsersService
)

UsersRouter = APIRouter(prefix="/master/user", tags=["User"])


def getSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@UsersRouter.get("", response_model=OperationResultDTO)
def getAll(response: Response, session: Session = Depends(getSession)
           ) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info("getAll - Ingresa a recuperar todos los usuarios")

    try:
        usersService = UsersService(log, session=session)
        users = usersService.getAllUsers()

        return OperationResultDTO(
            data=[user.model_dump(mode="json") for user in users]
        )
    except Exception:
        log.exception("getAll - Error al recuperar los usuarios")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al recuperar los usuarios."
        )


@UsersRouter.get("/{username}", response_model=OperationResultDTO)
def getUser(username: str, response: Response,
            session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"getUser - Buscando usuario: {username}")

    try:
        usersService = UsersService(log, session=session)
        user = usersService.getUser(username)

        return OperationResultDTO(
            data=user.model_dump(mode="json")
        )
    except UserNotFoundException as ex:
        response.status_code = 404
        return OperationResultDTO(message=str(ex))
    except InternalErrorException:
        log.exception("getUser - Error al recuperar el usuario")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al recuperar el usuario."
        )
    except Exception:
        log.exception("getUser - Error inesperado")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al recuperar el usuario."
        )


@UsersRouter.post("", status_code=201, response_model=OperationResultDTO)
def create(userData: UserDTO, response: Response,
           session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"create - Ingresa con: {userData}")

    try:
        usersService = UsersService(log, session=session)
        userCreated = usersService.createUser(userData)

        return OperationResultDTO(
            data=userCreated.model_dump(mode="json")
        )
    except UserAlreadyExistsException as ex:
        response.status_code = 409
        return OperationResultDTO(message=str(ex))
    except (InvalidUserException, InvalidRolException) as ex:
        response.status_code = 400
        return OperationResultDTO(message=str(ex))
    except InternalErrorException:
        log.exception("create - Error al crear el usuario")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al crear el usuario."
        )
    except Exception:
        log.exception("create - Error inesperado")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al crear el usuario."
        )


@UsersRouter.put("/{username}", response_model=OperationResultDTO)
def update(username: str, userData: UserDTO, response: Response,
           session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"update - Actualizando usuario '{username}' con datos: {userData}")

    try:
        usersService = UsersService(log, session=session)
        userUpdated = usersService.updateUser(username, userData)

        return OperationResultDTO(
            data=userUpdated.model_dump(mode="json")
        )
    except UserNotFoundException as ex:
        response.status_code = 404
        return OperationResultDTO(message=str(ex))
    except (InvalidUserException, InvalidRolException) as ex:
        response.status_code = 400
        return OperationResultDTO(message=str(ex))
    except InternalErrorException:
        log.exception("update - Error al actualizar el usuario")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al actualizar el usuario."
        )
    except Exception:
        log.exception("update - Error inesperado")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al actualizar el usuario."
        )


@UsersRouter.delete("/{username}", response_model=OperationResultDTO)
def delete(username: str, response: Response,
           session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"delete - Eliminando usuario: {username}")

    try:
        usersService = UsersService(log, session=session)
        usersService.deleteUser(username)

        return OperationResultDTO(
            message=f"Usuario '{username}' eliminado exitosamente."
        )
    except UserNotFoundException as ex:
        response.status_code = 404
        return OperationResultDTO(message=str(ex))
    except InternalErrorException:
        log.exception("delete - Error al eliminar el usuario")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al eliminar el usuario."
        )
    except Exception:
        log.exception("delete - Error inesperado")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al eliminar el usuario."
        )
