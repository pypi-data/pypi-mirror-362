from typing import Optional, List, Union
from enum import Enum

from pytos2.utils import propify, prop
from pytos2.models import Jsonable


@propify
class ServiceObject(Jsonable):
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"
        UID = "uid"
        GLOBAL = "global"

    class ServiceObjectXsiType(Enum):
        TRANSPORT_SERVICE_TYPE = "transport_service"
        IP_SERVICE_TYPE = "ip_service"
        ICMP_SERVICE_TYPE = "icmp_service"
        SERVICE_GROUP_TYPE = "service_group"
        RPC_SERVICE_TYPE = "rpc_service"
        ANY_APPLICATION_TYPE = "any_application"
        ANY_SERVICE_TYPE = "any_service"

    class Referenced(Enum):
        FALSE = "FALSE"
        SELF_TABLE_ONLY = "SELF_TABLE_ONLY"
        UNKNOWN = "UNKNOWN"
        FROM_RULE = "FROM_RULE"
        FROM_NON_RULE_OBJECTS = "FROM_NON_RULE_OBJECTS"
        TRUE = "TRUE"

    xsi_type: ServiceObjectXsiType = prop(ServiceObjectXsiType.TRANSPORT_SERVICE_TYPE)

    min_value_source: Optional[int] = prop(None)
    max_value_source: Optional[int] = prop(None)

    uid: Optional[Union[str, int]] = prop(
        None, converter=str, repr=False, key=Prop.UID.value
    )
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)
    origin: Optional[str] = prop(None, repr=False)
    is_global: Optional[bool] = prop(None, key=Prop.GLOBAL.value, cmp=False, repr=False)
    implicit: Optional[bool] = prop(None, repr=False)
    shared: Optional[bool] = prop(None, repr=False)
    timeout: Optional[int] = prop(None, repr=False)

    comment: Optional[str] = prop(None, repr=False)
    version_id: Optional[int] = prop(None, repr=False)
    referenced: Optional[Referenced] = prop(None, repr=False)
    type_on_device: Optional[str] = prop(None, repr=False)

    negate: Optional[bool] = prop(None, repr=False)
    match_for_any: Optional[bool] = prop(None, repr=False)

    @classmethod
    def from_securetrack(cls, obj):
        return _from_securetrack(obj)


def _from_securetrack(obj):
    from pytos2.securetrack.service_object import (
        TCPServiceObject,
        UDPServiceObject,
        PortServiceObject,
        ICMPServiceObject,
        ICMPV6ServiceObject,
        ICMPV6IPServiceObject,
        ServiceGroup,
        DCERPCService,
        RPCServiceObject,
        OtherIPServiceObject,
        AnyIPServiceObject,
    )

    def _mv_key(j, src, dest):
        if src not in j:
            return

        j[dest] = j[src]
        del j[src]

    j = dict(obj._json)

    if isinstance(obj, (TCPServiceObject, UDPServiceObject, PortServiceObject)):
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.TRANSPORT_SERVICE_TYPE.value
        _mv_key(j, "min", "min_port")
        _mv_key(j, "max", "max_port")

        return TransportService.kwargify(j)
    elif isinstance(
        obj, (ICMPServiceObject, ICMPV6ServiceObject, ICMPV6IPServiceObject)
    ):
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.ICMP_SERVICE_TYPE.value
        _mv_key(j, "min", "min_icmp_type")
        _mv_key(j, "max", "max_icmp_type")
        return ICMPService.kwargify(j)
    elif isinstance(obj, ServiceGroup):
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.SERVICE_GROUP_TYPE.value
        return ServiceGroup.kwargify(j)
    elif isinstance(obj, (DCERPCService, RPCServiceObject)):
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.RPC_SERVICE_TYPE.value
        return ServiceObject.kwargify(j)
    elif isinstance(obj, (OtherIPServiceObject, AnyIPServiceObject)):
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.IP_SERVICE_TYPE.value
        return ServiceObject.kwargify(j)
    else:
        j["@xsi.type"] = ServiceObject.ServiceObjectXsiType.TRANSPORT_SERVICE_TYPE.value
        return TransportService.kwargify(j)


@propify
class TransportService(ServiceObject):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.TRANSPORT_SERVICE_TYPE
    )
    protocol: Optional[int] = prop(None)
    min_port: Optional[int] = prop(None)
    max_port: Optional[int] = prop(None)


@propify
class IPService(ServiceObject):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.IP_SERVICE_TYPE
    )
    min_protocol: Optional[int] = prop(None)
    max_protocol: Optional[int] = prop(None)


@propify
class AnyService(IPService):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.ANY_SERVICE_TYPE
    )


@propify
class ICMPService(ServiceObject):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.ICMP_SERVICE_TYPE
    )
    min_icmp_type: Optional[int] = prop(None)
    max_icmp_type: Optional[int] = prop(None)
    icmp_code: Optional[int] = prop(None)

    management_domain: Optional[str] = prop(None)


@propify
class AnyApplicationService(ServiceObject):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.ANY_APPLICATION_TYPE
    )
    protocol: Optional[int] = prop(None)
    min_port: Optional[int] = prop(None)
    max_port: Optional[int] = prop(None)


@propify
class RPCService(ServiceObject):
    xsi_type: ServiceObject.ServiceObjectXsiType = prop(
        ServiceObject.ServiceObjectXsiType.RPC_SERVICE_TYPE
    )


"""
@propify
class NetworkObject(Jsonable):
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"
        OBJECT_UID = "object_UID"
        GLOBAL = "global"


    uid: Optional[str] = prop(None, converter=str, repr=False)
    name: Optional[str] = prop(None, repr=False)
    display_name: Optional[str] = prop(None)
    origin: Optional[str] = prop(None, repr=False)
    is_global: Optional[bool] = prop(None, key=Prop.GLOBAL.value, cmp=False, repr=False)

    implicit: Optional[bool] = prop(None, repr=False)
    shared: Optional[bool] = prop(None, repr=False)
    ip_type: Optional[str] = prop(None)
    installable_target: Optional[bool] = prop(None, repr=False)
    group_ids: Optional[str] = prop(None, repr=False)  # belone to group
"""


def classify_service_type(service_object):
    if (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.TRANSPORT_SERVICE_TYPE.value
    ):
        return TransportService.kwargify(service_object)
    elif (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.IP_SERVICE_TYPE.value
    ):
        return IPService.kwargify(service_object)
    elif (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.ICMP_SERVICE_TYPE.value
    ):
        return ICMPService.kwargify(service_object)
    elif (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.SERVICE_GROUP_TYPE.value
    ):
        return ServiceGroup.kwargify(service_object)
    elif (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.ANY_APPLICATION_TYPE.value
    ):
        return AnyApplicationService.kwargify(service_object)
    elif (
        service_object["@xsi.type"]
        == ServiceObject.ServiceObjectXsiType.ANY_SERVICE_TYPE.value
    ):
        return AnyService.kwargify(service_object)
    else:
        return ServiceObject.kwargify(service_object)


@propify
class ServiceGroup(ServiceObject):
    class Prop(Enum):
        MEMBER = "member"

    members: List[Union[TransportService, IPService, ICMPService]] = prop(
        factory=list, repr=False, key=Prop.MEMBER.value, kwargify=classify_service_type
    )
