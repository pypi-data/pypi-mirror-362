import re
from copy import deepcopy
from datetime import datetime, date as datetime_date, time as datetime_time
from enum import Enum
from typing import Optional, List, ClassVar, Union

import attr
import netaddr
from netaddr import IPNetwork, IPRange, IPAddress  # type: ignore
from requests.exceptions import HTTPError

from pytos2.models import Jsonable, UnMapped
from pytos2.securechange.designer import DesignerResults
from pytos2.securechange.entrypoint import Scw
from pytos2.securechange.related_rules import RelatedRulesResult
from pytos2.securechange.risk_results import RiskAnalysisResult
from pytos2.securechange.service import PredefinedServiceName, ApplicationIdentityName
from pytos2.securechange.verifier import (
    AccessRequestVerifierResult,
    VerifierResultLink,
    classify_verifier_result,
)
from pytos2.securetrack import network_object
from pytos2.securetrack.device import Device
from pytos2.securetrack.entrypoint import St
from pytos2.securetrack.network_object import NetworkObjectGroup
from pytos2.securetrack.rule import BindingPolicy

# Avoid circular imports
from pytos2.utils import (
    jsonify,
    kwargify,
    propify,
    prop,
    sanitize_uid,
    TimeFormat,
)


# These are things that fields contains that aren't primitives.
# Things that can be PUT or POSTed should be mapped


# Field classes, Everything top level should be mapped
class FieldXsiType(Enum):
    MULTI_ACCESS_REQUEST = "multi_access_request"
    MULTI_SERVER_DECOMMISSION_REQUEST = "multi_server_decommission_request"
    RULE_DECOMMISSION = "rule_decommission"
    RULE_RECERTIFICATION = "rule_recertification"
    RULE_MODIFICATION_FIELD = "rule_modification_field"
    APPLICATION_CHANGE_APPROVE = "application_change_approve"
    APPLICATION_CHANGE_IMPLEMENT = "application_change_implement"
    MULTI_TEXT_AREA = "multi_text_area"
    TEXT_AREA = "text_area"
    MULTIPLE_SELECTION = "multiple_selection"
    MULTI_HYPERLINK = "multi_hyperlink"
    MULTI_GROUP_CHANGE = "multi_group_change"
    MULTI_TEXT_FIELD = "multi_text_field"
    MULTI_TARGET = "multi_target"
    MULTI_NETWORK_OBJECT = "multi_network_object"
    MULTI_SERVICE = "multi_service"
    APPROVE_REJECT = "approve_reject"
    CHECKBOX = "checkbox"
    DROP_DOWN_LIST = "drop_down_list"
    DATE = "date"
    TIME = "time"
    TEXT_FIELD = "text_field"
    MANAGER = "manager"
    HYPERLINK = "hyperlink"
    CLONE_SERVER_POLICY_REQUEST = "clone_server_policy_request"


class AtType(str, Enum):
    NETWORK = "NETWORK"
    HOST = "HOST"
    IP = "IP"
    RANGE = "RANGE"
    DNS = "DNS"
    OBJECT = "Object"
    INTERNET = "INTERNET"
    LDAP = "LDAP"
    EXTERNAL_RESOURCE = "EXTERNAL_RESOURCE"
    ANY = "ANY"


@propify
class Object(Jsonable):
    class Prop(Enum):
        ID = "id"
        OBJECT_NAME = "object_name"
        OBJECT_UID = "object_UID"
        AT_TYPE = "@type"
        OBJECT_TYPE = "object_type"

    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    at_type: AtType = prop(AtType.OBJECT, key=Prop.AT_TYPE.value, cmp=False, repr=False)

    uid: Optional[str] = prop(None, key=Prop.OBJECT_UID.value, cmp=False, repr=False)
    management_id: Optional[int] = prop(None, converter=attr.converters.optional(int))
    management_name: Optional[str] = prop(None, repr=False, cmp=False)
    name: Optional[str] = prop(None, key=Prop.OBJECT_NAME.value)
    type: Optional[str] = prop(None, key=Prop.OBJECT_TYPE.value, cmp=False, repr=False)


@propify
class Link(Jsonable):
    class Prop(Enum):
        HREF = "@href"

    href: str = prop("http://", key=Prop.HREF.value)


@propify
class Option(Jsonable):
    class Prop(Enum):
        VALUE = "value"

    value: Optional[str] = prop(None)


@propify
class Zone(Jsonable):
    is_global: Optional[str] = prop(False)
    name: Optional[str] = prop(None)

    def __str__(self):
        return self.name


@propify
class AddressBook(Jsonable):
    name: str = prop()

    def __str__(self):
        return self.name


@propify
class Any(Object):
    at_type: AtType = prop(AtType.ANY, key=Object.Prop.AT_TYPE.value)


@propify
class NetworkObject(Object):
    at_type: AtType = prop(AtType.ANY, key=Object.Prop.AT_TYPE.value)


@propify
class Target(Object):
    class ObjectType(Enum):
        ACL = "acl"
        FIREWALL = "firewall"
        POLICY = "policy"
        ZONE_TO_ZONE = "zone_to_zone"

    at_type: AtType = prop(AtType.OBJECT, key=Object.Prop.AT_TYPE.value)
    type: ObjectType = prop(
        ObjectType.FIREWALL, key=Object.Prop.OBJECT_TYPE.value, cmp=True, repr=False
    )


def classify_service_type(ar_service_json):
    ret = Any()
    if ar_service_json["@type"] == Service.ServiceAtType.PROTOCOL.value:
        if ar_service_json["protocol"] == Service.Protocol.TCP.value:
            ret = TCPService.kwargify(ar_service_json)
        elif ar_service_json["protocol"] == Service.Protocol.UDP.value:
            ret = UDPService.kwargify(ar_service_json)
        elif ar_service_json["protocol"] == Service.Protocol.ICMP.value:
            ret = ICMPService.kwargify(ar_service_json)
        elif ar_service_json["protocol"] == Service.Protocol.OTHER.value:
            ret = OtherService.kwargify(ar_service_json)

    elif ar_service_json["@type"] == Service.ServiceAtType.PREDEFINED.value:
        if ar_service_json["protocol"] == Service.Protocol.OTHER.value:
            ret = PredefinedOtherService.kwargify(ar_service_json)

        elif ar_service_json["protocol"] == Service.Protocol.TCP.value:
            ret = PredefinedTCPService.kwargify(ar_service_json)
        elif ar_service_json["protocol"] == Service.Protocol.UDP.value:
            ret = PredefinedUDPService.kwargify(ar_service_json)
        elif ar_service_json["protocol"] == Service.Protocol.ICMP.value:
            ret = PredefinedICMPService.kwargify(ar_service_json)

    elif ar_service_json["@type"] == Service.ServiceAtType.APPLICATION_IDENTITY.value:
        ret = ApplicationIdentity.kwargify(ar_service_json)

    elif ar_service_json["@type"] == Service.ServiceAtType.OBJECT.value:
        if ar_service_json["object_type"] == ExistService.ObjectType.GROUP.value:
            ret = ServiceGroup.kwargify(ar_service_json)

        elif ar_service_json["object_type"] == ExistService.ObjectType.TCP.value:
            ret = ExistTCPService.kwargify(ar_service_json)
        elif ar_service_json["object_type"] == ExistService.ObjectType.UDP.value:
            ret = ExistUDPService.kwargify(ar_service_json)
        elif ar_service_json["object_type"] == ExistService.ObjectType.ICMP.value:
            ret = ExistICMPService.kwargify(ar_service_json)
        elif ar_service_json["object_type"] == ExistService.ObjectType.OTHER.value:
            ret = ExistOtherService.kwargify(ar_service_json)
    ret.xsi_type = "serviceDTO"
    return ret


@propify
class Service(Jsonable):
    class Prop(Enum):
        ID = "id"
        XSI_TYPE = "@xsi.type"
        AT_TYPE = "@type"
        PROTOCOL = "PROTOCOL"

    class Protocol(Enum):
        TCP = "TCP"
        UDP = "UDP"
        ICMP = "ICMP"
        OTHER = "OTHER"

    class ServiceAtType(Enum):
        PROTOCOL = "PROTOCOL"
        PREDEFINED = "PREDEFINED"
        APPLICATION_IDENTITY = "APPLICATION_IDENTITY"
        OBJECT = "Object"

    @classmethod
    def from_string(cls, string):
        parts = re.split(r"\s+", string)
        at_type = Service.ServiceAtType.PROTOCOL

        if parts[0].lower() == "tcp":
            return TCPService(
                at_type=at_type, protocol=Service.Protocol.TCP, port=parts[1]
            )
        elif parts[0].lower() == "udp":
            return UDPService(
                at_type=at_type, protocol=Service.Protocol.UDP, port=parts[1]
            )
        elif parts[0].lower() == "icmp":
            return ICMPService(
                at_type=at_type, protocol=Service.Protocol.ICMP, type=parts[1]
            )
        else:
            try:
                return PredefinedService(
                    at_type=Service.ServiceAtType.PREDEFINED,
                    name=PredefinedServiceName(string),
                )
            except ValueError:
                return ApplicationIdentity(
                    at_type=Service.ServiceAtType.APPLICATION_IDENTITY,
                    name=ApplicationIdentityName(string),
                )

    at_type: ServiceAtType = prop(None, key=Prop.AT_TYPE.value, cmp=False, repr=False)


@propify
class ExistService(Object):
    class Prop(Enum):
        OBJECT_DETAILS = "object_details"

    class ObjectType(Enum):
        TCP = "tcp"
        UDP = "udp"
        ICMP = "icmp"
        GROUP = "group"
        OTHER = "other"

    obj_type: Optional[str] = prop(None, key=Object.Prop.OBJECT_TYPE.value)


@propify
class TCPService(Service):
    protocol: Optional[str] = prop(None)
    port: Optional[str] = prop(None, repr=True)


@propify
class UDPService(Service):
    protocol: Optional[str] = prop(None)
    port: Optional[str] = prop(None, repr=True)


@propify
class ICMPService(Service):
    protocol: Optional[str] = prop(None)
    type: Optional[str] = prop(None, repr=True)


@propify
class OtherService(Service):
    protocol: Optional[str] = prop(None)
    type: Optional[str] = prop(None, repr=True)


@propify
class ServiceGroup(ExistService):
    @property
    def members(self) -> List[str]:
        return self.object_details.split(" , ")

    object_details: Optional[str] = prop(None)


@propify
class ExistTCPService(ExistService, TCPService):
    protocol: Optional[str] = prop(None, key=Object.Prop.OBJECT_TYPE.value)
    port: Optional[str] = prop(None, key=ExistService.Prop.OBJECT_DETAILS.value)


@propify
class ExistUDPService(ExistService, UDPService):
    protocol: Optional[str] = prop(None, key=Object.Prop.OBJECT_TYPE.value)
    port: Optional[str] = prop(None, key=ExistService.Prop.OBJECT_DETAILS.value)


@propify
class ExistICMPService(ExistService, ICMPService):
    protocol: Optional[str] = prop(None, key=Object.Prop.OBJECT_TYPE.value)
    type: Optional[str] = prop(None, key=ExistService.Prop.OBJECT_DETAILS.value)


@propify
class ExistOtherService(ExistService, OtherService):
    protocol: Optional[str] = prop(None, key=Object.Prop.OBJECT_TYPE.value)
    type: Optional[str] = prop(None, key=ExistService.Prop.OBJECT_DETAILS.value)


@propify
class PredefinedService(Service):
    class Prop(Enum):
        PREDEFINED_NAME = "predefined_name"

    name: Optional[PredefinedServiceName] = prop(None, key=Prop.PREDEFINED_NAME.value)


@propify
class PredefinedTCPService(PredefinedService, TCPService):
    pass


@propify
class PredefinedUDPService(PredefinedService, UDPService):
    pass


@propify
class PredefinedICMPService(PredefinedService, ICMPService):
    pass


@propify
class PredefinedOtherService(PredefinedService, OtherService):
    pass


@propify
class ApplicationIdentity(Service):
    class Prop(Enum):
        APPLICATION_NAME = "application_name"

    name: Optional[ApplicationIdentityName] = prop(
        None, key=Prop.APPLICATION_NAME.value
    )
    services: List[
        Union[TCPService, UDPService, ICMPService, OtherService, ServiceGroup]
    ] = prop(factory=list, flatify="service", kwargify=classify_service_type)


@propify
class DNSObject(Object):
    class Prop(Enum):
        HOST_NAME = "host_name"
        DNS_IP_ADDRESSES = "dns_ip_addresses"

    at_type: AtType = prop(AtType.DNS, key=Object.Prop.AT_TYPE.value)
    host_name: Optional[str] = prop(None)
    dns_ip_addresses: List[IPAddress] = prop(factory=list, flatify="ip_address")

    @property
    def _json(self):
        if self._json_override is not None:
            return self._json_override
        _self = deepcopy(self)
        _self.dns_ip_addresses = [str(i) for i in _self.dns_ip_addresses]
        return jsonify(_self)

    @_json.setter
    def _json(self, val):
        self._json_override = val


@propify
class IPObject(Object):
    class Prop(Enum):
        IP_ADDRESS = "ip_address"
        NETMASK = "netmask"
        CIDR = "cidr"

    at_type: AtType = prop(AtType.IP, key=Object.Prop.AT_TYPE.value)

    # This might look strange, but this is how to use a managed property in attr
    _subnet: IPNetwork
    _ip_address: Optional[IPAddress] = prop(
        None, jsonify=Prop.IP_ADDRESS.value, cmp=False, init=False, repr=False
    )
    _netmask: IPAddress = prop(
        "255.255.255.255", jsonify=False, cmp=False, init=False, repr=False
    )
    _cidr: Optional[int] = prop(
        None,
        key=Prop.CIDR.value,
        cmp=False,
        init=False,
        jsonify=Prop.CIDR.value,
        repr=False,
    )

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        try:
            kwargs["subnet"] = IPNetwork(
                f"{_obj['ip_address']}/{_obj.get('netmask', '32')}"
            )
            return cls(**kwargs)
        except netaddr.core.AddrFormatError:
            kwargs["subnet"] = None
            r = cls(**kwargs)
            r._netmask = _obj.get(cls.Prop.NETMASK.value)
            r._ip_address = _obj.get(cls.Prop.IP_ADDRESS.value)
            return r

    @property
    def subnet(self):
        return self._subnet

    @subnet.setter
    def subnet(self, val):
        try:
            self._subnet = IPNetwork(val)
        except Exception:
            raise ValueError(
                "IPObject.subnet must be either an IPNetwork object or a valid argument to it's constructor, eg. 1.2.3.0/24"
            )

    @property
    def ip_address(self):
        return str(self.subnet.network if self.subnet else self._ip_address)

    @property
    def netmask(self):
        return str(self.subnet.netmask if self.subnet else self._netmask)

    @property
    def cidr(self):
        return int(self.subnet.prefixlen if self.subnet else self._cidr)


@propify
class NatIPObject(IPObject):
    class Prop(Enum):
        NAT_IP_ADDRESS = "nat_ip_address"
        NAT_NETMASK = "nat_netmask"

    _nat_subnet: IPNetwork
    _nat_ip_address: Optional[IPNetwork] = prop(
        None, jsonify=Prop.NAT_IP_ADDRESS.value, cmp=False, init=False, repr=False
    )
    _nat_netmask: IPNetwork = prop(
        "255.255.255.255",
        jsonify=Prop.NAT_NETMASK.value,
        cmp=False,
        init=False,
        repr=False,
    )

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        kwargs["subnet"] = IPNetwork(
            f"{_obj['ip_address']}/{_obj.get('netmask', '32')}"
        )
        kwargs["nat_subnet"] = IPNetwork(
            f"{_obj['nat_ip_address']}/{_obj.get('nat_netmask', '32')}"
        )
        return cls(**kwargs)

    @property
    def nat_subnet(self):
        return self._nat_subnet

    @property
    def nat_ip_address(self):
        return str(self.nat_subnet.network)

    @property
    def nat_netmask(self):
        return str(self.nat_subnet.netmask)

    @property
    def nat_cidr(self):
        return int(self.nat_subnet.prefixlen)

    @nat_subnet.setter
    def nat_subnet(self, val):
        try:
            self._nat_subnet = IPNetwork(val)
        except Exception:
            raise ValueError(
                "NatIPObject.nat_subnet must be either an IPNetwork object or a valid argument to it's constructor, eg. 1.2.3.0/24"
            )


@propify
class RangeObject(Object):
    class Prop(Enum):
        RANGE_FIRST_IP = "range_first_ip"
        RANGE_LAST_IP = "range_last_ip"

    at_type: AtType = prop(AtType.RANGE, key=Object.Prop.AT_TYPE.value)

    _range: IPRange
    _range_first_ip: Optional[IPAddress] = prop(
        None, cmp=False, init=False, jsonify=Prop.RANGE_FIRST_IP.value, repr=False
    )
    _range_last_ip: Optional[IPAddress] = prop(
        None, cmp=False, init=False, jsonify=Prop.RANGE_LAST_IP.value, repr=False
    )

    @classmethod
    def kwargify(cls, obj: dict) -> "RangeObject":
        _obj, kwargs = kwargify(cls, obj)
        kwargs["range"] = IPRange(
            _obj[cls.Prop.RANGE_FIRST_IP.value], _obj[cls.Prop.RANGE_LAST_IP.value]
        )
        return cls(**kwargs)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, val):
        if not isinstance(val, IPRange):
            try:
                if isinstance(val, str):
                    val = val.replace(" ", "").split("-")
                val = IPRange(*val)
            except Exception:
                raise ValueError(
                    "RangeObject.range must be a valid IPRange object or a string representation of one, eg. '1.2.3.4-1.2.3.10'"
                )
        self._range = val

    @property
    def range_first_ip(self):
        return str(IPAddress(self.range.first))

    @property
    def range_last_ip(self):
        return str(IPAddress(self.range.last))


@propify
class ExternalResource(Object):
    class Prop(str, Enum):
        ID = "id"
        pass

    at_type: AtType = prop(AtType.EXTERNAL_RESOURCE, key=Object.Prop.AT_TYPE.value)
    id: Optional[int] = prop(None, jsonify=Prop.ID.value, key=Prop.ID.value)
    _ips: List[IPNetwork]

    @classmethod
    def kwargify(cls, obj: dict) -> "ExternalResource":
        _obj, kwargs = kwargify(cls, obj)

        resource_ref: dict[str, Any] = obj.get("resource_ref", {})
        uid: Optional[str] = resource_ref.get("id")

        kwargs["ips"] = obj.get("ips", {}).get("ip", [])
        kwargs["name"] = resource_ref.get("name")
        if uid:
            kwargs["uid"] = sanitize_uid(uid)

        return cls(**kwargs)

    @property
    def ips(self) -> list[IPNetwork]:
        return self._ips

    @ips.setter
    def ips(self, val: Union[str, list[str]]):
        if isinstance(val, str):
            val = [val]
        try:
            self._ips = [IPNetwork(ip) for ip in val]
        except Exception:
            raise ValueError(
                "ExternalResourceObject.ips must be a list containing valid IP addresses, eg. ['1.2.3.4/32', '1.2.2.0/32']"
            )


def classify_ar_object(obj):
    return (
        {
            AtType.NETWORK.value: NetworkObject,
            AtType.HOST.value: IPObject,
            AtType.IP.value: NatIPObject if obj.get("nat_ip_address") else IPObject,
            AtType.RANGE.value: RangeObject,
            AtType.DNS.value: DNSObject,
            AtType.OBJECT.value: Object,
            AtType.INTERNET.value: Object,
            AtType.LDAP.value: Object,
            AtType.ANY.value: Any,
            AtType.EXTERNAL_RESOURCE.value: ExternalResource,
        }
        .get(obj.get(Object.Prop.AT_TYPE.value), UnMapped)
        .kwargify(obj)
    )


@propify
class AccessRequest(Jsonable):
    class Prop(Enum):
        ID = "id"
        ORDER = "order"
        RISK_ANALYSIS_RESULT = "risk_analysis_result"
        VERIFIER_RESULT = "verifier_result"
        USE_TOPOLOGY = "use_topology"
        TARGETS = "targets"
        USERS = "users"
        SOURCES = "sources"
        DESTINATIONS = "destinations"
        SOURCE_DOMAIN = "source_domain"
        DESTINATION_DOMAIN = "destination_domain"
        SERVICES = "services"
        ACTION = "action"
        LABELS = "labels"

    class Action(Enum):
        ACCEPT = "Accept"
        DROP = "Drop"
        REMOVE = "Remove"

    xsi_type: FieldXsiType = prop("accessRuleDTO", key=Jsonable.Prop.XSI_TYPE.value)

    _flatifies: dict = attr.ib(
        factory=lambda: {
            "sources": {Jsonable.Prop.XSI_TYPE.value: "multiSourceDTO"},
            "destinations": {Jsonable.Prop.XSI_TYPE.value: "multiDestinationDTO"},
            "services": {Jsonable.Prop.XSI_TYPE.value: "multi_service"},
            "targets": {Jsonable.Prop.XSI_TYPE.value: "multi_target"},
        },
        repr=False,
    )

    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    order: Optional[str] = prop(None, jsonify=False)
    sources: List[IPNetwork] = prop(
        factory=list, flatify="source", kwargify=classify_ar_object
    )
    destinations: List[IPNetwork] = prop(
        factory=list, flatify="destination", kwargify=classify_ar_object
    )
    source_domain: Optional[str] = prop(None)
    destination_domain: Optional[str] = prop(None)
    services: List[Service] = prop(
        factory=list, flatify="service", kwargify=classify_service_type
    )
    action: Action = prop(Action.ACCEPT)
    labels: List[str] = prop(factory=list, flatify="label")
    risk_analysis_result: Optional[RiskAnalysisResult] = prop(None, jsonify=False)
    verifier_result: Optional[VerifierResultLink] = prop(None, jsonify=False)

    use_topology: bool = prop(True)
    targets: List[Target] = prop(factory=list, flatify="target")
    users: List[str] = prop(factory=list, flatify="user")
    comment: Optional[str] = prop(None)

    def add_source(self, details=None, name=None, device=None, obj=None):
        if obj:
            obj = Object(
                name=obj.name, management_id=obj.device_id, uid=obj.uid, type=obj.type
            )
        else:
            if details:
                obj = smart_ar_object(netaddr_obj_from_details(details))
            else:
                obj = smart_ar_object(name=name, device=device)
            if not obj:
                return None
        obj.xsi_type = "sourceDTO"
        self.sources = [s for s in self.sources if not isinstance(s, Any)] + [obj]
        return obj

    def add_destination(self, details=None, name=None, device=None, obj=None):
        if obj:
            obj = Object(
                name=obj.name, management_id=obj.device_id, uid=obj.uid, type=obj.type
            )
        else:
            if details:
                obj = smart_ar_object(netaddr_obj_from_details(details))
            else:
                obj = smart_ar_object(name=name, device=device)
            if not obj:
                return None
        obj.xsi_type = "destinationDTO"
        self.destinations = [d for d in self.destinations if not isinstance(d, Any)] + [
            obj
        ]
        return obj

    def add_service(self, details=None, name=None, device=None, obj=None):
        if obj:
            obj = Object(
                name=obj.name, management_id=obj.device_id, uid=obj.uid, type=obj.type
            )
        else:
            if details:
                try:
                    obj = Service.from_string(details)
                except ValueError:
                    raise ValueError(
                        f"details: {details} is not a valid service identifier"
                    )
            else:
                return None
            if not obj:
                return None
        obj.xsi_type = "serviceDTO"
        self.services = [s for s in self.services if not isinstance(s, Any)] + [obj]
        return obj

    def add_target(
        self,
        device: Union[Device, str, int],
        policy: Union[BindingPolicy, str, None] = None,
        source_zone: Union[Zone, str, None] = None,
        destination_zone: Union[Zone, str, None] = None,
    ) -> Target:
        target = None
        if not isinstance(device, Device):
            _device: Device = St.default.get_device(device)
        else:
            _device = device

        if _device is None:
            return None

        if isinstance(policy, str) and _device.model is not Device.Model.ASA:
            policy = St.default.get_device_policy(device=_device.id, policy=policy)

        if _device.model is Device.Model.ASA:
            if not self.use_topology:
                if not policy:
                    raise ValueError(
                        f"ACL name must be specified in the policy argument to add a {_device.model.value} target to an AR with topology disbaled"
                    )
                target = Target(
                    type=Target.ObjectType.ACL,
                    name=policy,
                    management_id=_device.id,
                    management_name=_device.name,
                )
            else:
                target = Target(
                    type=Target.ObjectType.FIREWALL,
                    name=_device.name,
                    management_id=_device.id,
                    management_name=_device.name,
                )

        elif _device.model in (Device.Model.PANORAMA_NG_FW, Device.Model.FMG_FIREWALL):
            if not self.use_topology:
                raise ValueError(
                    f"Cannot add a {_device.model.value} target to an AR with topology disabled"
                )
            target = Target(
                name=_device.name,
                management_id=_device.id,
                management_name="/".join(map(lambda x: x.name, _device.parents)),
                type=Target.ObjectType.FIREWALL,
            )

        elif _device.model in (Device.Model.PANORAMA_DEVICE_GROUP,):
            if self.use_topology:
                raise ValueError(
                    f"Cannot add a {_device.model.value} target to an AR with topology enabled"
                )
            else:
                target = Target(
                    name=f"{source_zone}>{destination_zone}",
                    management_id=_device.id,
                    management_name=f'{"/".join(map(lambda x: x.name, _device.parents))}/{_device.name}',
                    type=Target.ObjectType.ZONE_TO_ZONE,
                )

        elif _device.model in (Device.Model.FMG_ADOM, Device.Model.FMG_VDOM):
            if self.use_topology:
                raise ValueError(
                    f"Cannot add a {_device.model.value} target to an AR with topology enabled"
                )
            else:
                if not self.use_topology and not policy:
                    raise ValueError(
                        "policy argument must be specified to add this type of target to this AR"
                    )
                target = Target(
                    name=f"{source_zone}>{destination_zone}",
                    management_id=_device.id,
                    management_name=f'{"/".join(map(lambda x: x.name, _device.parents))}/{_device.name}/{policy.name}',
                    type=Target.ObjectType.ZONE_TO_ZONE,
                )
        elif _device.model in (Device.Model.MODULE, Device.Model.MODULE_CLUSTER):
            target = Target(
                type=Target.ObjectType.FIREWALL,
                management_id=_device.parent_id,
                name=_device.name,
            )
        elif _device.model in (Device.Model.CP_CMA, Device.Model.CP_SMRT_CNTR):
            target = Target(
                type=Target.ObjectType.POLICY,
                management_id=_device.id,
                name=policy.name,
            )
        else:
            raise ValueError(
                f"Support for {_device.model.value} type targets is not been implemented."
            )
        self.targets = [
            t for t in self.targets if t != target and t.at_type is not AtType.ANY
        ] + [target]
        return target

    def get_linked_verifier_result(self) -> AccessRequestVerifierResult:
        if not self.verifier_result:
            raise AssertionError("No verifier result defined on access request")

        link = self.verifier_result.result.href
        response = Scw.default.api.session.get(link)
        if response.ok:
            _json = response.json()
            return classify_verifier_result(_json)
        else:
            try:
                msg = response.json().get("result").get("message")
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got message :{msg} from API error: {e}")

    @property
    def _json(self) -> dict:
        if self._json_override is not None:
            return self._json_override
        obj = deepcopy(self)
        for a in ("sources", "destinations", "targets", "services"):
            if not getattr(obj, a, []):
                delattr(obj, a)

        return jsonify(obj)


@propify
class GroupChangeMember(Jsonable):
    class Prop(Enum):
        OBJECT_UID = "object_UID"
        OBJECT_TYPE = "object_type"
        OBJECT_DETAILS = "object_details"
        OBJECT_UPDATED_STATUS = "object_updated_status"
        STATUS = "status"
        AT_TYPE = Object.Prop.AT_TYPE.value

    class ObjectUpdatedStatus(Enum):
        EXISTING_NOT_EDITED = "EXISTING_NOT_EDITED"
        EXISTING_EDITED = "EXISTING_EDITED"
        NEW = "NEW"

    class Status(Enum):
        NOT_CHANGED = "NOT_CHANGED"
        ADDED = "ADDED"
        DELETED = "DELETED"

    class ObjectType(Enum):
        GROUP = "Group"
        ADDRESS_RANGE = "Address Range"
        NETWORK = "Network"
        HOST = "Host"

    at_type: Optional[AtType] = prop(AtType.OBJECT, key=Prop.AT_TYPE.value, cmp=False)
    name: Optional[str] = prop(None)
    uid: Optional[str] = prop(None, key=Prop.OBJECT_UID.value, cmp=False, repr=False)
    object_type: Optional[ObjectType] = prop(
        None, cmp=False, jsonify="type", key="object_type", init=False, repr=False
    )
    comment: Optional[str] = prop(None, cmp=False, repr=False)
    management_id: Optional[int] = prop(None, converter=attr.converters.optional(int))
    management_name: Optional[str] = prop(None, repr=False, cmp=False)
    status: Status = prop(Status.NOT_CHANGED, cmp=False)
    updated_status: Optional[ObjectUpdatedStatus] = prop(
        None, key=Prop.OBJECT_UPDATED_STATUS.value, repr=False, cmp=False
    )

    def delete(self):
        if self.status is self.Status.NOT_CHANGED:
            self.status = self.Status.DELETED
            return self
        elif self.status is self.Status.DELETED:
            return self
        else:
            raise AssertionError(
                "This member was newly added; to delete it, pop it from the list of group_changes"
            )


@propify
class GroupChangeMemberHost(GroupChangeMember):
    at_type: Optional[AtType] = prop(
        AtType.HOST, key=GroupChangeMember.Prop.AT_TYPE.value, cmp=False
    )
    type: ClassVar = GroupChangeMember.ObjectType.HOST
    _ip: IPAddress
    _details: Optional[str] = prop(
        None,
        key=GroupChangeMember.Prop.OBJECT_DETAILS.value,
        jsonify="details",
        init=False,
        repr=False,
        cmp=False,
    )

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        try:
            self._ip = IPAddress(val)
        except Exception:
            raise ValueError(
                "GroupChangeMemberHost.ip must be either an IPAddress object or a valid argument to it's constructor, eg. 1.2.3.0"
            )

    @property
    def details(self):
        return str(self.ip)

    @classmethod
    def kwargify(cls, obj: dict):
        _obj, kwargs = kwargify(cls, obj)
        kwargs["ip"] = IPNetwork(
            _obj[GroupChangeMember.Prop.OBJECT_DETAILS.value]
        ).network
        return cls(**kwargs)


@propify
class GroupChangeMemberNetwork(GroupChangeMember):
    at_type: Optional[AtType] = prop(
        AtType.NETWORK, key=GroupChangeMember.Prop.AT_TYPE.value, cmp=False
    )
    type: ClassVar = GroupChangeMember.ObjectType.NETWORK
    _network: IPNetwork
    _details: Optional[str] = prop(
        None,
        key=GroupChangeMember.Prop.OBJECT_DETAILS.value,
        jsonify="details",
        init=False,
        repr=False,
        cmp=False,
    )

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, val):
        try:
            self._network = IPNetwork(val)
        except Exception:
            raise ValueError(
                "GroupChangeMemberNetwork.ip must be either an IPNetwork object or a valid argument to it's constructor, eg. 1.2.3.0"
            )

    @property
    def details(self):
        return f"{self._network.network}/{self._network.netmask}"

    @classmethod
    def kwargify(cls, obj: dict):
        _obj, kwargs = kwargify(cls, obj)
        kwargs["network"] = IPNetwork(_obj[GroupChangeMember.Prop.OBJECT_DETAILS.value])
        return cls(**kwargs)


@propify
class GroupChangeMemberRange(GroupChangeMember):
    at_type: Optional[AtType] = prop(
        AtType.RANGE, key=GroupChangeMember.Prop.AT_TYPE.value, cmp=False
    )
    type: ClassVar = GroupChangeMember.ObjectType.ADDRESS_RANGE
    _range: IPRange
    _details: Optional[str] = prop(
        None,
        key=GroupChangeMember.Prop.OBJECT_DETAILS.value,
        jsonify="details",
        init=False,
        repr=False,
        cmp=False,
    )

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, val):
        if not isinstance(val, IPRange):
            try:
                if isinstance(val, str):
                    val = val.replace(" ", "").split("-")
                val = IPRange(*val)
            except Exception:
                raise ValueError(
                    "RangeObject.range must be a valid IPRange object or a string representation of one, eg. '1.2.3.4-1.2.3.10'"
                )
        self._range = val

    @property
    def details(self):
        return f"[ {str(IPAddress(self.range.first))} - {str(IPAddress(self.range.last))} ]"

    @classmethod
    def kwargify(cls, obj: dict):
        _obj, kwargs = kwargify(cls, obj)
        r = re.sub(
            r"(\[|]| )", "", _obj[GroupChangeMember.Prop.OBJECT_DETAILS.value]
        ).split("-")
        kwargs["range"] = IPRange(*r)
        return cls(**kwargs)


GroupChangeMemberType = Union[
    GroupChangeMember, GroupChangeMember, GroupChangeMemberHost
]


def netaddr_obj_from_details(details):
    details = re.sub(r"(\[|]| )", "", details)
    try:
        netaddr_obj = IPNetwork(details)
    except netaddr.core.AddrFormatError:
        val = details.replace(" ", "").split("-")
        try:
            return IPRange(*val)
        except (netaddr.core.AddrFormatError, TypeError):
            raise ValueError(
                f"Could not convert details arg {details} to a valid member type"
            )
    else:
        return netaddr_obj.network if netaddr_obj.prefixlen == 32 else netaddr_obj


def smart_group_change_member(
    name: str,
    netaddr_obj: str,
    management_id: Optional[int],
    management_name: Optional[str] = None,
    comment: str = "",
):
    if isinstance(netaddr_obj, IPAddress):
        return GroupChangeMemberHost(
            ip=netaddr_obj,
            status=GroupChangeMember.Status.ADDED,
            management_id=management_id,
            management_name=management_name,
            updated_status=GroupChangeMember.ObjectUpdatedStatus.NEW,
            name=name,
            comment=comment,
        )
    elif isinstance(netaddr_obj, IPNetwork):
        return GroupChangeMemberNetwork(
            network=netaddr_obj,
            status=GroupChangeMember.Status.ADDED,
            management_id=management_id,
            management_name=management_name,
            updated_status=GroupChangeMember.ObjectUpdatedStatus.NEW,
            name=name,
            comment=comment,
        )
    elif isinstance(netaddr_obj, IPRange):
        return GroupChangeMemberRange(
            range=netaddr_obj,
            status=GroupChangeMember.Status.ADDED,
            management_id=management_id,
            management_name=management_name,
            updated_status=GroupChangeMember.ObjectUpdatedStatus.NEW,
            name=name,
            comment=comment,
        )


def smart_ar_object(
    netaddr_obj: str = None, name: str = None, device: Optional[Union[int, str]] = None
):
    if isinstance(netaddr_obj, (IPAddress, IPNetwork)):
        return IPObject(subnet=IPNetwork(netaddr_obj))
    elif isinstance(netaddr_obj, IPRange):
        return RangeObject(range=netaddr_obj)
    else:
        res = St.default.get_network_object(name, device)
        obj = res
        if isinstance(obj, network_object.NetworkObject):
            return Object(
                name=name, management_id=obj.device_id, uid=obj.uid, type=obj.type
            )
        return None


def classify_group_change_member_from_api(member: dict):
    return {
        GroupChangeMember.ObjectType.GROUP.value: GroupChangeMember.kwargify,
        GroupChangeMember.ObjectType.HOST.value: GroupChangeMemberHost.kwargify,
        GroupChangeMember.ObjectType.NETWORK.value: GroupChangeMemberNetwork.kwargify,
        GroupChangeMember.ObjectType.ADDRESS_RANGE.value: GroupChangeMemberRange.kwargify,
    }.get(member.get(GroupChangeMember.Prop.OBJECT_TYPE.value) or "", UnMapped)(member)


@propify
class GroupChange(Jsonable):
    class Prop(Enum):
        NAME = "name"
        OBJECT_UID = "object_UID"
        MANAGEMENT_ID = "management_id"
        MANAGEMENT_NAME = "management_name"
        CHANGE_IMPLEMENTATION_STATUS = "change_implementation_status"
        MEMBERS = "members"
        ZONE = "zone"
        ADDRESS_BOOK = "address_book"

    class ChangeAction(Enum):
        CREATE = "CREATE"
        UPDATE = "UPDATE"

    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    name: Optional[str] = prop(None)
    uid: Optional[str] = prop(None, key=Prop.OBJECT_UID.value, jsonify=True, repr=False)
    _parent_field: Optional[Jsonable] = attr.ib(None, eq=False)
    management_id: Optional[int] = prop(None, converter=attr.converters.optional(int))
    management_name: Optional[str] = prop(None)
    change_implementation_status: Optional[str] = prop(None, jsonify=False)
    change_action: ChangeAction = prop(ChangeAction.CREATE, jsonify=True)
    address_book: Optional[AddressBook] = prop(None, repr=False)
    zone: Optional[Zone] = prop(None, repr=False)
    members: List[GroupChangeMemberType] = prop(
        factory=list, flatify="member", kwargify=classify_group_change_member_from_api
    )

    def add_member(
        self,
        name: Optional[str] = None,
        details: Union[IPNetwork, IPRange, IPAddress, str, None] = None,
        uid: Optional[str] = None,
        comment: str = "",
        silence: bool = True,
    ):
        if uid:
            for member in self.members:
                if sanitize_uid(member.uid) == sanitize_uid(uid):
                    if member.status is GroupChangeMember.Status.DELETED:
                        member.status = GroupChangeMember.Status.NOT_CHANGED
                        return member
                    if silence:
                        return
                    else:
                        raise ValueError(f"Member with uid {uid} already added")
            st_obj = St.default.get_network_object(uid=uid, device=self.management_id)
            if st_obj:
                member = GroupChangeMember(
                    at_type=AtType.OBJECT,
                    uid=uid,
                    name=st_obj["display_name"],
                    status=GroupChangeMember.Status.ADDED,
                    management_id=self.management_id,
                    management_name=self.management_name,
                )
            else:
                raise ValueError(f"Could not find object with uid {uid}")

        # Not trying to add by UID
        elif name and details:
            netaddr_obj = (
                netaddr_obj_from_details(details)
                if not isinstance(details, (IPAddress, IPNetwork, IPRange))
                else details
            )
            member = smart_group_change_member(
                name, netaddr_obj, self.management_id, self.management_name, comment
            )

        else:
            raise TypeError("Name argument must be passed if uid is None")
        if member in self.members:
            if silence:
                return
            else:
                raise ValueError(f"member {name} already added")

        for new_device_id, new_member in self.new_objects.items():
            if member == new_member:
                member = GroupChangeMember(
                    at_type=AtType.OBJECT,
                    uid=new_member.uid,
                    status=GroupChangeMember.Status.ADDED,
                    management_id=self.management_id,
                    management_name=self.management_name,
                    name=name,
                    comment=comment,
                )
                break
        else:
            if any((member.name == name for member in self.members)):
                raise ValueError(
                    f"A different member object named {name} already exists"
                )
            elif any(
                m.name == name
                for m in self.new_objects.values()
                if m.management_id == self.management_id
            ):
                raise ValueError(
                    f"A different member object named {name} has already been added to another group change in this field"
                )
        if member in self.members:
            if silence:
                return
            else:
                raise ValueError(f"member {name} already added")

        self.members.append(member)
        return member

    @property
    def new_objects(self):
        return self._parent_field.new_objects


@propify
class Field(Jsonable):
    class Prop(Enum):
        ID = "id"
        NAME = "name"
        READ_ONLY = "read_only"

    class Meta(Enum):
        ROOT = "field"

    name: str = prop("No Name", converter=str, cmp=False, repr=True)
    id: Optional[int] = prop(None, cmp=False)
    read_only: Optional[bool] = prop(False, repr=False, cmp=False, jsonify=False)

    @property
    def _json(self) -> dict:
        if self._json_override is not None:
            return self._json_override
        if getattr(self, Field.Prop.READ_ONLY.value, None):
            return {}
        return jsonify(self)

    @_json.setter
    def _json(self, val):
        self._json_override = val

    @property
    def _dirty(self):
        return self.kwargify(self.data)._json != self._json


@propify
class TextField(Field):
    class Prop(Enum):
        TEXT = "text"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.TEXT_FIELD, key=Jsonable.Prop.XSI_TYPE.value
    )

    text: Optional[str] = prop(None, converter=str)


@propify
class MultiTextField(Field):
    class Prop(Enum):
        TEXT_FIELD = "text_field"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_TEXT_FIELD, key=Jsonable.Prop.XSI_TYPE.value
    )

    text_fields: List[TextField] = prop(
        factory=list, key=Prop.TEXT_FIELD.value, repr=False
    )


@propify
class TextArea(Field):
    class Prop(Enum):
        TEXT = "text"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.TEXT_AREA, key=Jsonable.Prop.XSI_TYPE.value
    )

    text: Optional[str] = prop(None, converter=str)


@propify
class Manager(Field):
    class Prop(Enum):
        TEXT = "text"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MANAGER, key=Jsonable.Prop.XSI_TYPE.value
    )

    text: Optional[str] = prop("", converter=str)


@propify
class Hyperlink(Field):
    class Prop(Enum):
        URL = "url"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.HYPERLINK, key=Jsonable.Prop.XSI_TYPE.value
    )

    url: Optional[str] = prop(None)


@propify
class MultiHyperlink(Field):
    class Prop(Enum):
        HYPERLINK = "hyperlink"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_HYPERLINK, key=Jsonable.Prop.XSI_TYPE.value
    )

    hyperlinks: List[Hyperlink] = prop(factory=list, key=Prop.HYPERLINK.value)


@propify
class MultiTarget(Field):
    class Prop(Enum):
        TARGET = "target"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_TARGET, key=Jsonable.Prop.XSI_TYPE.value
    )

    targets: List[Hyperlink] = prop(factory=list, key=Prop.TARGET.value)


@propify
class MultiService(Field):
    class Prop(Enum):
        SERVICE = "service"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_SERVICE, key=Jsonable.Prop.XSI_TYPE.value
    )

    services: List[Service] = prop(factory=list, key=Prop.SERVICE.value, repr=False)


@propify
class MultiNetworkObject(Field):
    class Prop(Enum):
        NETWORK_OBJECT = "network_object"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_NETWORK_OBJECT, key=Jsonable.Prop.XSI_TYPE.value
    )
    network_objects: List[NetworkObject] = prop(
        factory=list, key=Prop.NETWORK_OBJECT.value, repr=False
    )


@propify
class Designer(Jsonable):
    class Status(Enum):
        NOT_RUN = "not run"
        DESIGNER_RUNNING = "designer running"
        DESIGNER_SUCCESS = "designer success"
        DESIGNER_CANNOT_COMPUTE = "designer cannot compute"
        IMPLEMENTATION_RUNNING = "implementation running"
        IMPLEMENTATION_SUCCESS = "implementation success"
        IMPLEMENTATION_FAILURE = "implementation failure"
        DESIGNER_FULLY_IMPLEMENT = "designer fully implement"
        COMMIT_RUNNING = "commit running"
        COMMIT_SUCCESS = "commit success"
        COMMIT_FAILURE = "commit failure"

    cannot_compute_reason: Optional[str] = prop(None)
    warning_message: Optional[str] = prop(None)
    status: Optional[Status] = prop(None)
    result: Optional[str] = prop(None, flatify="@href")
    _designer_results: Optional[DesignerResults] = None

    def get_results(self, fresh=False):
        if (
            self.status
            in (
                self.Status.NOT_RUN,
                self.Status.DESIGNER_RUNNING,
            )
            or not self.result
        ):
            return None
        if not self._designer_results or fresh:
            self._designer_results = DesignerResults.kwargify(
                Scw.default.api.session.get(self.result).json()
            )
        return self._designer_results


@propify
class RelatedRules(Jsonable):
    result: Optional[str] = prop(None, flatify="@href")
    _related_rules_results: Optional[RelatedRulesResult] = None

    def get_results(self, fresh=False):
        if not self._related_rules_results or fresh:
            self._related_rules_results = RelatedRulesResult.kwargify(
                Scw.default.api.session.get(self.result).json()
            )
        return self._related_rules_results


@propify
class MultiAccessRequest(Field):
    class Prop(Enum):
        ACCESS_REQUEST = "access_request"
        DESIGNER_RESULT = "designer_result"

    class DesignerVerifierAdvancedOption(Enum):
        OPTIMIZED = "OPTIMIZED"
        CREATE_NEW_RULE = "CREATE_NEW_RULE"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_ACCESS_REQUEST, key=Jsonable.Prop.XSI_TYPE.value
    )

    access_requests: List[AccessRequest] = prop(
        repr=False, key=Prop.ACCESS_REQUEST.value, factory=list
    )
    designer_verifier_advanced_option: Optional[DesignerVerifierAdvancedOption] = prop(
        None, repr=False
    )
    designer_result: Optional[Designer] = prop(
        None, cmp=False, repr=False, jsonify=False
    )
    related_rules_result: Optional[RelatedRules] = prop(
        None, cmp=False, repr=False, jsonify=False
    )

    @property
    def ars(self) -> List[AccessRequest]:
        return self.access_requests

    def add_ar(self) -> AccessRequest:
        if len(self.access_requests) == 1:
            ar1 = self.access_requests[0]
            if all(
                (
                    x.at_type is AtType.ANY
                    for x in ar1.sources + ar1.destinations + ar1.services + ar1.targets
                )
            ):
                return ar1
        ar = AccessRequest()
        self.access_requests.append(ar)
        return ar


@propify
class MultiGroupChange(Field):
    class Prop(Enum):
        IMPLEMENTATION_STATUS = "implementation_status"
        DESIGNER_RESULT = "designer_result"
        GROUP_CHANGE = "group_change"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_GROUP_CHANGE, key=Jsonable.Prop.XSI_TYPE.value
    )

    implementation_status: Optional[str] = prop(None)
    group_changes: List[GroupChange] = prop(
        factory=list, repr=False, key=Prop.GROUP_CHANGE.value
    )
    designer_result: Optional[Designer] = prop(
        None, cmp=False, repr=False, jsonify=False
    )

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        inst = cls(**kwargs)
        for gc in inst.group_changes:
            gc._parent_field = inst
        return inst

    @property
    def new_objects(self):
        return {
            member.name: member
            for gc in self.group_changes
            for member in gc.members
            if member.updated_status is GroupChangeMember.ObjectUpdatedStatus.NEW
        }

    def add_group_change(
        self,
        name: Optional[str] = None,
        device: Union[None, int, str] = None,
        uid: Optional[str] = None,
    ) -> GroupChange:
        device_id = None
        kwargs: dict = dict(parent_field=self)
        if not uid and (not name or not device):
            raise ValueError("name and device arguments must be passed if uid is None")
        if device:
            device_obj = St.default.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
            else:
                device_id = device_obj.id
                device_name = device_obj.name
                kwargs["management_name"] = device_name
                kwargs["management_id"] = device_id
        members: list = []
        obj = St.default.get_network_object(name, device_id, uid)
        if obj:
            if not isinstance(obj, NetworkObjectGroup):
                raise ValueError(
                    f"Cannot add existing object of type {type(obj)} to a group change"
                )
            else:
                uid = obj["uid"]
                name = obj["display_name"]
                device_id = obj.device_id or device_id
                kwargs["management_id"] = device_id
                members = obj.members

        elif uid:
            raise ValueError(f"Cannot find existing object with uid {uid}")

        group_change = (
            GroupChange(
                uid=uid,
                name=name,
                change_action=GroupChange.ChangeAction.UPDATE,
                members=[
                    GroupChangeMember(
                        at_type=AtType.OBJECT,
                        management_id=device_id,
                        management_name=device_name,
                        name=member["display_name"],
                        uid=member["uid"],
                    )
                    for member in members
                ],
                **kwargs,
            )
            if uid
            else GroupChange(name=name, **kwargs)
        )
        self.group_changes.append(group_change)
        return group_change


@propify
class CloneServerPolicyRequest(Field):
    xsi_type: FieldXsiType = prop(
        FieldXsiType.CLONE_SERVER_POLICY_REQUEST, key=Jsonable.Prop.XSI_TYPE.value
    )

    comment: Optional[str] = prop(None)

    from_server: Optional[Object] = prop(None, repr=False, kwargify=classify_ar_object)

    to_servers: List[Object] = prop(
        factory=list,
        cmp=False,
        repr=False,
        jsonify=True,
        flatify="server",
        kwargify=classify_ar_object,
    )

    designer_result: Optional[Designer] = prop(
        None, cmp=False, repr=False, jsonify=False
    )

    verifier_result: Optional[dict] = prop(None, cmp=False, repr=False)


@propify
class ServerDecommissionRequest(Field):
    class Prop(Enum):
        TARGETS = "targets"
        SERVERS = "servers"
        COMMENT = "commment"
        IMPACT_ANALYSIS_RESULT = "impact_analysis_result"
        VERIFIER_RESULT = "verifier_result"
        DESIGNER_RESULT = "designer_result"

    targets: List[Target] = prop(
        factory=list, cmp=False, repr=False, jsonify=False, flatify="target"
    )
    servers: List[Object] = prop(
        factory=list,
        cmp=False,
        repr=False,
        jsonify=True,
        flatify="server",
        kwargify=classify_ar_object,
    )
    comment: Optional[str] = prop(None)
    impact_analysis_result: Optional[dict] = prop(
        None, cmp=False, repr=False, jsonify=False
    )
    verifier_result: Optional[dict] = prop(None, cmp=False, repr=False, jsonify=False)
    designer_result: Optional[Designer] = prop(
        None, cmp=False, repr=False, jsonify=False
    )

    def add_server(self, server_ip: str):
        try:
            self.servers.append(IPObject(subnet=IPNetwork(f"{server_ip}/32")))
        except netaddr.core.AddrFormatError:
            raise ValueError(f"{server_ip} is not a valid IP")


@propify
class MultiServerDecommissionRequest(Field):
    class Prop(Enum):
        SERVER_DECOMMISSION_REQUEST = "server_decommission_request"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_SERVER_DECOMMISSION_REQUEST, key=Jsonable.Prop.XSI_TYPE.value
    )

    server_decommission_requests: List[ServerDecommissionRequest] = prop(
        factory=list,
        repr=False,
        jsonify=True,
        key=Prop.SERVER_DECOMMISSION_REQUEST.value,
    )


@propify
class Date(Field):
    class Prop(Enum):
        VALUE = "value"

    xsi_type: FieldXsiType = prop(FieldXsiType.DATE, key=Jsonable.Prop.XSI_TYPE.value)

    _date: Optional[datetime_date] = None

    _value: str = prop(jsonify="value", init=False, cmp=False, repr=False)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        value = _obj.get(cls.Prop.VALUE.value)
        if value:
            kwargs["date"] = datetime.strptime(value, TimeFormat.DATE.value).date()
        return cls(**kwargs)

    @property
    def date(self) -> Optional[datetime_date]:
        return self._date

    @date.setter
    def date(self, val):
        if isinstance(val, datetime_date):
            self._date = val
        elif val:
            try:
                self._date = datetime.strptime(val, TimeFormat.DATE.value).date()
            except ValueError:
                raise TypeError(
                    "'date' attribute of a Date object from be a valid date() type"
                )

    @property
    def value(self) -> Optional[str]:
        return self.date.strftime(TimeFormat.DATE.value) if self.date else None


@propify
class Time(Field):
    class Prop(Enum):
        VALUE = "value"

    xsi_type: FieldXsiType = prop(FieldXsiType.TIME, key=Jsonable.Prop.XSI_TYPE.value)

    _time: Optional[datetime_time] = None

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        value = _obj.get(cls.Prop.VALUE.value)
        if value:
            kwargs["time"] = datetime.strptime(value, TimeFormat.SC_TIME.value).time()
        return cls(**kwargs)

    @property
    def time(self) -> datetime_time:
        return getattr(self, "_time", None)

    @time.setter
    def time(self, val):
        if isinstance(val, datetime_time):
            self._time = val
        elif val:
            raise TypeError(
                "'time' attribute of a Time object from be a valid time() type"
            )

    @property
    def value(self) -> Optional[str]:
        return self.time.strftime(TimeFormat.SC_TIME.value) if self.time else None


@propify
class ApproveReject(Field):
    class Prop(Enum):
        REASON = "reason"
        APPROVED = "approved"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.APPROVE_REJECT, key=Jsonable.Prop.XSI_TYPE.value
    )

    reason: Optional[str] = prop(None, cmp=False, repr=False)
    approved: Optional[bool] = prop(None)

    def __bool__(self):
        return bool(getattr(self, "approved", False))

    def approve(self, reason="None provided") -> None:
        self.approved = True
        self.reason = reason

    def reject(self, reason="None provided") -> None:
        self.approved = False
        self.reason = reason


@propify
class Checkbox(Field):
    class Prop(Enum):
        VALUE = "value"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.CHECKBOX, key=Jsonable.Prop.XSI_TYPE.value
    )

    value: Optional[bool] = prop(None)

    def __bool__(self):
        return self.value

    @property
    def checked(self):
        return self.value

    def check(self):
        self.value = True

    def uncheck(self):
        self.value = False

    def toggle(self):
        self.value = not self.value


@propify
class DropDownList(Field):
    class Prop(Enum):
        SELECTION = "selection"
        OPTIONS = "options"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.DROP_DOWN_LIST, key=Jsonable.Prop.XSI_TYPE.value
    )

    selection: Optional[str] = prop(None)
    options: List[Option] = prop(
        factory=list, repr=False, key=Prop.OPTIONS.value, flatify="option"
    )


@propify
class MultipleSelection(Field):
    class Prop(Enum):
        SELECTED_OPTIONS = "selected_options"
        OPTIONS = "options"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTIPLE_SELECTION, key=Jsonable.Prop.XSI_TYPE.value
    )

    selected_options: List[Option] = prop(factory=list, flatify="selected_option")
    options: List[Option] = prop(factory=list, flatify="option")


@propify
class MultiTextArea(Field):
    class Prop(Enum):
        TEXT_AREA = "text_area"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.MULTI_TEXT_AREA, key=Jsonable.Prop.XSI_TYPE.value
    )

    text_areas: List[TextArea] = prop(
        factory=list, key=Prop.TEXT_AREA.value, repr=False
    )


from .rule_operation import (  # noqa: E402
    RuleOperation,
    RuleDecommission,
    RuleRecertification,
    RuleModificationField,
)

FieldType = Union[
    MultiAccessRequest,
    MultiServerDecommissionRequest,
    MultiTextArea,
    TextArea,
    MultipleSelection,
    MultiHyperlink,
    MultiGroupChange,
    MultiTextField,
    MultiTarget,
    MultiNetworkObject,
    MultiService,
    ApproveReject,
    Checkbox,
    DropDownList,
    Date,
    Time,
    TextField,
    Manager,
    Hyperlink,
]


def get_field_class(_type):
    return {
        FieldXsiType.MULTI_ACCESS_REQUEST.value: MultiAccessRequest,
        FieldXsiType.MULTI_SERVER_DECOMMISSION_REQUEST.value: MultiServerDecommissionRequest,
        FieldXsiType.RULE_DECOMMISSION.value: RuleDecommission,
        FieldXsiType.RULE_RECERTIFICATION.value: RuleRecertification,
        FieldXsiType.RULE_MODIFICATION_FIELD.value: RuleModificationField,
        FieldXsiType.MULTI_TEXT_AREA.value: MultiTextArea,
        FieldXsiType.TEXT_AREA.value: TextArea,
        FieldXsiType.MULTIPLE_SELECTION.value: MultipleSelection,
        FieldXsiType.MULTI_HYPERLINK.value: MultiHyperlink,
        FieldXsiType.MULTI_GROUP_CHANGE.value: MultiGroupChange,
        FieldXsiType.MULTI_TEXT_FIELD.value: MultiTextField,
        FieldXsiType.MULTI_TARGET.value: MultiTarget,
        FieldXsiType.MULTI_NETWORK_OBJECT.value: MultiNetworkObject,
        FieldXsiType.MULTI_SERVICE.value: MultiService,
        FieldXsiType.APPROVE_REJECT.value: ApproveReject,
        FieldXsiType.CHECKBOX.value: Checkbox,
        FieldXsiType.DROP_DOWN_LIST.value: DropDownList,
        FieldXsiType.DATE.value: Date,
        FieldXsiType.TIME.value: Time,
        FieldXsiType.TEXT_FIELD.value: TextField,
        FieldXsiType.MANAGER.value: Manager,
        FieldXsiType.HYPERLINK.value: Hyperlink,
        FieldXsiType.CLONE_SERVER_POLICY_REQUEST.value: CloneServerPolicyRequest,
    }.get(_type, UnMapped)


def classify_field(obj):
    return get_field_class(obj.get(Jsonable.Prop.XSI_TYPE.value)).kwargify(obj)
