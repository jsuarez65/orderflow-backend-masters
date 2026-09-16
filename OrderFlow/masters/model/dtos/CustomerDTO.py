from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerDTO():
    cuit: str  
    razonSocial: str 
    telefono: Optional[str] = None 
    email: Optional[str] = None 
