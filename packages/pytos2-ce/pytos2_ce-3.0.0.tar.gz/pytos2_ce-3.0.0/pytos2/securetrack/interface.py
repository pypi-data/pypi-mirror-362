from enum import Enum
from typing import Optional, List

from attr.converters import optional
import attr

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify, get_api_node

import netaddr  # type: ignore
from netaddr import IPAddress, IPNetwork, IPRange  # type: ignore

from pytos2 import securetrack


class InterfaceXsiType(Enum):
    INTERFACE = "interfaceDTO"


@propify
class InterfaceIP(Jsonable):
    class Prop(Enum):
        IP = "ip"
        NETMASK = "netmask"

    netmask: Optional[IPNetwork] = prop(None)
    ip: Optional[IPAddress] = prop(None)
    visibility: Optional[str] = prop(None)
    precedence: Optional[str] = prop(None)


@propify
class Interface(Jsonable):
    class Meta(Enum):
        ROOT = "interface"

    class Prop(Enum):
        GLOBAL = "global"

    id: int = prop(None)
    uid: Optional[str] = prop(None)
    device_id: Optional[int] = prop(None, converter=optional(int))
    name: str = prop(None)
    is_global: bool = prop(False, key=Prop.GLOBAL.value)
    zone_id: int = prop(None)
    implicit: bool = prop(False, repr=False)
    interface_ips: List[IPAddress] = prop(factory=list, repr=False)
    int_ip_list: List[IPAddress] = prop(factory=list)
    acl_name: str = prop(None)
    direction: str = prop(None)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        int_list = _obj.get("interface_ips")

        if len(int_list) > 0:
            try:
                raw_ips = int_list.get("interface_ip")
                for i in raw_ips:
                    ip_addr = f"{i['ip']}/{IPAddress(i['netmask']).netmask_bits()}"
                    kwargs["int_ip_list"].append(ip_addr)
            except Exception as e:  # pragma: no cover
                pass

        return cls(**kwargs)


class BindableObjectXsiType(Enum):
    BINDABLE_OBJECT = "BindableObjectDTO"


@propify
class BindableObject(Interface):
    class Prop(Enum):
        GLOBAL = "global"

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        int_list = _obj.get("interface_ips")

        if len(int_list) > 0:
            try:
                raw_ips = int_list.get("interface_ip")
                for i in raw_ips:
                    ip_addr = f"{i['ip']}/{IPAddress(i['netmask']).netmask_bits()}"
                    kwargs["int_ip_list"].append(ip_addr)
            except Exception as e:  # pragma: no cover
                pass

        return cls(**kwargs)


@propify
class TopologyInterface(Jsonable):
    class Meta(Enum):
        ROOT = "interface"

    class Prop(Enum):
        IP_ADDRESS = "ip"
        NETMASK = "mask"
        CIDR = "cidr"

    ip: Optional[IPAddress] = prop(None)
    device_id: Optional[int] = prop(None, converter=optional(int))
    virtual_router: Optional[str] = prop(None)
    generic_device_id: Optional[int] = prop(None)
    name: str = prop(None)
    zone: Optional[int] = prop(None)
    mask: Optional[IPAddress] = prop(None, repr=False)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        kwargs["ip"] = IPNetwork(f"{_obj['ip']}/{_obj.get('mask', '32')}")

        return cls(**kwargs)


@propify
class PolicyZone(Jsonable):
    is_global: Optional[bool] = prop(False)
    name: Optional[str] = prop(None)
