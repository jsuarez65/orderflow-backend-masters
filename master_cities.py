from flask import Flask, request, jsonify, Response
from openpyxl import load_workbook
import psycopg2
import structlog
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,   
    filename="master_cities.log",
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
log = structlog.get_logger()

@app.route('/master/cities', methods=['POST'])


def import_zipCodes():

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No se envió archivo"}), 400

    conn = psycopg2.connect(
        host="ep-dry-art-acz5gndj-pooler.sa-east-1.aws.neon.tech",
        port="5432",
        dbname="orderflow",
        user="neondb_owner",
        password="npg_oYRmQ2e0IHaT",
        sslmode="require"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT codigo_postal
        FROM localidades
    """)

    cities_Db = {
        str(row[0]).strip()
    for row in cursor.fetchall()
    }

    workbook = load_workbook(file)
    sheet = workbook.active

    insertados = 0
    duplicados_en_excel = 0
    saltados = 0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue

        try:

            raw_cp = row[0]
            if isinstance(raw_cp, float):
                codigo_postal = str(int(raw_cp))
            else:
                codigo_postal = str(raw_cp).strip()

            if not codigo_postal:
                saltados += 1
                continue

            nombre_localidad = str(row[1]).strip().title() if row[1] and str(row[1]).strip() else ""

            # === CLAVE: Si ya está en el set, es duplicado (de la DB o del Excel) ===
            if codigo_postal in cities_Db:
                duplicados_en_excel += 1
                continue

            # Insertar
            cursor.execute("""
                INSERT INTO localidades (codigo_postal, nombre_localidad)
                VALUES (%s, %s)
                ON CONFLICT (codigo_postal) DO NOTHING
            """, (codigo_postal, nombre_localidad))

            cities_Db.add(codigo_postal)
            insertados += 1

        except Exception as e:
            saltados += 1
            continue

    conn.commit()
    cursor.close()
    conn.close()

    ya_existentes_reales = ya_existentes_en_db

    return jsonify({
        "message": "Importación finalizada",
        "insertados_nuevos": insertados,
        "duplicados_ignorados": duplicados_en_excel,
        "ya_existentes_en_db": ya_existentes_reales,
        "filas_saltadas": saltados,
        "total_procesadas": insertados + duplicados_en_excel + saltados
    })

if __name__ == '__main__':
    app.run(debug=True)