from repositories.CitiesRepository import CitiesRepository
from configuration.LogConfiguration import LogConfiguration

citiesRepository = CitiesRepository()

class CitiesService:
    def __init__(self):
        self.log = LogConfiguration.getLogger()
    
    def importPostalCodes(self, request):
        self.log.info("importPostalCodes - Entering postal codes import process")

        if 'file' not in request.files:
            self.log.warning("importPostalCodes - No file sent in request")
            return None
        
        file = request.files['file']
        if file.filename == '':
            self.log.warning("importPostalCodes - Empty filename")
            return None

        result = citiesRepository.importPostalCodes(file)
        return result