from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Type, Iterator
from typing_extensions import Literal
from time import sleep

# from requests import Response
# from requests.exceptions import HTTPError
# import attr

# from traversify import Traverser

# avoid circular imports
import pytos2  # noqa
from pytos2.utils import (
    propify,
    kwargify,
    prop,
    jsonify,
    safe_date,
    safe_iso8601_date,
    get_api_node,
    TimeFormat,
    safe_unwrap_msg,
)

from pytos2.models import Jsonable, UnMapped


@propify
class Query(Jsonable):

    class Meta(Enum):
        ROOT = "query"

    class Prop(Enum):
        LAST_USED = "lastUsed"
        CREATE_DATE = "createDate"
        UPDATE_DATE = "updateDate"

    type: str = prop(None)
    name: str = prop(None)
    description: Optional[str] = prop(None)
    last_used: Optional[datetime] = prop(
        None,
        key=Prop.LAST_USED.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
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


@propify
class ExpirationFilter(Jsonable):

    class Meta(Enum):
        ROOT = "expiration"

    class Prop(Enum):
        FROM_DATE = "fromDate"
        TO_DATE = "toDate"

    from_date: Optional[datetime] = prop(
        None,
        key=Prop.FROM_DATE.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
    to_date: Optional[datetime] = prop(
        None,
        key=Prop.TO_DATE.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )


@propify
class FieldFilter(Jsonable):

    class Meta(Enum):
        ROOT = "field"

    name: Optional[str] = prop(None)
    value: Optional[str] = prop(None)


@propify
class DetailedQueryFilters(Jsonable):

    class Meta(Enum):
        ROOT = "filters"

    class Priority(Enum):
        CRITICAL = "Critical"
        HIGH = "High"
        NORMAL = "Normal"
        LOW = "Low"

    class TicketStatus(Enum):
        IN_PROGRESS = "IN_PROGRESS"
        REJECTED = "REJECTED"
        CLOSED = "CLOSED"
        CANCELLED = "CANCELLED"
        RESOLVED = "RESOLVED"

    class SlaStatus(Enum):
        OK = "OK"
        WARNING = "WARNING"
        ALERT = "ALERT"
        ESCALATION = "ESCALATION"
        NA = "NA"

    class SlaOutcome(Enum):
        UNKNOWN = "UNKNOWN"
        MET = "MET"
        OVERDUE = "OVERDUE"
        NA = "NA"

    class TaskStatus(Enum):
        WAITING_TO_BE_ASSIGNED = "WAITING_TO_BE_ASSIGNED"
        ASSIGNED = "ASSIGNED"
        WAITING_FOR_MORE_INFO = "WAITING_FOR_MORE_INFO"
        DONE = "DONE"
        INVALID = "INVALID"
        PENDING = "PENDING"
        PENDING_LICENSE = "PENDING_LICENSE"

    class Prop(Enum):
        DOMAIN_ID = "domainIds"
        TASK_STATUS = "taskStatuses"
        TICKET_STATUS = "ticketStatuses"
        SLA_STATUS = "slaStatuses"
        SLA_OUTCOME = "slaOutcomes"
        ASSIGNED_TO = "assignedTo"
        CURRENT_STEP_NAME = "currentStepName"

    #    def __post_init__(self):
    #        from pytos2.securechange.ticket import Ticket  # Local import to avoid circular dependency
    #        self.priorities: List[Ticket.Priority] = prop(factory=list)
    #        self.slaStatuses: List[Ticket.SlaStatus] = prop(factory=list, kwargify=str)

    #    from pytos2.securechange.ticket import Ticket
    #    priorities: List[Ticket.Priority] = prop(factory=list, kwargify=str)

    expiration: Optional[ExpirationFilter] = prop(None)
    domain_id: List[int] = prop(factory=list, key=Prop.DOMAIN_ID.value)
    group: Optional[str] = prop(None)
    ticket_id: Optional[int] = prop(None)
    priorities: List[Priority] = prop(factory=list, kwargify=str)
    subject: Optional[str] = prop(None)
    current_step_name: Optional[str] = prop(None, key=Prop.CURRENT_STEP_NAME.value)
    ticket_statuses: List[TicketStatus] = prop(
        factory=list, key=Prop.TICKET_STATUS.value, kwargify=str
    )
    task_status: List[TaskStatus] = prop(
        factory=list, key=Prop.TASK_STATUS.value, kwargify=str
    )
    sla_status: List[SlaStatus] = prop(
        factory=list, key=Prop.SLA_STATUS.value, kwargify=str
    )
    sla_outcome: List[SlaOutcome] = prop(
        factory=list, key=Prop.SLA_OUTCOME.value, kwargify=str
    )
    requester: Optional[str] = prop(None)
    assigned_to: Optional[str] = prop(None, key=Prop.ASSIGNED_TO.value)
    field: Optional[FieldFilter] = prop(None)


@propify
class FreeTextQuery(Query):

    class Meta(Enum):
        ROOT = "freeTextQuery"

    class QueryType(Enum):
        FREE_TEXT = "FREE_TEXT"

    class Prop(Enum):
        LAST_USED = "lastUsed"
        CREATE_DATE = "createDate"
        UPDATE_DATE = "updateDate"
        SEARCH_TEXT = "searchText"

    description: Optional[str] = prop(None)
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
    search_text: str = prop(None, key=Prop.SEARCH_TEXT.value)
    last_used: Optional[datetime] = prop(
        None,
        key=Prop.LAST_USED.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
    name: str = prop(None)
    id: Optional[int] = prop(None)
    type: Optional[QueryType] = prop(None, kwargify=str)


@propify
class DetailedQuery(Query):

    class Meta(Enum):
        ROOT = "detailedQuery"

    class QueryType(Enum):
        DETAILED = "DETAILED"

    class Prop(Enum):
        LAST_USED = "lastUsed"
        CREATE_DATE = "createDate"
        UPDATE_DATE = "updateDate"

    description: Optional[str] = prop(None)
    filters: DetailedQueryFilters = prop(None)
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
    last_used: Optional[datetime] = prop(
        None,
        key=Prop.LAST_USED.value,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat(timespec="milliseconds") if d else None,
        repr=lambda v: v.isoformat(timespec="milliseconds") if v else "None",
    )
    name: str = prop(None)
    id: Optional[int] = prop(None)
    type: Optional[QueryType] = prop(None, kwargify=str)
