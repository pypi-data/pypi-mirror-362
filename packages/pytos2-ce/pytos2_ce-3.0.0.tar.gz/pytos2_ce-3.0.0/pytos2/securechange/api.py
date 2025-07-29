from enum import Enum
from typing import Optional

from pytos2.api import BaseAPI, get_app_api_session, boolify
from pytos2.utils import setup_logger

from requests import Response


LOGGER = setup_logger("scw_api")


class ScwAPI(BaseAPI):
    class Meta(Enum):
        PATH = "securechangeworkflow/api/securechange"
        APP = "SCW"
        TOS2_ENV = "SC_SERVER_SERVICE"

    def __init__(
        self, hostname: Optional[str], username: Optional[str], password: Optional[str]
    ):
        self.hostname, self.username, self.password, self.session = get_app_api_session(
            app=self, hostname=hostname, username=username, password=password
        )

    def get_workflow(
        self, _id: Optional[int] = None, name: Optional[str] = None
    ) -> Response:
        if _id and name:
            raise TypeError(
                "Either '_id' or 'name' can be passed as arguments, but not both."
            )
        params = boolify({"id": _id, "name": name})

        r = self.session.get("workflows", params=params)
        return r

    def redo_step(
        self,
        ticket_id: int,
        step_id: int,
        task_id: int,
        to_step_id: int,
        comment: str = "",
    ) -> Response:
        if not comment:
            comment = "Reassigned by script"

        body = {"redo_step_comment": {"comment": comment}}
        r = self.session.put(
            f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/redo/{to_step_id}",
            json=body,
        )
        return r

    def reassign_task(
        self,
        ticket_id: int,
        step_id: int,
        task_id: int,
        assignee_id: int,
        comment: str = "",
    ) -> Response:
        if not comment:
            comment = "Reassigned by script"

        body = {"reassign_task_comment": {"comment": comment}}
        r = self.session.put(
            f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/reassign/{assignee_id}",
            json=body,
        )
        return r

    def put_task(self, ticket_id: int, task_id: int, task: dict) -> Response:
        """This function intentionally doesn't have a step_id argument, because you can only put tasks at the current step"""
        r = self.session.put(
            f"tickets/{ticket_id}/steps/current/tasks/{task_id}", json=task
        )
        return r

    def reject_ticket(
        self,
        ticket_id: int,
        handler_id: Optional[int] = None,
        comment: Optional[str] = "",
    ) -> Response:
        params = {} if handler_id is None else {"handler_id": handler_id}
        comment = "None provided" if not comment else comment
        body = {"reject_comment": {"comment": comment}}
        r = self.session.put(f"tickets/{ticket_id}/reject", params=params, json=body)
        return r

    def put_field(
        self, ticket_id: int, task_id: int, field_id: int, field: dict
    ) -> Response:
        """This function intentionally doesn't have a step_id argument, because you can only put tasks at the current step"""
        r = self.session.put(
            f"tickets/{ticket_id}/steps/current/tasks/{task_id}/fields/{field_id}",
            json=field,
        )
        return r

    def put_fields(self, ticket_id: int, task_id: int, fields: dict) -> Response:
        """This function intentionally doesn't have a step_id argument, because you can only put tasks at the current step"""
        r = self.session.put(
            f"tickets/{ticket_id}/steps/current/tasks/{task_id}/fields", json=fields
        )
        return r

    def cancel_ticket(
        self, ticket_id: int, requestor_id: Optional[int] = None
    ) -> Response:
        params = {} if requestor_id is None else {"requestor_id": requestor_id}
        r = self.session.put(f"tickets/{ticket_id}/cancel", params=params)
        return r

    def confirm_ticket(
        self,
        ticket_id: int,
        comment: Optional[str] = "",
        requestor_id: Optional[int] = None,
    ) -> Response:
        comment = "None provided" if not comment else comment
        params = {} if requestor_id is None else {"requestor_id": requestor_id}
        r = self.session.put(
            f"tickets/{ticket_id}/confirm",
            params=params,
            json={"confirm_comment": {"comment": comment}},
        )
        return r
