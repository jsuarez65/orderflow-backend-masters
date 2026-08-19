from flask import Blueprint, request
from services.RolService import RolService
from configuration.LogConfiguration import LogConfiguration

rolBlueprint = Blueprint('roles', __name__, url_prefix='/roles')

rolService = RolService()
log = LogConfiguration.getLogger()


@rolBlueprint.route('/', methods=['POST'])
def createRol():
    
    rolData = request.get_json()

    if not rolData or 'rol' not in rolData:
        return {"message": "El campo 'rol' es obligatorio"}, 400

    if (rolService.createRol(rolData) == True):
        return {"message": "El rol se ingresó correctamente"}, 201
    else:
        return {"message": "Error al ingresar el rol o ya existe"}, 500


@rolBlueprint.route('/<nombre>', methods=['GET'])
def getRol(nombre):

    log.info(f"getRol - Ingresa a obtener el rol: {nombre}")

    if not nombre:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    rol = rolService.getRol(nombre)

    if rol:
        return rol, 200
    else:
        return {"message": "Rol no encontrado"}, 404
    



@rolBlueprint.route('/<nombre>', methods=['DELETE'])
def deleteRol(nombre):
    
    if rolService.deleteRol(nombre):
        return {"message": f"El rol '{nombre}' se eliminó correctamente"}, 200
    else:
        return {"message": f"Error al eliminar el rol '{nombre}' o no existe"}, 404