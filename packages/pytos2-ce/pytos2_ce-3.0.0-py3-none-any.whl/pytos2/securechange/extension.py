from typing import Optional, List

from enum import Enum

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify, get_api_node


@propify
class MarketplaceApp(Jsonable):
    class Prop(Enum):
        APP_ID = "appId"

    id: str = prop(key="appId")
    name: str = prop("")
    description: str = prop("", repr=False)
    url: str = prop("")
    version: str = prop("")
    installed: bool = prop(False)
    upsell: bool = prop(False, repr=False)

    @property
    def app_id(self):
        return self.id

    @app_id.setter
    def app_id(self, v):
        self.id = v
