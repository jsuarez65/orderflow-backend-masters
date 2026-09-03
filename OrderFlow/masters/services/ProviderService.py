from repositories.ProviderRepository import ProviderRepository
from configuration.LogConfiguration import LogConfiguration

providerRepository = ProviderRepository() 

class ProviderService:
    
     
    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProvider(self, provider):
        
        self.log.info("createProvider - Ingresa con provider: ", body=provider)

        if providerRepository.findById(provider['cuit']):
            self.log.warning("createProvider - El proveedor ya existe: ", body=provider)
            return None

        return providerRepository.save(provider)

    def updateProvider(self, provider):
        
        self.log.info("updateProvider - Ingresa con provider: ", body=provider)

        if providerRepository.findById(provider['cuit']):
            return providerRepository.save(provider)
        else:
            self.log.warning("updateProvider - El proveedor no existe: ", body=provider)
            return False

    def deleteProvider(self, cuit):
        """
        Lógica de negocio para la eliminación del proveedor.
        """
        return providerRepository.deleteProvider(cuit)