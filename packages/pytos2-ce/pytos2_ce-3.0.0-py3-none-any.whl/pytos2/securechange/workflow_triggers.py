from enum import Enum

from typing import Optional, List

from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class Script(Jsonable):
    class ScriptXsiType(Enum):
        SCRIPT_DTO = "ScriptDTO"

    xsi_type: ScriptXsiType = prop(
        ScriptXsiType.SCRIPT_DTO, key=Jsonable.Prop.XSI_TYPE.value
    )
    path: str = prop()
    arguments: str = prop("")


@propify
class Workflow(Jsonable):
    name: str = prop()
    parent_workflow_id: int = prop()


@propify
class Trigger(Jsonable):
    """
    This represents a workflow and event combination that the trigger script will be executed for.

    Specify workflow and events.
    """

    name: str = prop()
    workflow: Workflow = prop()
    events: List[str] = prop(factory=list)


@propify
class WorkflowTrigger(Jsonable):
    name: str = prop()
    script: Script = prop(None, key="executer")
    triggers: List[Trigger] = prop(factory=list)
