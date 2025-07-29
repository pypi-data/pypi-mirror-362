import pytest
import json

from pytos2.securechange.ticket import Ticket

from pytos2.securechange.fields import MultiAccessRequest, AccessRequest
from pytos2.securechange.risk_results import RiskAnalysisResult, RangeNetworkObject

from netaddr import IPRange


class TestRiskResults:
    @pytest.fixture
    def range_network_object(self) -> RangeNetworkObject:
        j = {"name": "TestRange", "min_ip": "192.168.1.120", "max_ip": "192.168.1.123"}
        return RangeNetworkObject.kwargify(j)

    @pytest.fixture
    def ticket(self):
        j = json.load(open("tests/securechange/json/risk_results_ticket.json"))
        return Ticket.kwargify(j)

    def test_attributes(self, ticket):
        multi_ar = ticket.steps[-1].tasks[0].fields[0]
        assert isinstance(multi_ar, MultiAccessRequest)

        ar: AccessRequest = multi_ar.access_requests[0]
        assert isinstance(ar, AccessRequest)
        result = ar.risk_analysis_result

        assert result.status == RiskAnalysisResult.RiskStatus.HAS_RISK

    def test_range_network_object(self, range_network_object):
        assert range_network_object.ip_range == IPRange(
            "192.168.1.120", "192.168.1.123"
        )
