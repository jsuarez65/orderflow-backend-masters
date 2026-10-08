from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class UserDTO:
    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None

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

    def to_dict(self) -> dict:
        return asdict(self)

    def __repr__(self) -> str:
        return (
            f"UserDTO(username={self.username!r}, "
            f"password='***', rol={self.rol!r})"
        )