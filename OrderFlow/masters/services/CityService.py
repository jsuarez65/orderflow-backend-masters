from repositories.CityRepository import CityRepository

class CityService:
    def __init__(self, log, session):
        self.log = log
        self.session = session
        self.cityRepository = CityRepository(log, session)
    
    def importZipCodes(self, request):
        if 'file' not in request.files:
            return None
        
        file = request.files['file']
        if file.filename == '':
            return None

        return self.cityRepository.importZipCodes(file)
    
    def getPostalCodes(self, postalCode: str = None, cityName: str = None):
        return self.cityRepository.getPostalCodes(postalCode, cityName)