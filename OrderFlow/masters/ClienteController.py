from flask import Blueprint, request
from services.ClienteService import ClienteService
from configuration.LogConfiguration import LogConfiguration

# CORRECCIÓN: Ahora el blueprint es 'cliente' y la ruta es /master/cliente
ClienteBlueprint = Blueprint('cliente', __name__, url_prefix='/master/cliente')

# CORRECCIÓN: Llama al servicio de clientes, no al de productos
clienteService = ClienteService()

# 1. POST (El que vino de ejemplo, pero adaptado a clientes)
@ClienteBlueprint.route('', methods=['POST'])
def createCliente():
    log = LogConfiguration.getLogger()
    cliente = request.get_json()

    log.info("createCliente - Ingresa con cliente: ", body=cliente)

    if (clienteService.createCliente(cliente) == True):
        return {"message": "El cliente se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el cliente"}, 500

# 2. GET (Agregado para cumplir la tarea)
@ClienteBlueprint.route('', methods=['GET'])
def getClientes():
    log = LogConfiguration.getLogger()
    log.info("getClientes - Ingresa a obtener todos los clientes")

    clientes = clienteService.getClientes()
    if clientes is not None:
        return clientes, 200
    else:
        return {"message": "Error al obtener los clientes"}, 500

# 3. PUT (Agregado para cumplir la tarea)
@ClienteBlueprint.route('', methods=['PUT'])
def updateCliente():
    log = LogConfiguration.getLogger()
    cliente = request.get_json()

    log.info("updateCliente - Ingresa con cliente para actualizar: ", body=cliente)

    if (clienteService.updateCliente(cliente) == True):
        return {"message": "El cliente se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el cliente"}, 500

# 4. DELETE (Agregado para cumplir la tarea)
@ClienteBlueprint.route('', methods=['DELETE'])
def deleteCliente():
    log = LogConfiguration.getLogger()
    id_cliente = request.args.get('id') 

    log.info(f"deleteCliente - Ingresa para eliminar el ID: {id_cliente}")

    if (clienteService.deleteCliente(id_cliente) == True):
        return {"message": "El cliente se eliminó correctamente"}, 200
    else:
        return {"message": "Error al eliminar el cliente"}, 500