from flask import Blueprint, request 
import ProviderService  
import logConfiguration

providerBlueprint = Blueprint('provider', __name__,"url_prefix='/master/provider'")


@providerBlueprint.route('', methods=['POST'])
def createProvider():
    
    log = LogConfiguration.getLogger()
    
    provider = request.get_json()

    log.info("createProvider - Ingresa con provider: ", body=provider)

    if (providerService.createProvider(provider) == True):
        return {"message": "El proveedor se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el proveedor"}, 500
