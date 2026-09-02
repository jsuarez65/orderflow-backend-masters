from flask import Blueprint, request
from services.PermissionService import PermissionService
from configuration.LogConfiguration import LogConfiguration
from model.dto.permissionDTO import permissionDTO

PermissionBlueprint = Blueprint('permisos', __name__, url_prefix='/permisos')

permissionService = PermissionService()
log = LogConfiguration.getLogger()

@PermissionBlueprint.route('/', methods=['POST'])
def createPermission():
    
    log = LogConfiguration.getLogger()
    
    permission = request.get_json()

    log.info(f"createPermission - Ingresa con permiso: {permission}")

    if not permission or 'nombre' not in permission or 'descripcion' not in permission:
        return {"message": "Los campos 'nombre' y 'descripcion' son obligatorios"}, 400

    if (permissionService.createPermission(permission) == True):
        return {"message": "El permiso se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el permiso"}, 500



@PermissionBlueprint.route('/', methods=['GET'])
def getPermission() -> list[permissionDTO]:
    
    """ 
    Permite recuperar todos los permisos registrados en la base de datos.
    ---
        responses:
            200:
                description: Lista de permisosDTO.
                schema:
                    type: array
                    items:
                        $ref: '#/definitions/permisosDTO'
        definitions:
            permissionDTO:
                type: object
                properties:
                    nombre:
                        type: string
                    descripcion:
                        type: string

    """

    log = LogConfiguration.getLogger()

    log.info(f"getPermission - Ingresa a obtener el permiso: {request.args}")

    permissionFound = permissionService.getPermission(request.args.get('nombre'))

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
    
