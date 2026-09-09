from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ProviderDTO:
    cuit: Optional[str]=None 
    company_name: Optional[str]=None 
    address: Optional[str]=None 
    email: Optional[str]=None 
    phone: Optional[str]=None 
    postal_code: Optional[str]=None 
    state_name: Optional[str]=None 