from flask import Flask, request
from flask import jsonify
from flask import Response

from flask_cors import CORS

import psycopg2, structlog, logging

app = Flask(__name__)




logging.basicConfig(
    level=logging.INFO,   
    filename="master_backend_service.log",
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

def getConnection():
            return psycopg2.connect(
                    host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
                    port="5432",
                    dbname="orderflow",
                    user="neondb_owner",
                    password="npg_oYRmQ2e0IHaT",
                    sslmode="require")

db = getConnection()
log = structlog.get_logger()

@app.route('/master/product', methods=['POST'])
def createProduct():
    
    product = request.get_json()

    log.info("createProduct - Ingresa con product: ", body=product)

    sqlCommand = None

    try:
        sqlCommand = db.cursor()

        sqlCommand.execute("""
            INSERT INTO Productos (codigo_interno, sku, codigo_barras, descripcion, 
             stock_minimo, stock_maximo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            product['codigo_interno'],
            product['sku'],
            product['codigo_barras'],
            product['descripcion'],
            product['stock_minimo'],
            product['stock_maximo']
        ))

        db.commit()

        return "El producto se ingresó correctamente", 200

    except Exception as ex:
        db.rollback()

        log.error(f"createProduct - Error al crear producto: {str(ex)}")

        return {"message": "Error al ingresar el producto",
                "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()

@app.route('/master/provider', methods=['POST'])
def createProvider():

    provider = request.get_json()
    
    log.info("createProvider - Ingresa con provider: ", body=provider)

    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
        sqlCommand.execute("""
            INSERT INTO proveedores (cuit, razon_social, domicilio, email, telefono, 
                localidad_codigo_postal, provincia_nombre)  
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

        db.commit() 

        return "El proveedor se ingresó correctamente", 200

    except Exception as ex:
        db.rollback() 
        log.error(f"Error al crear proveedor: {str(ex)}")
        return {"message": "Error al ingresar el proveedor", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()

@app.route('/master/providers', methods=['GET'])
def getProviders():
    
    log.info("getProviders - Ingreso")
    
    sqlCommand = None
    try:
        sqlCommand = db.cursor()
        
        sqlCommand.execute("""
            SELECT cuit, razon_social, domicilio, email, telefono, 
                localidad_codigo_postal, provincia_nombre 
            FROM proveedores;
        """)
        
        providers = sqlCommand.fetchall()
        
        providersResponse = []
        for provider in providers:
            providerResponse = {
                "cuit": provider['cuit'],
                "razon_social": provider['razon_social'],
                "domicilio": provider['domicilio'],
                "email": provider['email'],
                "telefono": provider['telefono'],
                "localidad_codigo_postal": provider['localidad_codigo_postal'],
                "provincia_nombre": provider['provincia_nombre']
            }
            
            providersResponse.append(providerResponse)
            
        return jsonify(providersResponse), 200

    except Exception as ex:
        log.error(f"getProviders - Error al obtener proveedores: {str(ex)}")
        return {"message": "Error al consultar los proveedores", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()


@app.route('/master/provider', methods=['PUT'])
def updateProvider():

    providerToUpdate = request.get_json()
    
    log.info(f"updateProvider - Ingresa con: ", body=providerToUpdate)
    
    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
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
            providerToUpdate['razon_social'],
            providerToUpdate['domicilio'],
            providerToUpdate['email'],
            providerToUpdate['telefono'],
            providerToUpdate['localidad_codigo_postal'],
            providerToUpdate['provincia_nombre'],
            providerToUpdate['cuit'] 
        ))

        db.commit() 

        return f"El proveedor con CUIT {providerToUpdate['cuit']} se modificó correctamente", 200

    except Exception as ex:
        db.rollback() 
        log.error(f"updateProvider - Error al modificar proveedor: {str(ex)}")
        return {"message": "Error al modificar el proveedor", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()


@app.route('/master/provider/<string:cuit>', methods=['DELETE'])
def deleteProvider(cuit):
    
    log.info(f"deleteProvider - Ingresa con CUIT: {cuit}")
    sqlCommand = None

    try:
        sqlCommand = db.cursor()
        
        sqlCommand.execute("""
            DELETE FROM proveedores 
            WHERE cuit = %s;
        """, (cuit,))  

        db.commit() 

        return f"El proveedor con CUIT {cuit} se eliminó correctamente", 200

    except Exception as ex:
        db.rollback() 
        log.error(f"deleteProvider - Error al eliminar proveedor: {str(ex)}")
        return {"message": "Error al eliminar el proveedor", "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()


@app.route('/customers', methods=['GET'])
def getCustomers():

    log.info("getCustomers - Ingreso")
    sqlCommand = db.cursor()
    
    sqlCommand.execute("SELECT cuit, razon_social, telefono, email 
            FROM clientes ORDER BY razon_social")
    
    customers = sqlCommand.fetchall()
    
    sqlCommand.close()
    
    customersResponse = [{"cuit": customer['cuit'], "razon_social": customer['razon_social'], 
                    "telefono": customer['telefono'], "email": customer['email']} 
                    for customer in customers]
    
    log.info("getCustomers - Respuesta obtenida", customers=customersResponse)

    return jsonify(customersResponse)
    
    
if __name__ == '__main__':
    app.run(debug=True)