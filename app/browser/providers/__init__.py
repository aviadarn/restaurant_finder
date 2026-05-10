from app.db.models import Provider
from app.browser.providers.base import ProviderAdapter
from app.browser.providers.dynamic import DynamicAdapter
from app.browser.providers.opentable import OpentableAdapter
from app.browser.providers.resy import ResyAdapter
from app.browser.providers.sevenrooms import SevenroomsAdapter
from app.browser.providers.tock import TockAdapter
from app.browser.providers.yelp import YelpAdapter


def build_provider_registry() -> dict[Provider, ProviderAdapter]:
    return {
        Provider.resy: ResyAdapter(),
        Provider.opentable: OpentableAdapter(),
        Provider.tock: TockAdapter(),
        Provider.sevenrooms: SevenroomsAdapter(),
        Provider.yelp: YelpAdapter(),
        Provider.dynamic: DynamicAdapter(),
    }
