from repositories.CustomerRepository import CustomerRepository
from configuration.LogConfiguration import LogConfiguration

customerRepository = CustomerRepository()

class CustomerService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createCustomer(self, customer):
        self.log.info("createCustomer - Ingresa con cliente: ", body=customer)
        return customerRepository.insert(customer)

    def getCustomers(self):
        self.log.info("getCustomers - Ingresa a buscar todos los cliente")
        return customerRepository.getAll()

    def updateCustomer(self, customer):
        self.log.info("updateCustomer - Ingresa con cliente para actualizar: ", body=customer)
        return customerRepository.update(customer)
    
    def deleteCustomer(self, cuit):
        self.log.info(f"deleteCustomer - Ingresa con CUIT para eliminar: {cuit}")
        return customerRepository.delete(cuit)