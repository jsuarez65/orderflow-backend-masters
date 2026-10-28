
from typing import Any
from pydantic import BaseModel


class OperationResultDTO(BaseModel):
    data: Any = None
    message: str | None = None