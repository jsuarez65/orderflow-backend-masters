from model.entities.CityEntity import CityEntity
from model.dtos.CityDTO import CityDTO

class CityMapper:

    @staticmethod
    def toDTO(entity: CityEntity) -> CityDTO:
        if entity is None:
            return None

        return CityDTO(
            id=entity.id,
            postal_code=entity.codigo_postal,
            city_name=entity.nombre_localidad
        )

    @staticmethod
    def toEntity(dto: CityDTO) -> CityEntity:
        if dto is None:
            return None

        return CityEntity(
            id=dto.id,
            codigo_postal=dto.postal_code,
            nombre_localidad=dto.city_name
        )

    @staticmethod
    def toListDTO(cities: list[CityEntity]) -> list[CityDTO]:
        if not cities:
            return []
        
        return [CityMapper.toDTO(city) for city in cities]