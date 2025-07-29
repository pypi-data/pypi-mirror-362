from typing import Optional, List

from pytos2.utils import propify, prop
from pytos2.models import Jsonable


@propify
class SecureChangeAddress(Jsonable):
    ip_address: str = prop("")
    type: str = prop("")


@propify
class Property(Jsonable):
    key: str = prop("")
    value: str = prop("")


@propify
class Properties(Jsonable):
    secure_change_addresses: List[SecureChangeAddress] = prop(
        factory=list, flatify="secure_change_address"
    )
    general_properties: List[Property] = prop(factory=list, flatify="property")
