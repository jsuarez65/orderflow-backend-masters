from flask import Blueprint, request
from services.PermissionService import PermissionService
from configuration.LogConfiguration import LogConfiguration

PermissionBlueprint = Blueprint('permisos', __name__, url_prefix='/permisos')

permissionService = PermissionService()

@PermissionBlueprint.route('/', methods=['POST'])
def createPermisos():
    
    log = LogConfiguration.getLogger()
    
    permisos = request.get_json()

    log.info("createPermisos - Ingresa con permisos: ", body=permisos)

    if (permissionService.createPermission(permisos) == True):
        return {"message": "El permiso se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el permiso"}, 500



@PermissionBlueprint.route('/buscar', methods=['GET'])
def getPermission():

    log = LogConfiguration.getLogger()

    NamePermission = request.args.get('nombre')

    log.info(f"getPermisos - Ingresa a obtener el permiso: {NamePermission}")

    if (permissionService.getPermisos(NamePermission) == True):
        return {"message": "Los permisos se obtuvieron correctamente"}, 200
    else:
        return {"message": "Error al obtener los permisos"}, 500
    
    
@PermissionBlueprint.route('/<nombre>', methods=['DELETE'])
def deletePermission(nombre):
    
    log = LogConfiguration.getLogger()
    
    log.info(f"deletePermission - Ingresa a eliminar el permiso: {nombre}")
    
    # Llamamos al servicio pasando el nombre
    if (permissionService.deletePermission(nombre) == True):
        return {"message": f"El permiso '{nombre}' se eliminó correctamente"}, 200
    else:
        return {"message": "Error al eliminar el permiso o el permiso no existe"}, 500
    
    
@PermissionBlueprint.route('/', methods=['PUT'])
def updatePermission():
    log = LogConfiguration.getLogger()
    
    permisos = request.get_json()
    
    log.info(f"updatePermission - Ingresa a actualizar el permiso: ", body=permisos)

    if (permissionService.createPermission(permisos) == True):
        return {"message": "El permiso se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el permiso"}, 500
    
