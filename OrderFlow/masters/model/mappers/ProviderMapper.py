from decimal import Decimal

from model.entities import ProviderEntity
from model.dtos.ProviderDTO import ProviderDTO

class ProviderMapper:

    @staticmethod
    def toDTO(entity: ProviderEntity) -> ProviderDTO:

        if entity is None:
            return None

        return ProviderDTO(
            cuit=entity.cuit,
            company_name=entity.razonSocial,
            address=entity.domicilio,
            email=entity.email,
            phone=entity.telefono,
            postalCode=entity.localidadCodigoPostal,
            stateName=entity.provinciaNombre
        )
    @staticmethod
    def toEntity(dto: ProviderDTO) -> ProviderEntity:
        
        if dto is None:
            return None

        return ProviderEntity(
            cuit=dto.cuit,
            razonSocial=dto.companyName,
            direccion=dto.address,
            email=dto.email,
            telefono=dto.phone,
            localidadCodigoPostal=dto.postalCode,
            provinciaNombre=dto.stateName
        )

    @staticmethod
    def toListDTO(providers: list[ProviderEntity]) -> list[ProviderDTO]:

        if not providers:
            return []
        
        return [ProviderMapper.toDTO(provider) for provider in providers]
        