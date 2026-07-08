from flask import Blueprint, request 
from services.ProviderService import ProviderService
from configuration.LogConfiguration import LogConfiguration


ProviderBlueprint = Blueprint('provider', __name__, url_prefix='/master/provider')

providerService = ProviderService()

@ProviderBlueprint.route('', methods=['GET'])
def getProviders():
    
    log = LogConfiguration.getLogger()
    
    log.info("getProviders - Ingresa a obtener proveedores")
    return {"message": "ok"}, 200

@ProviderBlueprint.route('', methods=['POST'])
def createProvider():
    
    log = LogConfiguration.getLogger()
    
    provider = request.get_json()

    log.info("createProvider - Ingresa con provider: ", body=provider)

    if (providerService.createProvider(provider) == True):
        return {"message": "El proveedor se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el proveedor"}, 500

@ProviderBlueprint.route('', methods=['PUT'])
def updateProvider():

    log = LogConfiguration.getLogger()
    
    provider = request.get_json()

    log.info("updateProvider - Ingresa con provider: ", body=provider)

    if (providerService.updateProvider(provider) == True):
        return {"message": "El proveedor se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el proveedor"}, 500
