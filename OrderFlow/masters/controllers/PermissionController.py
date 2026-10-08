from flask import Blueprint, request, jsonify, Response
from services.PermissionService import PermissionService
from model.dto.permissionDTO import PermissionDTO
from configuration.LogConfiguration import LogConfiguration

permissionBp = Blueprint('permissionBp', __name__)
log = LogConfiguration.getLogger()


@permissionBp.route('/permisos', methods=['POST'])
def createPermission() -> tuple[Response, int]:
    data = request.get_json(silent=True) or {}
    log.info(f"createPermission - Creando permiso con datos: {data}")

    try:
        dto = PermissionDTO(**data)
    except TypeError as e:
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    if not dto.validate():
        return jsonify({'error': 'Datos inválidos: nombre y descripción son obligatorios.'}), 400

    service = PermissionService(log)             
    created, error = service.createPermission(dto)

    if error:
        log.warning(f"createPermission - {error}")
        return jsonify({'error': error}), 409

    return jsonify(created.to_dict()), 201


@permissionBp.route('/permisos/<string:nombre>', methods=['GET'])
def getPermission(nombre: str) -> tuple[Response, int]:
    log.info(f"getPermission - Buscando permiso: {nombre}")

    service = PermissionService(log)              
    dto, error = service.getPermission(nombre)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(dto.to_dict()), 200


@permissionBp.route('/permisos', methods=['GET'])
def getAllPermissions() -> tuple[Response, int]:
    log.info("getAllPermissions - Ingresa a recuperar todos los permisos")

    service = PermissionService(log)              
    permissions, error = service.getAllPermissions()

    if error:
        log.error(f"getAllPermissions - {error}")
        return jsonify({'error': error}), 500

    return jsonify([p.to_dict() for p in permissions]), 200


@permissionBp.route('/permisos/<string:currentPermission>', methods=['PUT'])
def updatePermission(currentPermission: str) -> tuple[Response, int]:
    data = request.get_json(silent=True) or {}
    log.info(f"updatePermission - Actualizando '{currentPermission}' con datos: {data}")

    try:
        dto = PermissionDTO(**data)
    except TypeError as e:
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    if not dto.validate():
        return jsonify({'error': 'Datos inválidos: nombre y descripción son obligatorios.'}), 400

    service = PermissionService(log)             
    updated, error = service.updatePermission(currentPermission, dto)

    if error:
        return jsonify({'error': error}), 404

    return jsonify(updated.to_dict()), 200


@permissionBp.route('/permisos/<string:nombre>', methods=['DELETE'])
def deletePermission(nombre: str) -> tuple[Response, int]:
    log.info(f"deletePermission - Eliminando permiso: {nombre}")

    service = PermissionService(log)             
    deleted, error = service.deletePermission(nombre)

    if error:
        return jsonify({'error': error}), 404

    return jsonify({
        'message': f"Permiso '{deleted.nombre}' eliminado exitosamente.",
        'permiso': deleted.to_dict()
    }), 200