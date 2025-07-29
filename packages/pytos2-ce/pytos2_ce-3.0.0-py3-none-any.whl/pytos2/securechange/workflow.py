from enum import Enum
from typing import Optional, List, ForwardRef

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, multiroot_kwargify


class WorkflowType(Enum):
    GENERIC = "GENERIC"
    ACCESS_REQUEST_AND_MODIFY_GROUP = "ACCESS_REQUEST_AND_MODIFY_GROUP"
    ACCESS_REQUEST = "ACCESS_REQUEST"
    MODIFY_GROUP = "MODIFY_GROUP"
    DECOMMISSION_NETWORK_OBJECT = "DECOMMISSION_NETWORK_OBJECT"
    RULE_DECOMMISSION = "RULE_DECOMMISSION"
    RULE_RECERTIFICATION = "RULE_RECERTIFICATION"
    CLONE_NETWORK_OBJECT_POLICY = "CLONE_NETWORK_OBJECT_POLICY"
    RULE_MODIFICATION = "RULE_MODIFICATION"


@propify
class BasicWorkflowInfo(Jsonable):
    id: Optional[int] = prop(None)
    description: Optional[str] = prop("")
    name: Optional[str] = prop("")
    type: Optional[WorkflowType] = prop("")


@propify
class WorkflowFieldConfiguration(Jsonable):
    pass


@propify
class TicketTaskField(Jsonable):
    pass


@propify
class WorkflowField(Jsonable):
    class Prop(Enum):
        FIELD_VALUE = "fieldValue"

    name: Optional[str] = prop(None)
    tooltip: Optional[str] = prop(None)
    mandatory: Optional[bool] = prop(None)
    multiple: Optional[bool] = prop(None)
    type: Optional[str] = prop(None)
    configuration: Optional[WorkflowFieldConfiguration] = prop(None)
    field_value: Optional[TicketTaskField] = prop(None, key=Prop.FIELD_VALUE)

    pass


@propify
class WorkflowStep(Jsonable):
    pass


@propify
class FullWorkflow(Jsonable):
    class Config:
        has_multi_root = True
        root_default_cls = "FullWorkflow"
        root_dict = {"access_request_workflow": "FullARWorkflow"}

    class Prop(Enum):
        IS_ACTIVE = "isActive"
        IS_VALID = "isValid"
        REFERENCE_TICKET_ENABLED = "referenceTicketEnabled"
        DESCRIPTION = "description"
        ALLOW_REQUESTER_CONFIRMATION = "allowRequesterConfirmation"
        TIME_UNIT_AUTO_CONFIRM = "timeUnitAutoConfirm"
        TIME_TO_AUTO_CONFIRM = "timeToAutoConfirm"
        REOPEN_STEP_NAME = "reopenStepName"
        CLOSE_IMPLEMENTED = "closeImplemented"
        GLOBAL_FIELDS = "globalFields"

    id: Optional[int] = prop(None)
    type: Optional[WorkflowType] = prop(WorkflowType.GENERIC)
    name: Optional[str] = prop(None)
    is_active: Optional[bool] = prop(None, key=Prop.IS_ACTIVE)
    is_valid: Optional[bool] = prop(None, key=Prop.IS_VALID)
    reference_ticket_enabled: Optional[bool] = prop(
        None, key=Prop.REFERENCE_TICKET_ENABLED
    )
    description: Optional[str] = prop(None, key=Prop.DESCRIPTION)
    allow_requester_confirmation: Optional[bool] = prop(
        None, key=Prop.ALLOW_REQUESTER_CONFIRMATION
    )
    time_unit_auto_confirm: Optional[str] = prop(None, key=Prop.TIME_UNIT_AUTO_CONFIRM)
    time_to_auto_confirm: Optional[int] = prop(None, key=Prop.TIME_TO_AUTO_CONFIRM)
    reopen_step_name: Optional[str] = prop(None, key=Prop.REOPEN_STEP_NAME)
    close_implemented: Optional[bool] = prop(None, key=Prop.CLOSE_IMPLEMENTED)
    steps: List[WorkflowStep] = prop(factory=list)
    global_fields: List[WorkflowField] = prop(factory=list)

    @classmethod
    def kwargify(cls, data):
        return multiroot_kwargify(cls, data, _globals=globals(), _locals=locals())


@propify
class FullARWorkflow(FullWorkflow):
    pass
