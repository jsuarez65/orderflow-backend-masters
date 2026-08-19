        
from flask import Blueprint, request
from services.UsersService import UsersService
from configuration.LogConfiguration import LogConfiguration

usersBlueprint = Blueprint('users', __name__, url_prefix='/users')

usersService = UsersService()
log = LogConfiguration.getLogger()


@usersBlueprint.route('/<name>', methods=['POST'])
def createUser(name):
    
    userData = request.get_json()
    
    log.info(f"createUser - Ingresa con usuario: {name}", body=userData)

    
    if not userData or 'username' not in userData or 'password' not in userData or 'rol' not in userData:
        return {"message": "Los campos 'username', 'password' y 'rol' son obligatorios"}, 400

    if usersService.createUser(userData):
        return {"message": "El usuario se ingresó correctamente"}, 201
    else:
        return {"message": "Error al ingresar el usuario o ya existe"}, 500


@usersBlueprint.route('/<name>', methods=['GET'])
def getUser(name):

    log.info(f"getUser - Ingresa a obtener el usuario: {name}")

    if not name:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    user = usersService.getUser(name)

    if user:
        return {"message": "Usuario encontrado", "user": user}, 200
    else:
        return {"message": "Usuario no encontrado"}, 404


@usersBlueprint.route('/', methods=['PUT'])
def updateUser():
    
    userData = request.get_json()

    isUserDataIncomplete = (
        not userData
        or 'currentUsername' not in userData
        or 'username' not in userData
        or 'password' not in userData
        or 'rol' not in userData
    )
    if isUserDataIncomplete:
        return {"message": "Los campos 'currentUsername', 'username', 'password' y 'rol' son obligatorios en el body"}, 400

    if usersService.updateUser(userData['currentUsername'], userData):
        return {"message": f"El usuario '{userData['currentUsername']}' se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el usuario (no existe o el nuevo username ya está en uso)"}, 500


@usersBlueprint.route('/<name>', methods=['DELETE'])
def deleteUser(name):
    
    if usersService.deleteUser(name):
        return {"message": f"El usuario '{name}' se eliminó correctamente"}, 200
    else:
        return {"message": f"Error al eliminar el usuario '{name}' o no existe"}, 404

