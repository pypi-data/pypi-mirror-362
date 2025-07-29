from typing import Optional, List
from enum import Enum

from pytos2.models import Jsonable
from pytos2.utils import propify, prop
from .domain import Domain

from netaddr import IPAddress, IPNetwork  # type: ignore


@propify
class Zone(Jsonable):
    class Prop(Enum):
        USER_NETWORKS = "userNetworks"

    domain: Optional[Domain] = prop(False, repr=False)
    internet: Optional[bool] = prop(None, repr=False)
    unassociated_networks: Optional[bool] = prop(None, repr=False)
    user_networks: Optional[bool] = prop(None, repr=False, key=Prop.USER_NETWORKS.value)

    importing_domain: Optional[Domain] = prop(None, repr=False)
    comment: str = prop("")
    shared: bool = prop(False, repr=False)
    name: str = prop("")


@propify
class ZoneEntry(Jsonable):
    class Props(Enum):
        ZONE_ID = "zoneId"
        ZONE_NAME = "zoneName"

    id: int = prop(0, repr=False)
    ip: Optional[IPAddress] = prop(None)
    netmask: Optional[IPAddress] = prop(None, repr=False)
    prefix: int = prop(0)
    zone_id: int = prop(0, key=Props.ZONE_ID.value, repr=False)
    zone_name: str = prop("", key=Props.ZONE_NAME.value, repr=False)

    @property
    def subnet(self):
        return IPNetwork(str(self.ip) + "/" + str(self.prefix))


@propify
class ZoneReference(Jsonable):
    """
    For mapping zones/{id}/descendants and zones/{id}/ancestors.
    """

    id: int = prop(0)
    name: str = prop("")
    zones: List["ZoneReference"] = prop(factory=list, flatify="zone")
    clouds: List["Cloud"] = prop(factory=list, flatify="cloud")


@propify
class Subnet(Jsonable):
    id: int = prop()
    netmask: Optional[str] = prop(None)
    ip: Optional[str] = prop(None)
    uid: Optional[str] = prop(None)


@propify
class CloudEntry(Jsonable):
    class Prop(Enum):
        BEHIND_CLOUD = "behindCloud"

    id: int = prop(0)
    netmask: Optional[str] = prop(None)
    ip: Optional[str] = prop(None)
    uid: Optional[str] = prop(None)

    cloud: Optional["Cloud"] = prop(None)


@propify
class Cloud(Jsonable):
    class Prop(Enum):
        SECURITY_LEVEL = "securityLevel"
        CUSTOMER_ID_TAG = "customerIdTag"
        INTERFACE_IP = "interfaceIp"
        CUSTOMER_NAME = "customerName"

    id: int = prop()
    security_level: Optional[dict] = prop(None, key=Prop.SECURITY_LEVEL.value)
    customer_id_tag: Optional[int] = prop(None, key=Prop.CUSTOMER_ID_TAG.value)
    interface_ip: Optional[str] = prop(None, key=Prop.INTERFACE_IP.value)
    subnets: List[Subnet] = prop(factory=list)
    customer_name: Optional[str] = prop(None, key=Prop.CUSTOMER_NAME.value)
    entries: List[CloudEntry] = prop(factory=list)
    uid: Optional[str] = prop(None)
