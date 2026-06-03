from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import structlog
import logging

# =====================================================
# CONFIGURACIÓN
# =====================================================
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, filename="clientes_endpoints.log", filemode="a", format="%(message)s")

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory()
)

log = structlog.get_logger()

# =====================================================
# CONEXIÓN A POSTGRESQL
# =====================================================
def get_connection():
    return psycopg2.connect(
        host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
        port="5432",
        dbname="orderflow",
        user="neondb_owner",
        password="npg_oYRmQ2e0IHaT",
        sslmode="require"
    )

# =====================================================
# CLIENTES (GET y POST)
# =====================================================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        # POST: Crear cliente
        cliente = request.get_json()
        log.info("Ingreso a createCliente", body=cliente)

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO clientes (cuit, razon_social, telefono, email)
                VALUES (%s, %s, %s, %s)
            """, (
                cliente['cuit'],
                cliente['razon_social'],
                cliente.get('telefono'),
                cliente.get('email')
            ))

            connection.commit()
            return jsonify({"message": "Cliente creado correctamente"}), 201

        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"Error al crear cliente: {str(e)}")
            return jsonify({"message": "Error al insertar el cliente", "error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    else:
        # GET: Listar clientes
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT cuit, razon_social, telefono, email FROM clientes ORDER BY razon_social")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        clientes_lista = [{"cuit": r[0], "razon_social": r[1], "telefono": r[2], "email": r[3]} for r in rows]
        return jsonify(clientes_lista)

# =====================================================
# DOMICILIOS ENTREGA (GET y POST)
# =====================================================
@app.route('/domicilios', methods=['GET', 'POST'])
def domicilios():
    if request.method == 'POST':
        # POST: Crear domicilio
        domicilio = request.get_json()
        log.info("Ingreso a createDomicilio", body=domicilio)

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO domicilios_entrega (calle, numero, localidad_codigo_postal, provincia, cliente_cuit)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                domicilio['calle'],
                domicilio.get('numero'),
                domicilio.get('localidad_codigo_postal'),
                domicilio.get('provincia'),
                domicilio['cliente_cuit']
            ))

            connection.commit()
            return jsonify({"message": "Domicilio creado correctamente"}), 201

        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"Error al crear domicilio: {str(e)}")
            return jsonify({"message": "Error al insertar el domicilio", "error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    else:
        # GET: Listar domicilios
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, calle, numero, localidad_codigo_postal, provincia, cliente_cuit
            FROM domicilios_entrega
            ORDER BY id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        domicilios_lista = [{"id": r[0], "calle": r[1], "numero": r[2], "localidad_codigo_postal": r[3], "provincia": r[4], "cliente_cuit": r[5]} for r in rows]
        return jsonify(domicilios_lista)

# =====================================================
# HOME
# =====================================================
@app.route('/')
def home():
    return jsonify({
        "mensaje": "API Clientes y Domicilios funcionando",
        "endpoints": [
            {"GET /clientes": "Listar clientes"},
            {"POST /clientes": "Crear cliente (JSON con cuit, razon_social, telefono, email)"},
            {"GET /domicilios": "Listar domicilios"},
            {"POST /domicilios": "Crear domicilio (JSON con calle, numero, localidad_codigo_postal, provincia, cliente_cuit)"}
        ]
    })

# =====================================================
# EJECUCIÓN
# =====================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    