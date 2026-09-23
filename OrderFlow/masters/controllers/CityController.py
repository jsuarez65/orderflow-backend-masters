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
    
@CitiesBlueprint.route('', methods=['GET'])
def getPostalCodes():
    log = LogConfiguration.getLogger()
    log.info("getPostalCodes - Entering postal codes retrieval")

    postal_code = request.args.get('postal_code')
    city_name = request.args.get('city_name')

    result = cityService.getPostalCodes(postal_code, city_name)
    
    return result, 200