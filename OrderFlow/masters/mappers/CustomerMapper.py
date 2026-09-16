from model.entities.CustomerEntity import CustomerEntity
from model.dtos.CustomerDTO import CustomerDTO

class CustomerMapper:

    @staticmethod
    def toDTO(entity: CustomerEntity) -> CustomerDTO:

        if entity is None:
            return None

        return CustomerDTO(
            cuit=entity.cuit,
            razonSocial=entity.razonSocial,
            telefono=entity.telefono,
            email=entity.email
        )

    @staticmethod
    def toEntity(dto: CustomerDTO) -> CustomerEntity:
        
        if dto is None:
            return None

        return CustomerEntity(
            cuit=dto.cuit,
            razonSocial=dto.razonSocial,
            telefono=dto.telefono,
            email=dto.email
        )

    @staticmethod
    def toListDTO(customers: list[CustomerEntity]) -> list[CustomerDTO]:

        if not customers:
            return []
        
        return [CustomerMapper.toDTO(customer) for customer in customers]