from flask import Blueprint, request
from services.PermissionService import PermissionService
from configuration.LogConfiguration import LogConfiguration

PermissionBlueprint = Blueprint('permisos', __name__, url_prefix='/permisos')

permissionService = PermissionService()

@PermissionBlueprint.route('/<nombre>', methods=['POST'])
def createPermission(nombre):
    
    log = LogConfiguration.getLogger()
    
    permission = request.get_json()

    log.info(f"createPermission - Ingresa con permiso: {permission}")

    if not permission or 'nombre' not in permission or 'descripcion' not in permission:
        return {"message": "Los campos 'nombre' y 'descripcion' son obligatorios"}, 400

    if (permissionService.createPermission(permission) == True):
        return {"message": "El permiso se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el permiso"}, 500



@PermissionBlueprint.route('/<nombre>', methods=['GET'])
def getPermission(nombre):

    log = LogConfiguration.getLogger()

    log.info(f"getPermission - Ingresa a obtener el permiso: {nombre}")

    permissionFound = permissionService.getPermission(nombre)

    if permissionFound:
        return permissionFound, 200
    else:
        return {"message": "Permiso no encontrado"}, 404
    
    
@PermissionBlueprint.route('/<nombre>', methods=['DELETE'])
def deletePermission(nombre):
    
    log = LogConfiguration.getLogger()
    
    log.info(f"deletePermission - Ingresa a eliminar el permiso: {nombre}")
    
    if (permissionService.deletePermission(nombre) == True):
        return {"message": f"El permiso '{nombre}' se eliminó correctamente"}, 200
    else:
        return {"message": "Error al eliminar el permiso o el permiso no existe"}, 500
    
    
@PermissionBlueprint.route('/', methods=['PUT'])
def updatePermission():
    log = LogConfiguration.getLogger()
    
    permission = request.get_json()
    
    log.info(f"updatePermission - Ingresa a actualizar el permiso: {permission}")

    if (
        not permission
        or 'nombreActual' not in permission
        or 'nombre' not in permission
        or 'descripcion' not in permission
    ):
        return {"message": "Los campos 'nombreActual', 'nombre' y 'descripcion' son obligatorios"}, 400

    if permissionService.updatePermission(permission['nombreActual'], permission):
        return {"message": "El permiso se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el permiso"}, 500
    
