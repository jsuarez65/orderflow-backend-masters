from pydantic import BaseModel
from typing import Optional

class CustomerDTO(BaseModel):
    cuit: str  # Obligatorio
    razon_social: str # Obligatorio
    telefono: Optional[str] = None # Opcional
    email: Optional[str] = None # Opcional