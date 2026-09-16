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
            address=entity.direccion,
            email=entity.email,
            phone=entity.telefono,
            postal_code=entity.localidad_codigo_postal,
            state_name=entity.localidad_nombre
        )
    @staticmethod
    def toEntity(dto: ProviderDTO) -> ProviderEntity:
        
        if dto is None:
            return None

        return ProviderEntity(
            cuit=dto.cuit,
            razonSocial=dto.company_name,
            direccion=dto.address,
            email=dto.email,
            telefono=dto.phone,
            localidad_codigo_postal=dto.postal_code,
            localidad_nombre=dto.state_name
        )

    @staticmethod
    def toListDTO(providers: list[ProviderEntity]) -> list[ProviderDTO]:

        if not providers:
            return []
        
        return [ProviderMapper.toDTO(provider) for provider in providers]
        