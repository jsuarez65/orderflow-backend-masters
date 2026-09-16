from configuration.DatabaseConfiguration import sessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.CustomerEntity import CustomerEntity
from mappers.CustomerMapper import CustomerMapper
from model.dtos.CustomerDTO import CustomerDTO

class CustomerRepository:

    def __init__(self):
        self.log = LogConfiguration.getLogger()

    def save(self, customer_dto: CustomerDTO) -> CustomerDTO | None:
        session = sessionLocal()
        try:
            # 1. El Mapper convierte el DTO a Entity
            entity = CustomerMapper.toEntity(customer_dto)
            
            # 2. SQLAlchemy hace el INSERT o UPDATE
            session.merge(entity)
            session.commit()
            
            # 3. El Mapper convierte la Entity guardada de vuelta a DTO
            return CustomerMapper.toDTO(entity)

        except Exception as ex:
            session.rollback()
            self.log.error(f"Error guardando cliente: {str(ex)}")
            return None

        finally:
            session.close()

    def getAllCustomers(self) -> list[CustomerDTO]:
        session = sessionLocal()
        try:
            entities = session.query(CustomerEntity).all()
            return CustomerMapper.toListDTO(entities)
        except Exception as ex:
            self.log.error(f"Error obteniendo clientes: {str(ex)}")
            return []
        finally:
            session.close()

    def deleteCustomer(self, cuit: str) -> bool:
        session = sessionLocal()
        try:
            entity = session.query(CustomerEntity).filter(CustomerEntity.cuit == cuit).first()
            if entity:
                session.delete(entity)
                session.commit()
                return True
            return False
        except Exception as ex:
            session.rollback()
            self.log.error(f"Error eliminando cliente: {str(ex)}")
            return False
        finally:
            session.close()