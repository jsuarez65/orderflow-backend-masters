        
from flask import Blueprint, request
from services.UsersService import UsersService
from configuration.LogConfiguration import LogConfiguration

usersBlueprint = Blueprint('users', __name__, url_prefix='/users')

usersService = UsersService()
log = LogConfiguration.getLogger()


@usersBlueprint.route('/', methods=['POST'])
def createUser():
    
    userData = request.get_json()
    
    log.info("createUser - Ingresa con usuario: ", body=userData)

    # Validamos que existan los 3 campos
    if not userData or 'username' not in userData or 'password' not in userData or 'rol' not in userData:
        return {"message": "Los campos 'username', 'password' y 'rol' son obligatorios"}, 400

    if usersService.createUser(userData):
        return {"message": "El usuario se ingresó correctamente"}, 201
    else:
        return {"message": "Error al ingresar el usuario o ya existe"}, 500


@usersBlueprint.route('/buscar', methods=['GET'])
def getUser():

    nameUser = request.args.get('nombre')
    
    log.info(f"getUser - Ingresa a obtener el usuario: {nameUser}")

    if not nameUser:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    user = usersService.getUser(nameUser)

    if user:
        return {"message": "Usuario encontrado", "user": user}, 200
    else:
        return {"message": "Usuario no encontrado"}, 404


@usersBlueprint.route('/<nombre>', methods=['PUT'])
def updateUser(nombre):
    
    userData = request.get_json()

    # Validamos que lleguen los 3 campos para actualizar
    if not userData or 'username' not in userData or 'password' not in userData or 'rol' not in userData:
        return {"message": "Los campos 'username', 'password' y 'rol' son obligatorios en el body"}, 400

    if usersService.updateUser(nombre, userData):
        return {"message": f"El usuario '{nombre}' se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el usuario (no existe o el nuevo username ya está en uso)"}, 500


@usersBlueprint.route('/<nombre>', methods=['DELETE'])
def deleteUser(nombre):
    
    if usersService.deleteUser(nombre):
        return {"message": f"El usuario '{nombre}' se eliminó correctamente"}, 200
    else:
        return {"message": f"Error al eliminar el usuario '{nombre}' o no existe"}, 404

