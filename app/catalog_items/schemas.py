from datetime import timedelta
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CatalogItemBase(BaseModel):
    barber_id: int
    name: str
    description: str
    price: float
    duration: timedelta


class CatalogItemCreateDTO(CatalogItemBase):
    pass


class CatalogItemResponseDTO(CatalogItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CatalogItemUpdateDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[timedelta] = None