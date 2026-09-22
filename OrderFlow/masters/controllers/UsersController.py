from flask import Blueprint, request
from services.UsersService import UsersService
from configuration.LogConfiguration import LogConfiguration
from model.dto import userDTO

usersBlueprint = Blueprint('users', __name__, url_prefix='/users')
usersService = UsersService()


@usersBlueprint.route('/', methods=['POST'])
def createUser():
    log = LogConfiguration.getLogger()
    body = request.get_json()

    if (not body or 'username' not in body
            or 'password' not in body or 'rol' not in body):
        return {"message": "Los campos 'username', 'password' y 'rol' son obligatorios"}, 400

    log.info(f"createUser - Ingresa con usuario: {body['username']}", body=body)

    user = userDTO(
        username=body['username'],
        password=body['password'],
        rol=body['rol']
    )

    if usersService.createUser(user):
        return {"message": "El usuario se ingresó correctamente"}, 201
    return {"message": "Error al ingresar el usuario o ya existe"}, 500


@usersBlueprint.route('/<name>', methods=['GET'])
def getUser(name):
    log = LogConfiguration.getLogger()
    log.info("getUser - Ingresa a obtener el usuario: ", body=name)
    if not name:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    user = usersService.getUser(name)
    if user is not None:
        return {
            "message": "Usuario encontrado",
            "user": {"username": user.username, "rol": user.rol}
        }, 200
    return {"message": "Usuario no encontrado"}, 404


@usersBlueprint.route('/', methods=['PUT'])
def updateUser():
    log = LogConfiguration.getLogger()
    body = request.get_json()
    if (not body or 'currentUsername' not in body
            or 'username' not in body
            or 'password' not in body
            or 'rol' not in body):
        return {"message": "Los campos 'currentUsername', 'username', 'password' y 'rol' son obligatorios"}, 400

    user = userDTO(
        username=body['username'],
        password=body['password'],
        rol=body['rol']
    )

    if usersService.updateUser(body['currentUsername'], user):
        return {"message": f"El usuario '{body['currentUsername']}' se actualizó correctamente"}, 200
    return {"message": "Error al actualizar el usuario"}, 500


@usersBlueprint.route('/<name>', methods=['DELETE'])
def deleteUser(name):
    log = LogConfiguration.getLogger()
    log.info("deleteUser - Ingresa a eliminar el usuario: ", body=name)
    if usersService.deleteUser(name):
        return {"message": f"El usuario '{name}' se eliminó correctamente"}, 200
    return {"message": f"Error al eliminar el usuario '{name}' o no existe"}, 404