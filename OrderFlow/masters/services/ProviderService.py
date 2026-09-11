
from OrderFlow.masters.model.mappers.ProvoderMapper import ProviderMapper
from model.dtos import ProviderDTO
from repositories.ProviderRepository import ProviderRepository


class ProviderService:
         
    def __init__(self,log, session): 
        self.log = log
        self.providerRepository = ProviderRepository(session)

    def findAll(self) -> list[ProviderDTO]:

        providerEntities = self.providerRepository.findAll()
        return ProviderMapper.toListDTO(providerEntities)  
    
    def create(self, provider: ProviderDTO) -> ProviderDTO | None:
        
        self.log.info("create - Ingresa con provider: ", body=provider)

        if self.providerRepository.existsById(provider.cuit):
            self.log.warning("create - El proveedor ya existe: ", body=provider)
            return None

        providerToCreate = ProviderMapper.toEntity(provider)
        return ProviderMapper.toDTO(self.providerRepository.save(providerToCreate))

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
