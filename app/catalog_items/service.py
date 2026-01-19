from fastapi import HTTPException
from app.catalog_items.repository import CatalogItemRepository
from app.catalog_items.schemas import CatalogItemCreateDTO, CatalogItemResponseDTO, CatalogItemUpdateDTO


class CatalogItemService:
    def __init__(self, catalog_item_repo: CatalogItemRepository):
        self.catalog_item_repo = catalog_item_repo
    
    async def create(self, data: CatalogItemCreateDTO):
        catalog_item = await self.catalog_item_repo.create(data)
        return CatalogItemResponseDTO.model_validate(catalog_item)
    
    async def get_all(self):
        catalog_items = await self.catalog_item_repo.get_all()
        return [CatalogItemResponseDTO.model_validate(catalog_item) for catalog_item in catalog_items]
    
    async def get(self, id: int):
        catalog_item = await self.catalog_item_repo.get(id)
        if not catalog_item:
            raise HTTPException(404, "serviço não encontrado")
        return CatalogItemResponseDTO.model_validate(catalog_item)
    
    async def update(self, id: int, data: CatalogItemUpdateDTO):
        catalog_item = await self.catalog_item_repo.update(id, data.model_dump(exclude_unset=True))
        if not catalog_item:
            raise HTTPException(404, "serviço não encontrado")
        return CatalogItemResponseDTO.model_validate(catalog_item)

    async def delete(self, id: int):
        catalog_item_id = await self.catalog_item_repo.delete(id)
        if not catalog_item_id:
            raise HTTPException(404, "serviço não encontrado")
        return None