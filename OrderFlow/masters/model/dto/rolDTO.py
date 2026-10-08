from dataclasses import dataclass
from typing import Optional

@dataclass
class RolDTO:
    rol: Optional[str] = None
    
    def validate(self) -> bool:
        if not self.rol or not self.rol.strip():
            return False
        return True
    
    
    