from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from copy import deepcopy

from attr.converters import optional

from pytos2.models import Jsonable, IPType
from pytos2.utils import jsonify, propify, prop, safe_iso8601_date

from pytos2.securetrack.network_object import NetworkObject, Interface, ObjectReference

from .device import Device


class SecurityRuleType(Enum):
    CLOUD_SECURITY_RULE = "cloudSecurityRuleDTO"
    SECURITY_RULE = "securityRuleDTO"


@propify
class Track(Jsonable):
    class Level(Enum):
        DISABLED = "DISABLED"
        LOG = "LOG"
        NONE = "NONE"

    level: Optional[Level] = prop(None, repr=False)


@propify
class PolicyTarget(Jsonable):
    pass


@propify
class InstallableTarget(Jsonable):
    device_id: Optional[int] = prop(None, converter=optional(int))
    firewall_id: Optional[str] = prop(None)
    virtual_firewall_name: Optional[str] = prop(None, repr=False)
    virtual_firewall_securetrack_name: Optional[str] = prop(None)


@propify
class Zone(Jsonable):
    class Prop(Enum):
        GLOBAL = "global"

    name: Optional[str] = prop(None, repr=False)
    is_global: Optional[bool] = prop(None, repr=False, key=Prop.GLOBAL.value)


@propify
class PolicyXsiType(Enum):
    MANAGEMENT_POLICY = "managementPolicyDTO"


@propify
class BindingPolicy(Jsonable):
    class Prop(Enum):
        UNIQUE_ACTIVE_IN_ITG = "unique_active_in_itg"
        POLICY_TARGETS = "policyTargets"
        INSTALLABLE_TARGET = "installable_target"

    xsi_type: Optional[PolicyXsiType] = prop(
        None, repr=False, key=Jsonable.Prop.XSI_TYPE.value
    )
    name: Optional[str] = prop(None, repr=False)
    itg_id: Optional[int] = prop(None, converter=optional(int), repr=False)
    itg: Optional[str] = prop(None, repr=False)
    is_unique_active_in_itg: bool = prop(
        False, repr=False, key=Prop.UNIQUE_ACTIVE_IN_ITG.value
    )
    policy_targets: List[PolicyTarget] = prop(
        factory=list, repr=False, key=Prop.POLICY_TARGETS.value
    )
    installable_targets: List[InstallableTarget] = prop(
        factory=list, repr=False, flatify="installable_target"
    )


@propify
class BindingACL(Jsonable):
    class Prop(Enum):
        GLOBAL = "global"

    name: Optional[str] = prop(None, repr=False)
    is_global: Optional[bool] = prop(None, repr=False, key=Prop.GLOBAL.value)
    interfaces: List[Interface] = prop(factory=list, repr=False)
    ipv6_only: Optional[bool] = prop(None, repr=False)


@propify
class RuleBinding(Jsonable):
    class Prop(Enum):
        FROM_ZONE = "from_zone"
        TO_ZONE = "to_zone"

    class Direction(Enum):
        INBOUND = "inbound"
        OUTBOUND = "outbound"

    policy: Optional[BindingPolicy] = prop(None, repr=False)
    acl: Optional[BindingACL] = prop(None, repr=False)
    rule_count: int = prop(0)
    security_rule_count: int = prop(0)
    default: Optional[bool] = prop(None, repr=False)
    uid: Optional[str] = prop(None)
    direction: Optional[Direction] = prop(None)
    display_name: Optional[str] = prop(None)
    sub_policy_name: Optional[str] = prop(None, repr=False)
    is_shared: Optional[bool] = prop(None, repr=False)
    is_global: Optional[bool] = prop(None, repr=False)
    from_zones: List[Zone] = prop(factory=list, repr=False, key=Prop.FROM_ZONE.value)
    to_zones: List[Zone] = prop(factory=list, repr=False, key=Prop.TO_ZONE.value)
    ip_type: Optional[IPType] = prop(None, repr=False)


@propify
class SecurityRuleBase(Jsonable):
    class Prop(Enum):
        DISABLED = "disabled"
        BINDING = "binding"
        INSTALL = "install"

    class Type(Enum):
        RULE = "rule"

    id: int = prop(0, converter=int)
    device: Optional[Device] = prop(None)
    uid: Optional[str] = prop(None)
    order: Optional[int] = prop(None, converter=optional(int), repr=False)
    is_disabled: Optional[bool] = prop(None, repr=False, key=Prop.DISABLED.value)
    bindings: List[RuleBinding] = prop(factory=list, repr=False, key=Prop.BINDING.value)

    installs: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.INSTALL.value
    )


@propify
class NatRule(SecurityRuleBase):
    class Prop(Enum):
        AUTO_NAT = "autoNat"
        ORIG_SRC_NETWORK = "orig_src_network"
        ORIG_DST_NETWORK = "orig_dst_network"
        TRANSLATED_DST_NETWORK = "translated_dst_network"
        TRANSLATED_SRC_NETWORK = "translated_src_network"
        TRANSLATED_SERVICE = "translated_service"

    xsi_type: Optional[SecurityRuleType] = prop(
        None, repr=False, key=Jsonable.Prop.XSI_TYPE.value
    )
    is_auto_nat: bool = prop(None, repr=False, key=Prop.AUTO_NAT.value)
    egress_interface: List[Interface] = prop(factory=list, repr=False)
    orig_service: List[ObjectReference] = prop(factory=list, repr=False)

    install: List[str] = prop(factory=list, repr=False)
    enable_net4tonet6: Optional[bool] = prop(None, repr=False)
    enable_route_lookup: Optional[bool] = prop(None, repr=False)
    orig_src_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.ORIG_SRC_NETWORK.value
    )
    orig_dest_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.ORIG_DST_NETWORK.value
    )
    translated_dest_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.TRANSLATED_DST_NETWORK.value
    )
    translated_src_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.TRANSLATED_SRC_NETWORK.value
    )
    translated_services: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.TRANSLATED_SERVICE.value
    )
    type: Optional[SecurityRuleBase.Type] = prop(None, repr=False)


@propify
class RecordSet(Jsonable):
    class Prop(Enum):
        BUSINESS_OWNER_EMAIL = "businessOwnerEmail"
        BUSINESS_OWNER_NAME = "businessOwnerName"
        EXPIRATION_DATE = "expireDate"
        TICKET_CR = "ticketCr"
        TICKET_ORIGIN = "ticketOrigin"
        TICKET_STATUS = "ticketStatus"

    class TicketOrigin(Enum):
        SCW = "scw"

    business_owner_email: Optional[str] = prop(
        None, key=Prop.BUSINESS_OWNER_EMAIL.value
    )
    business_owner_name: Optional[str] = prop(None, key=Prop.BUSINESS_OWNER_NAME.value)
    expiration_date: Optional[datetime] = prop(
        None,
        key=Prop.EXPIRATION_DATE.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat() if d else None,
    )

    ticket_cr: str = prop("", key=Prop.TICKET_CR.value)
    ticket_origin: Optional[TicketOrigin] = prop(None, key=Prop.TICKET_ORIGIN.value)
    ticket_status: str = prop("", key=Prop.TICKET_STATUS.value)

    _exists_on_server: bool = prop(False, jsonify=False)


@propify
class Violation(Jsonable):
    name: str = prop("")
    type: str = prop("")


@propify
class SecurityPolicyViolation(Jsonable):
    class Severity(Enum):
        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

    severity: Severity = prop()


class SecurityPolicyViolationType(Enum):
    SECURITY_POLICY = "SECURITY_POLICY"
    PCI = "PCI"
    SOX = "SOX"


@propify
class SecureAppApplication(Jsonable):
    app_name: str = prop("")
    app_owner: str = prop("")


def record_set_from_server(obj):
    record_set = RecordSet.kwargify(obj)
    record_set._exists_on_server = True

    return record_set


@propify
class Documentation(Jsonable):
    class Prop(Enum):
        RECORD_SETS = "record_set"
        SECURE_APP_APPLICATIONS = "secure_app_application"

    class Shadowed(Enum):
        Fully = "Fully shadowed"
        Not = "Not shadowed"
        NotApplicable = "N/A"
        Empty = ""

    class CertificationStatus(Enum):
        CERTIFIED = "CERTIFIED"
        DECERTIFIED = "DECERTIFIED"

    comment: Optional[str] = prop(None)
    legacy_rule: Optional[bool] = prop(None)
    stealth_rule: Optional[bool] = prop(None)
    shadowed: Optional[Shadowed] = prop(None)
    record_sets: List[RecordSet] = prop(
        factory=list, key=Prop.RECORD_SETS.value, kwargify=record_set_from_server
    )
    last_modified: Optional[str] = prop(None)
    last_hit: Optional[str] = prop(None)
    permissiveness_level: Optional[str] = prop(None)

    violations: List[Violation] = prop(factory=list, flatify="violation")
    certification_status: Optional[CertificationStatus] = prop(None)
    certification_date: Optional[datetime] = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )

    certification_expiration_date: Optional[datetime] = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )

    secure_app_applications: List[SecureAppApplication] = prop(
        factory=list, key=Prop.SECURE_APP_APPLICATIONS.value
    )

    tech_owner: Optional[str] = prop(None)

    @property
    def _json(self) -> dict:
        if self._json_override is not None:
            return self._json_override
        obj = deepcopy(self)
        obj.record_sets = [rs for rs in obj.record_sets if not rs._exists_on_server]

        return jsonify(obj)


@propify
class SecurityRule(SecurityRuleBase):
    class Meta(Enum):
        ROOT = "rule"

    class Prop(Enum):
        IMPLICIT = "implicit"
        EXTERNAL = "external"
        TRACK = "track"
        AUTHENTICATION_STATUS = "authentication_status"
        SRC_NETWORK = "src_network"
        DST_NETWORK = "dst_network"
        SRC_SERVICE = "src_service"
        DST_SERVICE = "dst_service"
        APPLICATION = "application"
        TIME = "time"
        VPN = "vpn"
        OPTION = "option"
        URL_CATEGORY = "url_category"
        SRC_ZONE = "src_zone"
        DST_ZONE = "dst_zone"
        SRC_ZONE_ANY = "src_zone_any"
        DST_ZONE_ANY = "dst_zone_any"
        ADDITIONAL_PARAMETER = "additional_parameter"
        AUTHENTICATION_RULE = "authentication_rule"
        USERS = "users"
        ASSOCIATED_NAT_RULE = "associatedNatRule"
        SUB_POLICY_GLOBAL = "sub_policy_global"
        SUB_POLICY_SHARED = "sub_policy_shared"

    class GlobalLocation(Enum):
        AFTER = "AFTER"
        BEFORE = "BEFORE"
        MIDDLE = "MIDDLE"

    class Action(Enum):
        ACCEPT = "Accept"
        CONTINUE = "Continue"
        DENY = "Deny"
        DROP = "Drop"
        INLINE_LAYER = "Inline Layer"
        REJECT = "Reject"

    class Option(Enum):
        LOG = "LOG"
        LOG_FORWARDING = "LOG_FORWARDING"
        LOG_SESSION = "LOG_SESSION"
        RETURNING_TRAFFIC = "RETURNING_TRAFFIC"

    class RuleType(Enum):
        INTERZONE = "interzone"
        INTRAZONE = "intrazone"
        UNIVERSAL = "universal"

    xsi_type: Optional[SecurityRuleType] = prop(
        None, repr=False, key=Jsonable.Prop.XSI_TYPE.value
    )
    cp_uid: Optional[str] = prop(None, repr=False)
    name: Optional[str] = prop(None, repr=False)
    comment: Optional[str] = prop(None, repr=False)
    action: Optional[Action] = prop(None)
    is_implicit: Optional[bool] = prop(None, repr=False, key=Prop.IMPLICIT.value)
    is_external: Optional[bool] = prop(None, repr=False, key=Prop.EXTERNAL.value)
    global_location: Optional[GlobalLocation] = prop(False, repr=False)
    acceleration_breaker: Optional[bool] = prop(None, repr=False)
    is_authentication_rule: bool = prop(
        False, repr=False, key=Prop.AUTHENTICATION_RULE.value
    )
    rule_number: Optional[int] = prop(None, converter=optional(int), repr=False)
    track: Optional[Track] = prop(None, repr=False)
    options: List[Option] = prop(factory=list, repr=False, key=Prop.OPTION.value)
    src_networks_negated: Optional[bool] = prop(None, repr=False)
    dest_networks_negated: Optional[bool] = prop(None, repr=False)
    src_services_negated: Optional[bool] = prop(None, repr=False)
    dest_services_negated: Optional[bool] = prop(None, repr=False)
    src_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.SRC_NETWORK.value
    )
    dest_networks: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.DST_NETWORK.value
    )
    src_services: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.SRC_SERVICE.value
    )
    dest_services: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.DST_SERVICE.value
    )
    applications: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.APPLICATION.value
    )
    times: List[ObjectReference] = prop(factory=list, repr=False, key=Prop.TIME.value)

    vpns: List[ObjectReference] = prop(factory=list, repr=False, key=Prop.VPN.value)

    users: List[ObjectReference] = prop(factory=list, repr=False)
    user_access: List[ObjectReference] = prop(factory=list, repr=False)
    url_categories: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.URL_CATEGORY.value
    )
    rule_type: Optional[RuleType] = prop(None, repr=False)
    src_zones: List[str] = prop(factory=list, repr=False, key=Prop.SRC_ZONE.value)
    dest_zones: List[str] = prop(factory=list, repr=False, key=Prop.DST_ZONE.value)
    is_src_zone_any: Optional[bool] = prop(
        None, repr=False, key=Prop.SRC_ZONE_ANY.value
    )
    is_dest_zone_any: Optional[bool] = prop(
        None, repr=False, key=Prop.DST_ZONE_ANY.value
    )
    rule_location: Optional[str] = prop(None, repr=False)
    rule_location_display: Optional[str] = prop(None, repr=False)
    additional_parameters: List[ObjectReference] = prop(
        factory=list, repr=False, key=Prop.ADDITIONAL_PARAMETER.value
    )
    type: Optional[SecurityRuleBase.Type] = prop(None, repr=False)

    ip_type: Optional[IPType] = prop(None, repr=False)
    fmg_from_zone: Optional[str] = prop(None, repr=False)
    fmg_to_zone: Optional[str] = prop(None, repr=False)
    associated_nat_rule: Optional[NatRule] = prop(
        None, repr=False, key=Prop.ASSOCIATED_NAT_RULE.value
    )
    textual_rep: Optional[str] = prop(None, repr=False)

    priority: Optional[str] = prop(None, repr=False)
    sub_policy: Optional[str] = prop(None, repr=False)
    sub_policy_uid: Optional[str] = prop(None, repr=False)
    is_sub_policy_global: bool = prop(
        False, repr=False, key=Prop.SUB_POLICY_GLOBAL.value
    )
    is_sub_policy_shared: bool = prop(
        False, repr=False, key=Prop.SUB_POLICY_SHARED.value
    )
    documentation: Optional[Documentation] = prop(None)


@propify
class RuleLastUsage(Jsonable):
    rule_uid: str = prop("", key="rule_UID")
    users: dict = prop(None)
    applications: dict = prop(None)
    rule_last_hit: Optional[datetime] = prop(
        None,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat() if d else None,
        repr=lambda v: v.isoformat() if v else "None",
    )
