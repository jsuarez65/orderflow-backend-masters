from flask import Blueprint, request
from services.CustomerService import CustomerService
from configuration.LogConfiguration import LogConfiguration


CustomerBlueprint = Blueprint('cliente', __name__, url_prefix='/master/cliente')

customerService = CustomerService()

@CustomerBlueprint.route('', methods=['POST'])
def createCustomer():
    log = LogConfiguration.getLogger()
    customer = request.get_json()

    log.info("createCustomer - Ingresa con cliente: ", body=customer)

    if (customerService.createCustomer(customer) == True):
        return {"message": "El cliente se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el cliente"}, 500

@CustomerBlueprint.route('', methods=['GET'])
def getCustomers():
    log = LogConfiguration.getLogger()
    log.info("getCustomers - Ingresa a obtener todos los clientes")

    customers = customerService.getCustomers()
    if customers is not None:
        return customers, 200
    else:
        return {"message": "Error al obtener los clientes"}, 500

@CustomerBlueprint.route('', methods=['PUT'])
def updateCustomer():
    log = LogConfiguration.getLogger()
    customer = request.get_json()

    log.info("updateCustomer - Ingresa con cliente para actualizar: ", body=customer)

    if (customerService.updateCustomer(customer) == True):
        return {"message": "El cliente se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el cliente"}, 500

@CustomerBlueprint.route('', methods=['DELETE'])
def deleteCustomer():
    log = LogConfiguration.getLogger()
    cuit = request.args.get('cuit')

    log.info(f"deleteCustomer - Ingresa para eliminar el CUIT: {cuit}")

    if (customerService.deleteCustomer(cuit) == True):
        return {"message": "El cliente se eliminó correctamente"}, 200
    else:
        return {"message": "Error al eliminar el cliente"}, 500
    