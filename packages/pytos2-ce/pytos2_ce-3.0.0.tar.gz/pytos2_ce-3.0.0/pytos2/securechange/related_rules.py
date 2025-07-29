from typing import Optional, List
from enum import Enum

from pytos2.utils import propify, prop
from pytos2.models import Jsonable

from .rule import SlimRule


@propify
class MarkedObjects(Jsonable):
    uid: str = prop(None)


@propify
class IntersectingObjects(Jsonable):
    found_in_source: Optional[MarkedObjects] = prop(None)
    found_in_destination: Optional[MarkedObjects] = prop(None)
    found_in_service: Optional[MarkedObjects] = prop(None)


@propify
class RelatedRuleContainer(Jsonable):
    ignore: Optional[bool] = prop(None)
    rule: Optional[SlimRule] = prop(None)
    intersecting_objects: Optional[IntersectingObjects] = prop(None)


@propify
class RelatedRulesBinding(Jsonable):
    related_rules: List[RelatedRuleContainer] = prop(
        factory=list, flatify="related_rule", key="rules"
    )


@propify
class RelatedRulesDevice(Jsonable):
    bindings: List[RelatedRulesBinding] = prop(
        factory=list, flatify="binding", key="bindings"
    )
    management_id: Optional[int] = prop(None)


@propify
class RelatedRulesAccessRequest(Jsonable):
    ar: Optional[int] = prop(None, key="AR")
    devices: List[RelatedRulesDevice] = prop(
        factory=list, flatify="device", key="devices"
    )


@propify
class RelatedRulesResult(Jsonable):
    class Meta(Enum):
        ROOT = "related_rules"

    access_requests: List[RelatedRulesAccessRequest] = prop(
        factory=list, flatify="access_request", key="access_requests"
    )
