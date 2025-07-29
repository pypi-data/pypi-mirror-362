from enum import Enum
from typing import Optional

from pytos2.utils import propify, prop
from pytos2.models import Jsonable


@propify
class Binding(Jsonable):
    class XsiType(Enum):
        POLICY_BINDING = "policy__binding"

    xsi_type: XsiType = prop(XsiType.POLICY_BINDING, key=Jsonable.Prop.XSI_TYPE.value)

    policy_name: Optional[str] = prop(None)
    installed_on_module: Optional[str] = prop(None)
