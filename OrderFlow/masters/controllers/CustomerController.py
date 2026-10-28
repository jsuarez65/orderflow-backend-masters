from flask import Blueprint, request, jsonify
from dataclasses import asdict
from services.CustomerService import CustomerService
from model.dtos.CustomerDTO import CustomerDTO
from configuration.LogConfiguration import LogConfiguration

CustomerBlueprint = Blueprint('cliente', __name__, url_prefix='/master/cliente')

customerService = CustomerService()

@CustomerBlueprint.route('', methods=['POST'])
def createCustomer():
    log = LogConfiguration.getLogger()
    json_data = request.get_json()
    
    customer = CustomerDTO(**json_data)
    
    log.info("createCustomer - Ingresa con cliente: ", body=customer)

    customerCreated = customerService.createCustomer(customer)
    if (customerCreated is not None):
        return {customerCreated}, 200
    else:
        return {"message": "Error al ingresar el cliente"}, 500


@CustomerBlueprint.route('', methods=['GET'])
def getCustomers() -> tuple[list[dict], int]:

    log = LogConfiguration.getLogger()

    log.info("getCustomers - Ingresa a obtener todos los clientes")

    customers = customerService.getCustomers()
    if customers is not None:
        return [asdict(customer) for customer in customers], 200
    else:
        return {"message": "Error al obtener los clientes"}, 500

@CustomerBlueprint.route('', methods=['PUT'])
def updateCustomer():

    log = LogConfiguration.getLogger()
    json_data = request.get_json()
    
    customer = CustomerDTO(**json_data)
    
    log.info("updateCustomer - Ingresa con cliente para actualizar: ", 
             body=customer)

    customerUpdated = customerService.updateCustomer(customer)
    if (customerUpdated is not None):
        return {customerUpdated}, 200
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