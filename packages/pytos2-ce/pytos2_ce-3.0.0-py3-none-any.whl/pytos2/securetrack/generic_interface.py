from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj

from netaddr import IPAddress


@propify
class GenericInterface(Jsonable):
    class Type(Enum):
        EXTERNAL = "external"
        INTERNAL = "internal"

    id: Optional[int] = prop(None, converter=optional(int))
    device_id: Optional[int] = prop(None, converter=optional(int), key="mgmtId")
    name: str = prop(None)
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    mask: Optional[IPAddress] = prop(
        None,
        converter=optional(IPAddress),
        jsonify=stringify_optional_obj,
    )
    vrf: Optional[str] = prop(None)
    mpls: Optional[bool] = prop(False)
    unnumbered: Optional[bool] = prop(False)
    type: Optional[Type] = prop(None)
