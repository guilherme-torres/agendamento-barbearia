from app.exceptions import AppBaseException


class CatalogItemNotFound(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Serviço não encontrado",
            error_code="catalog_item_not_found",
            status_code=404
        )