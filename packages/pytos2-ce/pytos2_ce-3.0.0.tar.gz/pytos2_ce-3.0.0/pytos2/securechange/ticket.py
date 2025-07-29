from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Type, Iterator
from typing_extensions import Literal
from time import sleep

from requests import Response
from requests.exceptions import HTTPError
import attr

from traversify import Traverser

# avoid circular imports
import pytos2  # noqa
from pytos2.securechange.entrypoint import Scw
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

from .fields import (
    Link,
    classify_field,
    get_field_class,
    Field,
    MultiGroupChange,
    MultiAccessRequest,
    FieldXsiType,
    FieldType,
)

from .user import NotificationGroup, SCWGroup, SCWUser

from pytos2.models import Jsonable, ObjectReference, UnMapped


@propify
class Workflow(Jsonable):
    class Meta(Enum):
        ROOT = "workflow"

    class Prop(Enum):
        ID = "id"
        NAME = "name"
        USES_TOPOLOGY = "uses_topology"

    name: Optional[str] = prop(None)
    uses_topology: Optional[bool] = prop(None, jsonify=False)
    id: Optional[int] = prop(None, cmp=False, jsonify=False)


@propify
class ApplicationDetails(Jsonable):
    class Meta(Enum):
        ROOT = "application_details"

    class Prop(Enum):
        ID = "id"
        NAME = "name"
        DISPLAY_NAME = "display_name"
        LINK = "link"

    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)
    link: Optional[Link] = prop(None, repr=False)


@propify
class Task(Jsonable):
    class Meta(Enum):
        ROOT = "task"

    class Prop(Enum):
        ID = "id"
        NAME = "name"
        STATUS = "status"
        ASSIGNEE = "assignee"
        ASSIGNEE_ID = "assignee_id"
        PENDING_REASON = "pending_reason"
        PENDING_REASON_DESCRIPTION = "pending_reason_description"
        FIELDS = "fields"

    class Status(Enum):
        WAITING_TO_BE_ASSIGNED = "WAITING_TO_BE_ASSIGNED"
        ASSIGNED = "ASSIGNED"
        WAITING_FOR_MORE_INFO = "WAITING_FOR_MORE_INFO"
        DONE = "DONE"
        INVALID = "INVALID"
        PENDING = "PENDING"
        PENDING_LICENSE = "PENDING_LICENSE"

    fields: List[FieldType] = prop(
        factory=list, repr=False, flatify=Field.Meta.ROOT.value, kwargify=classify_field
    )
    id: Optional[int] = prop(None, cmp=False)
    name: Optional[str] = prop(None, repr=False)
    status: Optional[Status] = prop(None)
    assignee: Optional[str] = prop(None, jsonify=False)
    assignee_id: Optional[str] = prop(None, repr=False, jsonify=False)
    pending_reason: Optional[str] = prop(None, repr=False, jsonify=False)
    pending_reason_description: Optional[str] = prop(None, repr=False, jsonify=False)

    def _get_fields(self, *types: Type[Field]) -> List[FieldType]:
        return [f for f in self.fields if isinstance(f, types)]

    def create_field(self, name: str, field_type: Union[Type[Field], FieldXsiType]):
        if isinstance(field_type, FieldXsiType):
            cls = get_field_class(field_type.value)
        else:
            cls = field_type

        field = cls.kwargify({"name": name})

        self.fields.append(field)
        return field

    def get_field(
        self, name: Optional[str] = None, *types: Type[Field]
    ) -> Optional[FieldType]:
        field = None
        for field in self.fields:
            field_name = getattr(field, "name", None) or field._json.get("name")
            if field_name == name:
                if types:
                    if isinstance(field, types):
                        return field
                else:
                    return field
            if name is None:
                if isinstance(field, types):
                    return field
        return None

    @property
    def group_modify(self) -> Optional[MultiGroupChange]:
        return self.get_field(None, MultiGroupChange)  # type: ignore

    @property
    def access_request(self) -> Optional[MultiAccessRequest]:
        return self.get_field(None, MultiAccessRequest)  # type: ignore

    def done(self) -> None:
        self.status = self.Status.DONE

    @property
    def is_done(self) -> bool:
        return self.status is self.Status.DONE

    @property
    def _dirty(self) -> bool:
        return (
            False
            if not self.status
            else True if not self.data else self.status.value != self.data.get("status")
        )

    @property
    def _dirty_fields(self) -> List:
        return [
            f
            for f in self.fields
            if isinstance(f, UnMapped) or (not f.read_only and f._dirty)
        ]

    @property
    def _json(self) -> dict:
        if self._json_override is not None:
            return self._json_override  # pragma: no cover
        j = jsonify(self)
        if not self.fields:
            j["fields"] = {}
        return j


@propify
class Step(Jsonable):
    class Meta(Enum):
        ROOT = "step"

    class Prop(Enum):
        ID = "id"
        NAME = "name"
        REDONE = "redone"
        SKIPPED = "skipped"
        TASKS = "tasks"

    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    name: Optional[str] = prop(None)
    redone: Optional[bool] = prop(None, jsonify=False)
    skipped: Optional[bool] = prop(None, jsonify=False)
    tasks: List[Task] = prop(factory=list, repr=False, flatify=Task.Meta.ROOT.value)

    def get_task(self, identifier):
        task = None
        if isinstance(identifier, int):
            try:
                task = self.tasks[identifier]
            except IndexError:
                return None
        else:
            for task in self.tasks:
                if task.name == identifier:
                    break
            else:
                return None
        return task

    def get_task_fields(self, identifier, *types: Type[Field]):
        task = self.get_task(identifier)
        return task._get_fields(*types)

    def create_task(self):
        task = Task()
        self.tasks.append(task)
        return task

    @property
    def last_task(self) -> Task:
        return self.get_task(-1)

    def done(self):
        for task in self.tasks:
            task.done()

    @property
    def is_done(self):
        return all(task.is_done for task in self.tasks)


@propify
class CurrentStep(Jsonable):
    class Meta(Enum):
        ROOT = "current_step"

    class Prop(Enum):
        ID = "id"
        NAME = "name"

    name: Optional[str] = prop(None)
    id: Optional[int] = prop(None, cmp=False, jsonify=False)


class TicketStatus(Enum):
    ALL = "__ALL__"
    CLOSED = "Ticket Closed"
    CANCELLED = "Ticket Cancelled"
    REJECTED = "Ticket Rejected"
    RESOLVED = "Ticket Resolved"
    INPROGRESS = "In Progress"


@propify
class Attachment(Jsonable):
    uid: str
    name: str
    link: str = prop(None, flatify="@href")


@propify
class Comment(Jsonable):
    class Prop(Enum):
        USERS = "user"
        ATTACHMENT = "attachment"

    class CommentType(Enum):
        COMMENT = "comment"

    content: Optional[str] = prop(None)
    created: Optional[datetime] = prop(None, kwargify=safe_iso8601_date)
    task_name: Optional[str] = prop(None)
    commentType: Optional[CommentType] = prop(None)
    users: List[str] = prop(None, key=Prop.USERS.value)
    attachments: List[Attachment] = prop(
        None, jsonify=False, flatify=Prop.ATTACHMENT.value
    )


@propify
class TicketHistoryEntry(Jsonable):
    id: Optional[int] = prop(None, repr=False)

    date: Optional[datetime] = prop(
        None,
        kwargify=safe_iso8601_date,
        jsonify=lambda d: d.isoformat() if d else None,
        repr=lambda v: v.isoformat() if v else "None",
    )

    performed_by: Optional[str] = prop(None)
    description: Optional[str] = prop(None)
    step_name: Optional[str] = prop(None)
    task_name: Optional[str] = prop(None)


@propify
class PushCommandResult(Jsonable):
    class Status(Enum):
        SUCCEEDED = "SUCCEEDED"

    status: Optional[Status] = prop(None)
    order: int = prop()
    command: Optional[str] = prop(None)
    failure_reason: Optional[str] = prop(None)


@propify
class DesignerUpdateDeviceHistory(TicketHistoryEntry):
    vendor_name: Optional[str] = prop(None)
    device_name: Optional[str] = prop(None)

    push_command_results: List[PushCommandResult] = prop(
        flatify="push_command_result", factory=list, repr=False
    )


def get_ticket_history_entry_class(obj):
    if "@xsi.type" in obj:
        return {"designerUpdateDeviceHistoryDTO": DesignerUpdateDeviceHistory}.get(
            obj["@xsi.type"], TicketHistoryEntry
        )
    else:
        return TicketHistoryEntry


def classify_ticket_history_entry(obj):
    return get_ticket_history_entry_class(obj).kwargify(obj)


def _summarize_history_activity(v):
    if isinstance(v, list):
        return f"[... list with {len(v)} entries ...]"
    return repr(v)


@propify
class TicketHistory(Jsonable):
    ticket_id: int = prop()
    ticket_history_activity: List[TicketHistoryEntry] = prop(
        factory=list,
        kwargify=classify_ticket_history_entry,
        repr=_summarize_history_activity,
    )


@propify
class Ticket(Jsonable):
    """
    This class represents a SecureChange ticket object.
    """

    class Meta(Enum):
        ROOT = "ticket"

    class Priority(Enum):
        CRITICAL = "Critical"
        HIGH = "High"
        NORMAL = "Normal"
        LOW = "Low"

    class SlaStatus(Enum):
        OK = "OK"
        WARNING = "Warning"
        ALERT = "Alert"
        ESCALATION = "Escalation"
        NA = "NA"

    class SlaOutcome(Enum):
        UNKNOWN = "unknown"
        MET = "met"
        OVERDUE = "overdue"
        NA = "NA"

    class Prop(Enum):
        SUBJECT = "subject"
        ID = "id"
        PRIORITY = "priority"
        STATUS = "status"
        DOMAIN_NAME = "domain_name"
        SLA_STATUS = "sla_status"
        SLA_OUTCOME = "sla_outcome"
        COMMENTS = "comment"
        REQUESTER = "requester"
        REQUESTER_ID = "requester_id"
        STEPS = "steps"
        CURRENT_STEP = "current_step"
        WORKFLOW = "workflow"
        APPLICATION_DETAILS = "application_details"
        EXPIRATION_DATE = "expiration_date"
        EXPIRATION_FIELD_NAME = "expiration_field_name"

    subject: Optional[str] = prop("No Subject")
    id: Optional[int] = prop(None, cmp=False, jsonify=False)
    workflow: Optional[Workflow] = prop(None, repr=False)
    steps: List[Step] = prop(factory=list, repr=False, flatify=Step.Meta.ROOT.value)
    status: Optional[TicketStatus] = prop(None, jsonify=False)
    domain_name: Optional[str] = prop(None, repr=False)
    sla_status: Optional[SlaStatus] = prop(None, repr=False, jsonify=False)
    sla_outcome: Optional[SlaOutcome] = prop(None, repr=False, jsonify=False)
    expiration_field_name: Optional[str] = prop(None, repr=False, jsonify=False)
    comments: List[Comment] = prop(None, jsonify=False, flatify=Prop.COMMENTS.value)
    _current_step: Optional[Step] = None
    requester: Optional[str] = prop(None, repr=False, jsonify=False)
    requester_id: Optional[int] = prop(None, repr=False)
    expiration_date: Optional[datetime] = prop(
        None,
        repr=False,
        jsonify=False,
        kwargify=lambda val: safe_date(val, TimeFormat.DATE),
    )
    application_details: Optional[ApplicationDetails] = prop(
        None, repr=False, jsonify=False
    )
    priority: Optional[Priority] = prop(Priority.NORMAL, repr=False)
    referenced_ticket: Optional[ObjectReference] = prop(None, repr=False)
    notification_group: Optional[NotificationGroup] = prop(None, repr=False)

    data: Optional[dict] = attr.ib(None, repr=False)
    _json_override: dict = attr.ib(None, repr=False, eq=False, init=False)

    @classmethod
    def create(cls, workflow: str, subject: Optional[str] = None):
        ticket = cls(subject=subject)
        ticket.workflow = Workflow(name=workflow)

        return ticket

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        inst = cls(**kwargs)
        inst.current_step = _obj.get("current_step")
        return inst

    @property
    def current_step_name(self) -> Optional[str]:
        if self.current_step:
            return self.current_step.name
        return None

    @property
    def _json(self) -> dict:
        return (
            self._json_override
            if self._json_override is not None
            else {self.Meta.ROOT.value: jsonify(self)}
        )

    @_json.setter
    def _json(self, val) -> None:
        self._json_override = val

    @property
    def current_step_index(self) -> Optional[int]:
        if not self._current_step:
            return None

        for idx, s in enumerate(self.steps):
            if s.id == self._current_step.id:
                return idx

    @property
    def previous_step(self) -> Optional[Step]:
        current_step_idx = self.current_step_index
        if current_step_idx is None or current_step_idx == 0:
            return None
        else:
            return self.steps[current_step_idx - 1]

    @property
    def current_step(self) -> Optional[Step]:
        return self._current_step

    @current_step.setter
    def current_step(self, step):
        if isinstance(step, dict):
            # extract the current_step name from the API output
            step = step.get("name")
        current_step = self.get_step(step)
        if current_step:
            self._current_step = current_step

    def create_step(self, name) -> Step:
        step = Step(name=name)
        self.steps.append(step)
        return step

    def get_step(self, identifier: Union[int, str]) -> Optional[Step]:
        step = None
        if isinstance(identifier, int):
            try:
                step = self.steps[identifier]
            except IndexError:
                return None
        else:
            for step in self.steps:
                if step.name == identifier:
                    break
            else:
                return None
        return step

    def _get_step(self, step_id: int) -> Optional[Step]:
        step = [s for s in self.steps if s.id == step_id]
        return step[0] if step else None

    def get_step_task(
        self, identifier: Union[int, str], task: Union[int, str] = 0
    ) -> Optional[Task]:
        step = self.get_step(identifier)
        return step.get_task(task) if step else None

    def get_step_task_fields(
        self,
        identifier: Union[int, str],
        task: Union[int, str] = -1,
        *types: Type[Field],
    ) -> Optional[list]:
        _task = self.get_step_task(identifier, task)
        if _task:
            return _task._get_fields(*types)
        return None

    @property
    def last_step(self) -> Step:
        return self.steps[-1]

    @property
    def last_task(self) -> Task:
        return self.last_step.last_task

    @property
    def current_task(self) -> Optional[Task]:
        if self.current_step:
            if len(self.current_step.tasks) > 1:
                raise ValueError(
                    "Ticket.current_task cannot be used when the current step has more than one task, use Ticket.current_tasks instead"
                )
        return self.current_step.last_task if self.current_step else None

    @property
    def current_tasks(self) -> List[Task]:
        return self.current_step.tasks if self.current_step else []

    @property
    def post_json(self) -> dict:
        _self = deepcopy(self)
        _self.steps = [self.steps[0]]
        return _self._json

    @property
    def group_modify(self) -> Optional[MultiGroupChange]:
        if self.current_task:
            return self.current_task.group_modify
        return None

    @property
    def access_request(self) -> Optional[MultiAccessRequest]:
        if self.current_task:
            return self.current_task.access_request
        return None

    @property
    def ar(self) -> Optional[MultiAccessRequest]:
        return self.access_request

    def add_comment(
        self,
        comment: str,
        attachment_uuids: List[str] = None,
        step_id: Union[int, str] = None,
        task_id: Union[int, str] = None,
    ) -> str:
        if step_id is None:
            step_id = self.current_step.id

        if task_id is None:
            task_id = self.current_task.id
        return Scw.add_comment(
            Scw.default, self.id, step_id, task_id, comment, attachment_uuids
        )

    def add_comments(
        self,
        comments: List[Comment],
        step_id: Union[int, str] = None,
        task_id: Union[int, str] = None,
    ) -> List[str]:
        return [
            self.add_comment(
                comment.content,
                [a.uid for a in comment.attachments] if comment.attachments else None,
                step_id,
                task_id,
            )
            for comment in comments
        ]

    def delete_comment(
        self,
        comment_id: Union[int, str] = None,
    ):
        Scw.delete_comment(Scw.default, self.id, comment_id)

    def delete_comments(
        self,
        comment_ids: List[Union[int, str]],
    ):
        for id in comment_ids:
            self.delete_comment(id)

    def get_history(self):
        return Scw.get_ticket_history(Scw.default, self.id)

    def post(self) -> "Ticket":
        res = Scw.default.api.session.post("tickets", json=self.post_json)
        Scw.default.api.handle_response(
            r=res, fn_name="post", action="create", resource="ticket"
        )
        created_url = res.headers.get("Location", "")
        tid: str = created_url.split("/")[-1]
        return Scw.default.get_ticket(int(tid))

    def advance(
        self, save: bool = True, silence: Optional[bool] = False
    ) -> Union["Ticket", bool]:
        if self.current_step:
            self.current_step.done()
            if not silence:
                return self.save()  # type: ignore
            else:
                self.save(silence=True)
        else:
            raise AssertionError(
                f"Ticket is currently {self.status}, and cannot be modified"
            )

    def reject(
        self,
        handler_id: Optional[int] = None,
        comment: Optional[str] = "",
    ) -> "Ticket":
        if not self.id:
            raise ValueError("You cannot reject a ticket with no id")
        r = Scw.default.api.reject_ticket(
            self.id, comment=comment, handler_id=handler_id
        )
        if not r.ok:
            try:
                response_body = r.json()
                r.raise_for_status()
            except HTTPError as e:
                msg = response_body.get("result").get("message")
                raise HTTPError(f"Got msg: {msg} from error :{e}")
            except ValueError as e:
                raise ValueError(e)

        else:
            return Scw.default.get_ticket(self.id)

    def cancel(
        self,
        requestor_id: Optional[int] = None,
    ) -> "Ticket":
        r = Scw.default.api.cancel_ticket(self.id, requestor_id=requestor_id)
        if not r.ok:
            msg = safe_unwrap_msg(r)
            raise ValueError(f"Got error: {msg} with status code {r.status_code}")
        return Scw.default.get_ticket(self.id)

    def confirm(
        self,
        requestor_id: Optional[int] = None,
        comment: Optional[str] = "",
    ) -> "Ticket":
        r = Scw.default.api.confirm_ticket(
            self.id, comment=comment, requestor_id=requestor_id
        )
        if not r.ok:
            msg = safe_unwrap_msg(r)
            raise ValueError(f"Got error: {msg} with status code {r.status_code}")
        return Scw.default.get_ticket(self.id)

    def save(
        self, force: Optional[bool] = False, silence: Optional[bool] = False
    ) -> "Ticket":
        if not self.current_step:
            raise AssertionError(
                f"Ticket status is {self.status}, and cannot be modified"
            )
        if not self.id:
            raise AssertionError("Cannot save new Ticket, use Ticket.post() instead")
        for task in self.current_step.tasks:
            res = None
            if not task.id:
                continue
            if force:
                res = Scw.default.api.put_task(self.id, task.id, task._json)
            elif task._dirty:
                res = Scw.default.api.put_task(self.id, task.id, save_task_body(task))
            elif task._dirty_fields:
                res = Scw.default.api.put_fields(
                    self.id, task.id, save_fields_body(task)
                )

            if res is not None and not res.ok:
                try:
                    res.raise_for_status()
                except HTTPError as e:
                    msg = safe_unwrap_msg(res)
                    raise ValueError(
                        f"Status: '{res.status_code}' Message: '{msg}' from API.  Exception: {e}"
                    )
        if not silence:
            return Scw.default.get_ticket(self.id)

    def change_requester(
        self,
        user: Union[SCWUser, int, str],
        comment: str = "",
    ) -> None:
        return Scw.default.change_requester(self, user=user, comment=comment)

    def reassign(
        self,
        user: Union[SCWUser, int, str],
        step: Union[None, Step, int, str] = None,
        task: Union[None, Task, int] = None,
        comment: str = "",
    ) -> None:
        return Scw.default.reassign_ticket(
            self, user=user, step=step, task=task, comment=comment
        )

    def redo(self, step: Union[Step, int, str], comment: str = "") -> "Ticket":
        if len(self.steps) < 2:
            raise AssertionError("Cannot redo a ticket on the first step")
        if not self.current_step:
            raise AssertionError(f"Cannot redo ticket with status {self.status}")
        if not isinstance(step, Step):
            _step = self.get_step(step)
            if not _step:
                raise IndexError(f"Step {step} not found")
            step = _step
        if not step.id:
            raise AssertionError(f"Step {step.name} has no id")
        if step == self.current_step:
            raise AssertionError(f"Cannot redo to current step {step.name}")
        if not self.id:
            raise AssertionError("Cannot redo ticket with no id")
        if not self.current_step.id:
            raise AssertionError("Cannot redo ticket at step with no id")
        if not self.current_step.last_task.id:
            raise AssertionError("Cannot redo ticket at task with no id")
        r = Scw.default.api.redo_step(
            self.id,
            self.current_step.id,
            self.current_step.last_task.id,
            step.id,
            comment,
        )
        if r.ok:
            ticket = Scw.default.get_ticket(self.id)
            count = 0
            while ticket.current_step.id != step.id:  # type: ignore
                count += 1
                if count > 20:  # pragma: no cover
                    raise TimeoutError("Timed out getting ticket after redo")
                sleep(0.5)
                ticket = Scw.default.get_ticket(self.id)

            return ticket

        else:
            r.raise_for_status()

    def map_rules(
        self,
        handler_id: int = None,
    ) -> None:
        Scw.default.map_rules(self.id, handler_id)

    def designer_redesign(self) -> None:
        Scw.default.designer_redesign(
            self.id,
            self.current_step.id,
            self.current_task.id,
            self.current_task.access_request.id,
        )

    def designer_device_commit(self, device_id) -> None:
        Scw.default.designer_device_commit(
            self.id,
            self.current_step.id,
            self.current_task.id,
            self.current_task.access_request.id,
            device_id,
        )

    def designer_device_update(self, device_id) -> None:
        Scw.default.designer_device_update(
            self.id,
            self.current_step.id,
            self.current_task.id,
            self.current_task.access_request.id,
            device_id,
        )


def save_task_body(task: Task) -> dict:
    put_task = deepcopy(task)
    put_task.fields = put_task._dirty_fields

    return {Task.Meta.ROOT.value: put_task._json}


def save_fields_body(task: Task) -> dict:
    put_task = deepcopy(task)
    put_task.fields = put_task._dirty_fields
    _json = put_task._json
    return {Task.Prop.FIELDS.value: _json[Task.Prop.FIELDS.value]}


class TicketIterator(Iterator):
    def __init__(self, session, params):
        self.params = params
        self.data = None
        self.data_index = 0
        self.next_page_link = None
        self.reached_last_page = False
        self.has_error_occurred = False

        self.session = session

    def __iter__(self):
        return self

    def fetch(self):
        if self.next_page_link is not None:
            response = self.session.get(self.next_page_link)
            if response.ok:
                self.has_error_occurred = False
                self.process_response(response)
            else:
                response.raise_for_status()
        elif self.reached_last_page:
            self.data = None
        else:
            response = self.session.get("tickets", params=self.params)

            if response.ok:
                self.has_error_occurred = False
                self.process_response(response)
            else:
                response.raise_for_status()

        self.data_index = 0
        return True

    def process_response(self, response):
        _json = Traverser(response.json())

        self.next_page_link = _json.tickets.get("next", {"@href": None})["@href"]
        data = get_api_node(_json(), "tickets.ticket", listify=True)
        self.data = [Ticket.kwargify(ticket) for ticket in data]
        self.reached_last_page = self.next_page_link is None

    def __next__(self):
        if self.has_error_occurred:
            raise StopIteration

        if self.data is None:
            res = self.fetch()
            if not res:
                self.data = None
                self.has_error_occurred = True
                return res
        elif self.data_index >= len(self.data):
            if self.next_page_link:
                res = self.fetch()

                if not res:
                    self.data = None
                    self.has_error_occurred = True
                    return res
            else:
                raise StopIteration

        if not self.data:
            raise StopIteration

        ret = self.data[self.data_index]
        self.data_index += 1
        return ret


@propify
class CurrentTicketTask(Jsonable):
    id: int = prop(0)
    name: str = prop(None)
    participants: List[dict] = prop(factory=list, flatify="participant")
    status: Optional[dict] = prop(None)


@propify
class CurrentTicketStage(Jsonable):
    id: int = prop(0)
    tasks: List[CurrentTicketTask] = prop(factory=list, flatify="task")


@propify
class TicketSearchResult(Jsonable):
    """
    This class represents a SecureChange ticket search result object returned by tickets/search_by/details
    """

    class Prop(Enum):
        REQUESTER_NAME = "requesterName"
        WORKFLOW_NAME = "workflowName"
        ASSIGNED_TO_NAME = "assignedToName"
        DOMAIN_NAME = "domainName"

    current_step: Optional[str] = prop(None)
    sla_status: Optional[Ticket.SlaStatus] = prop(None)
    requester_name: Optional[str] = prop(None, key=Prop.REQUESTER_NAME.value)
    workflow_name: Optional[str] = prop(None, key=Prop.WORKFLOW_NAME.value)
    assigned_to_name: Optional[str] = prop(None, key=Prop.ASSIGNED_TO_NAME.value)
    domain_name: Optional[str] = prop(None, key=Prop.DOMAIN_NAME.value)
    duration: Optional[int] = prop(None)
    subject: Optional[str] = prop(None)
    status: Optional[TicketStatus] = prop(None)
    priority: Optional[Ticket.Priority] = prop(None)
    id: int = prop(0)

    current_stage: Optional[CurrentTicketStage] = prop(None)

    @property
    def task_status(self) -> Optional[Task.Status]:
        if self.current_stage and self.current_stage.tasks:
            status = self.current_stage.tasks[0].status.get("status", None)
            if status:
                return Task.Status(status)
        return None

    def get_full_ticket(self) -> Ticket:
        return Scw.default.get_ticket(self.id)


# @propify
# class TicketSearchByFreeText(Jsonable):
#     """
#     This class represents a SecureChange ticket search result object returned by tickets/search_by/free_text
#     """

#     class Prop(Enum):
#         workflow_name = "workflowName"
#         domain_name = "domainName"
#         assigned_group = "assignedGroup"


#     assigned_group: Optional[str] = prop(None, key=Prop.assigned_group.value)
#     current_step: Optional[str] = prop(None)
#     sla_status: Optional[Ticket.SlaStatus] = prop(None)
#     requester_name: Optional[str] = prop(None, key=Prop.REQUESTER_NAME.value)
#     workflow_name: Optional[str] = prop(None, key=Prop.workflow_name.value)
#     assigned_to_name: Optional[str] = prop(None, key=Prop.ASSIGNED_TO_NAME.value)
#     domain_name: Optional[str] = prop(None, key=Prop.domain_name.value)
#     duration: Optional[int] = prop(None)
#     subject: Optional[str] = prop(None)
#     status: Optional[TicketStatus] = prop(None)
#     priority: Optional[Ticket.Priority] = prop(None)
#     id: int = prop(0)

#     task_status: Optional[Task.Status] = prop(None)


@propify
class TicketEventParticipant(Jsonable):
    participant_id: int = prop(0)
    participant_name: str = prop(None)


@propify
class TicketEventTaskAssignedData(Jsonable):
    assignee_id: int = prop(0)
    assignee_name: str = prop(None)
    participant_id: int = prop(0)
    participant_name: str = prop(None)


@propify
class TicketEvent(Jsonable):
    """
    This class represents a SecureChange ticket event object returned by tickets/lifecycle_events
    """

    ticket_id: int = prop(0)
    workflow_name: str = prop(None)
    domain_id: int = prop(0)
    parent_workflow_id: int = prop(0)
    timestamp: datetime = prop(None, kwargify=safe_iso8601_date)
    type: str = prop(None)
    step_id: Optional[int] = prop(None)
    step_name: Optional[str] = prop(None)
    task_id: Optional[int] = prop(None)
    task_name: Optional[str] = prop(None)
    potential_participants: List[TicketEventParticipant] = prop(factory=list)
    task_assigned_data: TicketEventTaskAssignedData = prop(None)
