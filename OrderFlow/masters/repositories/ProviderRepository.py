<<<<<<< Updated upstream

from model.entities import ProviderEntity
from model.dtos import ProviderDTO


=======
from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration
from model.dtos.ProviderDTO import ProviderDTO
>>>>>>> Stashed changes

class ProviderRepository:
   
    def __init__(self, log, session):
        self.session = session
        self.log = log

<<<<<<< Updated upstream
    def findAll(self) -> list[ProviderEntity]:#que le llega y que devuelve 
=======
    def save(self, provider : ProviderDTO) -> ProviderDTO | None:
        
        sqlCommand = None
>>>>>>> Stashed changes

        try:
            return self.session.query(ProviderEntity).all()
        
        except Exception as ex:
            self.log.error(f"findAll - Error al obtener todos los proveedores: {str(ex)}")
            return []

<<<<<<< Updated upstream
    def save(self, provider: ProviderEntity) -> ProviderEntity | None:#que le llega y que devuelve 

        try:
            providerFound = self._findByCuit(provider.cuit)
=======
            providerFound = self.existsById(provider.cuit)
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    def existsById(self, cuit:str) -> bool:#que le llega y que devuelve 
        return self._findByCuit(cuit) is not None
=======
        finally:
            if sqlCommand:
                sqlCommand.close()

    def existsById(self, cuit: str) -> bool:

        sqlCommand = None
>>>>>>> Stashed changes

    def _findByCuit(self, cuit:str) -> ProviderEntity | None:
        
        try:
            return (
                self.session.query(ProviderEntity)
                .filter(ProviderEntity.cuit == cuit)
                .first()
            )

        except Exception as ex:
<<<<<<< Updated upstream
            self.log.error(
                f"_findByCuit - Error al buscar proveedor: {str(ex)}"
            )
            return None
=======
            self.log.error(f"existsById - Error al buscar proveedor por CUIT: {str(ex)}")
            return False
>>>>>>> Stashed changes


<<<<<<< Updated upstream
    def _insert(self, provider: ProviderEntity) -> ProviderEntity:
        
        self.session.add(provider)
        self.session.commit()
        
        return provider

    def _update(self,entityToUpdate: ProviderEntity, entity: ProviderEntity) -> ProviderEntity:
        
        entityToUpdate.cuit = entity.cuit
        entityToUpdate.razonSocial = entity.companyName
        entityToUpdate.domicilio = entity.address
        entityToUpdate.email = entity.email
        entityToUpdate.telefono = entity.phone
        entityToUpdate.localidadCodigoPostal = entity.postalCode
        entityToUpdate.provinciaNombre = entity.stateName
        entityToUpdate.ciudad = entity.city

        self.session.commit()
=======
    def _insert(self, sqlCommand, provider: ProviderDTO) -> ProviderDTO | None:
        
        sqlCommand.execute("""
            INSERT INTO Proveedores (cuit, razon_social, domicilio, email, telefono, localidad_codigo_postal, provincia_nombre)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            provider.cuit,
            provider.company_name,
            provider.address,
            provider.email,
            provider.phone,
            provider.postal_code,
            provider.state_name
        ))
        return provider

    def _update(self, sqlCommand, provider: ProviderDTO) -> ProviderDTO | None:
        
        sqlCommand.execute("""
            UPDATE Proveedores SET razon_social=%s, domicilio=%s, telefono=%s, email=%s
            WHERE cuit=%s""", (
                provider.cuit,
                provider.company_name,
                provider.address,
                provider.email,
                provider.phone,
                provider.postal_code,
                provider.state_name,
                
            ))
        return provider

    def deleteProvider(self, cuit: str):  
        sqlCommand = None
>>>>>>> Stashed changes

        return entityToUpdate