from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj
from netaddr import IPAddress


@propify
class GenericIgnoredInterface(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int), repr=False)
    interface_name: str = prop(None, key="interfaceName")
    device_id: Optional[int] = prop(None, converter=optional(int), key="mgmtId")
    ip: Optional[IPAddress] = prop(
        None,
        jsonify=stringify_optional_obj,
        converter=optional(IPAddress),
    )
