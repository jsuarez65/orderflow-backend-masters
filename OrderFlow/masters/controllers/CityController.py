from flask import Blueprint, request
from OrderFlow.masters.services.CityService import CitiesService
from configuration.LogConfiguration import LogConfiguration

CitiesBlueprint = Blueprint('cities', __name__, url_prefix='/master/cities')

citiesService = CitiesService()

@CitiesBlueprint.route('', methods=['POST'])
def importZipCodes():
    
    log = LogConfiguration.getLogger()
    
    log.info("importZipCodes - Entering zip codes import")

    cityService = CitiesService()

    result = cityService.importZipCodes(request)
    
    if result is not None:
        return result, 200
    else:
        return {"message": "Error importing zip codes"}, 400