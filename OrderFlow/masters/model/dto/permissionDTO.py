from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class permissionDTO:
    nombre: Optional[str] = None
    descripcion: Optional[str] = None