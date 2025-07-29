from typing import Optional, List

from netaddr import IPAddress, IPNetwork, IPRange  # type: ignore

from pytos2.utils import propify, prop, stringify_optional_obj
from pytos2.models import Jsonable


@propify
class TopologySyncStatus(Jsonable):
    percentage: Optional[int] = prop(None)
    description: Optional[str] = prop(None)


@propify
class TopologyMode(Jsonable):
    domain_id: int = prop(None, key="domainId")
    device_id: int = prop(None, key="mgmtId")
    mode: str = prop("")  # Will be "DISABLED" or "ENABLED"


@propify
class TopologySubnet(Jsonable):
    name: str = prop("")
    ip: IPAddress = prop(None, converter=IPAddress, jsonify=stringify_optional_obj)
    mask: IPAddress = prop(None, converter=IPAddress, jsonify=stringify_optional_obj)
    domain_id_tag: Optional[int] = prop(None, key="domainIdTag")


@propify
class SubnetDevice(Jsonable):
    is_generic: bool = prop(None)
    name: str = prop("")
    interface_id: Optional[int] = prop(None)
    interface_name: str = prop("")
    interface_ip: Optional[IPAddress] = prop(
        None, converter=IPAddress, jsonify=stringify_optional_obj
    )


@propify
class TopologySubnetDetailed(TopologySubnet):
    attached_devices: List[SubnetDevice] = prop(factory=list, flatify="attached_device")
    join_candidates: List[SubnetDevice] = prop(factory=list, flatify="join_candidate")
