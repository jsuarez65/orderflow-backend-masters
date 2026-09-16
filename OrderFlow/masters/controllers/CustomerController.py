from flask import Blueprint, request, jsonify
from services.CustomerService import CustomerService
from model.dtos.CustomerDTO import CustomerDTO
from configuration.LogConfiguration import LogConfiguration

CustomerBlueprint = Blueprint('cliente', __name__, url_prefix='/master/cliente')

customerService = CustomerService()

@CustomerBlueprint.route('', methods=['POST'])
def createCustomer():
    log = LogConfiguration.getLogger()
    json_data = request.get_json()
    
    try:
        # Acá Pydantic valida que el JSON tenga los tipos de datos correctos
        customer = CustomerDTO(**json_data)
    except Exception as ex:
        log.error(f"Error de validación Pydantic: {str(ex)}")
        return {"message": "Error de validación de datos", "error": str(ex)}, 422

    log.info("createCustomer - Ingresa con cliente: ", body=json_data)

    # Convertimos el JSON a un CustomerDTO
    customer = CustomerDTO(**json_data)

    # Como el Service ahora devuelve el cliente guardado o None, cambiamos el IF
    customerCreated = customerService.createCustomer(customer)
    if (customerCreated is not None):
        return {"message": "El cliente se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el cliente"}, 500

@CustomerBlueprint.route('', methods=['GET'])
def getCustomers():
    log = LogConfiguration.getLogger()
    log.info("getCustomers - Ingresa a obtener todos los clientes")

    customers = customerService.getCustomers()
    if customers is not None:
        return jsonify(customers), 200
    else:
        return {"message": "Error al obtener los clientes"}, 500

@CustomerBlueprint.route('', methods=['PUT'])
def updateCustomer():
    log = LogConfiguration.getLogger()
    json_data = request.get_json()
    
    try:
        customer = CustomerDTO(**json_data)
    except Exception as ex:
        log.error(f"Error de validación Pydantic: {str(ex)}")
        return {"message": "Error de validación de datos", "error": str(ex)}, 422

    log.info("updateCustomer - Ingresa con cliente para actualizar: ", body=json_data)

    customer = CustomerDTO(**json_data)

    customerUpdated = customerService.updateCustomer(customer)
    if (customerUpdated is not None):
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