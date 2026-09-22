from flask import Blueprint, request
from services.RolService import RolService
from repositories.RolRepository import DeleteResult
from configuration.LogConfiguration import LogConfiguration
from model.dto import rolDTO

roleBlueprint = Blueprint('rols', __name__, url_prefix='/rols')
roleService = RolService()


@roleBlueprint.route('/', methods=['POST'])
def createRol():
    log = LogConfiguration.getLogger()
    body = request.get_json()
    if not body or 'rol' not in body:
        return {"message": "El campo 'rol' es obligatorio"}, 400

    log.info("createRol - Ingresa con rol: ", body=body)
    rol = rolDTO(rol=body['rol'])

    if roleService.createRol(rol):
        return {"message": "El rol se ingresó correctamente"}, 201
    return {"message": "Error al ingresar el rol o ya existe"}, 500


@roleBlueprint.route('/<name>', methods=['GET'])
def getRol(name):
    log = LogConfiguration.getLogger()
    log.info("getRol - Ingresa a obtener el rol: ", body=name)
    role = roleService.getRol(name)
    if role is not None:
        return {"rol": role.rol}, 200
    return {"message": "Rol no encontrado"}, 404


@roleBlueprint.route('/<name>', methods=['DELETE'])
def deleteRol(name):
    log = LogConfiguration.getLogger()
    log.info("deleteRol - Ingresa a eliminar el rol: ", body=name)

    result = roleService.deleteRol(name)

    if result == DeleteResult.OK:
        return {"message": f"El rol '{name}' se eliminó correctamente"}, 200
    if result == DeleteResult.NOT_FOUND:
        return {"message": f"El rol '{name}' no existe"}, 404
    if result == DeleteResult.IN_USE:
        return {"message": (
            f"No se puede eliminar el rol '{name}' porque está asignado "
            f"a uno o más usuarios."
        )}, 409
    return {"message": f"Error interno al eliminar el rol '{name}'"}, 500