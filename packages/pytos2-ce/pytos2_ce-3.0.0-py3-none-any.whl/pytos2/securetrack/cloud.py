from enum import Enum
from typing import Optional, List

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, stringify_optional_obj

from netaddr import IPAddress


@propify
class RestCloudMember(Jsonable):
    name: str = prop(None)
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )


@propify
class RestAnonymousSubnet(Jsonable):
    ip: Optional[IPAddress] = prop(None)
    mask: Optional[IPAddress] = prop(None)


@propify
class RestCloud(Jsonable):
    class TopologyCloudType(Enum):
        NON_JOINED = "NON_JOINED"
        JOINED = "JOINED"
        MEMBER = "MEMBER"

    name: str = prop(None)
    domain: int = prop(converter=int)
    type: TopologyCloudType = prop(None)
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    members: List[RestCloudMember] = prop(factory=list)


@propify
class JoinCloud(Jsonable):
    name: str = prop(None)
    clouds: List[int] = prop(factory=list)


@propify
class SuggestedCloud(Jsonable):
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    management_name: str = prop("")
    management_id: Optional[int] = prop(None)
    routes_count: int = prop()
    cloud_name: str = prop("")
    is_parent: bool = prop()
    cloud_id: int = prop()
    parent_vertex_id: Optional[int] = prop(None)
    parent_cloud_name: Optional[str] = prop("")
    parent_cloud_id: Optional[int] = prop(None)
    vertex_id: int = prop()
