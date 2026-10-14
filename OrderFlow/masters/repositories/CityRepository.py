from sqlalchemy.exc import IntegrityError

from model.entities.CityEntity import CityEntity
from mappers.CityMapper import CityMapper

class CityRepository:
    def __init__(self, log, session):
        self.log = log
        self.session = session

    def importZipCodes(self, cityEntities):
        inserted = 0
        ignoredDuplicates = 0
        skipped = 0

        for cityEntity in cityEntities:
            try:
                self.session.add(cityEntity)
                self.session.commit()
                inserted += 1

            except IntegrityError:
                self.session.rollback()
                ignoredDuplicates += 1
            except Exception as e:
                self.session.rollback()
                skipped += 1
                self.log.error(f"Error importing city: {e}")
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