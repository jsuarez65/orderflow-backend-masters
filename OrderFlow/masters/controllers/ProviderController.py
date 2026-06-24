from flask import Blueprint, request 
from services.ProviderService import ProviderService
from configuration.LogConfiguration import LogConfiguration


ProviderBlueprint = Blueprint('provider', __name__, url_prefix='/master/provider')



@ProviderBlueprint.route('', methods=['POST'])
def createProvider():
    
    log = LogConfiguration.getLogger()
    
    provider = request.get_json()

    log.info("createProvider - Ingresa con provider: ", body=provider)

    if (providerService.createProvider(provider) == True):
        return {"message": "El proveedor se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el proveedor"}, 500
