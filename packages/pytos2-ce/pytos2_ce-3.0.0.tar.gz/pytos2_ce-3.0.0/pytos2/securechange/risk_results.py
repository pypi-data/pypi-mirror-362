from pytos2.utils import propify, prop
from pytos2.models import Jsonable

from netaddr import IPAddress, IPRange

from typing import List, Optional
from enum import Enum

from attr.converters import optional


def _classify(obj, type_dict, default_type):
    xsi_type = obj.get(Jsonable.Prop.XSI_TYPE.value)

    cls = type_dict.get(xsi_type, None)
    if cls:
        return cls.kwargify(obj)
    else:
        return default_type.kwargify(obj)


def classify_violation(obj):
    type_dict = {
        SecurityPolicyViolationType.SECURITY_ZONE_MATRIX_VIOLATION.value: SecurityZoneMatrixViolation,
        SecurityPolicyViolationType.UNMATCHED_PRIVATE_ADDRESS_VIOLATION.value: UnmatchedPrivateAddressViolation,
    }

    return _classify(obj, type_dict, SecurityPolicyViolation)


def classify_violation_network_object(obj):
    type_dict = {
        NetworkObjectType.IP_NETWORK_OBJECT.value: IpNetworkObject,
        NetworkObjectType.RANGE_NETWORK_OBJECT.value: RangeNetworkObject,
        NetworkObjectType.ANY_NETWORK_OBJECT.value: AnyNetworkObject,
        NetworkObjectType.SINGLE_NETWORK_OBJECT.value: SingleNetworkObject,
        NetworkObjectType.GROUP_MEMBER_NETWORK_OBJECT.value: GroupMemberNetworkObject,
        NetworkObjectType.LDAP_ENTITY.value: LDAPEntity,
    }

    return _classify(obj, type_dict, NetworkObjectInViolation)


def classify_matrix_cell(obj):
    type_dict = {
        MatrixCellType.BLOCKED_CELL_VIOLATION.value: BlockedCellViolation,
        MatrixCellType.RESTRICTED_CELL.value: RestrictedCellViolation,
    }

    return _classify(obj, type_dict, MatrixCellViolation)


def classify_violation_service(obj):
    type_dict = {
        ServiceType.ANY_SERVICE.value: AnyService,
        ServiceType.SINGLE_SERVICE.value: None,
        ServiceType.SINGLE_SERVICE_OBJECT.value: None,
        ServiceType.GROUP_MEMBER_SERVICE_OBJECT.value: None,
    }

    return _classify(obj, type_dict, ServiceInViolation)


@propify
class SecurityZoneMatrix(Jsonable):
    name: str = prop()


class SecurityPolicyViolationType(Enum):
    SECURITY_ZONE_MATRIX_VIOLATION = "security_zone_matrix_violation"
    UNMATCHED_PRIVATE_ADDRESS_VIOLATION = "unmatched_private_address_violation"


class ServiceType(Enum):
    ANY_SERVICE = "any_service"
    SINGLE_SERVICE = "single_service"
    SINGLE_SERVICE_OBJECT = "single_service_object"
    GROUP_MEMBER_SERVICE_OBJECT = "group_member_service_object"


class NetworkObjectType(Enum):
    IP_NETWORK_OBJECT = "ip_network_object"
    RANGE_NETWORK_OBJECT = "range_network_object"

    ANY_NETWORK_OBJECT = "any_network_object"
    SINGLE_NETWORK_OBJECT = "single_network_object"
    GROUP_MEMBER_NETWORK_OBJECT = "group_member_network_object"
    LDAP_ENTITY = "ldap_entity"


class MatrixCellType(Enum):
    BLOCKED_CELL_VIOLATION = "blocked_cell_violation"
    RESTRICTED_CELL = "restricted_cell"


@propify
class ServiceInViolation(Jsonable):
    name: Optional[str] = prop(None)


@propify
class AnyService(ServiceInViolation):
    pass


@propify
class SingleService(ServiceInViolation):
    protocol: Optional[str] = prop(None)
    port: Optional[int] = prop(None, converter=optional(int))


@propify
class SingleServiceObject(ServiceInViolation):
    uid: Optional[str] = prop(None)
    management_id: Optional[int] = prop(None)


@propify
class GroupMemberServiceObject(ServiceInViolation):
    group_member: Optional[SingleServiceObject] = prop(None)
    group_member_path: Optional[str] = prop(None)


@propify
class NetworkObjectInViolation(Jsonable):
    name: Optional[str] = prop(None)


class AnyNetworkObject(NetworkObjectInViolation):
    pass


@propify
class SingleNetworkObject(NetworkObjectInViolation):
    uid: Optional[str] = prop(None)
    management_id: Optional[int] = prop(None)


@propify
class GroupMemberNetworkObject(NetworkObjectInViolation):
    group_member: Optional[SingleNetworkObject] = prop(None)
    group_member_path: Optional[str] = prop(None)
    name: Optional[str] = prop(None)


@propify
class LDAPEntity(NetworkObjectInViolation):
    ldap_dn: Optional[str] = prop(None)
    ldap_id: Optional[str] = prop(None)
    name: Optional[str] = prop(None)


@propify
class IpNetworkObject(NetworkObjectInViolation):
    ip: Optional[IPAddress] = prop(None)
    mask: Optional[str] = prop(None)
    name: Optional[str] = prop(None)


@propify
class RangeNetworkObject(NetworkObjectInViolation):
    min_ip: Optional[IPAddress] = prop(None)
    max_ip: Optional[IPAddress] = prop(None)

    @property
    def ip_range(self) -> Optional[IPRange]:
        if self.min_ip and self.max_ip:
            return IPRange(self.min_ip, self.max_ip)


@propify
class MatrixCellViolation(Jsonable):
    from_zone: Optional[str] = prop(None)
    to_zone: Optional[str] = prop(None)

    sources: List[NetworkObjectInViolation] = prop(
        factory=list, flatify="source", kwargify=classify_violation_network_object
    )
    destinations: List[NetworkObjectInViolation] = prop(
        factory=list, flatify="destination", kwargify=classify_violation_network_object
    )

    allowed_services: List[ServiceInViolation] = prop(
        factory=list, flatify="allowed_service", kwargify=classify_violation_service
    )
    not_allowed_services: List[ServiceInViolation] = prop(
        factory=list, flatify="not_allowed_service", kwargify=classify_violation_service
    )
    blocked_services: List[ServiceInViolation] = prop(
        factory=list, flatify="blocked_service", kwargify=classify_violation_service
    )
    not_blocked_services: List[ServiceInViolation] = prop(
        factory=list, flatify="not_blocked_service", kwargify=classify_violation_service
    )


@propify
class BlockedCellViolation(MatrixCellViolation):
    pass


class RestrictedCellViolation(MatrixCellViolation):
    class Prop(Enum):
        VIOLATING_SERVICES = "violatingServices"
        REQUIREMENT_SERVICES = "requirementServices"

    violating_services: List[ServiceInViolation] = prop(
        factory=list, key=Prop.VIOLATING_SERVICES.value
    )
    flow: Optional[str] = prop(None)
    requirement_services: List[ServiceInViolation] = prop(
        factory=list, key=Prop.REQUIREMENT_SERVICES.value
    )
    flow_sources: List[NetworkObjectInViolation] = prop(
        factory=list, flatify="flow_source"
    )
    flow_destination: List[NetworkObjectInViolation] = prop(
        factory=list, flatify="flow_destination"
    )


@propify
class SecurityPolicyViolation(Jsonable):
    class Severity(Enum):
        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

    severity: Severity = prop()


@propify
class SecurityZoneMatrixViolation(SecurityPolicyViolation):
    security_zone_matrix: Optional[SecurityZoneMatrix] = prop(None)
    matrix_cell_violation: Optional[MatrixCellViolation] = prop(
        None, kwargify=classify_matrix_cell
    )


@propify
class UnmatchedPrivateAddressViolation(SecurityPolicyViolation):
    violation_source_networks: List[NetworkObjectInViolation] = prop(
        factory=list,
        kwargify=classify_violation_network_object,
        flatify="violation_source_network",
    )
    violation_destination_networks: List[NetworkObjectInViolation] = prop(
        factory=list,
        kwargify=classify_violation_network_object,
        flatify="violation_destination_network",
    )


@propify
class ComplianceRule(Jsonable):
    name: Optional[str] = prop(None)
    number: Optional[str] = prop(None)


@propify
class CompliancePolicy(Jsonable):
    compliance_rules: List[ComplianceRule] = prop(
        factory=list, flatify="compliance_rule"
    )
    name: Optional[str] = prop(None)
    type: Optional[str] = prop(None)


@propify
class RiskAnalysisResult(Jsonable):
    class RiskStatus(Enum):
        HAS_RISK = "has risk"
        NO_RISK = "no risk"
        NOT_RUN = "not run"

    status: RiskStatus = prop()
    compliance_policies: List[CompliancePolicy] = prop(
        factory=list, flatify="compliance_policy"
    )
    security_policy_violations: List[SecurityPolicyViolation] = prop(
        factory=list, flatify="security_policy_violation", kwargify=classify_violation
    )
