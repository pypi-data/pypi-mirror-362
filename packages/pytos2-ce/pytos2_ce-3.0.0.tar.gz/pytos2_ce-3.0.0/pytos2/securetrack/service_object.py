from enum import Enum
from typing import Optional, List, Union

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop


class ServiceXsiType(Enum):
    SERVICE_GROUP_OBJECT = "serviceGroupDTO"
    SINGLE_SERVICE_OBJECT = "singleServiceDTO"


@propify
class Service(Jsonable):
    class ClassName(Enum):
        # classname and # type map
        ANY_OBJECT = "any_object"  # ip_service
        TCP_SERVICE = "tcp_service"  # tcp_service
        ICMP_SERVICE = "icmp_service"  # icmp_service
        OTHER_SERVICE = "other_service"  # ip_service, other_service
        UDP_SERVICE = "udp_service"  # udp_service
        SERVICE_GROUP = "service_group"  # group
        RPC_SERVICE = "rpc_service"  # rpc_service
        DCERPC_SERVICE = "dcerpc_service"  # other_service
        COMPOUND_TCP_SERVICE = "compound_tcp_service"  # other_service
        GTP_MM_V1_SERVICE = "gtp_mm_v1_service"  # other_service
        GTP_MM_V0_SERVICE = "gtp_mm_v0_service"  # other_service
        GTP_SERVICE = "gtp_service"  # other_service
        GTP_V1_SERVICE = "gtp_v1_service"  # other_service
        ICMP_V6_SERVICE = "icmp_v6_service"  # other_service (no min/max port)
        ICMPV6_SERVICE = "icmpv6_service"  # ip_service (has min/max port)
        PORT_SERVICE = "port_service"  # port_service
        TCP_CITRIX_SERVICE = "tcp_citrix_service"  # other_service
        SERVICE = "service"  # other_service

    class Type(Enum):
        TCP_SERVICE = "tcp_service"
        IP_SERVICE = "ip_service"
        GROUP = "group"
        ICMP_SERVICE = "icmp_service"
        UDP_SERVICE = "udp_service"
        OTHER_SERVICE = "other_service"
        RPC_SERVICE = "rpc_service"
        PORT_SERVICE = "port_service"

    class Protocol(Enum):
        TCP = 6
        UDP = 17
        ICMP = 13

    class Prop(Enum):
        XSI_TYPE = "@xsi.type"
        GLOBAL = "global"
        MIN = "min"
        MAX = "max"
        IMPLICIT = "implicit"
        ICMP_CODE = "icmp_code"

    xsi_type: Optional[ServiceXsiType] = prop(
        None, key=Jsonable.Prop.XSI_TYPE.value, repr=False
    )
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)
    class_name: Optional[ClassName] = prop(None, repr=False)
    type: Optional[Type] = prop(None, repr=False)
    is_global: bool = prop(False, key=Prop.GLOBAL.value, repr=False)
    comment: Optional[str] = prop(None, repr=False)
    uid: Optional[str] = prop(None, repr=False)
    overrides: bool = prop(False, repr=False)
    negate: bool = prop(False, repr=False)
    timeout: Optional[Union[str, int]] = prop(None, repr=False)
    is_implicit: bool = prop(False, repr=False, key=Prop.IMPLICIT.value)

    device_id: Optional[int] = prop(None, repr=False)


@propify
class ServiceObjectReference(Jsonable):
    uid: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)


@propify
class TCPServiceObject(Service):
    protocol: Optional[int] = prop(None)
    min_port: Optional[int] = prop(None, key=Service.Prop.MIN.value)
    max_port: Optional[int] = prop(None, key=Service.Prop.MAX.value)


@propify
class UDPServiceObject(Service):
    protocol: Optional[int] = prop(None, converter=optional(int))
    min_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MIN.value
    )
    max_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MAX.value
    )


@propify
class ICMPServiceObject(Service):
    protocol: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.ICMP_CODE.value
    )
    min_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MIN.value
    )
    max_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MAX.value
    )


@propify
class IPServiceObject(Service):
    min_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MIN.value
    )
    max_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MAX.value
    )


@propify
class PortServiceObject(Service):
    min_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MIN.value
    )
    max_port: Optional[int] = prop(
        None, converter=optional(int), key=Service.Prop.MAX.value
    )


@propify
class ICMPV6ServiceObject(Service):
    management_domain_securetrack_name: Optional[str] = prop(None)
    management_domain: Optional[str] = prop(None)


@propify
class ICMPV6IPServiceObject(IPServiceObject, ICMPV6ServiceObject):
    pass


@propify
class OtherServiceObject(Service):
    pass


@propify
class OtherIPServiceObject(OtherServiceObject, IPServiceObject):
    pass


@propify
class AnyObject(Service):
    pass


@propify
class AnyIPServiceObject(AnyObject, IPServiceObject):
    pass


@propify
class ServiceGroup(Service):
    class Prop(Enum):
        MEMBER = "member"

    members: List[ServiceObjectReference] = prop(
        key=Prop.MEMBER.value, factory=list, repr=False
    )


@propify
class RPCServiceObject(Service):
    pass


@propify
class DCERPCService(Service):
    pass


@propify
class DefaultService(Service):
    pass


def classify_service_object(obj):
    # Handle a raer case where the singleServiceDTO result is missing a class_name
    key_name = "class_name" if "class_name" in obj else "type"

    if obj[key_name] == Service.ClassName.TCP_SERVICE.value:
        return TCPServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.UDP_SERVICE.value:
        return UDPServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.ICMP_SERVICE.value:
        return ICMPServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.SERVICE_GROUP.value:
        return ServiceGroup.kwargify(obj)
    elif obj[key_name] == Service.ClassName.OTHER_SERVICE.value:
        if obj["type"] == Service.Type.IP_SERVICE.value:
            return OtherIPServiceObject.kwargify(obj)
        elif obj["type"] == Service.Type.OTHER_SERVICE.value:
            return OtherServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.RPC_SERVICE.value:
        return RPCServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.DCERPC_SERVICE.value:
        return DCERPCService.kwargify(obj)
    elif obj[key_name] == Service.ClassName.ANY_OBJECT.value:
        if obj["type"] == Service.Type.IP_SERVICE.value:
            return AnyIPServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.PORT_SERVICE.value:
        return PortServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.ICMPV6_SERVICE.value:
        return ICMPV6IPServiceObject.kwargify(obj)
    elif obj[key_name] == Service.ClassName.ICMP_V6_SERVICE.value:
        return ICMPV6ServiceObject.kwargify(obj)
    else:  # ultimate safe catch
        return DefaultService.kwargify(obj)  # pragma: no cover
