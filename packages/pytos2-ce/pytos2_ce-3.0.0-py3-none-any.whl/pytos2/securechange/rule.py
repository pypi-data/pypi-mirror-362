from typing import List, Optional
from enum import Enum

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, deprecated_property

from pytos2.securechange.network_object import (
    classify_object_type,
    NetworkObject,
)


from pytos2.securechange.designer_verifier_common import (
    classify_service_type,
    ServiceObject,
)


@propify
class SlimRule(Jsonable):
    class XsiType(Enum):
        SLIM_RULE_WITH_METADATA = "ns3:slimRuleWithMetadataDTO"

    class Prop(Enum):
        RULE_NUMBER = "ruleNumber"
        SOURCE_NETWORKS = "sourceNetworks"
        SOURCE_SERVICES = "sourceServices"
        DESTINATION_NETWORKS = "destinationNetworks"
        DESTINATION_SERVICES = "destinationServices"

    uid: str = prop("")
    is_disabled: bool = prop(False)
    rule_number: int = prop(0, key=Prop.RULE_NUMBER.value)
    sources: List[NetworkObject] = prop(
        factory=list, key=Prop.SOURCE_NETWORKS.value, kwargify=classify_object_type
    )
    destinations: List[NetworkObject] = prop(
        factory=list, key=Prop.DESTINATION_NETWORKS.value, kwargify=classify_object_type
    )
    source_services: List[ServiceObject] = prop(
        factory=list,
        key=Prop.SOURCE_SERVICES.value,
        kwargify=classify_service_type,
    )
    destination_services: List[ServiceObject] = prop(
        factory=list,
        key=Prop.DESTINATION_SERVICES.value,
        kwargify=classify_service_type,
    )
    track: Optional[dict] = prop(None)
    install_ons: List[dict] = prop(factory=list)
    communities: List[dict] = prop(factory=list)
    times: List[dict] = prop(factory=list)

    from_zone: Optional[str] = prop(None, repr=False)
    to_zone: Optional[str] = prop(None, repr=False)

    source_objects = deprecated_property("source_objects", "sources")
    source_networks = deprecated_property("source_networks", "sources")
    destination_objects = deprecated_property("destination_objects", "destinations")
    destination_networks = deprecated_property("destination_networks", "destinations")
    services = deprecated_property("services", "destination_services")


@propify
class SlimRuleMetadata(Jsonable):
    permisssiveness_level: str = prop("")
    violations: List[str] = prop(factory=list)
    last_hit: str = prop("")
    shadowed_status: str = prop("")
    ticket_ids: List[int] = prop(factory=list)
    business_owners: List[str] = prop(factory=list)
    expirations: List[str] = prop(factory=list)
    applications: List[str] = prop(factory=list)
    last_modified: str = prop("")


@propify
class SlimRuleWithMetadata(SlimRule):
    rule_metadata: Optional[SlimRuleMetadata] = prop(None)
