from model.dtos import ProviderDTO
from model.entities import ProviderEntity



class ProviderRepository:
   
    def __init__(self, log, session):
        self.session = session
        self.log = log

    def findAll(self) -> list[ProviderEntity]:

        try:
            return self.session.query(ProviderEntity).all()
        except Exception as ex:
            self.log.error(f"findAll - Error al obtener todos los proveedores: {str(ex)}")
            return []

    def save(self, provider: ProviderEntity) -> ProviderEntity | None:


        try:
            providerFound = self.findBycuit(provider.cuit)

            if providerFound:
                self.log.warning(
                    f"save - El proveedor ya existe, se procederá a actualizarlo: {provider}"
                )
                return self._update(providerFound, provider)

            return self._insert(provider)

        except Exception as ex:
            self.log.error(f"save - Error al guardar proveedor: {str(ex)}")
            self.session.rollback()
            return None

    def existsById(self, cuit:str) -> bool:
        return self._findBycuit(cuit) is not None

    def _findBycuit(self, cuit:str) -> ProviderEntity | None:
        
        try:
            return (
                self.session.query(ProviderEntity)
                .filter(ProviderEntity.cuit == cuit)
                .first()
            )

        except Exception as ex:
            self.log.error(
                f"_findBycuit - Error al buscar proveedor: {str(ex)}"
            )
            return None


    def _insert(self, provider: ProviderEntity) -> ProviderEntity:
        
        self.session.add(provider)
        self.session.commit()
        
        return provider

    def update(self,entityToUpdate: ProviderEntity, entity: ProviderEntity) -> ProviderEntity:
        
        entityToUpdate.cuit = entity.cuit
        entityToUpdate.razonSocial = entity.company_name
        entityToUpdate.domicilio = entity.address
        entityToUpdate.email = entity.email
        entityToUpdate.telefono = entity.phone
        entityToUpdate.localidad_codigo_postal = entity.postal_code
        entityToUpdate.provincia_nombre = entity.state_name
        


        self.session.commit()

        return entityToUpdate