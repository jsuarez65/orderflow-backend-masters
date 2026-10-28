<<<<<<< Updated upstream
=======
from model.dtos.ProviderDTO import ProviderDTO
from repositories.ProviderRepository import ProviderRepository
from configuration.LogConfiguration import LogConfiguration
>>>>>>> Stashed changes

from model.mappers.ProviderMapper import ProviderMapper
from model.dtos import ProviderDTO
from repositories.ProviderRepository import ProviderRepository


class ProviderService:
<<<<<<< Updated upstream
         
    def __init__(self,log, session): #recibe el log y la session de la base de datos por inyeccion de dependencias para poder usarlo en los metodos de la clase y para poder crear una instancia de ProviderRepository con la session de la base de datos
        self.log = log
        self.providerRepository = ProviderRepository(session)

    def findAll(self) -> list[ProviderDTO]:

        providerEntities = self.providerRepository.findAll()
        return ProviderMapper.toListDTO(providerEntities)  
    
    def create(self, provider: ProviderDTO) -> ProviderDTO | None:
        
        self.log.info("create - Ingresa con provider: ", body=provider)

        if self.providerRepository.existsById(provider.cuit):
            self.log.warning("create - El proveedor ya existe: ", body=provider)
=======
    
     
    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProvider(self, provider: ProviderDTO):
        
        self.log.info("createProvider - Ingresa con provider: ", body=provider)

        if providerRepository.findById(provider.cuit):
            self.log.warning("createProvider - El proveedor ya existe: ", body=provider)
>>>>>>> Stashed changes
            return None

        providerToCreate = ProviderMapper.toEntity(provider)
        return ProviderMapper.toDTO(self.providerRepository.save(providerToCreate))

<<<<<<< Updated upstream
    def update(self, provider: ProviderDTO) -> ProviderDTO | None:

        self.log.info("update - Ingresa con provider: ", body=provider)

        if not self.providerRepository.existsById(provider.cuit):
            self.log.warning("update - El proveedor no existe: ", body=provider)
            return None

        providerToUpdate = ProviderMapper.toEntity(provider)
        return ProviderMapper.toDTO(self.providerRepository.save(providerToUpdate))

    def delete(self, cuit):
        """
        Lógica de negocio para la eliminación del proveedor.
        """
        return self.providerRepository.deleteProvider(cuit)
=======
    def updateProvider(self, provider: ProviderDTO):
        
        self.log.info("updateProvider - Ingresa con provider: ", body=provider)

        if providerRepository.existsById(provider.cuit):
            return providerRepository.save(provider)
        else:
            self.log.warning("updateProvider - El proveedor no existe: ", body=provider)
            return False

   def deleteProvider(self, cuit: str):
    """
    Lógica de negocio para la eliminación del proveedor.
    """
    return providerRepository.deleteProvider(cuit)
>>>>>>> Stashed changes
