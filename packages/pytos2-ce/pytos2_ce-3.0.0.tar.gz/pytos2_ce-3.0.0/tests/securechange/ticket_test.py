import json

import pytest
import responses
from requests.exceptions import HTTPError
from . import conftest  # noqa
from pytos2.securechange.ticket import Ticket, TicketStatus, Step, Task
from pytos2.securechange.fields import (
    AccessRequest,
    DNSObject,
    IPObject,
    MultiAccessRequest,
    MultiServerDecommissionRequest,
    RangeObject,
    RuleDecommission,
    RuleRecertification,
    RuleModificationField,
    MultiTextArea,
    Service,
    TextArea,
    MultipleSelection,
    MultiHyperlink,
    MultiGroupChange,
    MultiTextField,
    MultiTarget,
    MultiNetworkObject,
    MultiService,
    ApproveReject,
    Checkbox,
    DropDownList,
    Date,
    Time,
    TextField,
    Manager,
    Hyperlink,
    CloneServerPolicyRequest,
    Link,
    classify_field,
    get_field_class,
    Field,
    FieldXsiType,
)


class TestTicketAttributes(object):
    def test_steps(self, all_fields_ticket):
        assert isinstance(all_fields_ticket.steps, list)

    def test_workflow(self, all_fields_ticket):
        workflow = all_fields_ticket.workflow

        assert workflow.name == "AR all fields"

    def test_current_step_props(self, all_fields_ticket):
        assert all_fields_ticket.current_step_index == 3
        assert all_fields_ticket.current_step_name == "No Fields"

        assert all_fields_ticket.previous_step.name == "Duplicate"

        empty_ticket = Ticket.create("test_workflow", "test_step")
        assert empty_ticket.current_step_index is None
        assert empty_ticket.previous_step is None

    @pytest.mark.parametrize(
        "attr, value",
        [
            ("id", 288),
            ("subject", "Better Tests"),
            ("requester", "r"),
            ("requester_id", 4),
            ("priority", Ticket.Priority.NORMAL),
            ("status", TicketStatus.INPROGRESS),
            ("expiration_field_name", "Expiration"),
            ("expiration_date", None),
            ("domain_name", "Default"),
            ("sla_status", Ticket.SlaStatus.NA),
            ("sla_outcome", Ticket.SlaOutcome.NA),
        ],
    )
    def test_values(self, all_fields_ticket, attr, value):
        assert getattr(all_fields_ticket, attr) == value

    def test_last_step(self, all_fields_ticket, scw):
        assert all_fields_ticket.last_step.name == "No Fields"

    def test_current_step(self, all_fields_ticket, closed_group_modify_ticket):
        assert (
            all_fields_ticket.current_step_name
            == all_fields_ticket.last_step.name
            == all_fields_ticket.data["ticket"]["current_step"]["name"]
        )
        assert closed_group_modify_ticket.current_step_name is None

    def test_access_request(
        self, open_access_request_ticket, closed_group_modify_ticket
    ):
        assert open_access_request_ticket.access_request
        assert closed_group_modify_ticket.access_request is None

    def test_group_modify(self, open_group_modify_ticket, closed_group_modify_ticket):
        assert open_group_modify_ticket.group_modify
        assert closed_group_modify_ticket.group_modify is None

    def test_last_task(self, all_fields_ticket):
        assert all_fields_ticket.last_task is all_fields_ticket.steps[-1].tasks[-1]

    def test_current_task(self, all_fields_ticket):
        assert all_fields_ticket.current_task is all_fields_ticket.steps[-1].tasks[-1]

    def test_current_task_dynamic_assignment(self, dynamic_assignment_ticket):
        with pytest.raises(ValueError):
            dynamic_assignment_ticket.current_task

    def test_current_tasks(self, all_fields_ticket):
        assert all_fields_ticket.current_tasks is all_fields_ticket.steps[-1].tasks

    def test_json(self, all_fields_ticket):
        assert isinstance(json.dumps(all_fields_ticket._json), str)

    def test_application_details(self, application_details):
        assert application_details.id == 8


class TestTicketFunctions(object):
    def test_create_ticket(self):
        ticket = Ticket.create("workflow", "test subject")
        assert ticket.subject == "test subject"
        assert ticket.workflow.name == "workflow"

        ticket.create_step("Step Name")
        assert ticket.steps[0].name == "Step Name"
        assert isinstance(ticket.steps[0], Step)

    def test_get_step(self, all_fields_ticket):
        assert (
            all_fields_ticket.get_step("invalid")
            is all_fields_ticket.get_step(100)
            is None
        )
        assert (
            all_fields_ticket.get_step("Open request")
            == all_fields_ticket.get_step(0)
            == all_fields_ticket.steps[0]
        )

    def test_get_step_by_id(self, all_fields_ticket):
        assert all_fields_ticket._get_step(1590).id == 1590

    def test_step_task(self, all_fields_ticket):
        assert (
            all_fields_ticket.get_step_task("invalid", 0)
            is all_fields_ticket.get_step_task("invalid", "invalid")
            is None
        )
        assert all_fields_ticket.get_step_task("invalid", 0) is None

    def test_step_task_fields(self, all_fields_ticket):
        assert all_fields_ticket.get_step_task_fields("invalid", 0) is None
        assert not all_fields_ticket.get_step_task_fields(1)

    @responses.activate
    def test_advance(self, first_step_ticket, redo_ticket, closed_ticket):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/252/steps/1246/tasks/1258",
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/252",
            json=closed_ticket.data,
        )
        res = redo_ticket.advance()
        assert isinstance(res, Ticket)
        first_step_ticket.advance(save=False)
        assert all(t.is_done for t in first_step_ticket.current_step.tasks)

    def test_advance_closed(self, closed_group_modify_ticket):
        with pytest.raises(AssertionError):
            closed_group_modify_ticket.advance()

    def test_save_new(self, all_fields_ticket):
        all_fields_ticket.id = None
        with pytest.raises(AssertionError):
            all_fields_ticket.save()

    @responses.activate
    def test_save_exceptions(self, all_fields_ticket, scw):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/steps/current/tasks/1625",
            status=406,
        )
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/steps/current/tasks/1625/fields",
            status=406,
        )

        new_field = all_fields_ticket.last_task.create_field(
            "TestField", FieldXsiType.TEXT_FIELD
        )
        new_field.text = "123"
        with pytest.raises(ValueError):
            all_fields_ticket.save()

        with pytest.raises(ValueError):
            all_fields_ticket.save(force=True)

        all_fields_ticket.last_task.done()
        with pytest.raises(ValueError):
            all_fields_ticket.save()

    @responses.activate
    def test_save_unchanged(self, all_fields_ticket):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json={"ticket": {**all_fields_ticket.data["ticket"], "id": 288}},
        )
        assert isinstance(all_fields_ticket.save(), Ticket)

    @responses.activate
    def test_save_field(self, open_access_request_ticket):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242/steps/current/tasks/1216/fields",
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242",
            json={"ticket": {**open_access_request_ticket.data["ticket"], "id": 242}},
        )

        open_access_request_ticket.last_task.get_field("Design comment").text = (
            "new text"
        )
        assert isinstance(open_access_request_ticket.save(), Ticket)

    @responses.activate
    def test_save_task(self, open_access_request_ticket):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242/steps/current/tasks/1216",
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242",
            json={"ticket": {**open_access_request_ticket.data["ticket"], "id": 242}},
        )
        open_access_request_ticket.last_task.status = Task.Status.DONE
        open_access_request_ticket.current_step.tasks.append(Task())

        assert isinstance(open_access_request_ticket.save(), Ticket)

    @responses.activate
    def test_save_task_force(self, open_access_request_ticket):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242/steps/current/tasks/1216",
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/242",
            json={"ticket": {**open_access_request_ticket.data["ticket"], "id": 242}},
        )
        open_access_request_ticket.last_task.status = Task.Status.DONE

        assert isinstance(open_access_request_ticket.save(force=True), Ticket)

    @responses.activate
    def test_redo(self, closed_ticket, first_step_ticket, redo_ticket):
        counter = {"count": 0}

        def ticket_cb(c):
            def _f(request):
                c["count"] += 1
                if c["count"] < 2:
                    return (200, {}, json.dumps(redo_ticket.data))
                else:
                    return (200, {}, json.dumps(first_step_ticket.data))

            return _f

        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/252/steps/1246/tasks/1258/redo/1245",
        )
        responses.add_callback(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/252",
            callback=ticket_cb(counter),
        )
        res = redo_ticket.redo(0)
        assert len(res.steps) == 1

    @responses.activate
    def test_redo_failed(self, closed_ticket, first_step_ticket, redo_ticket):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/252/steps/1246/tasks/1258/redo/1245",
            status=400,
        )
        with pytest.raises(HTTPError):
            redo_ticket.redo(0)

    def test_redo_closed(self, closed_ticket):
        with pytest.raises(AssertionError):
            closed_ticket.redo(0)

    def test_redo_missing_step(self, redo_ticket):
        with pytest.raises(IndexError):
            redo_ticket.redo(10000)

    def test_redo_first_step(self, first_step_ticket):
        with pytest.raises(AssertionError):
            first_step_ticket.redo(0)

    def test_redo_no_step_id(self, redo_ticket):
        redo_ticket.steps[0].id = None
        with pytest.raises(AssertionError):
            redo_ticket.redo(0)

    def test_redo_current_step(self, redo_ticket):
        with pytest.raises(AssertionError):
            redo_ticket.redo(1)

    def test_misc_redo_errors(self, redo_ticket):
        redo_ticket.current_task.id = None
        with pytest.raises(AssertionError):
            redo_ticket.redo(0)
        redo_ticket.current_step.id = None
        with pytest.raises(AssertionError):
            redo_ticket.redo(0)
        redo_ticket.id = None
        with pytest.raises(AssertionError):
            redo_ticket.redo(0)

    def test_save_closed(self, closed_group_modify_ticket, scw):
        with pytest.raises(AssertionError):
            closed_group_modify_ticket.save()

    def test_json_override(self, all_fields_ticket):
        all_fields_ticket._json = {}
        assert all_fields_ticket._json == {}

    def test_post_json(self, all_fields_ticket):
        new_json = all_fields_ticket._json
        new_json["ticket"]["steps"]["step"] = [new_json["ticket"]["steps"]["step"][0]]
        assert all_fields_ticket.post_json == new_json

    @responses.activate
    def test_post(self, all_fields_ticket, scw):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets",
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/614"
            },
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/614",
            json={"ticket": {**all_fields_ticket.data["ticket"], "id": 614}},
        )

        t = all_fields_ticket.post()
        assert t.id == 614

    @responses.activate
    def test_bad_post(self, all_fields_ticket, scw, post_bad_ticket_json):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets",
            status=400,
            json=post_bad_ticket_json,
        )
        with pytest.raises(ValueError):
            all_fields_ticket.post()

    @responses.activate
    def test_reject(self, all_fields_ticket, scw):
        responses.add(
            responses.PUT,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{all_fields_ticket.id}/reject",
        )
        responses.add(
            responses.GET,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{all_fields_ticket.id}",
            json=all_fields_ticket.data,
        )
        assert isinstance(all_fields_ticket.reject(), Ticket)
        all_fields_ticket.id = None
        with pytest.raises(ValueError):
            all_fields_ticket.reject()

    @responses.activate
    def test_reject_not_supported(self, all_fields_ticket, scw):
        responses.add(
            responses.PUT,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{all_fields_ticket.id}/cancel",
        )
        responses.add(
            responses.PUT,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{all_fields_ticket.id}/reject",
            json={
                "result": {
                    "code": "WEB_APPLICATION_ERROR",
                    "message": "HTTP 404 Not Found",
                }
            },
            status=400,
        )
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/reject",
            json={"result": {"code": "WEB_APPLICATION_ERROR"}},
            status=400,
        )
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/2/reject",
            json={"result": {"code": "WEB_APPLICATION_ERROR", "message": "scarry"}},
            status=400,
        )
        responses.add(
            responses.GET,
            f"https://198.18.0.1/securechangeworkflow/api/securechange/tickets/{all_fields_ticket.id}",
            json=all_fields_ticket.data,
        )
        with pytest.raises(HTTPError):
            all_fields_ticket.reject()
        all_fields_ticket.id = 1
        with pytest.raises(HTTPError):
            all_fields_ticket.reject()
        all_fields_ticket.id = 2
        with pytest.raises(HTTPError):
            all_fields_ticket.reject()


class TestStep(object):
    @pytest.fixture()
    def current_step(self, all_fields_ticket):
        return all_fields_ticket.current_step

    @pytest.fixture()
    def first_step(self, all_fields_ticket):
        return all_fields_ticket.get_step(0)

    @pytest.fixture()
    def all_fields_step(self, all_fields_ticket):
        return all_fields_ticket.get_step(1)

    def test_step_index(self, all_fields_ticket, all_fields_step_json):
        assert (
            all_fields_ticket.get_step(3).name
            == all_fields_ticket.get_step(-1).name
            == all_fields_step_json[-1]
        )

    def test_create_task(self):
        step = Step()

        assert len(step.tasks) == 0
        step.create_task()
        assert len(step.tasks) == 1
        assert isinstance(step.tasks[0], Task)

    def test_task(self, all_fields_step):
        assert all_fields_step.get_task(0).name is None
        assert all_fields_step.get_task(None).name is None
        assert all_fields_step.get_task("missing") is None
        assert all_fields_step.get_task(100) is None

    def test_task_field(self, all_fields_step):
        fields = all_fields_step.get_task_fields(0, TextArea)
        print(fields)

        assert len(fields) == 2
        assert isinstance(fields[0], TextArea)

        fields = all_fields_step.get_task_fields(0, MultiAccessRequest)
        assert len(fields) == 1
        assert isinstance(fields[0], MultiAccessRequest)

        fields = all_fields_step.get_task_fields(0)
        assert len(fields) == 0

    def test_done(self, current_step):
        stat = not all(t.status is Task.Status.DONE for t in current_step.tasks)
        assert stat  # all(t.status is Task.Status.DONE for t in current_step.tasks) is False
        current_step.done()
        assert all(t.status is Task.Status.DONE for t in current_step.tasks)

    def test_is_done(self, first_step):
        assert first_step.is_done


class TestTask(object):
    @pytest.fixture()
    def task(self, all_fields_ticket):
        return all_fields_ticket.get_step_task(1)

    @pytest.fixture()
    def open_task(self, all_fields_ticket):
        return all_fields_ticket.last_task

    def test_create_field(self):
        cls_list = [
            MultiAccessRequest,
            MultiServerDecommissionRequest,
            RuleDecommission,
            RuleRecertification,
            RuleModificationField,
            MultiTextArea,
            TextArea,
            MultipleSelection,
            MultiHyperlink,
            MultiGroupChange,
            MultiTextField,
            MultiTarget,
            MultiNetworkObject,
            MultiService,
            ApproveReject,
            Checkbox,
            DropDownList,
            Date,
            Time,
            TextField,
            Manager,
            Hyperlink,
            CloneServerPolicyRequest,
        ]
        task = Task()

        for cls in cls_list:
            task.create_field("field1", cls)
            assert isinstance(task.fields[0], cls)
            task.fields = []

        assert len(task.fields) == 0
        task.create_field("TestField", TextArea)
        assert isinstance(task.fields[0], TextArea)

        assert len(task.fields) == 1
        assert isinstance(task.fields[0], TextArea)
        assert task.fields[0].name == "TestField"

        task.fields = []
        task.create_field("TestField2", FieldXsiType.TEXT_FIELD)

        assert len(task.fields) == 1
        assert isinstance(task.fields[0], TextField)
        assert task.fields[0].name == "TestField2"

    def test_fields(self, task):
        assert all(
            t.xsi_type
            in (FieldXsiType.TEXT_FIELD, FieldXsiType.TEXT_AREA, FieldXsiType.CHECKBOX)
            for t in task._get_fields(TextField, TextArea, Checkbox)
        )

    def test_get_field(self, task):
        assert task.get_field("Text area")
        assert task.get_field("Text area", TextArea)
        assert isinstance(task.get_field(None, TextArea), TextArea)
        assert task.get_field("Text area", TextField) is None
        assert task.get_field("Text field", TextField, TextArea)

    def test_dirty(self, open_task):
        open_task.done()
        assert open_task._dirty

    def test_dirty_fields(self, task):
        f = task.get_field("Approve / Reject")
        f.approve()
        assert task._dirty_fields


class TestTicketIterator:
    @responses.activate
    def test_iterator(self, scw, tickets_mock):
        # looks like ticket_mock can't differenciate different params, so I changed it to a dummy url
        tickets = scw.get_tickets(TicketStatus.CLOSED)

        assert len(tickets) == 200
        assert isinstance(tickets, list)
        assert isinstance(tickets[0], Ticket)


class TestTicketLifecycle:
    @responses.activate
    def test_change_requester(self, ticket_life_cycle_mock, scw):
        ticket = scw.get_ticket(288)
        user = scw.get_user(45)

        scw.change_requester(ticket, user, "change requester")
        scw.change_requester(288, 45, "change requester")

        ticket.change_requester(user, "change requester")
        ticket.change_requester(45, "change requester")

    @responses.activate
    def test_reassign_ticket(self, ticket_life_cycle_mock, scw):
        ticket = scw.get_ticket(288)
        step = ticket.current_step
        task = step.last_task
        user = scw.get_user(45)

        scw.reassign_ticket(ticket, user, step, task, "reassign ticket")
        scw.reassign_ticket(288, 45, step, task, "reassign ticket")

        ticket.reassign(user, step, task, "reassign ticket")
        ticket.reassign(45, step, task, "reassign ticket")

    @responses.activate
    def test_reject_ticket(self, ticket_life_cycle_mock, scw):
        ticket = scw.get_ticket(288)
        ticket.reject()
        ticket.reject(comment="Customer comment")
        ticket.reject(comment="Customer comment", handler_id=45)

    @responses.activate
    def test_cancel_ticket(self, ticket_life_cycle_mock, scw):
        ticket = scw.get_ticket(288)
        ticket.cancel()
        ticket.cancel(requestor_id=45)

    @responses.activate
    def test_confirm_ticket(self, ticket_life_cycle_mock, scw):
        ticket = scw.get_ticket(288)
        ticket.confirm()
        ticket.confirm(comment="Customer comment")
        ticket.confirm(comment="Customer comment", requestor_id=45)

    @responses.activate
    def test_get_ticket_events(self, ticket_life_cycle_ticket_events_mock, scw):
        ticket_events = scw.get_ticket_events()

        assert ticket_events[0].ticket_id == 1036
        assert ticket_events[0].workflow_name == "Firewall Change Request Workflow"
        assert ticket_events[0].domain_id == 1
        assert ticket_events[0].parent_workflow_id == 324
        assert ticket_events[0].timestamp.strftime("%Y-%m-%d") == "2024-04-25"
        assert ticket_events[0].type == "TICKET_SLA_OVERDUE"
        assert ticket_events[0].step_id is None
        assert ticket_events[0].step_name is None
        assert ticket_events[0].task_id is None
        assert ticket_events[0].task_name is None
        assert len(ticket_events[0].potential_participants) == 0
        assert ticket_events[0].task_assigned_data is None

        assert ticket_events[1].ticket_id == 1036
        assert ticket_events[1].workflow_name == "Firewall Change Request Workflow"
        assert ticket_events[1].domain_id == 1
        assert ticket_events[1].parent_workflow_id == 324
        assert ticket_events[1].timestamp.strftime("%Y-%m-%d") == "2024-02-18"
        assert ticket_events[1].type == "TASK_READY_TO_BE_ASSIGNED"
        assert ticket_events[1].step_id == 5679
        assert ticket_events[1].step_name == "Business Approval"
        assert ticket_events[1].task_id == 5695
        assert ticket_events[1].task_name == "Default"
        assert ticket_events[1].potential_participants[0].participant_id == 9
        assert (
            ticket_events[1].potential_participants[0].participant_name
            == "Security Team"
        )
        assert ticket_events[1].potential_participants[1].participant_id == 4
        assert ticket_events[1].potential_participants[1].participant_name == "r"
        assert ticket_events[1].task_assigned_data is None

        assert ticket_events[2].ticket_id == 1036
        assert ticket_events[2].workflow_name == "Firewall Change Request Workflow"
        assert ticket_events[2].domain_id == 1
        assert ticket_events[2].parent_workflow_id == 324
        assert ticket_events[2].timestamp.strftime("%Y-%m-%d") == "2024-02-18"
        assert ticket_events[2].type == "TASK_ASSIGNED"
        assert ticket_events[2].step_id == 5679
        assert ticket_events[2].step_name == "Business Approval"
        assert ticket_events[2].task_id == 5695
        assert ticket_events[2].task_name == "Default"
        assert len(ticket_events[2].potential_participants) == 0
        assert ticket_events[2].task_assigned_data.assignee_id == 4
        assert ticket_events[2].task_assigned_data.assignee_name == "r"
        assert ticket_events[2].task_assigned_data.participant_id == 9
        assert ticket_events[2].task_assigned_data.participant_name == "Security Team"

        assert ticket_events[3].ticket_id == 1031
        assert ticket_events[3].workflow_name == "Access Request Workflow"
        assert ticket_events[3].domain_id == 1
        assert ticket_events[3].parent_workflow_id == 322
        assert ticket_events[3].timestamp.strftime("%Y-%m-%d") == "2024-02-15"
        assert ticket_events[3].type == "TASK_DONE"
        assert ticket_events[3].step_id == 5645
        assert ticket_events[3].step_name == "Identify Targets and Risks"
        assert ticket_events[3].task_id == 5661
        assert ticket_events[3].task_name == "Default"
        assert len(ticket_events[3].potential_participants) == 0
        assert ticket_events[3].task_assigned_data is None

    @responses.activate
    def test_get_ticket_events_by_filter(
        self, ticket_life_cycle_ticket_events_mock, scw
    ):
        ticket_events = scw.get_ticket_events(type="TICKET_SLA_OVERDUE")
        assert len(ticket_events) == 1
        assert ticket_events[0].type == "TICKET_SLA_OVERDUE"

        ticket_events = scw.get_ticket_events(assignee_name="r")
        assert len(ticket_events) == 1
        assert ticket_events[0].task_assigned_data.assignee_name == "r"

        ticket_events = scw.get_ticket_events(assignee_id=4)
        assert len(ticket_events) == 1
        assert ticket_events[0].task_assigned_data.assignee_id == 4

        ticket_events = scw.get_ticket_events(participant_name="Security Team")
        assert len(ticket_events) == 1
        assert ticket_events[0].task_assigned_data.participant_name == "Security Team"

        ticket_events = scw.get_ticket_events(participant_id=9)
        assert len(ticket_events) == 1
        assert ticket_events[0].task_assigned_data.participant_id == 9

        ticket_events = scw.get_ticket_events(ticket_id=1031)
        assert len(ticket_events) == 1
        assert ticket_events[0].ticket_id == 1031

        ticket_events = scw.get_ticket_events(workflow_name="Access Request Workflow")
        assert len(ticket_events) == 1
        assert ticket_events[0].workflow_name == "Access Request Workflow"

        ticket_events = scw.get_ticket_events(parent_workflow_id=322)
        assert len(ticket_events) == 1
        assert ticket_events[0].parent_workflow_id == 322

        ticket_events = scw.get_ticket_events(step_name="Identify Targets and Risks")
        assert len(ticket_events) == 1
        assert ticket_events[0].step_name == "Identify Targets and Risks"

        ticket_events = scw.get_ticket_events(step_id=5645)
        assert len(ticket_events) == 1
        assert ticket_events[0].step_id == 5645

        ticket_events = scw.get_ticket_events(date_from="2024-04-25")
        assert len(ticket_events) == 1
        assert ticket_events[0].timestamp.strftime("%Y-%m-%d") == "2024-04-25"

        ticket_events = scw.get_ticket_events(date_to="2024-02-16")
        assert len(ticket_events) == 1
        assert ticket_events[0].timestamp.strftime("%Y-%m-%d") == "2024-02-15"

    @responses.activate
    def test_backfill_ticket_events(self, ticket_life_cycle_ticket_events_mock, scw):
        scw.backfill_ticket_events("2023-11-05")

    @responses.activate
    def test_get_ticket_historical_events_status(
        self, ticket_life_cycle_ticket_events_mock, scw
    ):
        historical_events_status = scw.get_ticket_historical_events_status()
        assert historical_events_status == "NOT_RUNNING"

    @responses.activate
    def test_map_rules(self, ticket_life_cycle_mock, scw):
        scw.map_rules(1037)
        scw.map_rules(1037, 5)

        ticket = scw.get_ticket(1037)
        ticket.map_rules()

    @responses.activate
    def test_designer_redesign(self, ticket_life_cycle_mock, scw):
        scw.designer_redesign(1037, 5689, 5705, 61671)

        ticket = scw.get_ticket(1037)
        ticket.designer_redesign()

    @responses.activate
    def test_designer_device_commit(self, ticket_life_cycle_mock, scw):
        scw.designer_device_commit(1037, 5689, 5705, 61671, 8)

        ticket = scw.get_ticket(1037)
        ticket.designer_device_commit(8)

    @responses.activate
    def test_designer_device_update(self, ticket_life_cycle_mock, scw):
        scw.designer_device_update(1037, 5689, 5705, 61671, 8)
        scw.designer_device_update(1037, 5689, 5705, 61671, 8, True)

        ticket = scw.get_ticket(1037)
        ticket.designer_device_update(8)
