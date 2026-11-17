from pydantic import BaseModel
from dataclasses import dataclass, asdict



class PermissionDTO(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None

    @classmethod
    def of (cls, data: dict) -> "PermissionDTO":
        return cls(
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion")
        )
