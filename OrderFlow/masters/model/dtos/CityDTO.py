from dataclasses import dataclass
from typing import Optional

@dataclass
class CityDTO:
    id: Optional[int] = None
    postalCode: Optional[str] = None
    cityName: Optional[str] = None