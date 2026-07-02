from flask import Blueprint, request
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

ProviderBlueprint = Blueprint('provider', __name__, url_prefix='/master/provider') 

@ProviderBlueprint.route('', methods=['POST']) 
def createProvider():
    
    provider = request.get_json()

    log.info("createProvider - Ingresa con provider: ", body=provider)

