from repositories.ProviderRepository import ProviderRepository
from configuration.LogConfiguration import LogConfiguration

providerRepository = ProviderRepository() 

class ProviderService:
    
    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def createProvider(provider):
    
        self.log.info("createProvider - Ingresa con provider: ", body=provider)
        return providerRepository.insertProvider(provider)