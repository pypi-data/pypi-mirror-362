import pytest
import responses
from dateutil import parser

from pytos2.api import ApiError


class TestRequests:
    @responses.activate
    def test_get_requests(self, ticket_requests_mock, scw):
        data = scw.get_requests("GROUP_REQUESTS", group_id=9)
        assert data[0]["id"] == 1057
        assert data[0]["type"] == "TICKET"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[0]["id"] == 10
        assert memberships[0]["name"] == "FW Operation"
        security_team = memberships[2]
        assert security_team["id"] == 9
        assert security_team["name"] == "Security Team"
        auditor = security_team["memberships"][0]["memberships"][0]
        assert auditor["id"] == 29
        assert auditor["name"] == "Auditor"

        data = scw.get_requests("MY_REQUESTS", request_id=1059)
        assert data[0]["id"] == 1059
        assert data[0]["ticket_id"] == 1046
        assert data[0]["subject"] == "Test_request_trigger10"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[0]["id"] == 10
        assert memberships[0]["name"] == "FW Operation"

        data = scw.get_requests("ALL_REQUESTS", type="TICKET")
        assert data[0]["id"] == 1059
        assert data[0]["type"] == "TICKET"
        assert data[0]["ticket_id"] == 1046
        assert data[0]["subject"] == "Test_request_trigger10"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[0]["id"] == 10
        assert memberships[0]["name"] == "FW Operation"

        data = scw.get_requests("MY_REQUESTS", ticket_status="CLOSED")
        assert data[0]["id"] == 938
        assert data[0]["type"] == "TICKET"
        assert data[0]["ticket_id"] == 952
        assert data[0]["subject"] == "RC-22"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[1]["id"] == 2
        assert memberships[1]["name"] == "Any User"

        data = scw.get_requests("ALL_REQUESTS", ticket_id=815)
        assert data[0]["id"] == 838
        assert data[0]["type"] == "TICKET"
        assert data[0]["ticket_id"] == 815
        assert data[0]["subject"] == "AD- Check Point"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[2]["id"] == 9
        assert memberships[2]["name"] == "Security Team"
        membership_level1 = memberships[2]["memberships"]
        assert membership_level1[0]["id"] == 28
        assert membership_level1[0]["name"] == "NOC"
        membership_level2 = membership_level1[0]["memberships"]
        assert membership_level2[0]["id"] == 29
        assert membership_level2[0]["name"] == "Auditor"

        data = scw.get_requests("ALL_REQUESTS", ticket_requires_attention="true")
        assert data[0]["id"] == 1041
        assert data[0]["type"] == "TICKET"
        assert data[0]["ticket_id"] == 1031
        assert data[0]["subject"] == "AR - East West traffic Azure firewall"
        assert data[0]["required_attentions"][0]["type"] == "REJECTED"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[2]["id"] == 9
        assert memberships[2]["name"] == "Security Team"
        membership_level1 = memberships[2]["memberships"]
        assert membership_level1[0]["id"] == 28
        assert membership_level1[0]["name"] == "NOC"
        membership_level2 = membership_level1[0]["memberships"]
        assert membership_level2[0]["id"] == 29
        assert membership_level2[0]["name"] == "Auditor"

        data = scw.get_requests("MY_REQUESTS", ticket_id=1046)
        assert data[0]["id"] == 1059
        assert data[0]["ticket_id"] == 1046
        assert data[0]["subject"] == "Test_request_trigger10"
        assert data[0]["priority"] == "Normal"
        assert data[0]["status"] == "IN_PROGRESS"
        expected_create_date = parser.isoparse("2024-10-10T01:04:47.629-07:00")
        assert data[0]["create_date"] == expected_create_date
        expected_update_date = parser.isoparse("2024-10-10T01:04:47.66-07:00")
        assert data[0]["update_date"] == expected_update_date
        current_step = data[0]["current_step"]
        assert current_step["id"] == 5740
        assert current_step["name"] == "Test -  Server Decommission Request"
        assert current_step["order"] == 1
        tasks = current_step["tasks"][0]
        assert tasks["id"] == 5756
        assert tasks["status"]["status"] == "ASSIGNED"
        assert tasks["handler"]["user"] == "r"
        assert tasks["handler"]["type"] == "LOCAL_USER"
        assert tasks["handler"]["first_name"] == "Henry"
        assert tasks["handler"]["last_name"] == "Carr"
        assert tasks["handler"]["id"] == 4
        task_memberships = tasks["handler"]["memberships"]
        assert task_memberships[0]["id"] == 10
        assert task_memberships[0]["name"] == "FW Operation"
        assert task_memberships[2]["id"] == 9
        assert task_memberships[2]["name"] == "Security Team"
        membership_level1 = task_memberships[2]["memberships"]
        assert membership_level1[0]["id"] == 28
        assert membership_level1[0]["name"] == "NOC"
        membership_level2 = membership_level1[0]["memberships"]
        assert membership_level2[0]["id"] == 29
        assert membership_level2[0]["name"] == "Auditor"
        assert tasks["participants"][0]["user"] == "r"
        assert tasks["participants"][0]["type"] == "LOCAL_USER"
        assert tasks["participants"][0]["first_name"] == "Henry"
        assert tasks["participants"][0]["last_name"] == "Carr"
        assert tasks["participants"][0]["id"] == 4
        participants_memberships = tasks["participants"][0]["memberships"]
        assert participants_memberships[0]["id"] == 10
        assert participants_memberships[0]["name"] == "FW Operation"
        assert participants_memberships[2]["id"] == 9
        assert participants_memberships[2]["name"] == "Security Team"
        memberships = data[0]["requester"]["memberships"]
        assert memberships[0]["id"] == 10
        assert memberships[0]["name"] == "FW Operation"

    @responses.activate
    def test_get_requests_bad_request(self, bad_ticket_requests_mock, scw):
        with pytest.raises(ApiError):
            scw.get_requests("blahblah")

    @responses.activate
    def test_cancel_request_bad_request(self, bad_ticket_requests_mock, scw):
        id = 6000
        with pytest.raises(ApiError) as exc_info:
            scw.cancel_request(id)

        assert "404" in str(exc_info.value)
        assert "There is no request with ID 6,000." in str(exc_info.value)
