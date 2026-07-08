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

    # ==========================================
    # CARGAR TODOS LOS CODIGOS POSTALES A MEMORIA
    # ==========================================

    cursor.execute("""
        SELECT codigo_postal
        FROM localidades
    """)

    # Set para busquedas O(1)
    localidades_db = {
        str(row[0]).strip()
    for row in cursor.fetchall()
    }
    # ==========================================
    # LEER EXCEL
    # ==========================================

    workbook = load_workbook(file)
    sheet = workbook.active

    insertados = 0
    duplicados_en_excel = 0
    saltados = 0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue

        try:
            # Conversión segura de zipcode (maneja 1001.0 de Excel)
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
            if codigo_postal in localidades_db:
                duplicados_en_excel += 1
                continue

            # Insertar
            cursor.execute("""
                INSERT INTO localidades (codigo_postal, nombre_localidad)
                VALUES (%s, %s)
                ON CONFLICT (codigo_postal) DO NOTHING
            """, (codigo_postal, nombre_localidad))

            localidades_db.add(codigo_postal)
            insertados += 1

        except Exception as e:
            saltados += 1
            continue

    conn.commit()
    cursor.close()
    conn.close()

    # Calculamos cuántos eran duplicados del Excel vs ya estaban en la DB
    ya_existentes_reales = ya_existentes_en_db  # Los que estaban antes de empezar

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