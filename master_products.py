from flask import Flask, request
from flask import jsonify
from flask import Response

from flask_cors import CORS

import psycopg2, structlog, logging

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

def get_connection():
    return psycopg2.connect(host="localhost", port="5432",
        dbname="orderflow", user="postgres", password="juliadri")

db = get_connection()
log = structlog.get_logger()

@app.route('/master/product', methods=['POST'])
def createProduct():
    product = request.get_json()

    log.info("Ingreso a createProduct", body=product)

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

        log.error(f"Error al crear producto: {str(ex)}")

        return {"message": "Error al ingresar el producto",
                "error": str(ex)}, 500

    finally:
        if sqlCommand:
            sqlCommand.close()

    

    
if __name__ == '__main__':
    app.run(debug=True)