from flask import Blueprint, request
from services.RolService import RolService
from configuration.LogConfiguration import LogConfiguration
from model.dto.rolDTO import rolDTO

roleBlueprint = Blueprint('rols', __name__, url_prefix='/rols')

roleService = RolService()
log = LogConfiguration.getLogger()


@roleBlueprint.route('/', methods=['POST'])
def createRol():
    
    roleData = request.get_json()

    if not roleData or 'rol' not in roleData:
        return {"message": "El campo 'rol' es obligatorio"}, 400

    if (roleService.createRol(roleData) == True):
        return {"message": "El rol se ingresó correctamente"}, 201
    else:
        return {"message": "Error al ingresar el rol o ya existe"}, 500


@roleBlueprint.route('/<name>', methods=['GET'])
def getRol(name) -> list[rolDTO]:
    """
    permite recuperar un rol registrado en la base de datos por su nombre.
    ---
        responses:
            200:
                description: Rol encontrado.
                schema:
                    $ref: '#/definitions/rolDTO'
        definitions:
            rolDTO:
                type: object
                properties:
                    rol:
                        type: string
    """
    

    log.info(f"getRol - Ingresa a obtener el rol: {name}")

    if not name:
        return {"message": "El parámetro 'nombre' es obligatorio"}, 400

    role = roleService.getRol(name)

    if role:
        return role, 200
    else:
        return {"message": "Rol no encontrado"}, 404
    



@roleBlueprint.route('/<name>', methods=['DELETE'])
def deleteRol(name):
    
    if roleService.deleteRol(name):
        return {"message": f"El rol '{name}' se eliminó correctamente"}, 200
    else:
        return {"message": f"Error al eliminar el rol '{name}' o no existe"}, 404