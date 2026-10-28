from dataclasses import dataclass
<<<<<<< Updated upstream
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
    city: Optional[str]=None 
=======
from typing import Optional

@dataclass
class ProviderDTO:
    cuit: Optional[str] = None 
    company_name: Optional[str] = None 
    address: Optional[str] = None  
    email: Optional[str] = None 
    phone: Optional[str] = None 
    postal_code: Optional[str] = None 
    state_name: Optional[str] = None 
>>>>>>> Stashed changes
