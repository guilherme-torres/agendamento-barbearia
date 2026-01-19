from dataclasses import dataclass
from datetime import timedelta


@dataclass
class CatalogItem:
    id: int
    barber_id: int
    name: str
    description: str
    price: float
    duration: timedelta