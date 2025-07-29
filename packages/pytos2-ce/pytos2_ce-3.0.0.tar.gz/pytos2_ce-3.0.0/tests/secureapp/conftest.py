import json
import re

import pytest  # type: ignore
import responses

from pytos2.secureapp import SaAPI
from pytos2.secureapp.entrypoint import Sa

from tests.securechange.conftest import users_mock, scw


@pytest.fixture
def sa_api():
    return SaAPI(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def sa():
    return Sa(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def application_identities_mock():
    application_identities_json = json.load(
        open("tests/secureapp/json/application_identities.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/application_identities",
        json=application_identities_json,
    )


@pytest.fixture
def failure_mock():
    responses.add(
        responses.GET,
        re.compile("https://198.18.0.1/securechangeworkflow/api/secureapp.*"),
        status=500,
    )


@pytest.fixture
def applications_mock():
    applications_json = json.load(open("tests/secureapp/json/applications.json"))
    application_54_json = json.load(open("tests/secureapp/json/application_54.json"))

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications",
        json=applications_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
        json=application_54_json,
    )


@pytest.fixture
def application_connections_mock():
    application_connections_json = json.load(
        open("tests/secureapp/json/app_60_connections.json")
    )

    extended_json = json.load(
        open("tests/secureapp/json/app_60_connections_extended.json")
    )

    application_connection_126_json = json.load(
        open("tests/secureapp/json/app_60_connection_126.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections",
        json=application_connections_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections_extended",
        json=extended_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126",
        json=application_connection_126_json,
    )


@pytest.fixture
def application_history_mock():
    application_history_json = json.load(
        open("tests/secureapp/json/app_60_history.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/history",
        json=application_history_json,
    )


@pytest.fixture
def application_interfaces_mock():
    application_interfaces_json = json.load(
        open("tests/secureapp/json/app_242_interfaces.json")
    )

    application_interface_31_json = json.load(
        open("tests/secureapp/json/app_242_iface_31.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces",
        json=application_interfaces_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31",
        json=application_interface_31_json,
    )


@pytest.fixture
def application_interface_connections_mock():
    application_interface_connections_json = json.load(
        open("tests/secureapp/json/app_242_iface_31_conns.json")
    )

    app_242_iface_31_conn_494_json = json.load(
        open("tests/secureapp/json/app_242_iface_31_conn_494.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections",
        json=application_interface_connections_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections/494",
        json=app_242_iface_31_conn_494_json,
    )


@pytest.fixture
def application_connections_to_applications_mock():
    application_connections_to_applications_json = json.load(
        open("tests/secureapp/json/app_8_connections_to_applications.json")
    )

    app_8_conn_to_app_3_json = json.load(
        open("tests/secureapp/json/app_8_connection_to_application_3.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications",
        json=application_connections_to_applications_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications/3",
        json=app_8_conn_to_app_3_json,
    )


@pytest.fixture
def application_access_requests_mock():
    app_8_access_requests = json.load(
        open("tests/secureapp/json/application_8_access_requests.json")
    )

    app_8_access_request_1 = json.load(
        open("tests/secureapp/json/app_8_access_request_1.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests",
        json=app_8_access_requests,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1",
        json=app_8_access_request_1,
    )
