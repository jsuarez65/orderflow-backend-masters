from model.dtos.CustomerDTO import CustomerDTO
from repositories.CustomerRepository import CustomerRepository
from configuration.LogConfiguration import LogConfiguration

customerRepository = CustomerRepository()

class CustomerService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createCustomer(self, customer: CustomerDTO):
        self.log.info("createCustomer - Ingresa con customer: ", body=customer)
        return customerRepository.save(customer)

    def getCustomers(self):
        self.log.info("getCustomers - Ingresa a obtener todos los clientes")
        return customerRepository.getAllCustomers()

    def updateCustomer(self, customer: CustomerDTO):
        self.log.info("updateCustomer - Ingresa con customer para actualizar: ", body=customer)
        return customerRepository.save(customer)

    def deleteCustomer(self, cuit: str):
        self.log.info(f"deleteCustomer - Ingresa para eliminar el CUIT: {cuit}")
        return customerRepository.deleteCustomer(cuit)