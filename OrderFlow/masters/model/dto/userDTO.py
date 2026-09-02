from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class userDTO:
    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None