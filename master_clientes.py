from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import structlog
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, filename="master_clientes.log", filemode="a", format="%(message)s")

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory()
)

log = structlog.get_logger()

def get_connection():
    """Crea una nueva conexión a la base de datos"""
    return psycopg2.connect(
        host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
        port="5432",
        dbname="orderflow",
        user="neondb_owner",
        password="npg_oYRmQ2e0IHaT",
        sslmode="require"
    )

# =====================================================
# CLIENTES
# =====================================================

@app.route('/clientes', methods=['GET'])
def get_clientes():
    log.info("Obteniendo clientes")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cuit, razon_social, telefono, email FROM clientes ORDER BY razon_social")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    clientes = [{"cuit": r[0], "razon_social": r[1], "telefono": r[2], "email": r[3]} for r in rows]
    return jsonify(clientes)

@app.route('/clientes/<cuit>', methods=['GET'])
def get_cliente(cuit):
    log.info("Obteniendo cliente", cuit=cuit)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cuit, razon_social, telefono, email FROM clientes WHERE cuit = %s", (cuit,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    return jsonify({"cuit": row[0], "razon_social": row[1], "telefono": row[2], "email": row[3]})

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    log.info("Creando cliente", body=data)
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO clientes (cuit, razon_social, telefono, email)
            VALUES (%s, %s, %s, %s)
        """, (data['cuit'], data['razon_social'], data.get('telefono'), data.get('email')))
        conn.commit()
        return jsonify({"message": "Cliente creado correctamente"}), 201
    except Exception as e:
        if conn:
            conn.rollback()
        log.error(f"Error al crear cliente: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/clientes/<cuit>', methods=['PUT'])
def update_cliente(cuit):
    data = request.get_json()
    log.info("Actualizando cliente", cuit=cuit)
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes SET razon_social = %s, telefono = %s, email = %s
            WHERE cuit = %s
        """, (data['razon_social'], data.get('telefono'), data.get('email'), cuit))
        conn.commit()
        return jsonify({"message": "Cliente actualizado correctamente"})
    except Exception as e:
        if conn:
            conn.rollback()
        log.error(f"Error al actualizar cliente: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/clientes/<cuit>', methods=['DELETE'])
def delete_cliente(cuit):
    log.info("Eliminando cliente", cuit=cuit)
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE cuit = %s", (cuit,))
        conn.commit()
        return jsonify({"message": "Cliente eliminado correctamente"})
    except Exception as e:
        if conn:
            conn.rollback()
        log.error(f"Error al eliminar cliente: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# =====================================================
# DOMICILIOS_ENTREGA
# =====================================================

@app.route('/domicilios', methods=['GET'])
def get_domicilios():
    log.info("Obteniendo domicilios")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.id, d.calle, d.numero, d.localidad_codigo_postal, d.provincia, d.cliente_cuit
        FROM domicilios_entrega d
        ORDER BY d.id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    domicilios = [{"id": r[0], "calle": r[1], "numero": r[2], "localidad_codigo_postal": r[3], "provincia": r[4], "cliente_cuit": r[5]} for r in rows]
    return jsonify(domicilios)

@app.route('/clientes/<cuit>/domicilios', methods=['GET'])
def get_domicilios_by_cliente(cuit):
    log.info("Obteniendo domicilios del cliente", cuit=cuit)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, calle, numero, localidad_codigo_postal, provincia
        FROM domicilios_entrega WHERE cliente_cuit = %s
    """, (cuit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    domicilios = [{"id": r[0], "calle": r[1], "numero": r[2], "localidad_codigo_postal": r[3], "provincia": r[4]} for r in rows]
    return jsonify(domicilios)

@app.route('/domicilios', methods=['POST'])
def create_domicilio():
    data = request.get_json()
    log.info("Creando domicilio", body=data)
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO domicilios_entrega (calle, numero, localidad_codigo_postal, provincia, cliente_cuit)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (data['calle'], data.get('numero'), data.get('localidad_codigo_postal'), data.get('provincia'), data['cliente_cuit']))
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Domicilio creado correctamente", "id": new_id}), 201
    except Exception as e:
        if conn:
            conn.rollback()
        log.error(f"Error al crear domicilio: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/domicilios/<int:id>', methods=['DELETE'])
def delete_domicilio(id):
    log.info("Eliminando domicilio", id=id)
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM domicilios_entrega WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Domicilio eliminado correctamente"})
    except Exception as e:
        if conn:
            conn.rollback()
        log.error(f"Error al eliminar domicilio: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/")
def home():
    return "API ABM Clientes y Domicilios - PostgreSQL (Neon.tech)"

if __name__ == '__main__':
    app.run(debug=True)