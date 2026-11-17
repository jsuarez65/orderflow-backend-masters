from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from exceptions.rol_exceptions import (
    RolAlreadyExistsException,
    RolNotFoundException,
    RolUpdateException,
    RolCreationException
)

from model.dto.OperationResultDTO import OperationResultDTO
from model.dto.rolDTO import RolDTO
from services.RolService import RolService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal



rolRouter = APIRouter(prefix="/master/rol", tags=["Rol"])

def getSession():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()



@rolRouter.post("/roles", status_code=201, response_model=OperationResultDTO)
def create(rolData: RolDTO, response: Response,
           session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"createRol - Creando rol con datos: {rolData}")

    try:
        RolService = RolService(log, session=session)
        createdRol = RolService.create(rolData)
        
        return OperationResultDTO(
            data=createdRol.model_dump(mode="json")
        )
    except RolAlreadyExistsException as e:
        response.status_code = 409
        return OperationResultDTO(message=str(e))

    except RolCreationException:
        log.exception("createRol - Error al crear el rol")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al crear el rol."
        )
    except Exception:
        log.exception("createRol - Error inesperado al crear el rol")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno inesperado al crear el rol."
        )


@rolRouter.get("", response_model=OperationResultDTO)
def getAll(response: Response, session: Session = Depends(getSession)) -> OperationResultDTO:
    
    log = LogConfiguration.getLogger()
    log.info(f"getAll - Buscando todos los roles")

    
    try:
        rolservice = RolService(log, session=session)
        roles = rolservice.getAllRoles()
        
        return OperationResultDTO(
            data=[roles]
        )
    except Exception:
        log.exception(f"getAll - Error al recuperar los roles")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al recuperar los roles."
        )



@rolRouter.put("", response_model=OperationResultDTO)
def update(rolData: RolDTO, response: Response, session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"updateRol - Actualizando rol con datos: {rolData}")

    try:
        rolService = RolService(log, session=session)
        updatedRol = rolService.update(rolData)

        return OperationResultDTO(
            data=updatedRol.model_dump(mode="json")
        )
    except RolNotFoundException as e:
        response.status_code = 404
        return OperationResultDTO(message=str(e))

    except RolUpdateException:
        log.exception("updateRol - Error al actualizar el rol")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno al actualizar el rol."
        )
    except Exception:
        log.exception("updateRol - Error inesperado al actualizar el rol")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno inesperado al actualizar el rol."
        )


@rolRouter.delete("/{rol_id}", response_model=OperationResultDTO)
def delete(rol_id: int, response: Response, session: Session = Depends(getSession)) -> OperationResultDTO:
    log = LogConfiguration.getLogger()
    log.info(f"deleteRol - Eliminando rol con ID: {rol_id}")

    try:
        rolService = RolService(log, session=session)
        rolService.delete(rol_id)

        return OperationResultDTO(
            message=f"Rol con ID {rol_id} eliminado exitosamente."
        )
    except RolNotFoundException as e:
        response.status_code = 404
        return OperationResultDTO(message=str(e))

    except Exception:
        log.exception("deleteRol - Error inesperado al eliminar el rol")
        response.status_code = 500
        return OperationResultDTO(
            message="Error interno inesperado al eliminar el rol."
        )