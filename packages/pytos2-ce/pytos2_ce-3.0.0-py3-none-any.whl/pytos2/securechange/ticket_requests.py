from typing import List, Optional, Union
from enum import Enum
from datetime import datetime
from pytos2.models import Jsonable, UnMapped
from pytos2.utils import prop, propify, safe_iso8601_date


@propify
class RequestsSearchList(Jsonable):
    class Meta(Enum):
        ROOT = "requests"

    requests: List["RequestSearch"] = prop(factory=list)


@propify
class RequestSearch(Jsonable):
    class TicketType(Enum):
        TICKET = "TICKET"
        TICKET_DRAFT = "TICKET_DRAFT"

    class Prop(Enum):
        CREATE_DATE = "create_date"
        UPDATE_DATE = "update_date"

    id: Optional[int] = prop(None)
    type: Optional[TicketType] = prop(None, kwargify=str)  # TICKET or TICKET_DRAFT
    priority: Optional[str] = prop(None)
    create_date: Optional[datetime] = prop(
        None,
        key=Prop.CREATE_DATE.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
    update_date: Optional[datetime] = prop(
        None,
        key=Prop.UPDATE_DATE.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
    subject: Optional[str] = prop(None)
    requester: Optional["LocalUser"] = prop(None)
    domain: Optional["Domain"] = prop(None)


@propify
class TicketDraftRequestSearch(RequestSearch):
    ticket_draft_id: Optional[int] = prop(None)


@propify
class TicketRequestSearch(RequestSearch):
    from pytos2.securechange.saved_search import DetailedQueryFilters

    ticket_id: Optional[int] = prop(None)
    status: Optional[DetailedQueryFilters.TicketStatus] = prop(
        None, kwargify=str
    )  # Ticketstatus
    current_step: Optional["CurrentStage"] = prop(None)
    application_details: Optional["ApplicationDetails"] = prop(None)
    required_attentions: List["RequiredAttention"] = prop(factory=list)
    completion_ticket_details: Optional["CompletionTicketDetails"] = prop(None)


@propify
class Domain(Jsonable):
    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)


@propify
class AbstractUserRequest(Jsonable):
    class PartyType(Enum):
        LOCAL_USER = "LOCAL_USER"
        USER = "USER"

    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    type: Optional[PartyType] = prop(None, kwargify=str)  # PartyTypeDTO


@propify
class User(AbstractUserRequest):
    memberships: List["AbstractGroupSearch"] = prop(factory=list)


@propify
class LocalUser(User):
    first_name: Optional[str] = prop(None)
    last_name: Optional[str] = prop(None)
    user: Optional[str] = prop(None)


@propify
class AbstractGroupSearch(Jsonable):
    class PartyType(Enum):
        LOCAL_GROUP = "LOCAL_GROUP"
        GROUP = "GROUP"

    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    type: Optional[PartyType] = prop(None, kwargify=str)  # PartyTypeDTO
    memberships: List["AbstractGroupSearch"] = prop(factory=list)


@propify
class Group(AbstractGroupSearch):
    pass


@propify
class LocalGroup(Group):
    pass


@propify
class CurrentStage(Jsonable):
    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    order: Optional[int] = prop(None)
    tasks: List["TicketTask"] = prop(factory=list)


@propify
class TicketTask(Jsonable):
    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    status: Optional["TicketTaskStatus"] = prop(None)
    handler: Optional["PartySearch"] = prop(None)
    assigned_group: Optional["AbstractGroupSearch"] = prop(None)
    participants: List["PartySearch"] = prop(factory=list)
    unread_comments: Optional[bool] = prop(None)
    task_business_duration: Optional[str] = prop(None)


@propify
class TicketTaskStatus(Jsonable):
    reason: Optional[str] = prop(None)
    status: Optional[str] = prop(None)  # TaskStatusSearchEnumDTO


@propify
class PartySearch(Jsonable):
    class PartyType(Enum):
        LOCAL_USER = "LOCAL_USER"
        USER = "USER"
        LOCAL_GROUP = "LOCAL_GROUP"
        GROUP = "GROUP"

    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    type: Optional[PartyType] = prop(None, kwargify=str)  # PartyTypeDTO
    handler: Optional[LocalUser] = prop(None)
    memberships: List[AbstractGroupSearch] = prop(factory=list)
    first_name: Optional[str] = prop(None)
    last_name: Optional[str] = prop(None)
    user: Optional[str] = prop(None)


@propify
class ApplicationDetails(Jsonable):
    id: Optional[int] = prop(None)
    name: Optional[str] = prop(None)
    domain: Optional["Domain"] = prop(None)


@propify
class RequiredAttention(Jsonable):
    class RequiredAttentionType(Enum):
        MORE_INFORMATION = "MORE_INFORMATION"
        REJECTED = "REJECTED"
        CONFIRM = "CONFIRM"
        RESUBMIT = "RESUBMIT"
        EXPIRED = "EXPIRED"
        ABOUT_TO_EXPIRE = "ABOUT_TO_EXPIRE"

    type: Optional[RequiredAttentionType] = prop(
        None, kwargify=str
    )  # RequiredAttentionType


@propify
class CompletionTicketDetails(Jsonable):
    user: Optional["AbstractUserRequest"] = prop(None)
    last_active_step: Optional["CurrentStage"] = prop(None)
