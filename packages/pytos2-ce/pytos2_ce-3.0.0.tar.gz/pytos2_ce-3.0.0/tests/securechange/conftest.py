import json
from typing import List

import pytest  # type: ignore
import responses  # type: ignore
from responses import matchers

from pytos2.securetrack import StAPI
from pytos2.securechange import ScwAPI
from pytos2.securechange.entrypoint import Scw
from pytos2.securechange.ticket import Ticket, ApplicationDetails
from tests.securetrack.conftest import (
    network_objects_mock,
    devices_mock,
    device_rules_mock,
    search_rules_on_open_tickets_mock,
)  # noqa
from pytos2.securechange.fields import MultiAccessRequest

from pytos2.securetrack.device import Device
from pytos2.securetrack.rule import SecurityRule
from pytos2.securetrack.network_object import NetworkObject
from pytos2.securetrack import St

from pytos2.utils import safe_iso8601_date


class MockExit(Exception):
    pass


def _api_path(path):
    return f"https://198.18.0.1/securechangeworkflow/api/securechange/{path}"


@pytest.fixture
def st_api():
    return StAPI(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def st():
    return St(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def device_20_network_objects():
    js = json.load(open("tests/securetrack/json/network_objects/20.json"))
    objects = [
        NetworkObject.kwargify(j) for j in js["network_objects"]["network_object"]
    ]
    return objects


@pytest.fixture
def device_20_rules():
    dev = json.load(open("tests/securetrack/json/devices/device-20.json"))
    dev = Device.kwargify(dev)

    js = json.load(open("tests/securetrack/json/rules/device-20.json"))
    rules = [SecurityRule.kwargify(j) for j in js["rules"]["rule"]]

    for rule in rules:
        rule.device = dev

    return rules


@pytest.fixture
def mock_devices() -> List[Device]:
    js = json.load(open("tests/securetrack/json/devices/devices.json"))
    devices = [Device.kwargify(j) for j in js["devices"]["device"]]
    return devices


@pytest.fixture
def st_devices_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices",
        json=json.load(open("tests/securetrack/json/devices/devices.json")),
    )


@pytest.fixture
def device_20_rules_mock(st, st_devices_mock):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/20/rules",
        json=json.load(open("tests/securetrack/json/rules/device-20.json")),
    )


@pytest.fixture
def device_1_rules():
    dev = json.load(open("tests/securetrack/json/devices/device-1.json"))
    dev = Device.kwargify(dev)

    js = json.load(open("tests/securetrack/json/rules/device-1.json"))
    rules = [SecurityRule.kwargify(j) for j in js["rules"]["rule"]]

    for rule in rules:
        rule.device = dev

    return rules


@pytest.fixture
def all_fields_ticket_json():
    return json.load(open("tests/securechange/json/ticket/all_fields-ticket.json"))


@pytest.fixture
def all_fields_workflow_json(scw_api, all_fields_ticket_json):
    return json.load(open("tests/securechange/json/all_fields-workflow.json"))


@pytest.fixture
def all_fields_step_json(all_fields_ticket_json):
    return [step["name"] for step in all_fields_ticket_json["ticket"]["steps"]["step"]]


@pytest.fixture
def all_fields_field_json(all_fields_ticket_json):
    return all_fields_ticket_json["ticket"]["steps"]["step"][0]["tasks"]["task"][
        "fields"
    ]


@pytest.fixture
def application_details():
    return ApplicationDetails.kwargify(
        json.load(open("tests/securechange/json/application_details.json"))
    )


@pytest.fixture
def post_bad_ticket_json():
    json.load(open("tests/securechange/json/ticket/post_bad_ticket.json"))


@pytest.fixture
def closed_group_modify_ticket(scw_api):
    return Ticket.kwargify(
        json.load(
            open("tests/securechange/json/ticket/closed_group_modify-ticket.json")
        )
    )


@pytest.fixture
def closed_ticket(scw_api):
    return Ticket.kwargify(json.load(open("tests/securechange/json/ticket/redo.json")))


@pytest.fixture
def first_step_ticket(scw_api):
    ticket = json.load(open("tests/securechange/json/ticket/redo.json"))
    redo = ticket["ticket"]
    step_one = redo["steps"]["step"][0]
    redo["status"] = "In Progress"
    redo["steps"]["step"] = [step_one]
    redo["current_step"] = {"id": step_one["id"], "name": step_one["name"]}
    return Ticket.kwargify(ticket)


@pytest.fixture
def redo_ticket(scw_api):
    ticket = json.load(open("tests/securechange/json/ticket/redo.json"))
    redo = ticket["ticket"]
    step_two = redo["steps"]["step"][1]
    redo["status"] = "In Progress"
    redo["steps"]["step"] = redo["steps"]["step"][0:2]
    redo["current_step"] = {"id": step_two["id"], "name": step_two["name"]}
    return Ticket.kwargify(ticket)


@pytest.fixture
def open_access_request_ticket(scw_api):
    return Ticket.kwargify(
        json.load(
            open("tests/securechange/json/ticket/open_with_access_request-ticket.json")
        )
    )


@pytest.fixture
def open_group_modify_ticket(scw_api):
    return Ticket.kwargify(
        json.load(
            open("tests/securechange/json/ticket/open_with_group_modify-ticket.json")
        )
    )


@pytest.fixture
def ar_with_designer_results(scw):
    return MultiAccessRequest.kwargify(
        json.load(
            open(
                "tests/securechange/json/field/multi_access_request_with_designer_results-field.json"
            )
        )
    )


@pytest.fixture
def tickets_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets",
        json=json.load(open("tests/securechange/json/ticket/tickets-0-99.json")),
    )

    responses.add(
        responses.GET,
        "https://10.100.0.1/securechangeworkflow/api/securechange/tickets/fake-url-due-to-params/count_100/start_100",
        json=json.load(open("tests/securechange/json/ticket/tickets-100-199.json")),
    )


@pytest.fixture
def ticket_488():
    return json.load(open("tests/securechange/json/ticket/ticket-488.json"))


@pytest.fixture
def scw_api():
    return ScwAPI(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def scw():
    return Scw(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def ticket_search_mock():
    ticket_search_by_status = json.load(
        open("tests/securechange/json/ticket/ticket_search_assigned.json")
    )

    ticket_search_by_step = json.load(
        open("tests/securechange/json/ticket/ticket_search_by_step_name.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search",
        json=ticket_search_by_status,
        match=[matchers.query_string_matcher("status=ASSIGNED")],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search",
        json=ticket_search_by_step,
        match=[matchers.query_string_matcher("current_step=manual%20step")],
    )


@pytest.fixture
def ticket_search_by_details_mock():
    ticket_search_by_details_by_status = json.load(
        open("tests/securechange/json/ticket/ticket_search_assigned.json")
    )

    ticket_search_by_details_by_step = json.load(
        open("tests/securechange/json/ticket/ticket_search_by_step_name.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/details?task_status=ASSIGNED",
        json=ticket_search_by_details_by_status,
        match_querystring=True,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/details?current_step=manual%20step",
        json=ticket_search_by_details_by_step,
    )


@pytest.fixture
def ticket_search_by_query_mock():
    ticket_search_by_query_id = json.load(
        open("tests/securechange/json/ticket/ticket_search_by_query_id.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/query?query_id=14",
        json=ticket_search_by_query_id,
        match_querystring=True,
    )


@pytest.fixture
def ticket_search_by_query_failed_mock():

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/query?query_id=140",
        status=400,
        json=json.load(
            open("tests/securechange/json/ticket/ticket_search_by_query_id_failed.json")
        ),
    )


@pytest.fixture
def ticket_search_by_group_mock():
    ticket_search_by_group_id = json.load(
        open("tests/securechange/json/ticket/ticket_search_by_group_id.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/group?group_id=9",
        json=ticket_search_by_group_id,
        match_querystring=True,
    )


@pytest.fixture
def ticket_search_by_group_failed_mock():

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/group?group_id=40",
        status=400,
        json=json.load(
            open("tests/securechange/json/ticket/ticket_search_by_group_failed.json")
        ),
    )


@pytest.fixture
def ticket_search_by_free_text_mock():
    ticket_search_by_free_text = json.load(
        open("tests/securechange/json/ticket/ticket_search_by_free_text.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/search_by/free_text?parameter=taskstatus:ASSIGNED",
        json=ticket_search_by_free_text,
        match_querystring=True,
    )


@pytest.fixture
@responses.activate
def all_fields_mock(scw_api, all_fields_ticket_json):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/283",
        json=all_fields_ticket_json,
    )
    return Ticket.get(283)


@pytest.fixture
def all_fields_ticket(scw_api, all_fields_ticket_json):
    return Ticket.kwargify(all_fields_ticket_json)


@pytest.fixture
def dynamic_assignment_ticket(scw_api, all_fields_ticket_json):
    return Ticket.kwargify(
        json.load(open("tests/securechange/json/ticket/dynamic_assignment-ticket.json"))
    )


@pytest.fixture
def get_test_field():
    def f(field_cls):
        xsi_type = [
            a.default for a in field_cls.__attrs_attrs__ if a.name == "xsi_type"
        ][0]
        return field_cls.kwargify(
            json.load(
                open(f"tests/securechange/json/field/{xsi_type.value}-field.json")
            )
        )

    return f


@pytest.fixture
def users_mock():
    users_json = json.load(open("tests/securechange/json/users/users_by_username.json"))
    all_users_json = json.load(open("tests/securechange/json/users/all_users.json"))

    responses.add(
        responses.GET,
        _api_path("users"),
        match=[matchers.query_string_matcher("user_name=r&exact_name=True")],
        json=users_json,
    )

    responses.add(responses.GET, _api_path("users"), json=all_users_json)


@pytest.fixture
def user_mock():
    user_json = json.load(open("tests/securechange/json/users/user_45.json"))
    group_json = json.load(open("tests/securechange/json/users/user_49.json"))

    responses.add(
        responses.GET,
        _api_path("users/45"),
        match=[matchers.query_string_matcher("")],
        json=user_json,
    )

    responses.add(
        responses.GET,
        _api_path("users/49"),
        match=[matchers.query_string_matcher("")],
        json=group_json,
    )


@pytest.fixture
def ticket_history_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
        json=json.load(open("tests/securechange/json/ticket/all_fields-ticket.json")),
    )

    responses.add(
        responses.GET,
        _api_path("tickets/288/history"),
        json=json.load(
            open("tests/securechange/json/ticket_history/ticket_history_288.json")
        ),
    )

    responses.add(
        responses.GET,
        _api_path("tickets/828/history"),
        json=json.load(
            open("tests/securechange/json/ticket_history/ticket_history_828.json")
        ),
    )

    responses.add(
        responses.GET,
        _api_path("tickets/2/history"),
        status=400,
    )

    responses.add(
        responses.GET,
        _api_path("tickets/3/history"),
        body="<xml/>",
    )

    responses.add(
        responses.GET,
        _api_path("tickets/4/history"),
        json={"ticket_history_activities": {}},
    )


@pytest.fixture
def workflow_triggers_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/triggers",
        json=json.load(open("tests/securechange/json/workflow_triggers/triggers.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/triggers?id=4",
        json=json.load(
            open("tests/securechange/json/workflow_triggers/trigger-4.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/triggers?name=Contoso",
        json=json.load(
            open("tests/securechange/json/workflow_triggers/trigger-14.json")
        ),
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/triggers",
        status=201,
    )


@pytest.fixture
def ticket_life_cycle_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
        json=json.load(open("tests/securechange/json/ticket/all_fields-ticket.json")),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users",
        json=json.load(open("tests/securechange/json/users/all_users.json")),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users/45",
        json=json.load(open("tests/securechange/json/users/user_45.json")),
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/change_requester/45",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/steps/1593/tasks/1625/reassign/45",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/reject?handler_id=45",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/reject",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/cancel?requester_id=45",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/cancel",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/confirm?requester_id=45",
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288/confirm",
        status=200,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037",
        json=json.load(
            open("tests/securechange/json/ticket/access_request_for_lifecycle.json")
        ),
    )
    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/map_rules?handler_id=5",
        status=201,
    )
    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/map_rules",
        status=201,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/steps/5689/tasks/5705/fields/61671/designer/redesign",
        status=202,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/steps/5689/tasks/5705/fields/61671/designer/device/8/commit",
        status=202,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/steps/5689/tasks/5705/fields/61671/designer/device/8/update?force=true",
        status=202,
    )
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1037/steps/5689/tasks/5705/fields/61671/designer/device/8/update",
        status=202,
    )


@pytest.fixture
def ticket_life_cycle_ticket_events_mock():
    def filter_ticket_events_callback(request):
        assert request.params["start"] == "0"
        assert request.params["count"] == "2000"
        assert request.params["get_total"] == "true"

        def test_event(event, filters):
            for key, value in filters:
                if key in ["date_from", "date_to"]:
                    test_value = event["timestamp"]
                    if (key == "date_from" and test_value < value) or (
                        key == "date_to" and test_value > value
                    ):
                        return False
                else:
                    if key in [
                        "assignee_id",
                        "assignee_name",
                        "participant_id",
                        "participant_name",
                    ]:
                        if "task_assigned_data" not in event:
                            return False
                        test_value = event["task_assigned_data"].get(key)
                    else:
                        if key not in ["start", "count", "get_total"]:
                            test_value = event.get(key)
                            if str(test_value) != value:
                                return False
            return True

        json_data = json.load(
            open("tests/securechange/json/ticket_event/ticket_events.json")
        )
        parts = request.url.split("?")
        if len(parts) > 1:
            filters = request.params.items()
            events = []
            for event in json_data["ticket_events"]["ticket_event"]:
                if test_event(event, filters):
                    events.append(event)
            json_data["ticket_events"]["ticket_event"] = events
        return (200, {}, json.dumps(json_data))

    responses.add_callback(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/lifecycle_events",
        callback=filter_ticket_events_callback,
    )
    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/lifecycle_events/historical_events",
        status=202,
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/lifecycle_events/historical_events_status",
        json=json.load(
            open("tests/securechange/json/ticket_event/historical_events_status.json")
        ),
        status=200,
    )


@pytest.fixture
def workflows_mock(scw_api):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows/active_workflows?type=ACCESS_REQUEST",
        json=json.load(
            open("tests/securechange/json/workflows/workflows_ACCESS_REQUEST.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows/active_workflows",
        json=json.load(open("tests/securechange/json/workflows/workflows.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows?name=Fully automated Firewall change request",
        json=json.load(open("tests/securechange/json/workflows/workflow_586.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows?id=586",
        json=json.load(open("tests/securechange/json/workflows/workflow_586.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows?id=600",
        json=json.load(open("tests/securechange/json/workflows/workflow_600.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/workflows?name=Generic Workflow",
        json=json.load(open("tests/securechange/json/workflows/workflow_600.json")),
    )


@pytest.fixture
def extensions_mock():
    responses.add(
        responses.GET,
        _api_path("extensions"),
        json=json.load(open("tests/securechange/json/extension/all_extensions.json")),
    )


@pytest.fixture
def related_rules_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/49/steps/177/tasks/177/fields/2929/related_rules",
        json=json.load(
            open("tests/securechange/json/related_rules/related_rules_results.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/49",
        json=json.load(
            open("tests/securechange/json/ticket/related_rules_ticket.json")
        ),
    )


@pytest.fixture
def roles_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/roles",
        json=json.load(open("tests/securechange/json/role/all_roles.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/roles/8",
        json=json.load(open("tests/securechange/json/role/role_8.json")),
    )


@pytest.fixture
def user_or_group_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users/group",
        status=201,
        headers={
            "Location": "https://198.18.0.1/securechangeworkflow/api/securechange/users/49"
        },
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users/group/54",
        status=200,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users/70",
        status=201,
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users/import",
        status=201,
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/users",
        status=201,
        headers={
            "Location": "https://198.18.0.1/securechangeworkflow/api/securechange/users/45"
        },
    )


@pytest.fixture
def saved_search_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries",
        json=json.load(open("tests/securechange/json/saved_search/saved_search.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/14",
        json=json.load(
            open("tests/securechange/json/saved_search/detailed_saved_search.json")
        ),
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/",
        status=201,
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/81",
        status=204,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/81",
        status=204,
    )


@pytest.fixture
def bad_saved_search_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/",
        status=400,
        json=json.load(
            open("tests/securechange/json/saved_search/create_bad_saved_search.json")
        ),
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/97",
        status=400,
        json=json.load(
            open("tests/securechange/json/saved_search/update_bad_saved_search.json")
        ),
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries/97",
        status=400,
        json=json.load(
            open("tests/securechange/json/saved_search/delete_bad_saved_search.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/queries",
        status=401,
        body=open(
            "tests/securechange/json/saved_search/unauthorized_error.json"
        ).read(),
        content_type="text/html",
    )


@pytest.fixture
def domains_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/domains",
        json=json.load(open("tests/securechange/json/domain/all_domains.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/domains/2",
        json=json.load(open("tests/securechange/json/domain/domain_2.json")),
    )


@pytest.fixture
def ticket_requests_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=GROUP_REQUESTS&groupId=9",
        json=json.load(
            open("tests/securechange/json/ticket_requests/group_request-groupId.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=MY_REQUESTS&requestId=1059",
        json=json.load(
            open("tests/securechange/json/ticket_requests/my_requests-requestId.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=ALL_REQUESTS&type=TICKET",
        json=json.load(
            open("tests/securechange/json/ticket_requests/all_request-type.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=MY_REQUESTS&ticketStatus=CLOSED",
        json=json.load(
            open(
                "tests/securechange/json/ticket_requests/my_requests-ticket_status.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=ALL_REQUESTS&ticketId=815",
        json=json.load(
            open("tests/securechange/json/ticket_requests/all_requests-ticketId.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=ALL_REQUESTS&ticketRequiresAttention=true",
        json=json.load(
            open(
                "tests/securechange/json/ticket_requests/all_request-requires_attention.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=MY_REQUESTS&ticketId=1046",
        json=json.load(
            open("tests/securechange/json/ticket_requests/my_request-ticketId.json")
        ),
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/1060/cancel",
        status=200,
    )


@pytest.fixture
def bad_ticket_requests_mock():
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/6000/cancel",
        status=404,
        json=json.load(
            open("tests/securechange/json/ticket_requests/invalid_request_id.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/securechange/requests/search?view=blahblah",
        status=404,
        json=json.load(
            open("tests/securechange/json/ticket_requests/bad_request.json"),
        ),
    )
