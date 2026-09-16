from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ProviderDTO:
    cuit: str=None 
    companyName: str=None 
    address: Optional[str]=None 
    email: Optional[str]=None 
    phone: Optional[str]=None 
    postalCode: Optional[str]=None 
    stateName: Optional[str]=None 