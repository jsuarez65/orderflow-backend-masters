from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerDTO():
    cuit: str  
    razon_social: str 
    telefono: Optional[str] = None 
    email: Optional[str] = None 
