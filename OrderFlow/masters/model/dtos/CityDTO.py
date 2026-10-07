from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CityDTO:
    codigo_postal: Optional[str] = None
    nombre_localidad: Optional[str] = None