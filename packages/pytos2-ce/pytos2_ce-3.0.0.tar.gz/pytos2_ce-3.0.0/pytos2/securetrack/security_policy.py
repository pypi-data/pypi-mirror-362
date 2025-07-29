from enum import Enum
from typing import Optional, List

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify


class CSVData(str):
    pass


class SecurityPolicyMatrixType(Enum):
    SECURITY_ZONE_MATRIX = "SECURITY_ZONE_MATRIX"


@propify
class SecurityPolicy(Jsonable):
    name: Optional[str] = prop(None)
    domain_id: Optional[str] = prop(None)
    domain_name: Optional[str] = prop(None)


@propify
class SecurityZoneMatrix(SecurityPolicy):
    description: Optional[str] = prop(None)
    type: Optional[SecurityPolicyMatrixType] = prop(None)


@propify
class SecurityPolicyInterface(Jsonable):
    name: str = prop(None)
    zones: List[str] = prop(factory=list, key="zones", flatify="zone")


@propify
class SecurityPolicyDeviceMapping(Jsonable):
    device_id: int = prop(None)
    affiliated_interfaces: List[SecurityPolicyInterface] = prop(factory=list)
    interfaces: List[SecurityPolicyInterface] = prop(
        factory=list, key="interfaces", flatify="interface"
    )


@propify
class ZoneUserAction(Jsonable):
    action: Optional[str] = prop(None)
    zone_id: Optional[str] = prop(None, key="zoneId")


@propify
class InterfaceUserMapping(Jsonable):
    interface_name: Optional[str] = prop(None)
    zones_user_actions: List[ZoneUserAction] = prop(factory=list)


@propify
class InterfacesManualMappings(Jsonable):
    interface_manual_mapping: List[InterfaceUserMapping] = prop(factory=list)
