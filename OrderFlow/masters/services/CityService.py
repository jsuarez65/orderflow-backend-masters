from repositories.CityRepository import CityRepository
from configuration.LogConfiguration import LogConfiguration


class CityService:

    def __init__(self):
        self.log = LogConfiguration.getLogger()
        self.cityRepository = CityRepository()
    
    def importZipCodes(self, request):
        self.log.info("importZipCodes - Entering zip codes import process")

        if 'file' not in request.files:
            self.log.warning("importZipCodes - No file sent in request")
            return None
        
        file = request.files['file']
        if file.filename == '':
            self.log.warning("importZipCodes - Empty filename")
            return None

        result = self.cityRepository.importZipCodes(file)
        return result
    
    def getPostalCodes(self, postal_code: str = None, city_name: str = None):
        self.log.info("getPostalCodes - Retrieving postal codes")
        return self.cityRepository.getPostalCodes(postal_code, city_name)