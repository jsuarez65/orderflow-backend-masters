from openpyxl import load_workbook
from sqlalchemy.exc import IntegrityError

from model.entities.CityEntity import CityEntity
from mappers.CityMapper import CityMapper

class CityRepository:
    def __init__(self, log, session):
        self.log = log
        self.session = session

    def importZipCodes(self, file):
        workbook = load_workbook(file)
        sheet = workbook.active

        inserted = 0
        ignoredDuplicates = 0
        skipped = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not row or row[0] is None:
                skipped += 1
                continue

            try:
                rawCp = row[0]
                postalCode = str(int(rawCp)) if isinstance(rawCp, float) else str(rawCp).strip()

                if not postalCode:
                    skipped += 1
                    continue

                cityName = str(row[1]).strip().title() if row[1] and str(row[1]).strip() else ""

                cityEntity = CityEntity(
                    codigo_postal=postalCode,
                    nombre_localidad=cityName
                )

                self.session.add(cityEntity)
                self.session.commit()
                inserted += 1

            except IntegrityError:
                self.session.rollback()
                ignoredDuplicates += 1
            except Exception as e:
                self.session.rollback()
                skipped += 1
                self.log.error(f"Error in row {row}: {e}")
                continue

        return {
            "message": "Import finished successfully",
            "insertedNew": inserted,
            "ignoredDuplicates": ignoredDuplicates,
            "skippedRows": skipped,
            "totalProcessed": inserted + ignoredDuplicates + skipped
        }

    def getPostalCodes(self, postalCode: str = None, cityName: str = None):
        query = self.session.query(CityEntity)

        if postalCode:
            query = query.filter(CityEntity.codigo_postal == postalCode.strip())
        
        if cityName:
            query = query.filter(CityEntity.nombre_localidad.ilike(f"%{cityName.strip()}%"))

        cities = query.all()
        return CityMapper.toListDTO(cities)