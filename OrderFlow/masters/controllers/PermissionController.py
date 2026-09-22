from flask import Blueprint, request
from services.PermissionService import PermissionService
from configuration.LogConfiguration import LogConfiguration
from model.dto import permissionDTO

PermissionBlueprint = Blueprint('permisos', __name__, url_prefix='/permisos')
permissionService = PermissionService()


@PermissionBlueprint.route('/', methods=['POST'])
def createPermission():
    log = LogConfiguration.getLogger()
    body = request.get_json()

    if not body or 'nombre' not in body:
        return {"message": "El campo 'nombre' es obligatorio"}, 400

    log.info("createPermission - Ingresa con permiso: ", body=body)

    permiso = permissionDTO(
        nombre=body['nombre'],
        descripcion=body.get('descripcion')
    )

    if permissionService.createPermission(permiso):
        return {"message": "El permiso se ingresó correctamente"}, 200
    return {"message": "Error al ingresar el permiso"}, 500


@PermissionBlueprint.route('', methods=['GET'])
def getPermission():
    log = LogConfiguration.getLogger()
    nombre = request.args.get('nombre')
    if not nombre:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    log.info(f"getPermission - Ingresa a obtener el permiso: {nombre}")
    permission = permissionService.getPermission(nombre)
    if permission is not None:
        return {"nombre": permission.nombre, "descripcion": permission.descripcion}, 200
    return {"message": f"El permiso '{nombre}' no existe"}, 404


@PermissionBlueprint.route('/', methods=['DELETE'])
def deletePermission():
    log = LogConfiguration.getLogger()
    name = request.args.get('name')
    if not name:
        return {"message": "El parámetro 'name' es obligatorio"}, 400

    log.info(f"deletePermission - Ingresa a eliminar el permiso: {name}")
    if permissionService.deletePermission(name):
        return {"message": f"El permiso '{name}' se eliminó correctamente"}, 200
    return {"message": "Error al eliminar el permiso o el permiso no existe"}, 500


@PermissionBlueprint.route('/', methods=['PUT'])
def updatePermission():
    log = LogConfiguration.getLogger()
    body = request.get_json()
    if not body or 'nombre' not in body:
        return {"message": "El campo 'nombre' es obligatorio"}, 400

    nombreActual = request.args.get('nombreActual', body['nombre'])
    log.info(f"updatePermission - Ingresa a actualizar el permiso: {nombreActual}")

    permiso = permissionDTO(
        nombre=body['nombre'],
        descripcion=body.get('descripcion')
    )

    if permissionService.updatePermission(nombreActual, permiso):
        return {"message": "El permiso se actualizó correctamente"}, 200
    return {"message": "Error al actualizar el permiso"}, 500