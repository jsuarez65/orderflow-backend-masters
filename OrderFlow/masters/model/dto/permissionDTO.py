from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PermissionDTO:
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

    def validate(self) -> bool:
        
        if not self.nombre or not self.nombre.strip():
            return False
        if len(self.nombre) > 100:
            return False
        if not self.descripcion or not self.descripcion.strip():
            return False
        if len(self.descripcion) > 200:
            return False
        return True

    def to_dict(self) -> dict:
        return asdict(self)