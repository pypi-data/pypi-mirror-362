from typing import Optional, List, Union
from enum import Enum

from pytos2.utils import deprecated_property, propify, prop
from pytos2.models import Jsonable

from .rule import SlimRule

from .network_object import (
    classify_object_type,
    NetworkObject,
    HostObject,
    SubnetObject,
    RangeObject,
    GroupObject,
)

from .designer_verifier_common import (
    ServiceObject,
    TransportService,
    IPService,
    ICMPService,
    AnyApplicationService,
    ServiceGroup,
    classify_service_type,
)


@propify
class Zone(Jsonable):
    class Prop(Enum):
        GLOBAL = "global"
        TYPE = "type"

    name: Optional[str] = prop(None)
    _type: Optional[str] = prop(
        None, key=Prop.TYPE.value, cmp=False, repr=False, init=False
    )
    _global: Optional[bool] = prop(
        None, key=Prop.GLOBAL.value, cmp=False, repr=False, init=False
    )


@propify
class Instruction(Jsonable):
    class InstructionType(Enum):
        NA = "NA"
        NEW_RULE = "NEW_RULE"
        ADD_OBJECT_TO_DEVICE = "ADD_OBJECT_TO_DEVICE"
        UPDATE_RULE = "UPDATE_RULE"
        UPDATE_GROUP = "UPDATE_GROUP"
        REMOVE_RULE = "REMOVE_RULE"
        RULE_REPLACE = "RULE_REPLACE"
        FULLY_IMPLEMENTED = "FULLY_IMPLEMENTED"
        NO_SECURITY_ON_INTERFACE = "NO_SECURITY_ON_INTERFACE"
        NO_NEED_TO_CHANGE = "NO_NEED_TO_CHANGE"

    class RulePlacement(Enum):
        BEFORE = "BEFORE"
        AFTER = "AFTER"

    class ChangeAction(Enum):
        ADD = "ADD"
        REMOVE = "REMOVE"

    change_action: Optional[ChangeAction] = prop(None)
    rule: Optional[SlimRule] = prop(None)

    rule_order: Optional[str] = prop(None)
    rule_placement: Optional[RulePlacement] = prop(None)

    implements_access_requests: List[str] = prop(
        factory=list, flatify="order", repr=True
    )
    status: Optional[str] = prop(None)
    comment: Optional[str] = prop(None)
    instruction_type: Optional[InstructionType] = prop(None)

    sources: List[NetworkObject] = prop(
        factory=list,
        repr=False,
        kwargify=classify_object_type,
        flatify="source_object",
        key="source_objects",
    )
    destinations: List[NetworkObject] = prop(
        factory=list,
        repr=False,
        kwargify=classify_object_type,
        flatify="destination_object",
        key="destination_objects",
    )

    services: List[ServiceObject] = prop(
        factory=list,
        repr=False,
        kwargify=classify_service_type,
        flatify="service_object",
        key="service_objects",
    )


Rule = SlimRule


@propify
class ErrorInstruction(Instruction):
    error_message: Optional[str] = prop(None)


@propify
class NoSecurityInstruction(Instruction):
    pass


@propify
class FullyImplementedInstruction(Instruction):
    pass


@propify
class AddServiceObjectInstruction(Instruction):
    class Prop(Enum):
        DeviceAddedServiceObject = "device_added_service_object"

    object: Union[
        TransportService, IPService, ICMPService, ServiceGroup, AnyApplicationService
    ] = prop(
        None,
        repr=False,
        key=Prop.DeviceAddedServiceObject.value,
        kwargify=classify_service_type,
    )


@propify
class AddNetworkObjectInstruction(Instruction):
    class Prop(Enum):
        DeviceAddedNetworkObject = "device_added_network_object"

    object: Union[HostObject, SubnetObject, RangeObject, GroupObject] = prop(
        None,
        repr=False,
        key=Prop.DeviceAddedNetworkObject.value,
        kwargify=classify_object_type,
    )


@propify
class AddNewRuleInstruction(Instruction):
    pass


@propify
class UpdateGroupInstruction(Instruction):
    modified_object_name: Optional[str] = prop(None)
    modified_object_uid: Optional[str] = prop(None)


@propify
class RemoveRuleInstruction(Instruction):
    modified_object_name: Optional[str] = prop(None)
    modified_object_uid: Optional[str] = prop(None)

    rule_uid: Optional[str] = prop(None)

    original_shadowed_rule_num: Optional[int] = prop(None)


@propify
class UpdateRuleInstruction(Instruction):
    class RulePlacement(Enum):
        ModifiedObjectUID = "modified_object_uid"

    class ChangeAction(Enum):
        ADD = "ADD"

    rule: Optional[SlimRule] = prop(None)

    modified_object_name: Optional[str] = prop(None)
    modified_object_uid: str = prop(None)


def get_instruction_type(instruction: dict):
    if (
        instruction["instruction_type"]
        == Instruction.InstructionType.ADD_OBJECT_TO_DEVICE.value
    ):
        if "device_added_service_object" in instruction:
            return AddServiceObjectInstruction.kwargify(instruction)
        else:
            return AddNetworkObjectInstruction.kwargify(instruction)
    elif instruction["instruction_type"] == Instruction.InstructionType.NEW_RULE.value:
        return AddNewRuleInstruction.kwargify(instruction)
    elif (
        instruction["instruction_type"] == Instruction.InstructionType.REMOVE_RULE.value
    ):
        return RemoveRuleInstruction.kwargify(instruction)
    elif (
        instruction["instruction_type"] == Instruction.InstructionType.UPDATE_RULE.value
    ):
        return UpdateRuleInstruction.kwargify(instruction)
    elif (
        instruction["instruction_type"]
        == Instruction.InstructionType.UPDATE_GROUP.value
    ):
        return UpdateGroupInstruction.kwargify(instruction)
    elif (
        instruction["instruction_type"]
        == Instruction.InstructionType.FULLY_IMPLEMENTED.value
        or instruction["status"] == "DESIGN_FULLY_IMPLEMENTED"
    ):
        return FullyImplementedInstruction.kwargify(instruction)
    elif (
        instruction["instruction_type"]
        == Instruction.InstructionType.NO_SECURITY_ON_INTERFACE.value
    ):
        return NoSecurityInstruction.kwargify(instruction)
    elif instruction["instruction_type"] == Instruction.InstructionType.NA.value:
        return ErrorInstruction.kwargify(instruction)
    else:
        return Instruction.kwargify(instruction)


@propify
class BindingSuggestion(Jsonable):
    binding_uid: Optional[str] = prop(None)
    binding_name: Optional[str] = prop(None)
    instructions: List[Instruction] = prop(
        factory=list, flatify="instruction", repr=True, kwargify=get_instruction_type
    )


@propify
class DeviceSuggestion(Jsonable):
    class Prop(Enum):
        SUGGESTIONS_PER_BINDING = "suggestions_per_binding"

    management_name: Optional[str] = prop(None)
    management_id: Optional[int] = prop(None)
    vendor_name: Optional[str] = prop(None, repr=False)
    revision_number: Optional[int] = prop(None, repr=False)
    offline_device: Optional[bool] = prop(False, repr=False)
    device_software_version: Optional[str] = prop(None, repr=False)

    ancestor_management_id: Optional[int] = prop(None, repr=False)
    ancestor_management_name: Optional[str] = prop(None, repr=False)
    ancestor_management_revision_id: Optional[int] = prop(None, repr=False)
    push_status: Optional[str] = prop(None)
    binding_suggestions: List[BindingSuggestion] = prop(
        factory=list,
        key=Prop.SUGGESTIONS_PER_BINDING.value,
        flatify="binding_suggestion",
        repr=False,
    )


@propify
class DesignerResults(Jsonable):
    class Prop(Enum):
        ID = "id"
        DEVICE_SUGGESTION = "device_suggestion"

    class Meta(Enum):
        ROOT = "designer_results"

    device_suggestions: List[DeviceSuggestion] = prop(
        factory=list, flatify=Prop.DEVICE_SUGGESTION.value, key="suggestions_per_device"
    )

    def get_instruction_by_id(self, id):
        for suggestion in self.device_suggestions:
            for binding_suggestion in suggestion.binding_suggestions:
                for instruction in binding_suggestion.instructions:
                    if instruction.id == id:
                        return instruction
