from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from exceptions.permission_exceptions import (
    PermissionAlreadyExistsException,
    PermissionCreationException,
    PermissionNotFoundException,
    PermissionUpdateException
)

from model.dto.OperationResultDTO import OperationResultDTO
from model.dto.permissionDTO import PermissionDTO
from services.PermissionService import PermissionService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

PermissionRouter = APIRouter(prefix="/master/permission", tags=["Permission"])


def getSession():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

@PermissionRouter.get("", response_model=OperationResultDTO)
def getAll(response: Response, session: Session = Depends(getSession)
           ) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("getAll - Ingresa a recuperar todos los permisos")

    try:
        permissionService = PermissionService(log, session=session)
        permission = permissionService.findAll()

        return OperationResultDTO(
            data=[permission]
        )

    except Exception:
        log.exception("getAll - Error al recuperar los permisos")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al recuperar los permisos."
        )


@PermissionRouter.post("", status_code=201, response_model=OperationResultDTO)
def create(permissionData: PermissionDTO, response: Response, 
           session: Session = Depends(getSession) ) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("create - Ingresa con: {}", permissionData)

    try:
        permissionService = PermissionService(log, session=session)
        permissionCreated = permissionService.create(permissionData)

        return OperationResultDTO(
            data=permissionCreated.model_dump(mode="json")
        )

    except PermissionAlreadyExistsException as ex:
        response.status_code = 409
        return OperationResultDTO(message=str(ex))

    except PermissionCreationException:
        log.exception("create - Error al crear el permiso")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al crear el permiso."
        )

    except Exception:
        log.exception("create - Error inesperado")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al crear el permiso."
        )


@PermissionRouter.put("", response_model=OperationResultDTO)
def update(permissionData: PermissionDTO, response: Response, 
           session: Session = Depends(getSession)) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("update - Ingresa con: {}", permissionData)

    try:
        permissionService = PermissionService(log, session=session)
        permissionUpdated = permissionService.update(permissionData)

        return OperationResultDTO(
            data=permissionUpdated.model_dump(mode="json")
        )

    except PermissionNotFoundException as ex:
        response.status_code = 404
        return OperationResultDTO(message=str(ex))

    except PermissionUpdateException:
        log.exception("update - Error al actualizar el permiso")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al actualizar el permiso."
        )

    except Exception:
        log.exception("update - Error inesperado")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al actualizar el permiso."
        )