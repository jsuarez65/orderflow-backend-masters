from pydantic import BaseModel
from dataclasses import dataclass, asdict

class RolDTO(BaseModel):
    rol: str | None = None
    
    @classmethod
    def of (cls, data: dict) -> "RolDTO":
        return cls(
            rol=data.get("rol")
        )
    