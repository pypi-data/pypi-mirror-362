from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj

from netaddr import IPAddress


@propify
class GenericVpn(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    device_id: Optional[int] = prop(None, converter=optional(int), key="deviceId")
    generic: Optional[bool] = prop(None)
    vpn_name: Optional[str] = prop(None, key="vpnName")
    interface_name: Optional[str] = prop(None, key="interfaceName")
    tunnel_source_ip_addr: Optional[IPAddress] = prop(
        None,
        repr=False,
        jsonify=stringify_optional_obj,
        converter=optional(IPAddress),
        key="tunnelSourceIpAddr",
    )
    tunnel_dest_ip_addr: Optional[IPAddress] = prop(
        None,
        repr=False,
        jsonify=stringify_optional_obj,
        converter=optional(IPAddress),
        key="tunnelDestIpAddr",
    )
