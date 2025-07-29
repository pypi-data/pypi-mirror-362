from enum import Enum
from typing import Optional

from pytos2.utils import propify, prop, kwargify
from pytos2.models import Jsonable


@propify
class GenericDevice(Jsonable):
    id: Optional[int] = prop(None)
    customer_id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
