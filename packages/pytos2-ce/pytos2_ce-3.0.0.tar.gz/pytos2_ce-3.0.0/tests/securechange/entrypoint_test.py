import json
import pytest
import responses
from requests.exceptions import HTTPError


# from pytos2.securechange.entrypoint import Scw
from pytos2.api import ApiError
from pytos2.securechange.ticket import Ticket, TicketStatus, Task, Comment, Attachment

from pytos2.securechange.user import SCWParty, UserXsiType, UserRole, Permission


class TestEntrypoint:
    @responses.activate
    def test_ticket_search(self, scw, ticket_search_mock):
        arr = scw.ticket_search(status=Task.Status.ASSIGNED)
        # first = next(arr)
        first = arr[0]
        assert first is not None

        # assert first.duration == 2180
        assert first.priority == Ticket.Priority.CRITICAL
        # assert first.workflow_name == "Reg Workflow"
        assert first.id == 8
        assert first.status == TicketStatus.INPROGRESS
        assert first.requester_name == "Smith"
        assert first.subject == "new 1401234982542"
        assert first.sla_status == Ticket.SlaStatus.ESCALATION
        assert first.current_step == "verifier"

    @responses.activate
    def test_ticket_search_by_details(self, scw, ticket_search_by_details_mock):
        arr = scw.ticket_search_by_details(task_status=Task.Status.ASSIGNED)
        # first = next(arr)
        first = arr[0]
        assert first is not None

        assert first.priority == Ticket.Priority.CRITICAL
        # assert first.workflow_name == "Reg Workflow"
        assert first.id == 8
        assert first.status == TicketStatus.INPROGRESS
        assert first.requester_name == "Smith"
        assert first.subject == "new 1401234982542"
        assert first.sla_status == Ticket.SlaStatus.ESCALATION
        assert first.current_step == "verifier"

    @responses.activate
    def test_ticket_search_by_query(self, scw, ticket_search_by_query_mock):
        arr = scw.ticket_search_by_saved_search(saved_search_id=14)
        first = arr[0]
        assert first is not None

        assert first.priority == Ticket.Priority.NORMAL
        assert first.id == 1018
        assert first.status == TicketStatus.INPROGRESS
        assert first.requester_name == "Henry Carr"
        assert first.subject == "CSP - CheckPoint Smart-1 - Palo Alto Prisma "
        assert first.sla_status == Ticket.SlaStatus.OK
        assert first.current_step == "Business Approval"

    @responses.activate
    def test_ticket_search_by_query_failed(
        self, scw, ticket_search_by_query_failed_mock
    ):
        with pytest.raises(ApiError) as exc_info:
            scw.ticket_search_by_saved_search(saved_search_id=140)

        response_json = json.load(
            open("tests/securechange/json/ticket/ticket_search_by_query_id_failed.json")
        )

        assert "400" in str(exc_info.value)
        assert response_json["result"]["message"] == "Query ID 140 was not found."

    @responses.activate
    def test_ticket_search_by_group(self, scw, ticket_search_by_group_mock):
        arr = scw.ticket_search_by_group(group_id=9)
        first = arr[0]
        assert first is not None

        assert first.priority == Ticket.Priority.NORMAL
        assert first.id == 1029
        assert first.status == TicketStatus.INPROGRESS
        assert first.requester_name == "Henry Carr"
        assert first.subject == "AR - Palo Alto - Users from Networks"
        assert first.sla_status == Ticket.SlaStatus.OK
        assert first.current_step == "Business Approval"

    @responses.activate
    def test_ticket_search_by_group_failed(
        self, scw, ticket_search_by_group_failed_mock
    ):
        with pytest.raises(ApiError) as exc_info:
            scw.ticket_search_by_group(group_id=40)

        response_json = json.load(
            open("tests/securechange/json/ticket/ticket_search_by_group_failed.json")
        )

        assert "400" in str(exc_info.value)
        assert response_json["result"]["message"] == "Group ID 40 was not found."

    @responses.activate
    def test_ticket_search_by_free_text(self, scw, ticket_search_by_free_text_mock):
        arr = scw.ticket_search_by_free_text(parameter="taskstatus:ASSIGNED")
        first = arr[0]
        assert first is not None

        assert first.priority == Ticket.Priority.NORMAL
        assert first.id == 1046
        assert first.status == TicketStatus.INPROGRESS
        assert first.requester_name == "Henry Carr"
        assert first.subject == "Test_request_trigger10"
        assert first.sla_status == Ticket.SlaStatus.WARNING
        assert first.current_step == "Test -  Server Decommission Request"

    @responses.activate
    def test_get_users(self, scw, users_mock):
        users = scw.get_users(user_name="r", exact_name=True)

        # user = next(users)
        user = users[0]
        assert user is not None

        assert user.display_name == "r"
        assert user.origin_type == SCWParty.OriginType.LOCAL
        assert user.member_of[0].name == "Regi's Grp"
        assert user.roles[0].name == "Role with WorkFlow"
        assert user.id == 289
        assert user.xsi_type == UserXsiType.USER

    @responses.activate
    def test_get_user(self, scw, users_mock, user_mock):
        user = scw.get_user(45)

        assert user is not None

        assert user.display_name == "Johnny_Smith"
        assert user.origin_type == SCWParty.OriginType.LDAP
        assert user.member_of[0].name == "Advertising"
        assert user.roles[0].name == "Role with WorkFlow"
        assert user.id == 45
        assert user.xsi_type == UserXsiType.USER

        user = scw.get_user(45, expand=True)

        assert user is not None

        assert user.display_name == "johnny_smith"
        assert user.origin_type == SCWParty.OriginType.LDAP
        assert user.member_of[0].name == "Advertising"
        assert user.roles[0].name == "Role with WorkFlow"
        assert user.id == 45
        assert user.xsi_type == UserXsiType.USER

    @responses.activate
    def test_get_attachment(self, scw, all_fields_ticket):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json={"ticket": {**all_fields_ticket.data["ticket"], "id": 288}},
        )

        comment = all_fields_ticket.comments[0]
        assert isinstance(comment, Comment)
        attachment = comment.attachments[0]
        assert isinstance(attachment, Attachment)
        assert attachment.uid == "b5672678-d9c5-46ee-87cc-d8fa7fce1a43"
        responses.add(
            responses.GET,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/attachments/{attachment.uid}",
        )
        attachment_content = scw.get_attachment(attachment.uid)
        assert isinstance(attachment_content, bytes)

    @responses.activate
    def test_add_attachment(self, scw):
        id = "b5672678-d9c5-46ee-87cc-d8fa7fce1a43"
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/securechange/attachments",
            id,
        )

        uuid = scw.add_attachment("tests/securechange/files/test.pdf")
        assert isinstance(uuid, str)
        assert uuid == id

    @responses.activate
    def test_add_comment(self, scw):
        id = "1"
        ticket_id = 1
        step_id = 1
        task_id = 1
        responses.add(
            responses.POST,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/comments",
            id,
        )

        comment_id = scw.add_comment(
            ticket_id,
            step_id,
            task_id,
            "New Comment",
            ["b5672678-d9c5-46ee-87cc-d8fa7fce1a43"],
        )
        assert isinstance(comment_id, str)
        assert comment_id == id

    @responses.activate
    def test_delete_comment(self, scw):
        """Delete comment by ticket and comment id"""
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/404/comments/404",
            status=404,
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/comments/1",
            status=200,
        )

        test_one = scw.delete_comment(1, 1)
        test_two = scw.delete_comment(1, "1")
        test_three = scw.delete_comment("1", 1)
        assert all([comment is None for comment in [test_one, test_two, test_three]])

        with pytest.raises(ValueError) as exception:
            scw.delete_comment(404, 404)
        assert "Not Found" in str(exception.value)

        with pytest.raises(ValueError) as exception:
            scw.delete_comment(404, "404")
        assert "Not Found" in str(exception.value)
        with pytest.raises(ValueError) as exception:
            scw.delete_comment("404", 404)
        assert "Not Found" in str(exception.value)

        with pytest.raises(ValueError) as exception:
            scw.delete_comment("404", "404")
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_roles(self, roles_mock, scw):
        roles = scw.get_roles()
        assert roles[0].id == 8
        assert roles[0].name == "Application Admin"
        assert roles[0].description == "Can Approve and Edit SA applications"
        assert roles[0].permissions[0].name == "Assign or reassign tickets to all users"
        assert roles[0].permissions[0].value is False
        assert roles[0].permissions[0].key == "REASSIGN_TICKETS_TO_ALL_USERS"

        role = scw.get_role(8)
        assert role.id == 8
        assert role.name == "Application Admin"
        assert role.description == "Can Approve and Edit SA applications"
        assert role.permissions[0].name == "Assign or reassign tickets to all users"
        assert role.permissions[0].value is False
        assert role.permissions[0].key == "REASSIGN_TICKETS_TO_ALL_USERS"
