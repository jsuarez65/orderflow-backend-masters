from services.ExcelService import ExcelService
from repositories.CityRepository import CityRepository
from model.entities.CityEntity import CityEntity

class CityService:
    def __init__(self, log, session):
        self.log = log
        self.session = session
        self.excelService = ExcelService(log)
        self.cityRepository = CityRepository(log, session)
    
    def importZipCodes(self, request):
        if 'file' not in request.files:
            return None
        
        file = request.files['file']
        if file.filename == '':
            return None

        postalCodes = self.excelService.readPostalCodes(file)
        
        cityEntities = [
            CityEntity(codigo_postal=postalCode, nombre_localidad=cityName)
            for postalCode, cityName in postalCodes
        ]

        return self.cityRepository.importZipCodes(cityEntities)
    
    def getPostalCodes(self, postalCode: str = None, cityName: str = None):
        return self.cityRepository.getPostalCodes(postalCode, cityName)