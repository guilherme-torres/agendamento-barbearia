from typing import List
from fastapi import APIRouter, Depends
from app.catalog_items.dependencies import get_catalog_item_service
from app.catalog_items.schemas import CatalogItemCreateDTO, CatalogItemResponseDTO, CatalogItemUpdateDTO
from app.catalog_items.service import CatalogItemService


router = APIRouter(prefix="/catalog-items", tags=["Catalog Items"])

@router.post("/", response_model=CatalogItemResponseDTO)
async def create_catalog_item(
    data: CatalogItemCreateDTO,
    service: CatalogItemService = Depends(get_catalog_item_service)
):
    return await service.create(data)

@router.get("/", response_model=List[CatalogItemResponseDTO])
async def list_catalog_items(service: CatalogItemService = Depends(get_catalog_item_service)):
    return await service.get_all()

@router.get("/{id}", response_model=CatalogItemResponseDTO)
async def get_catalog_item(id: int, service: CatalogItemService = Depends(get_catalog_item_service)):
    return await service.get(id)

@router.patch("/{id}", response_model=CatalogItemResponseDTO)
async def update_catalog_item(
    id: int,
    data: CatalogItemUpdateDTO,
    service: CatalogItemService = Depends(get_catalog_item_service)
):
    return await service.update(id, data)

@router.delete("/{id}")
async def delete_catalog_item(id: int, service: CatalogItemService = Depends(get_catalog_item_service)):
    return await service.delete(id)