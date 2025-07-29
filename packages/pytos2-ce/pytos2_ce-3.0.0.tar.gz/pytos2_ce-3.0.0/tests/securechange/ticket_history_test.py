import pytest
import json
import responses

from requests.exceptions import HTTPError

from pytos2.securechange.ticket import DesignerUpdateDeviceHistory, TicketHistory


class TestTicketHistory:
    @responses.activate
    def test_get_ticket_history(self, ticket_history_mock, scw):
        ticket_history = scw.get_ticket_history(288)
        assert ticket_history.ticket_id == 288
        assert (
            ticket_history.ticket_history_activity[0].date.strftime("%Y-%m-%dT%H:%M:%S")
            == "2023-10-03T12:36:20"
        )
        assert ticket_history.ticket_history_activity[0].performed_by == "Henry Carr"
        assert (
            ticket_history.ticket_history_activity[0].description
            == "Update field with ID 65,019 using PUT method in REST API"
        )
        assert (
            ticket_history.ticket_history_activity[0].step_name
            == "Scripted commit to selected gateways"
        )
        assert ticket_history.ticket_history_activity[0].task_name == "Default"

        with pytest.raises(ValueError):
            scw.get_ticket_history(2)
        with pytest.raises(ValueError):
            scw.get_ticket_history(3)
        with pytest.raises(ValueError):
            scw.get_ticket_history(4)

        ticket = scw.get_ticket(288)
        ticket_history = ticket.get_history()
        assert ticket_history.ticket_id == 288
        assert (
            ticket_history.ticket_history_activity[0].date.strftime("%Y-%m-%dT%H:%M:%S")
            == "2023-10-03T12:36:20"
        )

        ticket_history = scw.get_ticket_history(828)
        assert isinstance(
            ticket_history.ticket_history_activity[13], DesignerUpdateDeviceHistory
        )

    @responses.activate
    def test_ticket_history_reprs(self, ticket_history_mock, scw):
        ticket_history = scw.get_ticket_history(288)
        assert "list with" in repr(ticket_history) and "entries" in repr(ticket_history)

        ticket_history.ticket_history_activity = ""
        assert "ticket_history_activity=''" in repr(ticket_history)
