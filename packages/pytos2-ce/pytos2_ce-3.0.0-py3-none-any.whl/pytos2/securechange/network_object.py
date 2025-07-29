from enum import Enum
from typing import Optional, List, Union

from netaddr import IPRange, IPAddress, IPNetwork

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj

from attr.converters import optional


@propify
class NetworkObject(Jsonable):
    class XsiType(Enum):
        HOST_NETWORK_OBJECT = "ns_sc_policy:host_network_object"
        HOST_NETWORK_OBJECT_NO_NAMESPACE = "host_network_object"
        HOST_NETWORK_OBJECT_WITH_INTERFACES = "host_network_object_with_interfaces"
        NETWORK_OBJECT_GROUP = "network_object_group"
        CLOUD_SECURITY_GROUP = "cloud_security_group"
        SUBNET_NETWORK_OBJECT = "subnet_network_object"
        RANGE_NETWORK_OBJECT = "range_network_object"
        ANY_NETWORK_OBJECT = "any_network_object"

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

    class Origin(Enum):
        DEVICE = "device"

    class IPType(Enum):
        IPV4 = "IPV4"
        IPV6 = "IPV6"
        OTHER = "OTHER"

    class Vendor(Enum):
        CISCO = "Cisco"
        FORTINET = "Fortinet"
        NETSCREEN = "Netscreen"
        CHECKPOINT = "Checkpoint"
        PALO_ALTO = "PaloAltoNetworks"
        NEW_F5 = "NewF5"
        F5 = "f5"
        MCAFEE = "Mcafee"
        STONESOFT = "Stonesoft"
        BLUECOAT = "bluecoat"
        GENERIC = "Generic"
        LINUX = "linux"
        VMWARE = "VMware"
        AMAZON = "Amazon"
        OPENSTACK = "OpenStack"
        AZURE = "Azure"

    class Prop(Enum):
        GLOBAL = "global"
        IMPLICIT = "implicit"
        SHARED = "shared"

    xsi_type: Optional[XsiType] = prop(None, key=Jsonable.Prop.XSI_TYPE.value)
    uid: str = prop("")
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)
    class_name: Optional[ClassName] = prop(None)
    origin: Optional[Origin] = prop(None)
    is_global: bool = prop(False, key=Prop.GLOBAL.value)
    is_implicit: bool = prop(False, key=Prop.IMPLICIT.value)
    is_shared: bool = prop(False, key=Prop.SHARED.value)
    comment: Optional[str] = prop(None)
    id: Union[str, int] = prop()
    version_id: int = prop(0)
    device_type: Optional[Vendor] = prop(None)  # This seems to be the vendor field.
    ip_type: Optional[IPType] = prop(None)
    referenced: str = prop("")
    installable_target: bool = prop(False)

    @property
    def implicit(self):
        return self.is_implicit

    @implicit.setter
    def implicit(self, v):
        self.is_implicit = v

    @property
    def shared(self):
        return self.is_shared

    @shared.setter
    def shared(self, v):
        self.is_shared = v


@propify
class AnyNetworkObject(NetworkObject):
    xsi_type: NetworkObject.XsiType = prop(NetworkObject.XsiType.ANY_NETWORK_OBJECT)


@propify
class HostNetworkObject(NetworkObject):
    xsi_type: NetworkObject.XsiType = prop(NetworkObject.XsiType.HOST_NETWORK_OBJECT)
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    netmask: Optional[IPAddress] = prop(
        converter=optional(IPAddress),
        jsonify=stringify_optional_obj,
        factory=lambda: IPAddress("255.255.255.255"),
    )


@propify
class InterfaceIP(Jsonable):
    ip: Optional[IPAddress] = prop(None)
    subnet_mask: Optional[IPAddress] = prop(None)


@propify
class Interface(Jsonable):
    name: Optional[str] = prop(None)
    anti_spoof_disabled: Optional[bool] = prop(None)
    interface_ips: List[InterfaceIP] = prop(factory=list, flatify="interface_ip")


@propify
class HostNetworkObjectWithInterfaces(HostNetworkObject):
    interfaces: List[Interface] = prop(factory=list, key="interface")


@propify
class SubnetObject(NetworkObject):
    ip: Optional[str] = prop(None)
    subnet_mask: Optional[str] = prop(None)


@propify
class RangeObject(NetworkObject):
    min_ip: Optional[str] = prop(None)
    max_ip: Optional[str] = prop(None)


@propify
class HostObject(HostNetworkObject):
    # NOT NEEDED?
    pass


def classify_object_type(network_object):
    if "@xsi.type" not in network_object:
        return NetworkObject.kwargify(network_object)

    if network_object["@xsi.type"] in (
        NetworkObject.XsiType.HOST_NETWORK_OBJECT.value,
        NetworkObject.XsiType.HOST_NETWORK_OBJECT_NO_NAMESPACE.value,
    ):
        return HostObject.kwargify(network_object)
    elif network_object["@xsi.type"] == NetworkObject.XsiType.ANY_NETWORK_OBJECT.value:
        return AnyNetworkObject.kwargify(network_object)
    elif network_object["@xsi.type"] == (
        NetworkObject.XsiType.HOST_NETWORK_OBJECT_WITH_INTERFACES.value
    ):
        return HostNetworkObjectWithInterfaces.kwargify(network_object)
    elif (
        network_object["@xsi.type"] == NetworkObject.XsiType.SUBNET_NETWORK_OBJECT.value
    ):
        return SubnetObject.kwargify(network_object)
    elif (
        network_object["@xsi.type"] == NetworkObject.XsiType.RANGE_NETWORK_OBJECT.value
    ):
        return RangeObject.kwargify(network_object)
    elif (
        network_object["@xsi.type"] == NetworkObject.XsiType.NETWORK_OBJECT_GROUP.value
    ):
        return GroupObject.kwargify(network_object)
    else:
        return NetworkObject.kwargify(network_object)


@propify
class GroupObject(NetworkObject):
    class Prop(Enum):
        MEMBER = "member"

    members: List[Union[HostObject, SubnetObject, RangeObject]] = prop(
        factory=list, repr=False, key=Prop.MEMBER.value, kwargify=classify_object_type
    )
