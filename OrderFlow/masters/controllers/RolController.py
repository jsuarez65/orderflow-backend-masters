from flask import Blueprint, request, jsonify, Response
from services.RolService import RolService
from model.dto.rolDTO import RolDTO
from configuration.LogConfiguration import LogConfiguration

rolBp = Blueprint('rolBp', __name__)
log = LogConfiguration.getLogger()


@rolBp.route('/roles', methods=['POST'])
def createRol() -> tuple[Response, int]:
    data = request.get_json(silent=True) or {}
    log.info(f"createRol - Creando rol con datos: {data}")

    try:
        dto = RolDTO(**data)
    except TypeError as e:
        log.warning(f"createRol - Datos inválidos: {e}")
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    if not dto.validate():
        log.warning("createRol - Validación fallida: nombre del rol es obligatorio.")
        return jsonify({'error': 'El nombre del rol es obligatorio y no puede estar vacío.'}), 400

    service = RolService(log)
    created, error, status = service.createRol(dto)  

    if error:
        log.warning(f"createRol - {error}")
        return jsonify({'error': error}), status

    log.info(f"createRol - Rol creado exitosamente: {created.rol}")
    return jsonify(created.to_dict() if hasattr(created, 'to_dict') else {'rol': created.rol}), status


@rolBp.route('/roles/<string:nameRol>', methods=['GET'])
def getRol(nameRol: str) -> tuple[Response, int]:
    log.info(f"getRol - Buscando rol: {nameRol}")

    service = RolService(log)
    dto, error, status = service.getRol(nameRol)

    if error:
        return jsonify({'error': error}), status

    return jsonify({'rol': dto.rol}), status


@rolBp.route('/roles', methods=['GET'])
def getAllRoles() -> tuple[Response, int]:
    log.info("getAllRoles - Obteniendo todos los roles")

    service = RolService(log)
    roles, error, status = service.getAllRoles()  

    if error:
        return jsonify({'error': error}), status

    log.info(f"getAllRoles - Total: {len(roles)}")
    return jsonify([{'rol': r.rol} for r in roles]), status


@rolBp.route('/roles/<string:nameRol>', methods=['PUT'])
def updateRol(nameRol: str) -> tuple[Response, int]:  
    data = request.get_json(silent=True) or {}
    log.info(f"updateRol - Actualizando rol '{nameRol}' con datos: {data}")

    try:
        dto = RolDTO(**data)
    except TypeError as e:
        log.warning(f"updateRol - Datos inválidos: {e}")
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    if not dto.validate():
        log.warning("updateRol - Validación fallida.")
        return jsonify({'error': 'El nuevo nombre del rol es obligatorio.'}), 400

    service = RolService(log)
    updated, error, status = service.updateRol(nameRol, dto)

    if error:
        log.warning(f"updateRol - {error}")
        return jsonify({'error': error}), status

    log.info(f"updateRol - Rol '{nameRol}' actualizado a '{updated.rol}'.")
    return jsonify({'message': f"Rol '{nameRol}' actualizado a '{updated.rol}' exitosamente."}), status


@rolBp.route('/roles/<string:nameRol>', methods=['DELETE'])
def deleteRol(nameRol: str) -> tuple[Response, int]:
    log.info(f"deleteRol - Eliminando rol: {nameRol}")

    service = RolService(log)
    deleted, error, status = service.deleteRol(nameRol)  

    if error:
        log.warning(f"deleteRol - {error}")
        return jsonify({'error': error}), status

    log.info(f"deleteRol - Rol '{nameRol}' eliminado exitosamente.")
    return jsonify({
        'message': f"Rol '{nameRol}' eliminado exitosamente.",
        'rol': deleted.rol
    }), status