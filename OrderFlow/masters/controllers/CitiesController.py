from flask import Blueprint, request
from services.CitiesService import CitiesService
from configuration.LogConfiguration import LogConfiguration

CitiesBlueprint = Blueprint('cities', __name__, url_prefix='/master/cities')

citiesService = CitiesService()

@CitiesBlueprint.route('', methods=['POST'])
def importPostalCodes():
    log = LogConfiguration.getLogger()
    
    log.info("importPostalCodes - Entering postal codes import")

    result = citiesService.importPostalCodes(request)
    
    if result is not None:
        return result, 200
    else:
        return {"message": "Error importing postal codes"}, 400