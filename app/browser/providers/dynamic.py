from app.db.models import Provider
from app.browser.providers.generic import GenericProviderAdapter


class DynamicAdapter(GenericProviderAdapter):
    def __init__(self) -> None:
        super().__init__(Provider.dynamic)
