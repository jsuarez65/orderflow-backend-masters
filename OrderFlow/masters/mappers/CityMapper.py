from model.entities.CityEntity import CityEntity
from model.dtos.CityDTO import CityDTO

class CityMapper:

    @staticmethod
    def toDTO(entity: CityEntity) -> CityDTO:
        if entity is None:
            return None

        return CityDTO(
            id=entity.id,
            postalCode=entity.postalCode,
            cityName=entity.cityName
        )

    @staticmethod
    def toEntity(dto: CityDTO) -> CityEntity:
        if dto is None:
            return None

        return CityEntity(
            id=dto.id,
            postalCode=dto.postal_code,
            cityName=dto.city_name
        )

    @staticmethod
    def toListDTO(cities: list[CityEntity]) -> list[CityDTO]:
        if not cities:
            return []
        
        return [CityMapper.toDTO(city) for city in cities]