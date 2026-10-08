from flask import Blueprint, request, jsonify, Response
from services.UsersService import UsersService
from model.dto.userDTO import UserDTO
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import SessionLocal

userBp = Blueprint('userBp', __name__)
log = LogConfiguration.getLogger()


@userBp.route('/usuarios', methods=['POST'])
def createUser() -> tuple[Response, int]:
    data = request.get_json(silent=True) or {}
    log.info(f"createUser - Creando usuario con datos: {data}")

    try:
        dto = UserDTO(**data)
    except TypeError as e:
        log.warning(f"createUser - Datos inválidos: {e}")
        return jsonify({'error': f'Datos inválidos: {e}'}), 400
    
    session = SessionLocal()
    if not dto.validate():
        log.warning("createUser - Validación fallida.")
        return jsonify({
            'error': 'Todos los campos (username, password, rol) son obligatorios y el rol debe ser válido.'
        }), 400

    service = UsersService(log)
    created, error, status = service.createUser(dto)

    if error:
        log.warning(f"createUser - {error}")
        return jsonify({'error': error}), status

    log.info(f"createUser - Usuario creado exitosamente: {created.username}")
    return jsonify({
        'message': f"Usuario '{created.username}' creado exitosamente.",
        'usuario': {'username': created.username, 'rol': created.rol}
    }), status
    

@userBp.route('/usuarios/<string:username>', methods=['GET'])
def getUser(username: str) -> tuple[Response, int]:
    log.info(f"getUser - Buscando usuario: {username}")
    

    service = UsersService(log)
    dto, error, status = service.getUser(username)

    if error:
        return jsonify({'error': error}), status

    return jsonify({'username': dto.username, 'rol': dto.rol}), status


@userBp.route('/usuarios', methods=['GET'])
def getAllUsers() -> tuple[Response, int]:
    log.info("getAllUsers - Obteniendo todos los usuarios")

    service = UsersService(log)
    users, error, status = service.getAllUsers()

    if error:
        return jsonify({'error': error}), status

    log.info(f"getAllUsers - Total: {len(users)}")
    return jsonify([{'username': u.username, 'rol': u.rol} for u in users]), status


@userBp.route('/usuarios/<string:username_actual>', methods=['PUT'])
def updateUser(username_actual: str) -> tuple[Response, int]:
    data = request.get_json(silent=True) or {}
    log.info(f"updateUser - Actualizando usuario '{username_actual}' con datos: {data}")

    try:
        dto = UserDTO(**data)
    except TypeError as e:
        log.warning(f"updateUser - Datos inválidos: {e}")
        return jsonify({'error': f'Datos inválidos: {e}'}), 400

    if not dto.validate():
        log.warning("updateUser - Validación fallida.")
        return jsonify({'error': 'Todos los campos son obligatorios y el rol debe ser válido.'}), 400

    service = UsersService(log)
    updated, error, status = service.updateUser(username_actual, dto)   # ⬅️ tupla

    if error:
        log.warning(f"updateUser - {error}")
        return jsonify({'error': error}), status

    log.info(f"updateUser - Usuario '{username_actual}' actualizado a '{updated.username}'.")
    return jsonify({
        'message': f"Usuario '{username_actual}' actualizado exitosamente.",
        'usuario': {'username': updated.username, 'rol': updated.rol}
    }), status


@userBp.route('/usuarios/<string:username>', methods=['DELETE'])
def deleteUser(username: str) -> tuple[Response, int]:
    log.info(f"deleteUser - Eliminando usuario: {username}")

    service = UsersService(log)
    deleted, error, status = service.deleteUser(username)

    if error:
        log.warning(f"deleteUser - {error}")
        return jsonify({'error': error}), status

    log.info(f"deleteUser - Usuario '{username}' eliminado exitosamente.")
    return jsonify({
        'message': f"Usuario '{username}' eliminado exitosamente.",
        'usuario': {'username': deleted.username, 'rol': deleted.rol}
    }), status