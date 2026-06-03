from flask import Flask, request, jsonify, Response
from openpyxl import load_workbook
import psycopg2
import structlog
import logging

app = Flask(__name__)

# 1. Configuración de logging nativo
logging.basicConfig(
    level=logging.INFO,   
    filename="master_cities.log",
    filemode="a",          
    format="%(message)s"
)

# 2. Configuración de structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory()
)
log = structlog.get_logger()

#apuntado al ENDOPINT
@app.route('/master/cities', methods=['POST'])


def import_codigos_postales():

    # 1. Buscamos la clave genérica 'file' que enviaremos desde Postman
    file = request.files['localidades.xlsx']

    if file.filename == '':
        return jsonify({"error": "No se envió archivo"}), 400

    conn = psycopg2.connect(
        host="localhost",
        port="5000",
        dbname="orderflow",
        user="postgres",
        password="123456789"
    )

    cursor = conn.cursor()

    # ==========================================
    # CARGAR TODOS LOS CODIGOS POSTALES A MEMORIA
    # ==========================================

    cursor.execute("""
        SELECT codigo_postal
        FROM codigos_postales
    """)

    # Set para busquedas O(1)
    codigos_postales_db = {
        str(row[0]).strip()
        for row in cursor.fetchall()
    }

    # ==========================================
    # LEER EXCEL
    # ==========================================

    workbook = load_workbook(file)
    sheet = workbook.active

    insertados = 0
    existentes = 0

    # Saltear encabezado
    for row in sheet.iter_rows(min_row=2, values_only=True):

        codigo_postal = str(row[0]).strip()
        ciudad = row[1]
        provincia = row[2]

        # Verificar en memoria
        if codigo_postal in codigos_postales_db:
            existentes += 1
            continue

        # Insertar
        cursor.execute("""
            INSERT INTO codigos_postales(
                codigo_postal,
                ciudad,
                provincia
            )
            VALUES(%s, %s, %s)
        """, (
            codigo_postal,
            ciudad,
            provincia
        ))

        # Agregar al set para evitar duplicados
        # dentro del mismo Excel
        codigos_postales_db.add(codigo_postal)

        insertados += 1

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Importación finalizada",
        "insertados": insertados,
        "existentes": existentes
    })


if __name__ == '__main__':
    app.run(debug=True)