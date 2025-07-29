import sys
import os

import responses
import pytest
from requests.exceptions import HTTPError
from pytos2.securechange.trigger import (
    on_create,
    on_test,
    on_advance,
    on_redo,
    on_resubmit,
    on_reopen,
    on_automation_failure,
    on_reject,
    on_cancel,
    on_close,
    _get_ticket_info_from_stdin,
    get_ticket_id_from_ticket_info,
    workflow_is,
    step_is,
)
import pytos2.securechange.trigger

from pytos2.securechange.ticket import Ticket
from pytos2.securechange.trigger import Trigger, TEST, CREATE, ADVANCE, NONE
from pytos2.securechange import trigger

from .conftest import MockExit


@pytest.fixture
def nonexistent_ticket_mock(monkeypatch, scw, all_fields_ticket_json):
    with monkeypatch.context() as m:
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/9999",
            status=404,
        )

        m.setattr(
            sys.stdin,
            "read",
            lambda: "<ticket_info><id>9999</id><open_request_stage/><current_stage><name>Duplicate</name></current_stage></ticket_info>",
        )
        m.setattr(sys.stdin, "isatty", lambda: False)
        yield m


@pytest.fixture
def ticket_mock(monkeypatch, scw, all_fields_ticket_json):
    with monkeypatch.context() as m:
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json=all_fields_ticket_json,
        )

        m.setattr(
            sys.stdin,
            "read",
            lambda: "<ticket_info><id>288</id><open_request_stage/><current_stage><name>Duplicate</name></current_stage></ticket_info>",
        )
        m.setattr(sys.stdin, "isatty", lambda: False)
        yield m


@pytest.fixture
def invalid_stdin_ticket_mock(monkeypatch, scw, all_fields_ticket_json):
    with monkeypatch.context() as m:
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json=all_fields_ticket_json,
        )

        m.setattr(
            sys.stdin,
            "read",
            lambda: "<ticket__info><id>288</id><open_request_stage/><current_stage><name>Duplicate</name></current_stage></ticket__info>",
        )
        m.setattr(sys.stdin, "isatty", lambda: False)
        yield m


@pytest.fixture
def invalid_xml_ticket_mock(monkeypatch, scw, all_fields_ticket_json):
    with monkeypatch.context() as m:
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json=all_fields_ticket_json,
        )

        m.setattr(
            sys.stdin,
            "read",
            lambda: '{ "ticket_info": { "id": 288, "open_request_stage": null, "current_stage": { "name": Duplicate" } } }',
        )
        m.setattr(sys.stdin, "isatty", lambda: False)
        yield m


@pytest.fixture
def isatty_ticket_mock(monkeypatch, scw, all_fields_ticket_json):
    with monkeypatch.context() as m:
        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/288",
            json=all_fields_ticket_json,
        )

        m.setattr(sys.stdin, "read", lambda: "")

        m.setattr(sys.stdin, "isatty", lambda: True)
        yield m


class TestTriggerMethods:
    def test_str(self):
        tr = TEST | CREATE

        assert str(tr) == "Test or Create Triggers"

    def test_repr(self):
        tr = TEST | CREATE

        assert repr(tr) == "TEST|CREATE"

    @responses.activate
    def test_get_ticket_id_from_ticket_info(self, ticket_mock):
        ticket_info = _get_ticket_info_from_stdin()()

        ticket_id = get_ticket_id_from_ticket_info(ticket_info)
        assert ticket_id == 288

    @responses.activate
    def test_get_ticket_id_from_invalid_ticket_info(self, invalid_stdin_ticket_mock):
        ticket_info = _get_ticket_info_from_stdin()()

        ticket_id = get_ticket_id_from_ticket_info(ticket_info)
        assert ticket_id is None

    def test_or_contains(self):
        tr = TEST | CREATE

        assert TEST in tr
        assert CREATE in tr

        tr |= TEST
        assert TEST in tr

        tr2 = TEST | CREATE | ADVANCE

        tr3 = tr | tr2
        tr4 = tr2 | tr

        assert tr2 in tr3
        assert tr2 in tr4

        assert CREATE in tr3
        assert CREATE in tr4

        tr5 = NONE | NONE
        assert CREATE not in tr5

        tr6 = tr | tr
        assert tr6 is tr

        tr7 = TEST | NONE

        assert tr7 == TEST


class TestTriggers:
    def setup_method(self, method):
        pytos2.securechange.trigger.get_ticket_info_from_stdin = (
            _get_ticket_info_from_stdin()
        )

    @responses.activate
    def test_nonexistent_ticket(self, monkeypatch, nonexistent_ticket_mock):
        nonexistent_ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        with pytest.raises(HTTPError):

            @on_advance(when=workflow_is("Fake") or step_is("Fake"))
            def f(ticket):
                results["ticket"] = ticket

    def test_isatty(self, isatty_ticket_mock):
        isatty_ticket_mock.setenv("SCW_EVENT", "ADVANCE")

        ticket_info = _get_ticket_info_from_stdin()()
        assert ticket_info is None

    @responses.activate
    def test_invalid_stdin_ticket(self, invalid_stdin_ticket_mock):
        invalid_stdin_ticket_mock.setenv("SCW_EVENT", "TEST")

        ticket_info = _get_ticket_info_from_stdin()()

        assert ticket_info is None

    @responses.activate
    def test_invalid_xml_ticket(self, invalid_xml_ticket_mock):
        invalid_xml_ticket_mock.setenv("SCW_EVENT", "TEST")

        ticket_info = _get_ticket_info_from_stdin()()

        assert ticket_info is None

    @responses.activate
    def test_step_is_matching(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        @on_advance(when=step_is("No Fields"))
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_step_is_not_matching(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        @on_advance(when=step_is("All Fields"))
        def f(ticket):
            results["ticket"] = ticket

        assert results.get("ticket") is None

    @responses.activate
    def test_workflow_is_matching(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        @on_advance(when=workflow_is("AR all fields"))
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_workflow_is_not_matching(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        @on_advance(when=workflow_is("Fake Workflow"))
        def f(ticket):
            results["ticket"] = ticket

        assert results.get("ticket") is None

    @responses.activate
    def test_cached_std_info(self, ticket_mock):
        get_ticket_info = _get_ticket_info_from_stdin()

        ticket_info = get_ticket_info()
        ticket_id = get_ticket_id_from_ticket_info(ticket_info)
        assert ticket_id == 288

        # Hits the cached std_info if-then
        ticket_info = get_ticket_info()
        ticket_id = get_ticket_id_from_ticket_info(ticket_info)
        assert ticket_id == 288

    @responses.activate
    def test_on_test(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "TEST")
        results = {}

        @on_test
        def f(ticket):
            results["ticket"] = ticket

        assert results.get("ticket") is None

    @responses.activate
    def test_on_create(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "CREATE")
        results = {}

        @on_create
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_advance(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "ADVANCE")
        results = {}

        @on_advance
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_redo(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "REDO")
        results = {}

        @on_redo
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_resubmit(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "RESUBMIT")
        results = {}

        @on_resubmit
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_reopen(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "REOPEN")
        results = {}

        @on_reopen
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_automation_failure(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "AUTOMATION_FAILED")
        results = {}

        @on_automation_failure
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_reject(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "REJECT")
        results = {}

        @on_reject
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_cancel(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "CANCEL")
        results = {}

        @on_cancel
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)

    @responses.activate
    def test_on_close(self, ticket_mock):
        ticket_mock.setenv("SCW_EVENT", "CLOSE")
        results = {}

        @on_close
        def f(ticket):
            results["ticket"] = ticket

        assert isinstance(results.get("ticket"), Ticket)


class TestTrigger:
    def test_none(self):
        assert str(Trigger.from_scw_event(123)) == "No Trigger"

    def test_contains_none(self):
        t = trigger.ADVANCE
        assert None not in t
