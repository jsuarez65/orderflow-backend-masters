from configuration.DatabaseConfiguration import DatabaseConfiguration
from configuration.LogConfiguration import LogConfiguration

class CitiesRepository:

        def __init__(self):
        self.db = DatabaseConfiguration.getConnection()
        self.log = LogConfiguration.getLogger()

        def exits (self, codZip):
                do: None

        def insert (self, codZip):

                file = request.files['file']

                if file.filename == '':
                        return jsonify({"error": "No se envió archivo"}), 400
                
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