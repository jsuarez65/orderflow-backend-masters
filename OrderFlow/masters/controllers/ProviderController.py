from dataclasses import asdict
from logging import log

from flask import Blueprint, request, session
from model.dtos.ProviderDTO import ProviderDTO
from services.ProviderService import ProviderService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

ProviderBlueprint = Blueprint('provider', __name__, url_prefix='/master/provider')

@ProviderBlueprint.route('', methods=['GET'])
def getAll() -> tuple[list[dict], int]:
    """ Create a new provider in the database.
    ---
    responses:
      200:
        description: A list of providers
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

    """

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