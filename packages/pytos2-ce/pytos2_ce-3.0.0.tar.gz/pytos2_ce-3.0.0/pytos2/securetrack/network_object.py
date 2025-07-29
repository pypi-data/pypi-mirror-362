from enum import Enum
from typing import Optional, List, Union

from attr.converters import optional
from netaddr import IPAddress, IPNetwork, IPRange  # type: ignore
from netaddr.core import AddrFormatError

from pytos2.models import FQDNIp, Jsonable, UnMapped, IPType
from pytos2.utils import propify, prop, kwargify, get_api_node


class NatXsiType(Enum):
    NAT_INFO = "natInfoDTO"
    MIP_NAT_INFO = "mipNatInfoDTO"
    VIP_NAT_INFO = "vipNatInfoDTO"
    DIP_NAT_INFO = "dipNatInfoDTO"
    CHECKPOINT_NAT_INFO = "checkpointNatInfoDTO"
    FORTIGATE_NAT_INFO = "fortigateNatInfoDTO"


class NetworkObjectXsiType(Enum):
    BASIC_NETWORK_OBJECT = "basicNetworkObjectDTO"
    CLOUD_SECURITY_GROUP = "cloudSecurityGroupDTO"
    DOMAIN_NETWORK_OBJECT = "DomainNetworkObjectDTO"
    HOST_NETWORK_OBJECT = "hostNetworkObjectDTO"
    HOST_NETWORK_OBJECT_WITH_INTERFACES = "hostNetworkObjectWithInterfacesDTO"
    IDENTITY_AWARENESS = "identityAwarenessDTO"
    IDENTITY_AWARENESS_USER = "identityAwarenessUserDTO"
    NETWORK_OBJECT = "networkObjectDTO"
    NETWORK_OBJECT_GROUP = "networkObjectGroupDTO"
    NETWORK_OBJECT_VIRTUAL_SERVER = "networkObjectVirtualServerDTO"
    RANGE_NETWORK_OBJECT = "rangeNetworkObjectDTO"
    SUBNET_NETWORK_OBJECT = "subnetNetworkObjectDTO"
    VM_NETWORK_OBJECT = "VMInstanceDTO"


@propify
class NatInfo(Jsonable):
    xsi_type: Optional[NatXsiType] = prop(
        None, key=Jsonable.Prop.XSI_TYPE.value, repr=False
    )
    interface_name: Optional[str] = prop(None)


@propify
class MipNatInfo(NatInfo):
    virtual_router: Optional[str] = prop(None)
    mapped_to_ip: Optional[str] = prop(None)


@propify
class DipNatInfo(NatInfo):
    shift_from: Optional[str] = prop(None)


@propify
class CheckpointNatInfo(NatInfo):
    class Prop(Enum):
        MAPPED_TO_IP = "mapped_to_ip"

    class CheckpointNatType(Enum):
        STATIC = "STATIC"
        HIDDEN = "HIDDEN"

    checkpoint_nat_type: Optional[CheckpointNatType] = prop(None)
    mapped_to_ip: Optional[Union[str, IPAddress]] = prop(None, kwargify=False)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        mapped_to_ip = _obj.get(cls.Prop.MAPPED_TO_IP.value)
        if mapped_to_ip:
            try:
                kwargs["mapped_to_ip"] = IPAddress(mapped_to_ip)
            except AddrFormatError:
                pass

        return cls(**kwargs)


@propify
class FortigateNatInfo(NatInfo):
    class Prop(Enum):
        MAPPED_IP = "mapped-ip"
        MAPPED_IP_MAX = "mapped-ip-max"
        EXTERNAL_PORT = "external-port"
        MAPPED_PORT = "mapped-port"

    port_forwarding_type: Optional[str] = prop(None)
    src_filter: Optional[str] = prop(None)
    src_interface_filter: Optional[str] = prop(None)
    mapped_ip: Optional[IPAddress] = prop(None, key=Prop.MAPPED_IP.value)
    mapped_ip_max: Optional[IPAddress] = prop(None, key=Prop.MAPPED_IP_MAX.value)
    external_port: Optional[str] = prop(None, key=Prop.EXTERNAL_PORT.value)
    mapped_port: Optional[str] = prop(None, key=Prop.MAPPED_PORT.value)
    forti_vip: Optional[bool] = prop(None)
    Interface: Optional[str] = prop(None)


def classify_nat_type(obj):
    return (
        {
            NatXsiType.CHECKPOINT_NAT_INFO.value: CheckpointNatInfo,
            NatXsiType.DIP_NAT_INFO.value: DipNatInfo,
            NatXsiType.FORTIGATE_NAT_INFO.value: FortigateNatInfo,
            NatXsiType.MIP_NAT_INFO.value: MipNatInfo,
            NatXsiType.VIP_NAT_INFO.value: NatInfo,
        }
        .get(obj.get(Jsonable.Prop.XSI_TYPE.value), UnMapped)
        .kwargify(obj)
    )


NatType = Union[CheckpointNatInfo, DipNatInfo, FortigateNatInfo, MipNatInfo, NatInfo]


@propify
class NetworkObject(Jsonable):
    IPType = IPType

    class Type(Enum):
        BASIC = "basic"
        HOST = "host"
        RANGE = "range"
        SUBNET = "subnet"
        GROUP = "group"
        DOMAIN = "domain"
        ANY = "any"
        INSTALLON = "installon"
        HOST_WITH_IFACES = "hostWithIfaces"
        USER = "user"
        USER_GROUP = "user-group"
        ALIAS = "alias"
        SECURITY_GROUP = "security_group"
        VM_INSTANCE = "vm_instance"
        INTERNET = "internet"
        REFERENCE = "reference"
        IDENTITY_AWARENESS = "identity_awareness"
        DOMAIN_NETWORK = "domain-network"

    class ClassName(Enum):
        ADDRESS_RANGE = "address_range"
        MULTICAST_ADDRESS_RANGE = "multicast_address_range"
        VPN_ROUTE = "vpn_route"
        INTERFACE = "interface"
        NETWORK_INTERFACE = "network_interface"
        FIREWALL_POLICY = "firewall_policy"
        SUB_POLICY = "sub_policy"
        SECURITY_RULE = "security_rule"
        ROUTING_ENTRY = "routing_entry"
        SECURITY_RULES_GROUP = "security_rules_group"
        RULE_SOURCE = "rule_source"
        RULE_DESTINATION = "rule_destination"
        RULE_INSTALL = "rule_install"
        OTHER_SERVICE = "other_service"
        OTHER_OBJECT = "other_object"
        ACCEPT_ACTION = "accept_action"
        DROP_ACTION = "drop_action"
        DENY_ACTION = "deny_action"
        CONTINUE_ACTION = "continue_action"
        TRUST_ACTION = "trust_action"
        RESET_CLIENT_ACTION = "reset_client_action"
        RESET_SERVER_ACTION = "reset_server_action"
        RESET_BOTH = "reset_both_action"
        NETWORK_OBJECT_GROUP = "network_object_group"
        GROUP_WITH_EXCEPTION = "group_with_exception"
        NETWORK = "network"
        HOST = "host_plain"
        FQDN = "fqdn"
        VIRTUAL_MACHINE_INSTANCE = "vm_instance"
        CONTROLLER = "controllers"
        TCP_SERVICE = "tcp_service"
        UDP_SERVICE = "udp_service"
        SCTP_SERVICE = "sctp_service"
        ICMP_SERVICE = "icmp_service"
        INSTALL_ON = "install_on"
        IP_SERVICE = "ip_service"
        SECURITY_HEADER_RULE = "security_header_rule"
        ZONE = "zone"
        DOMAIN = "domain"
        INTERNET_SERVICE = "internet-service"
        IPV6 = "ipv6_object"
        Range = "address_range"
        SERVICE_GROUP = "service_group"
        POLICIES_COLLECTION = "policies_collection"
        REJECT_ACTION = "reject_action"
        USER_AUTHENTICATE = "user_authenticate"
        CLIENT_AUTHENTICATE = "client_authenticate"
        UNSUPPORTED_NETWORK_OBJECT = "unsupported_object"
        SCHEDULED_EVENT = "scheduled_event"
        TIME = "time"
        TIME_PERIOD = "time_period"
        NAT_POOL = "nat_pool"
        NAT_HEADER = "nat_header_rule"
        ADTR_TRANSLATION_RULE = "address_translation_rule"
        TRANSLATE_STATIC = "translate_static"
        TRANSLATE_HIDDEN = "translate_hidden"
        TRANSLATE_SERVICE = "service_translate"
        BEHIND_INTERFACE_NAT = "behind_interface_nat"
        SECURITY_PROFILE = "security_profile"
        SECURITY_PROFILE_GROUP = "security_profile_group"
        RULE_SERVICES = "rule_services"
        RULE_VPN = "rule_vpn"
        ICMPV6_SERVICE = "icmpv6_service"
        ANY_OBJECT = "any_object"
        ACCESS_ROLE = "access_role"
        USER = "user"
        USER_GROUP = "user_group"
        AD_BRANCH = "ad_branch"
        AD_GROUP = "ad_group"
        AD_USER = "ad_user"
        ALL_IDENTIFIED = "all_identified"
        ENCRYPT = "encrypt"
        CLIENT_ENCRYPT = "client_encrypt"
        RPC_SERVICE = "rpc_service"
        DCE_RPC_SERVICE = "dcerpc_service"
        UNSUPPORTED_SERVICE = "unsupported_service"
        INLINE_LAYER_ACTION = "inline_layer_action"
        SUB_POLICY_COLLECTION = "sub_policy_collection"
        DYNAMIC_OBJECT = "dynamic_object"
        HOST_CKP = "host_ckp"
        GATEWAY_CKP = "gateway_ckp"
        SOFTWARE_GATEWAY = "sofaware_gateway"
        EMBEDDED_DEVICE = "embedded_device"
        GATEWAY_CLUSTER = "gateway_cluster"
        VS_CLUSTER_NETOBJ = "vs_cluster_netobj"
        VSX_CLUSTER_NETOBJ = "vsx_cluster_netobj"
        CLUSTER_MEMBER = "cluster_member"
        GPRS_APN = "gprs_apn"
        UTM_CLUSTER_MEMBER = "utm_cluster_member"
        VS_CLUSTER_MEMBER = "vs_cluster_member"
        VSX_CLUSTER_MEMBER = "vsx_cluster_member"
        VS_NETOBJ = "vs_netobj"
        VSX_NETOBJ = "vsx_netobj"
        SECURITY_ZONE = "security_zone"
        GATEWAY_PLAIN = "gateway_plain"
        GSN_HANDOVER_GROUP = "gsn_handover_group"
        DATA_CENTER = "data_center"
        DATA_CENTER_OBJECT = "data_center_object"
        ENDPOINT_GROUP = "endpoint_group"
        BRIDGE_DOMAIN = "bridge_domain"
        LEARNED_ENDPOINT = "learned_endpoint"
        EXTERNAL_ROUTED_NETWORK = "external_routed_network"
        LOGICAL_NODE_PROFILE = "logical_node_profile"
        LOGICAL_INTERFACE_PROFILE = "logical_interface_profile"
        EXTERNAL_EPG = "external_endpoint_group"
        CONFIGURED_NODE = "configured_node"
        EXTERNAL_INTERFACE = "external_interface"
        EPGS_GROUP = "epgs_group"

    class Prop(Enum):
        GLOBAL = "global"

    xsi_type: Optional[NetworkObjectXsiType] = prop(
        None, key=Jsonable.Prop.XSI_TYPE.value, repr=False
    )
    type_on_device: Optional[str] = prop(None, repr=False)
    domain_name: Optional[str] = prop(None, repr=False)
    ip_type: Optional[IPType] = prop(None, repr=False)
    any_zone: bool = prop(False, repr=False)
    management_domain_securetrack_name: Optional[str] = prop(None, repr=False)
    nat_info: Optional[NatType] = prop(None, repr=False, kwargify=classify_nat_type)
    implicit: bool = prop(False, repr=False)
    management_domain: Optional[str] = prop(None, repr=False)
    overrides: bool = prop(False, repr=False)
    type: Type = prop(Type.BASIC, repr=False)
    deviceName: Optional[str] = prop(None, repr=False)
    device_id: Optional[int] = prop(None, converter=optional(int), repr=False)
    application_id: Optional[int] = prop(None, converter=optional(int), repr=False)
    uid: Optional[str] = prop(None, repr=False)
    comment: Optional[str] = prop(None, repr=False)
    is_global: bool = prop(False, key=Prop.GLOBAL.value, repr=False)
    name: Optional[str] = prop(None)
    class_name: Optional[ClassName] = prop(None, repr=False)
    display_name: Optional[str] = prop(None)


@propify
class BasicNetworkObject(NetworkObject):
    pass


FQDNIP = FQDNIp


@propify
class DomainNetworkObject(NetworkObject):
    class Prop(Enum):
        IPS = "ips"

    domain: Optional[str] = prop(None, repr=False)
    ips: List[FQDNIP] = prop(factory=list, flatify="ip")


@propify
class PoolMember(Jsonable):
    class Prop(Enum):
        IP = "ip"
        NETMASK = "netmask"

    netmask: Optional[IPAddress] = prop(None)
    ip: Optional[IPAddress] = prop(None)
    name: Optional[str] = prop(None)


@propify
class NetworkObjectVirtualServer(NetworkObject):
    class Prop(Enum):
        VIRTUAL_IP = "virtual_ip"
        NETMASK = "netmask"
        POOL_MEMBER = "pool_member"

    class Protocol(Enum):
        TCP = "TCP"
        UDP = "UDP"
        SCTP = "SCTP"

    netmask: Optional[IPAddress] = prop(None)
    f5_device_name: Optional[str] = prop(None)
    virtual_ip: Optional[IPAddress] = prop(None)
    pool_member: List[PoolMember] = prop(
        factory=list, repr=False, key=Prop.POOL_MEMBER.value
    )
    protocol: Optional[Protocol] = prop(None)
    port: Optional[str] = prop(None)


@propify
class HostNetworkObject(NetworkObject):
    class Prop(Enum):
        IP = "ip"

    xsi_type: NetworkObjectXsiType = prop(NetworkObjectXsiType.HOST_NETWORK_OBJECT)
    ip: Optional[IPAddress] = prop(None)


@propify
class InterfaceIP(Jsonable):
    class Visibility(Enum):
        PRIVATE = "private"
        PUBLIC = "public"

    class Precedence(Enum):
        PRIMARY = "primary"
        SECONDARY = "secondary"

    netmask: Optional[IPAddress] = prop(None)
    visibility: Optional[Visibility] = prop(None)
    precedence: Optional[Precedence] = prop(None)
    vendorAttachmentPolicy: Optional[str] = prop(None)
    ip: Optional[IPAddress] = prop(None)


@propify
class Interface(Jsonable):
    name: Optional[str] = prop(None)
    interface_ips: List[InterfaceIP] = prop(factory=list, flatify="interface_ip")


@propify
class HostNetworkObjectWithInterfaces(HostNetworkObject):
    interfaces: List[Interface] = prop(factory=list, flatify="interface")


@propify
class SubnetNetworkObject(NetworkObject):
    class Prop(Enum):
        IP = "ip"
        NETMASK = "netmask"

    subnet: Optional[IPNetwork] = None

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)

        try:
            if cls.Prop.IP.value in _obj and cls.Prop.NETMASK.value in _obj:
                kwargs["subnet"] = IPNetwork(
                    f"{_obj[cls.Prop.IP.value]}/{_obj[cls.Prop.NETMASK.value]}"
                )
        except AddrFormatError:
            pass

        kwargs["type"] = kwargs.get("type", NetworkObject.Type.SUBNET)

        return cls(**kwargs)


@propify
class RangeNetworkObject(NetworkObject):
    class Prop(Enum):
        FIRST_IP = "first_ip"
        LAST_IP = "last_ip"

    range: Optional[IPRange] = prop(None)

    """
    reverse_range: Set to true if first is greater than last on the
    source network object.
    """
    reverse_range: bool = prop(False)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)

        kwargs["type"] = kwargs.get("type", NetworkObject.Type.RANGE)

        first = _obj.get(cls.Prop.FIRST_IP.value)
        last = _obj.get(cls.Prop.LAST_IP.value)

        try:
            start = IPAddress(first)
            end = IPAddress(last)
            kwargs["reverse_range"] = start > end
            kwargs["range"] = IPRange(min(start, end), max(start, end))
        except (AddrFormatError, ValueError) as e:
            msg = f"First IP {first} / Last IP {last} could not be cast to IPAddress / IPRange"
            raise ValueError(msg) from e

        return cls(**kwargs)

    @property
    def first(self):
        return self.range.first if not self.reverse_range else self.range.last

    @property
    def last(self):
        return self.range.last if not self.reverse_range else self.range.first


@propify
class ObjectReference(Jsonable):
    ip: Optional[IPAddress] = prop(None)
    uid: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    members: List["ObjectReference"] = prop(factory=list, flatify="member")
    type: Optional[NetworkObject.Type] = prop(None)
    display_name: Optional[str] = prop(None)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        # edge case of some strange rules on ASAs
        if "DM_INLINE_members" in _obj:
            kwargs["members"] = [
                cls.kwargify(o) for o in get_api_node(obj, "DM_INLINE_members.member")
            ]
        return cls(**kwargs)


@propify
class NetworkObjectGroup(NetworkObject):
    class Prop(Enum):
        EXCLUSION = "exclusion"
        MEMBER = "member"

    access_allowed: Optional[bool] = prop(None)
    exclusions: List[ObjectReference] = prop(
        factory=list, key=Prop.EXCLUSION.value, repr=False
    )
    members: List[ObjectReference] = prop(
        factory=list, key=Prop.MEMBER.value, repr=False
    )


@propify
class CloudSecurityGroup(NetworkObjectGroup):
    pass


@propify
class IdentityAwarenessUser(Jsonable):
    class Prop(Enum):
        GLOBAL = "global"

    xsi_type: Optional[str] = prop(None, key=Jsonable.Prop.XSI_TYPE.value, repr=False)
    dn: Optional[str] = prop(None)
    type: Optional[NetworkObject.Type] = prop(None)
    deviceName: Optional[str] = prop(None)
    device_id: Optional[int] = prop(None, converter=optional(int))
    application_id: Optional[int] = prop(None, converter=optional(int))
    uid: Optional[str] = prop(None)
    comment: Optional[str] = prop(None)
    is_global: bool = prop(False, key=Prop.GLOBAL.value)
    name: Optional[str] = prop(False)
    class_name: Optional[NetworkObject.ClassName] = prop(None)
    display_name: Optional[str] = prop(None)


@propify
class IdentityAwareness(NetworkObject):
    class Prop(Enum):
        USERS = "users"
        NETWORKS = "networks"

    users: List[IdentityAwarenessUser] = prop(factory=list)
    networks: List[ObjectReference] = prop(factory=list)


@propify
class VMNetworkObject(NetworkObject):
    xsi_type: NetworkObjectXsiType = prop(NetworkObjectXsiType.VM_NETWORK_OBJECT)
    id: Optional[str] = prop(None)
    type: NetworkObject.Type = prop(NetworkObject.Type.HOST)
    ip: Optional[IPAddress] = prop(None)
    interfaces: List[Interface] = prop(factory=list, flatify="interface")
    state: Optional[str] = prop(None)


def classify_network_object(obj):
    return (
        {
            NetworkObjectXsiType.BASIC_NETWORK_OBJECT.value: BasicNetworkObject,
            NetworkObjectXsiType.CLOUD_SECURITY_GROUP.value: CloudSecurityGroup,
            NetworkObjectXsiType.DOMAIN_NETWORK_OBJECT.value: DomainNetworkObject,
            NetworkObjectXsiType.HOST_NETWORK_OBJECT.value: HostNetworkObject,
            NetworkObjectXsiType.HOST_NETWORK_OBJECT_WITH_INTERFACES.value: HostNetworkObjectWithInterfaces,
            NetworkObjectXsiType.IDENTITY_AWARENESS.value: IdentityAwareness,
            NetworkObjectXsiType.NETWORK_OBJECT.value: NetworkObject,
            NetworkObjectXsiType.NETWORK_OBJECT_GROUP.value: NetworkObjectGroup,
            NetworkObjectXsiType.NETWORK_OBJECT_VIRTUAL_SERVER.value: NetworkObjectVirtualServer,
            NetworkObjectXsiType.RANGE_NETWORK_OBJECT.value: RangeNetworkObject,
            NetworkObjectXsiType.SUBNET_NETWORK_OBJECT.value: SubnetNetworkObject,
            NetworkObjectXsiType.VM_NETWORK_OBJECT.value: VMNetworkObject,
        }
        .get(obj.get(Jsonable.Prop.XSI_TYPE.value), UnMapped)
        .kwargify(obj)
    )
