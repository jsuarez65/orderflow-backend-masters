from repositories.ClienteRepository import ClienteRepository
from configuration.LogConfiguration import LogConfiguration

# Instanciamos el repositorio de forma global, tal cual lo hace el profe
clienteRepository = ClienteRepository()

class ClienteService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    # 1. POST
    def createCliente(self, cliente):
        self.log.info("createCliente - Ingresa con cliente: ", body=cliente)
        return clienteRepository.insert(cliente)

    # 2. GET
    def getClientes(self):
        self.log.info("getClientes - Ingresa a buscar todos los clientes")
        return clienteRepository.getAll()

    # 3. PUT
    def updateCliente(self, cliente):
        self.log.info("updateCliente - Ingresa con cliente para actualizar: ", body=cliente)
        return clienteRepository.update(cliente)

    # 4. DELETE
    def deleteCliente(self, id_cliente):
        self.log.info(f"deleteCliente - Ingresa con ID para eliminar: {id_cliente}")
        return clienteRepository.delete(id_cliente)