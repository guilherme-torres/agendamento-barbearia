from typing import Annotated
from fastapi import Depends
from app.catalog_items.repository import CatalogItemRepository
from app.catalog_items.service import CatalogItemService


def get_catalog_item_repo():
    return CatalogItemRepository()

def get_catalog_item_service(catalog_item_repo: Annotated[CatalogItemRepository, Depends(get_catalog_item_repo)]):
    return CatalogItemService(catalog_item_repo)