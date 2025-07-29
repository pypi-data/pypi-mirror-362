from enum import Enum
from typing import Optional

from netaddr import IPAddress
from attr.converters import optional
from pytos2.utils import prop, propify, stringify_optional_obj
from pytos2.models import Jsonable


@propify
class ApplicationAccessRequest(Jsonable):
    class Meta(Enum):
        ROOT = "application_access_request"

    class Action(str, Enum):
        APPROVE = "APPROVE"
        REJECT = "REJECT"
        OPENED = "OPENED"
        DENIED = "DENIED"
        WAITING_TICKET = "WAITING_TICKET"
        IN_TICKET = "IN_TICKET"
        CONFIRMED = "CONFIRMED"
        IMMEDIATE_CONFIRM = "IMMEDIATE_CONFIRM"
        IMMEDIATE_DENIED = "IMMEDIATE_DENIED"

    comment: Optional[str] = prop(None)

    action: Optional[Action] = prop(None)
    server_ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    server_group_id: Optional[int | str] = prop(None)
    server_group_name: Optional[str] = prop(None)
