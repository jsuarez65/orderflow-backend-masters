from dataclasses import asdict
from flask import Blueprint, request
from model.dtos.CityDTO import CityDTO
from services.CityService import CityService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

CitiesBlueprint = Blueprint('cities', __name__, url_prefix='/master/cities')

@CitiesBlueprint.route('', methods=['POST'])
def importZipCodes() -> tuple[dict, int]:
    session = sessionLocal()
    log = LogConfiguration.getLogger()
    cityService = CityService(log, session=session)
    
    log.info("importZipCodes - Entering zip codes import")

    if 'file' not in request.files:
        return {"message": "No file sent in request"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"message": "Empty filename"}, 400

    result = cityService.importZipCodes(request)
    
    if result is not None:
        return result, 200
    else:
        return {"message": "Error importing zip codes"}, 500

@CitiesBlueprint.route('', methods=['GET'])
def getPostalCodes() -> tuple[list[dict], int]:

    session = sessionLocal()
    log = LogConfiguration.getLogger()
    cityService = CityService(log, session=session)

    log.info("getPostalCodes - Entering postal codes retrieval")

    postalCode = request.args.get('postalCode')
    cityName = request.args.get('cityName')

    result = cityService.getPostalCodes(postalCode, cityName)
    
    # Convertimos la lista de DTOs a lista de diccionarios para la respuesta JSON
    return [asdict(city) for city in result], 200