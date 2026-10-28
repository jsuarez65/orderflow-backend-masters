from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from exceptions.product_exceptions import (
    ProductAlreadyExistsException,
    ProductCreationException,
    ProductNotFoundException,
    ProductUpdateException
)

from model.dtos.OperationResultDTO import OperationResultDTO
from model.dtos.ProductDTO import ProductDTO
from services.ProductService import ProductService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

ProductRouter = APIRouter(prefix="/master/product", tags=["Products"])


def getSession():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()


@ProductRouter.get("", response_model=OperationResultDTO)
def getAll(response: Response, session: Session = Depends(getSession)
           ) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("getAll - Ingresa a recuperar todos los productos")

    try:
        productService = ProductService(log, session=session)
        products = productService.findAll()

        return OperationResultDTO(
            data=[products]
        )

    except Exception:
        log.exception("getAll - Error al recuperar los productos")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al recuperar los productos."
        )


@ProductRouter.post("", status_code=201, response_model=OperationResultDTO)
def create(productData: ProductDTO, response: Response, 
           session: Session = Depends(getSession) ) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("create - Ingresa con: {}", productData)

    try:
        productService = ProductService(log, session=session)
        productCreated = productService.create(productData)

        return OperationResultDTO(
            data=productCreated.model_dump(mode="json")
        )

    except ProductAlreadyExistsException as ex:
        response.status_code = 409
        return OperationResultDTO(message=str(ex))

    except ProductCreationException:
        log.exception("create - Error al crear el producto")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al crear el producto."
        )

    except Exception:
        log.exception("create - Error inesperado")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al crear el producto."
        )


@ProductRouter.put("", response_model=OperationResultDTO)
def update(productData: ProductDTO, response: Response, 
           session: Session = Depends(getSession)) -> OperationResultDTO:

    log = LogConfiguration.getLogger()
    log.info("update - Ingresa con: {}", productData)

    try:
        productService = ProductService(log, session=session)
        productUpdated = productService.update(productData)

        return OperationResultDTO(
            data=productUpdated.model_dump(mode="json")
        )

    except ProductNotFoundException as ex:
        response.status_code = 404
        return OperationResultDTO(message=str(ex))

    except ProductUpdateException:
        log.exception("update - Error al actualizar el producto")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al actualizar el producto."
        )

    except Exception:
        log.exception("update - Error inesperado")
        response.status_code = 500

        return OperationResultDTO(
            message="Error interno al actualizar el producto."
        )