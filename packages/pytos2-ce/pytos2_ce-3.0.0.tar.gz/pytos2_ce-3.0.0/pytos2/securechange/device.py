from typing import List

from pytos2.utils import propify, prop
from pytos2.models import Jsonable


@propify
class DeviceExclusions(Jsonable):
    device_ids: List[int] = prop(factory=list, flatify="id")
