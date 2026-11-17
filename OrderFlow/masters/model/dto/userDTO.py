from typing import Any

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    username: str | None = None
    password: str | None = Field(default=None, repr=False)
    rol: str | None = None

    @classmethod
    def of(cls, data: dict[str, Any]) -> "UserDTO":
        return cls(
            username=data.get("username"),
            password=data.get("password"),
            rol=data.get("rol")
        )

    def validate(self) -> bool:
        if not self.username or not self.username.strip():
            return False
        if len(self.username) > 50:
            return False
        if not self.password or not self.password.strip():
            return False
        if len(self.password) > 255:
            return False
        if not self.rol or not self.rol.strip():
            return False
        if len(self.rol) > 50:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
