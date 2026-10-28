<<<<<<< Updated upstream
from dataclasses import asdict
from logging import log

from flask import Blueprint, request, session
=======
from flask import Blueprint, request 
>>>>>>> Stashed changes
from model.dtos.ProviderDTO import ProviderDTO
from services.ProviderService import ProviderService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

ProviderBlueprint = Blueprint('provider', __name__, url_prefix='/master/provider')

@ProviderBlueprint.route('', methods=['GET'])
<<<<<<< Updated upstream
def getAll() -> tuple[list[dict], int]:
    """ Create a new provider in the database.
    ---
    responses:
      200:
        description: A list of providers
=======
def getProviders():
     """ 
    Permite recuperar todos los proveedores registrados en la base de datos.
    ---
    responses:
      200:
        description: Lista de ProviderDTO.
>>>>>>> Stashed changes
        schema:
          type: array
          items:
            $ref: '#/definitions/ProviderDTO'
    definitions:
      ProviderDTO:
        type: object
        properties:
          cuit:
            type: string
<<<<<<< Updated upstream
          company_name:
            type: string
          address:
            type: string
          email:
            type: string
          phone:
            type: string
          postal_code:
            type: string
          state_name:
            type: string
          city:
            type: string

    """

=======
            example: "PROD-001"
          sku:
            type: string
            example: "SKU-12345"
          barcode:
            type: string
            example: "7791234567890"
          description:
            type: string
            example: "Descripción del producto"
          unitMeasurements:
            type: string
            example: "Unidades"
          weight:
            type: number
            format: float
            example: 1.5
          dimensions:
            type: string
            example: "10x20x30 cm"
          minimumStock:
            type: number
            format: float
            example: 10.0
          maximumStock:
            type: number
            format: float
            example: 100.0
          reorderPoint:
            type: number
            format: float
            example: 20.0
          productCategoriesId:
            type: integer
            example: 5
          providerTaxId:
            type: string
            example: "30-12345678-9"
    """

    
>>>>>>> Stashed changes
    log = LogConfiguration.getLogger()

    log.info("getAll - Ingresa a obtener proveedores")

    session = sessionLocal()
    providerService = ProviderService(log, session=session)
    providers = providerService.findAll()

    return {providers}, 200

@ProviderBlueprint.route('', methods=['POST'])
def create()-> tuple[dict, int]:

    session = sessionLocal()
    log = LogConfiguration.getLogger()
    
    provider = ProviderDTO(**request.get_json())

    providerService = ProviderService(log, session=session)

    log.info("create - Ingresa con provider: ", body=provider)

    providerCreated = providerService.create(provider)

    if providerCreated:
        return asdict(providerCreated), 200
    else:
        return {"message": "Error al crear el proveedor, debido a que ya existe"}, 500

@ProviderBlueprint.route('', methods=['PUT'])
def update()-> tuple[dict, int]:

    session = sessionLocal()
    log = LogConfiguration.getLogger()

    providerService = ProviderService(log, session=session)

    provider = ProviderDTO(**request.get_json())
    
    log.info("update - Ingresa con provider: ", body=provider)

    providerUpdated = providerService.update(provider)
    
    if (providerUpdated is not None):
        return asdict(providerUpdated), 200
    else:
        return {"message": "El producto a actualizar no existe"}, 500

@ProviderBlueprint.route('/<cuit>', methods=['DELETE'])
def deleteProvider(cuit):

    session = sessionLocal()
    log = LogConfiguration.getLogger()

    log.info(f"deleteProvider - Ingresa con CUIT: {cuit}")
    
    providerService = ProviderService(log, session=session)

    if providerService.deleteProvider(cuit):
        return {"message": "El proveedor se eliminó correctamente"}, 200
    else:
        return {"message": "Error al eliminar el proveedor"}, 500