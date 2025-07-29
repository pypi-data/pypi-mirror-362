from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj

from netaddr import IPAddress


@propify
class GenericRoute(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    device_id: Optional[int] = prop(None, converter=optional(int), key="mgmtId")
    destination: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    mask: Optional[IPAddress] = prop(
        None,
        converter=optional(IPAddress),
        jsonify=stringify_optional_obj,
    )
    interface_name: str = prop(None, key="interfaceName")
    next_hop: Optional[str] = prop(None, key="nextHop")
    next_hop_type: Optional[str] = prop(None, key="nextHopType")
    vrf: Optional[str] = prop(None)
