from flask import Flask, request
from flask import jsonify
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_cors import CORS
import psycopg2, logging, structlog

app = Flask(__name__)

CORS(app)

logging.basicConfig(
    level=logging.INFO,   
    filename="master_product.log",
    filemode="a",          
    format="%(message)s"
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory()
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_oYRmQ2e0IHaT@ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech:5432/orderflow?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

"""def get_connection():
    return psycopg2.connect(
                    host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
                    port="5432",
                    dbname="orderflow",
                    user="neondb_owner",
                    password="npg_oYRmQ2e0IHaT",
                    sslmode="require")"""

log = structlog.get_logger()



#-----------------ROLES-----------------

class Rol(db.Model):
    __tablename__ = 'rol'
    rol = db.Column(db.String(50), primary_key=True)

class Permiso(db.Model):
    __tablename__ = 'permisos'
    nombre = db.Column(db.String(100), primary_key=True)
    descripcion = db.Column(db.Text)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), db.ForeignKey('rol.rol'), nullable=False)

    # Relación opcional para acceder al objeto Rol
    rol_obj = db.relationship('Rol', backref='usuarios')
    
# Crear un nuevo rol   
@app.route('/roles', methods=['POST'])
def crear_rol():
    datos = request.get_json()
    if not datos or 'rol' not in datos:
        return jsonify({'error': 'Falta el campo rol'}), 400

    nuevo = Rol(rol=datos['rol'])
    db.session.add(nuevo)
    try:
        db.session.commit()
        return jsonify({'mensaje': 'Rol creado', 'rol': nuevo.rol}), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'El rol ya existe'}), 409
  
  
# Listar todos los roles  
@app.route('/roles', methods=['GET'])
def listar_roles():
    roles = Rol.query.all()
    return jsonify([{'rol': r.rol} for r in roles]), 200

# Obtener un rol específico por su ID (nombre del rol)
@app.route('/roles/<string:rol_id>', methods=['GET'])
def obtener_rol(rol_id):
    rol = Rol.query.get(rol_id)
    if not rol:
        return jsonify({'error': 'Rol no encontrado'}), 404
    return jsonify({'rol': rol.rol}), 200

# cambiar el nombre de un rol (actualizar)
@app.route('/roles/<string:rol_id>', methods=['PUT'])
def actualizar_rol(rol_id):
    rol = Rol.query.get(rol_id)
    if not rol:
        return jsonify({'error': 'Rol no encontrado'}), 404

    datos = request.get_json()
    nuevo_nombre = datos.get('rol')
    if not nuevo_nombre:
        return jsonify({'error': 'Falta el nuevo nombre del rol'}), 400

    # Como es clave primaria, debemos eliminarlo y crear uno nuevo
    # (o actualizar con una sentencia SQL directa – aquí lo hacemos de forma segura)
    try:
        # Primero verificamos que no exista otro rol con el nuevo nombre
        if Rol.query.get(nuevo_nombre):
            return jsonify({'error': 'El nuevo nombre de rol ya existe'}), 409
        
        # Creamos el nuevo rol
        nuevo_rol = Rol(rol=nuevo_nombre)
        db.session.add(nuevo_rol)
        
        # Actualizamos los usuarios que tenían el rol antiguo
        usuarios = Usuario.query.filter_by(rol=rol_id).all()
        for u in usuarios:
            u.rol = nuevo_nombre
        
        # Eliminamos el rol antiguo
        db.session.delete(rol)
        db.session.commit()
        return jsonify({'mensaje': 'Rol actualizado', 'rol': nuevo_nombre}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el rol', 'detalle': str(e)}), 500
 
 
# Eliminar un rol (si no hay usuarios asociados)    
@app.route('/roles/<string:rol_id>', methods=['DELETE'])
def eliminar_rol(rol_id):
    rol = Rol.query.get(rol_id)
    if not rol:
        return jsonify({'error': 'Rol no encontrado'}), 404

    # Si hay usuarios con ese rol, la FK lo impedirá (ON DELETE RESTRICT)
    if Usuario.query.filter_by(rol=rol_id).first():
        return jsonify({'error': 'No se puede eliminar: hay usuarios con ese rol'}), 409

    db.session.delete(rol)
    db.session.commit()
    return jsonify({'mensaje': 'Rol eliminado'}), 200

#------------PERMISOS-----------------

@app.route('/permisos', methods=['POST'])
def crear_permiso():
    datos = request.get_json()
    if not datos or 'nombre' not in datos:
        return jsonify({'error': 'Falta el campo nombre'}), 400
    nuevo = Permiso(nombre=datos['nombre'], descripcion=datos.get('descripcion', ''))
    db.session.add(nuevo)
    try:
        db.session.commit()
        return jsonify({'mensaje': 'Permiso creado', 'nombre': nuevo.nombre}), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'El permiso ya existe'}), 409

@app.route('/permisos', methods=['GET'])
def listar_permisos():
    permisos = Permiso.query.all()
    return jsonify([{'nombre': p.nombre, 'descripcion': p.descripcion} for p in permisos]), 200

@app.route('/permisos/<string:nombre>', methods=['GET'])
def obtener_permiso(nombre):
    p = Permiso.query.get(nombre)
    if not p:
        return jsonify({'error': 'Permiso no encontrado'}), 404
    return jsonify({'nombre': p.nombre, 'descripcion': p.descripcion}), 200

@app.route('/permisos/<string:nombre>', methods=['PUT'])
def actualizar_permiso(nombre):
    p = Permiso.query.get(nombre)
    if not p:
        return jsonify({'error': 'Permiso no encontrado'}), 404
    datos = request.get_json()
    # Podemos cambiar descripción y/o nombre (PK)
    nuevo_nombre = datos.get('nombre', nombre)
    nueva_desc = datos.get('descripcion', p.descripcion)
    
    if nuevo_nombre != nombre:
        if Permiso.query.get(nuevo_nombre):
            return jsonify({'error': 'El nuevo nombre ya existe'}), 409
        # Creamos nuevo permiso y eliminamos el viejo
        nuevo_permiso = Permiso(nombre=nuevo_nombre, descripcion=nueva_desc)
        db.session.add(nuevo_permiso)
        db.session.delete(p)
    else:
        p.descripcion = nueva_desc
    
    try:
        db.session.commit()
        return jsonify({'mensaje': 'Permiso actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/permisos/<string:nombre>', methods=['DELETE'])
def eliminar_permiso(nombre):
    p = Permiso.query.get(nombre)
    if not p:
        return jsonify({'error': 'Permiso no encontrado'}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({'mensaje': 'Permiso eliminado'}), 200

#-----------------USUARIOS-----------------

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    campos_obligatorios = ['username', 'password', 'rol']
    for campo in campos_obligatorios:
        if campo not in datos:
            return jsonify({'error': f'Falta el campo {campo}'}), 400

    # Verificar que el rol exista
    if not Rol.query.get(datos['rol']):
        return jsonify({'error': 'El rol especificado no existe'}), 400

    # Hashear la contraseña
    hashed = bcrypt.generate_password_hash(datos['password']).decode('utf-8')
    nuevo = Usuario(username=datos['username'], password=hashed, rol=datos['rol'])
    db.session.add(nuevo)
    try:
        db.session.commit()
        # No devolver la contraseña
        return jsonify({'mensaje': 'Usuario creado', 'username': nuevo.username, 'rol': nuevo.rol}), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'El usuario ya existe'}), 409

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = []
    for u in usuarios:
        resultado.append({
            'username': u.username,
            'rol': u.rol
            # no incluimos password
        })
    return jsonify(resultado), 200

@app.route('/usuarios/<string:username>', methods=['GET'])
def obtener_usuario(username):
    u = Usuario.query.get(username)
    if not u:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'username': u.username, 'rol': u.rol}), 200

@app.route('/usuarios/<string:username>', methods=['PUT'])
def actualizar_usuario(username):
    u = Usuario.query.get(username)
    if not u:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    datos = request.get_json()
    # Podemos actualizar password y/o rol
    if 'password' in datos:
        u.password = bcrypt.generate_password_hash(datos['password']).decode('utf-8')
    if 'rol' in datos:
        if not Rol.query.get(datos['rol']):
            return jsonify({'error': 'El nuevo rol no existe'}), 400
        u.rol = datos['rol']

    try:
        db.session.commit()
        return jsonify({'mensaje': 'Usuario actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/usuarios/<string:username>', methods=['DELETE'])
def eliminar_usuario(username):
    u = Usuario.query.get(username)
    if not u:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    db.session.delete(u)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado'}), 200


if __name__ == '__main__':
    app.run(debug=True)





'''@app.route('/master/product', methods=['POST'])
def createProduct():
    product = request.get_json()  # Obtener el JSON del cuerpo de la solicitud

    if not product:
        return jsonify({"message": "JSON inválido o cuerpo vacío"}), 400

    log.info("Ingreso a createProduct", body=product)  # Agregar el cuerpo de la solicitud al log

    connection = None
    cursor = None

    try:
        connection = db.engine.connect()
        cursor = connection.cursor()  # ejecuta sentencia SQL

        cursor.execute("""
            INSERT INTO Productos (codigo_interno, sku, codigo_barras, descripcion, stock_minimo, stock_maximo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            product['codigo_interno'],
            product['sku'],
            product['codigo_barras'],
            product['descripcion'],
            product['stock_minimo'],
            product['stock_maximo']
        ))

        connection.commit()  # cualquier sentencia SQL que modifique la base de datos, debe ser confirmada con commit()

        return jsonify({"message": "El producto se ingresó correctamente"}), 200

    except Exception as ex:
        if connection is not None:
            connection.rollback()

        log.error(f"Error al crear producto: {str(ex)}")

        return jsonify({"message": "Error al ingresar el producto",
                        "error": str(ex)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    

    
if __name__ == '__main__':
    app.run(debug=True)'''