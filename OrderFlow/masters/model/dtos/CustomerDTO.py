from dataclasses import dataclass
from typing import Optional

@dataclass
class CustomerDTO:
    cuit: Optional[str] = None
    razonSocial: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None