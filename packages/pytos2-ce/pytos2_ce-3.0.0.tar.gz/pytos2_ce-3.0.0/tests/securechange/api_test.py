import pytest
import responses

from requests.exceptions import HTTPError
from . import conftest  # noqa
from pytos2.securechange.entrypoint import Scw


class TestClient(object):
    def test_with_args(self, scw_api):
        assert scw_api.hostname == "198.18.0.1"
        assert scw_api.username == "username"
        assert scw_api.password == "password"

    def test_with_missing_args(self):
        with pytest.raises(ValueError) as e:
            Scw()
        assert "hostname argument must be provided" in str(e.value)


class TestClientMethods(object):
    @responses.activate
    def test_get_ticket_not_found(self, scw):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/100000000",
            body=open("tests/securechange/json/ticket/ticket_not_found.json").read(),
            content_type="application/xml",
            status=404,
        )
        with pytest.raises(HTTPError):
            scw.get_ticket(100000000)

    @responses.activate
    def test_get_ticket_error(self, scw):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/100000000",
            content_type="application/xml",
            status=500,
        )
        # XXX TODO: implement
        pass


class TestAPIMethods:
    @responses.activate
    def test_get_workflow(self, scw_api, all_fields_workflow_json):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/workflows",
            json=all_fields_workflow_json,
        )

        assert (
            scw_api.get_workflow(336).json()
            == scw_api.get_workflow(name="AR all fields").json()
        )

        with pytest.raises(TypeError):
            scw_api.get_workflow(336, name="AR all fields")

    @responses.activate
    def test_reassign_task(self, scw_api):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/steps/1234/tasks/1234/reassign/1",
        )
        r = scw_api.reassign_task(1, 1234, 1234, 1)
        assert r.ok

    @responses.activate
    def test_put_task(self, scw_api):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/steps/current/tasks/1234",
        )
        r = scw_api.put_task(1, 1234, {"id": 1234})
        assert r.ok

    @responses.activate
    def test_put_fields(self, scw_api, all_fields_field_json):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/steps/current/tasks/1234/fields",
        )
        r = scw_api.put_fields(1, 1234, all_fields_field_json)
        assert r.ok

    @responses.activate
    def test_cancel_ticket(self, scw_api):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/cancel",
        )
        r = scw_api.cancel_ticket(1, 123)
        assert r.ok

    @responses.activate
    def test_confirm_ticket(self, scw_api):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1/confirm",
        )
        r = scw_api.confirm_ticket(1)
        assert r.ok
