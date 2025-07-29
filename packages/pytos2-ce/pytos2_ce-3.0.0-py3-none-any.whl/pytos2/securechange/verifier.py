from datetime import datetime

from typing import Optional, List, Union
from enum import Enum

from pytos2.utils import propify, prop, TimeFormat
from pytos2.models import Jsonable, UnMapped

from pytos2.securetrack.device import Device
from pytos2.securechange.rule import SlimRule


class VerificationStatus(Enum):
    IMPLEMENTED = "implemented"
    NOT_IMPLEMENTED = "not implemented"


@propify
class Binding(Jsonable):
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"

    class XsiType(Enum):
        POLICY_BINDING = "policy__binding"
        ZONE_BINDING = "zone__binding"
        ZONE_WITH_POLICY_BINDING = "zone__with__policy__binding"
        ACL_BINDING = "acl__binding"
        NON_EXISTING_BINDING = "non_existing_binding"

    xsi_type: Optional[XsiType] = prop(None, key=Prop.XSI_TYPE.value)
    installed_on_module: List[str] = prop(factory=list)


@propify
class NonExistingBinding(Binding):
    incoming_interface_name: Optional[str] = prop(None)
    outgoing_interface_name: Optional[str] = prop(None)


@propify
class PolicyBinding(Binding):
    policy_name: Optional[str] = prop(None)


@propify
class ZoneWithPolicyBinding(PolicyBinding):
    pass


@propify
class ZoneBinding(Binding):
    from_zone: Optional[str] = prop(None)
    to_zone: Optional[str] = prop(None)

    pass


@propify
class ACLBinding(Binding):
    acl_name: Optional[str] = prop(None)
    incoming_interface_name: Optional[str] = prop(None)
    outgoing_interface_name: Optional[str] = prop(None)


def classify_binding(binding):
    binding_types = {
        Binding.XsiType.POLICY_BINDING.value: PolicyBinding,
        Binding.XsiType.ZONE_BINDING.value: ZoneBinding,
        Binding.XsiType.ZONE_WITH_POLICY_BINDING.value: ZoneWithPolicyBinding,
        Binding.XsiType.ACL_BINDING.value: ACLBinding,
        Binding.XsiType.NON_EXISTING_BINDING.value: NonExistingBinding,
    }

    if binding["@xsi.type"] in binding_types:
        cls = binding_types[binding["@xsi.type"]]
        return cls.kwargify(binding)
    else:
        return Binding.kwargify(binding)


@propify
class VerifierBinding(Jsonable):
    class ImplicitCleanupRule(Enum):
        VIOLATED = "VIOLATED"
        NOT_HANDLED = "NOT_HANDLED"
        IMPLEMENTED = "IMPLEMENTED"

    binding: Optional[Binding] = prop(None, kwargify=classify_binding)
    verified: bool = prop(False)
    verifier_error_code: Optional[str] = prop(None)
    verifier_warning: Optional[str] = prop(None)
    percent_implemented: int = prop(0)
    implementation_percentage_threshold: int = prop(0)
    implementing_rules: List[SlimRule] = prop(factory=list, flatify="implementing_rule")
    violating_rules: List[SlimRule] = prop(factory=list, flatify="violating_rule")
    handled_by_implicit_cleanup_rule: ImplicitCleanupRule = prop("")


@propify
class VerifierTarget(Jsonable):
    management_name: Optional[str] = prop(None)
    management_id: Optional[int] = prop(None)
    device_type: Optional[str] = prop(None)
    revision_number: Optional[int] = prop(None)
    administrator: Optional[str] = prop(None)
    vendor: Optional[Device.Vendor] = prop(None)
    verification_status: Optional[VerificationStatus] = prop(None)

    date: Optional[datetime.date] = prop(
        None, repr=False, kwargify=lambda d: datetime.strptime(d, TimeFormat.DATE.value)
    )
    time: Optional[datetime.time] = prop(
        None, repr=False, kwargify=lambda d: datetime.strptime(d, TimeFormat.TIME.value)
    )

    verifier_error_code: Optional[str] = prop(None)
    verifier_warning: Optional[str] = prop(None)

    verifier_bindings: List[VerifierBinding] = prop(
        factory=list, flatify="verifier_binding"
    )


@propify
class VerifierResultLinkInner(Jsonable):
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"
        HREF = "@href"

    xsi_type: str = prop(key=Prop.XSI_TYPE.value)
    href: str = prop(key=Prop.HREF.value)


@propify
class AccessRequestVerifierResult(Jsonable):
    verifier_targets: List[VerifierTarget] = prop(
        factory=list, flatify="verifier_target"
    )
    topology_image_link: str = prop("", flatify="@href")


@propify
class VerifierResultLink(Jsonable):
    status: Optional[VerificationStatus] = prop(None)
    result: Optional[VerifierResultLinkInner] = prop(None)


def classify_verifier_result(obj):
    if "access_request_verifier_result" in obj:
        return AccessRequestVerifierResult.kwargify(
            obj["access_request_verifier_result"]
        )
    else:
        return UnMapped()
