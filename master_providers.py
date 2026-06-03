from flask import Flask, request
from flask import jsonify
from flask import Response

import psycopg2
import structlog
import logging

app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------

#metodo post para crear un producto

@app.route('/master/proveedor', methods=['POST'])
def create_proveedor():
    # 1. Tomamos el JSON que viene desde el Body de Postman
    proveedor = request.get_json()
    
    log.info("Ingreso a create_proveedor", body=proveedor)
    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
        # 2. Armamos el INSERT INTO con los 7 campos exactos de tu tabla en la base de datos
        sqlCommand.execute("""
            INSERT INTO proveedores (cuit, razon_social, domicilio, email, telefono, localidad_codigo_postal, provincia_nombre)  
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            proveedor['cuit'],
            proveedor['razon_social'],
            proveedor['domicilio'],
            proveedor['email'],
            proveedor['telefono'],
            proveedor['localidad_codigo_postal'],
            proveedor['provincia_nombre']
        ))

        # 3. Confirmamos los cambios de forma permanente en PostgreSQL
        db.commit() 

        return "El proveedor se ingresó correctamente", 200

    except Exception as ex:
        # 4. Si el CUIT ya existe o hay un error, deshacemos el intento para no romper nada
        db.rollback() 
        log.error(f"Error al crear proveedor: {str(ex)}")
        return {"message": "Error al ingresar el proveedor", "error": str(ex)}, 500

    finally:
        # 5. Pase lo que pase, liberamos el cursor
        if sqlCommand:
            sqlCommand.close()





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
def get_connection():
    return psycopg2.connect(host="localhost", port="5432",
        dbname="orderflow", user="postgres", password="1234567890")

db = get_connection()
log = structlog.get_logger()

#-----------------------------------------------------------------------------------------------------

#metodo get para obtener todos los proveedores

@app.route('/master/providers', methods=['GET'])
def get_proveedores():
    log.info("Ingreso a get_proveedores")
    
    sqlCommand = None
    try:
        # 1. Creamos el cursor usando la conexión 'db' que ya tenés global
        sqlCommand = db.cursor()
        
        # 2. Le pedimos a la base de datos que seleccione todos los registros de 'proveedores'
        sqlCommand.execute("""
            SELECT cuit, razon_social, domicilio, email, telefono, localidad_codigo_postal, provincia_nombre 
            FROM proveedores;
        """)
        
        # 3. Traemos todas las filas resultantes de la consulta
        columnas = sqlCommand.fetchall()
        
        # 4. Como la base de datos devuelve una lista de "tuplas" (ej: [('30-123', 'Empresa S.A.'), ...])
        # vamos a armar una estructura limpia (una lista de diccionarios) para que se convierta en un JSON legible.
        lista_proveedores = []
        for fila in columnas:
            proveedor = {
                "cuit": fila[0],
                "razon_social": fila[1],
                "domicilio": fila[2],
                "email": fila[3],
                "telefono": fila[4],
                "localidad_codigo_postal": fila[5],
                "provincia_nombre": fila[6]
            }
            lista_proveedores.append(proveedor)
            
        # 5. Devolvemos la lista transformada a JSON con un estado 200 (Éxito)
        return jsonify(lista_proveedores), 200

    except Exception as ex:
        # Si algo falla (ej: se cayó la base de datos o escribiste mal la tabla), entra acá
        log.error(f"Error al obtener proveedores: {str(ex)}")
        return {"message": "Error al consultar los proveedores", "error": str(ex)}, 500

    finally:
        # Pase lo que pase, cerramos el cursor para liberar recursos
        if sqlCommand:
            sqlCommand.close()

#-----------------------------------------------------------------------------------------------------

#metodo put para modificar un proveedor por su CUIT


@app.route('/master/proveedor/<string:cuit>', methods=['PUT'])
def update_proveedor(cuit):
    # 1. Tomamos los datos nuevos que vienen en el Body de Postman
    datos_nuevos = request.get_json()
    
    log.info(f"Ingreso a update_proveedor para el CUIT: {cuit}", body=datos_nuevos)
    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
        # 2. Ejecutamos un UPDATE filtrando estrictamente por el CUIT de la URL
        sqlCommand.execute("""
            UPDATE proveedores 
            SET razon_social = %s, 
                domicilio = %s, 
                email = %s, 
                telefono = %s, 
                localidad_codigo_postal = %s, 
                provincia_nombre = %s
            WHERE cuit = %s;
        """, (
            datos_nuevos['razon_social'],
            datos_nuevos['domicilio'],
            datos_nuevos['email'],
            datos_nuevos['telefono'],
            datos_nuevos['localidad_codigo_postal'],
            datos_nuevos['provincia_nombre'],
            cuit  # Este es el CUIT que viene desde la URL
        ))

        # 3. Confirmamos la modificación en la base de datos
        db.commit() 

        return f"El proveedor con CUIT {cuit} se modificó correctamente", 200

    except Exception as ex:
        db.rollback() 
        log.error(f"Error al modificar proveedor: {str(ex)}")
        return {"message": "Error al modificar el proveedor", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()

#-----------------------------------------------------------------------------------------------------

#metodo delete para eliminar un proveedor por su CUIT

@app.route('/master/proveedor/<string:cuit>', methods=['DELETE'])
def delete_proveedor(cuit):
    log.info(f"Ingreso a delete_proveedor para el CUIT: {cuit}")
    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
        # Ejecutamos el comando DELETE filtrando estrictamente por el CUIT que viene en la URL
        sqlCommand.execute("""
            DELETE FROM proveedores 
            WHERE cuit = %s;
        """, (cuit,))  # Esa coma final es necesaria porque Python pide que sea una tupla

        # Confirmamos la eliminación de forma permanente
        db.commit() 

        return f"El proveedor con CUIT {cuit} se eliminó correctamente", 200

    except Exception as ex:
        db.rollback() 
        log.error(f"Error al eliminar proveedor: {str(ex)}")
        return {"message": "Error al eliminar el proveedor", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()


if __name__ == '__main__':
    app.run(debug=True)