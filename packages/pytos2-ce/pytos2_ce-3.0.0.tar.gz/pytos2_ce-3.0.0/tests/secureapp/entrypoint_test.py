from datetime import datetime
from netaddr import IPAddress
import pytest
import json
from pytos2.api import ApiError
from pytos2.secureapp.access_requests import ApplicationAccessRequest
from pytos2.secureapp.applications import ApplicationInterfaceInstance
import responses

from pytos2.secureapp.history import (
    HistoryConnectionBaseSnapshot,
    HistoryConnectionDetails,
)
from pytos2.securetrack.service_object import TCPServiceObject

from . import conftest  # noqa

from pytos2.secureapp.entrypoint import Sa
from pytos2.secureapp.application_identities import ApplicationIdentity
from dateutil.tz import tzoffset


class TestEntrypoint:
    @responses.activate
    def test_application_identities(self, sa: Sa, application_identities_mock):
        # print(dir(sa))
        identity = sa.application_identities[0]
        assert isinstance(identity, ApplicationIdentity)

    @responses.activate
    def test_application_identites_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.application_identities

    @responses.activate
    def test_applications(self, sa: Sa, applications_mock):
        applications = sa.get_applications()
        assert applications[0].id == 60
        assert (
            applications[0].connections[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126"
        )
        assert applications[0].owner and applications[0].owner.name == "r"

    @responses.activate
    def test_application(self, sa: Sa, applications_mock):
        application = sa.get_application(54)
        assert application.id == 54
        assert application.owner.name == "Jessica.Sanchez"
        assert (
            application.open_tickets[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/35"
        )

    @responses.activate
    def test_update_application(self, sa: Sa, applications_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
            status=200,
            body="",
        )

        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "There is no application with the specified ID 1337.",
                }
            },
        )

        application = sa.get_application(54)
        application.name = "New Name"

        sa.update_application(application)
        with pytest.raises(ApiError):
            sa.update_application(1337, name="New Name")

        sa.update_application(54, name="New Name", owner=7)

    @responses.activate
    def test_create_application(self, scw, sa: Sa, applications_mock, users_mock):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54"
            },
        )

        application = sa.add_application(
            name="VPN users access to RnD users", owner="r"
        )

        # Input and output don't really matter because we're mocking the response
        assert application.id == 54
        assert application.owner.name == "Jessica.Sanchez"
        assert application.name == "VPN users access to RnD users"

    @responses.activate
    def test_delete_application(self, sa: Sa, applications_mock):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "There is no application with the specified ID 1337.",
                }
            },
        )

        sa.delete_application(54)

        with pytest.raises(ApiError):
            sa.delete_application(1337)

    @responses.activate
    def test_bulk_update_applications(self, sa: Sa, applications_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/",
            status=200,
            body="",
        )

        app = sa.get_application(54)

        sa.bulk_update_applications([app])

    @responses.activate
    def test_application_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application(54)

        with pytest.raises(ValueError):
            sa.get_applications()

    @responses.activate
    def test_application_connections(self, sa: Sa, application_connections_mock):
        connections = sa.get_application_connections(60)
        assert connections[0].id == 126
        assert connections[0].name == "Connection 1"
        assert connections[0].comment == ""
        assert connections[0].external is False
        assert connections[0].sources[0].id == 762
        assert connections[0].sources[0].name == "CRM_01"
        assert connections[0].sources[0].display_name == "CRM_01"
        assert connections[0].sources[0].link.href == (
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/network_objects/762"
        )

        assert connections[0].destinations[0].id == 998
        assert connections[0].destinations[0].name == "Finance_192.168.50.100"
        assert connections[0].destinations[0].display_name == "Finance_192.168.50.100"
        assert connections[0].destinations[0].type == "host"

    @responses.activate
    def test_application_connections_extended(
        self, sa: Sa, application_connections_mock
    ):
        connections = sa.get_extended_application_connections(60)
        assert connections[0].id == 237
        assert connections[0].name == "Connection 4"
        assert connections[0].comment == ""
        assert connections[0].external is False
        assert connections[0].sources[0].id == 762
        assert connections[0].sources[0].name == "CRM_01"
        assert connections[0].sources[0].display_name == "CRM_01"
        assert connections[0].sources[0].xsi_type.value == "hostNetworkObjectDTO"

    @responses.activate
    def test_application_connection(self, sa: Sa, application_connections_mock):
        connection = sa.get_application_connection(60, 126)
        assert connection.name == "Connection 1"
        assert connection.sources[0].name == "CRM_01"

    @responses.activate
    def test_application_connection_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application_connection(60, 126)

        with pytest.raises(ValueError):
            sa.get_application_connections(60)

    @responses.activate
    def test_add_application_connection(self, sa: Sa, application_connections_mock):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126"
            },
        )

        connection = sa.add_application_connection(
            60, name="Connection 1", sources=[762]
        )

        assert connection.id == 126
        assert connection.name == "Connection 1"
        assert connection.sources[0].name == "CRM_01"
        assert connection.sources[0].id == 762
        assert connection.services[0].name == "ftp"
        assert connection.services[0].id == 44

    @responses.activate
    def test_update_application_connection(self, sa: Sa, application_connections_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126",
            status=200,
            body="",
        )

        conn = sa.get_application_connection(60, 126)
        sa.update_application_connection(60, conn)
        sa.update_application_connection(60, 126, name="New Name")

    @responses.activate
    def test_bulk_update_application_connections(
        self, sa: Sa, application_connections_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections",
            status=200,
            body="",
        )

        conn = sa.get_application_connection(60, 126)
        sa.bulk_update_application_connections(60, [conn])

    @responses.activate
    def test_delete_application_connection(self, sa: Sa, application_connections_mock):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "Connection with ID 1337 was not found for application with ID 60.",
                }
            },
        )

        sa.delete_application_connection(60, 126)

        with pytest.raises(ApiError):
            sa.delete_application_connection(60, 1337)

    @responses.activate
    def test_application_interfaces(self, sa: Sa, application_interfaces_mock):
        interfaces = sa.get_application_interfaces(242)
        assert interfaces[0].id == 31
        assert interfaces[0].name == "Interface to DNS clients"
        assert interfaces[0].comment == ""
        assert interfaces[0].is_published is False
        assert interfaces[0].application_id == 242
        assert interfaces[0].interface_connections[0].name == "DNS clients"
        assert interfaces[0].interface_connections[0].id == 494
        assert interfaces[0].interface_connections[0].open_tickets == []
        assert interfaces[0].interface_connections[0].services[0].name == "domain-udp"
        assert (
            interfaces[0].interface_connections[0].destinations[0].name
            == "DNS Server 1"
        )
        assert (
            interfaces[0].interface_connections[0].connected_servers[0].name
            == "Mail servers"
        )

    @responses.activate
    def test_get_application_interface(self, sa: Sa, application_interfaces_mock):
        # The reason these are different from above is that the data is from different
        # points in time, between which points I mutated data on the server from which
        # this data is.

        interface = sa.get_application_interface(242, 31)
        assert interface.id == 31
        assert interface.name == "Interface to DNS clients"
        assert interface.comment == ""
        assert interface.is_published is False
        assert interface.application_id == 242
        assert interface.interface_connections[0].name == "My Connection3"
        assert interface.interface_connections[0].id == 20117
        assert interface.interface_connections[0].open_tickets == []
        assert (
            interface.interface_connections[0].connected_servers[0].name
            == "Mail servers"
        )

    @responses.activate
    def test_add_application_interface(self, sa: Sa, application_interfaces_mock):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31"
            },
        )

        interface = sa.add_application_interface(
            242, name="Interface to DNS clients", comment=""
        )
        assert interface.id == 31
        assert interface.name == "Interface to DNS clients"
        assert interface.comment == ""

    @responses.activate
    def test_update_application_interface(self, sa: Sa, application_interfaces_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31",
            status=200,
            body="",
        )

        interface = sa.get_application_interface(242, 31)
        sa.update_application_interface(242, interface)

        sa.update_application_interface(242, 31, name="New Name")

    @responses.activate
    def test_delete_application_interface(self, sa: Sa, application_interfaces_mock):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "Application interface with ID 1337 was not found for application with ID 242.",
                }
            },
        )

        interface = sa.get_application_interface(242, 31)
        sa.delete_application_interface(242, 31)

        with pytest.raises(ApiError):
            sa.delete_application_interface(242, 1337)

    @responses.activate
    def test_get_application_interface_connections(
        self, sa: Sa, application_interface_connections_mock
    ):
        connections = sa.get_application_interface_connections(242, 31)
        assert connections[0].id == 20116
        assert connections[0].name == "My Connection3"
        assert connections[0].sources[0].name == "DNS Server 1"
        assert connections[0].connected_servers[0].name == "Mail servers"
        assert connections[0].services[0].name == "domain-udp"

    @responses.activate
    def test_get_application_interface_connection(
        self, sa: Sa, application_interface_connections_mock
    ):
        connection = sa.get_application_interface_connection(242, 31, 494)
        assert connection.id == 494
        assert connection.name == "DNS clients"
        assert connection.destinations[0].name == "DNS Server 1"
        assert connection.services[0].name == "domain-udp"

    @responses.activate
    def test_add_application_interface_connection(
        self, sa: Sa, application_interface_connections_mock
    ):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections/494"
            },
        )

        connection = sa.add_application_interface_connection(
            242,
            31,
            name="DNS clients",
            destinations=[4145, 4181, 5812],
            connected_servers=[4173],
            services=[28],
        )
        assert connection.id == 494
        assert connection.name == "DNS clients"

    @responses.activate
    def test_update_application_interface_connection(
        self, sa: Sa, application_interface_connections_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections/494",
            status=200,
            body="",
        )

        connection = sa.get_application_interface_connection(242, 31, 494)
        sa.update_application_interface_connection(242, 31, connection)

        with pytest.raises(ValueError):
            sa.update_application_interface_connection(
                242, 31, 494, name="New Name", destinations=[4145, 4181, 5812]
            )
        sa.update_application_interface_connection(
            242,
            31,
            494,
            name="New Name",
            destinations=[4145, 4181, 5812],
            connected_servers=[4173],
            services=[28],
            force_empty_lists=True,
        )

    @responses.activate
    def test_delete_application_interface_connection(
        self, sa: Sa, application_interface_connections_mock
    ):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections/494",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/242/application_interfaces/31/interface_connections/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "Application interface connection with ID 1337 was not found for application interface with ID 31.",
                }
            },
        )

        sa.delete_application_interface_connection(242, 31, 494)

        with pytest.raises(ApiError):
            sa.delete_application_interface_connection(242, 31, 1337)

    @responses.activate
    def test_get_application_connections_to_applications(
        self, sa: Sa, application_connections_to_applications_mock
    ):
        connections = sa.get_application_connections_to_applications(8)
        assert connections[0].id == 2
        assert connections[0].name == "AD access 01"
        assert connections[0].comment == ""
        assert connections[0].application_id == 8
        assert connections[0].connections[0].external is False
        assert connections[0].connections[0].status == "DISCONNECTED"
        assert connections[0].connections[0].id == 65
        assert connections[0].connections[0].name == "Access From AD"
        assert connections[0].connections[0].open_tickets[0].id == 21
        assert (
            connections[0].connections[0].open_tickets[0].name == "Active Directory #2"
        )

    @responses.activate
    def test_get_application_connection_to_application(
        self, sa: Sa, application_connections_to_applications_mock
    ):
        connection = sa.get_application_connection_to_application(8, 3)
        assert connection.id == 3
        assert connection.name == "AD access 02"
        assert connection.comment == ""
        assert connection.application_id == 8
        assert connection.connections[0].external is False
        assert connection.connections[0].status == "DISCONNECTED"
        assert connection.connections[0].id == 66
        assert connection.connections[0].name == "Access To AD"
        assert connection.connections[0].open_tickets[0].id == 21
        assert connection.connections[0].open_tickets[0].name == "Active Directory #2"

    @responses.activate
    def test_add_application_connection_to_application(
        self, sa: Sa, application_connections_to_applications_mock
    ):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications/3"
            },
        )

        connection = sa.add_application_connection_to_application(
            8, name="AD access 02", application_interface_id=6, servers=[8]
        )
        assert connection.id == 3

        connection = sa.add_application_connection_to_application(
            8,
            ApplicationInterfaceInstance(
                name="AD access 02", application_interface_id=6, servers=[8]
            ),
        )

        assert connection.id == 3

        with pytest.raises(ValueError):
            sa.add_application_connection_to_application(8)
        with pytest.raises(ValueError):
            sa.add_application_connection_to_application(8, name="AD access 02")

    @responses.activate
    def test_update_application_connection_to_application(
        self, sa: Sa, application_connections_to_applications_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications/3",
            status=200,
            body="",
        )

        with pytest.raises(ValueError):
            # Missing name
            sa.update_application_connection_to_application(
                8, 3, application_interface_id=6, servers=[8]
            )

        connection = sa.get_application_connection_to_application(8, 3)
        with pytest.raises(ValueError):
            sa.update_application_connection_to_application(8, connection)

        sa.update_application_connection_to_application(
            8,
            ApplicationInterfaceInstance(
                id=3, name="New Name", application_interface_id=6
            ),
        )

        with pytest.raises(ValueError):
            sa.update_application_connection_to_application(
                8, 3, name="New Name", application_interface_id=6
            )

        sa.update_application_connection_to_application(
            8, 3, name="New Name", application_interface_id=6, servers=[8]
        )

    @responses.activate
    def test_delete_application_connection_to_application(
        self, sa: Sa, application_connections_to_applications_mock
    ):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications/3",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/connections_to_applications/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "Connection to application with ID 1337 was not found for application with ID 8.",
                }
            },
        )

        sa.delete_application_connection_to_application(8, 3)

        with pytest.raises(ApiError):
            sa.delete_application_connection_to_application(8, 1337)

    @responses.activate
    def test_application_history(self, sa: Sa, application_history_mock):
        history = sa.get_application_history(60)

        assert history[0].change_description == "Connection deleted"

        assert history[0].change_details.xsi_type.value == "historyConnectionDetailsDTO"
        assert isinstance(history[0].change_details, HistoryConnectionDetails)

        assert history[0].change_details.removed_sources[0].name == "Any"
        assert history[0].change_details.removed_sources[0].id == 1
        assert history[0].change_details.removed_sources[0].display_name == "Any"
        assert (
            history[0].change_details.removed_sources[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/network_objects/1"
        )

        assert history[0].change_details.removed_destinations[0].name == "CRM_01"
        assert history[0].change_details.removed_destinations[0].id == 762
        assert (
            history[0].change_details.removed_destinations[0].display_name == "CRM_01"
        )
        assert (
            history[0].change_details.removed_destinations[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/network_objects/762"
        )

        assert history[0].change_details.removed_services[0].name == "amitay2"
        assert history[0].change_details.removed_services[0].id == 235
        assert history[0].change_details.removed_services[0].display_name == "amitay2"
        assert (
            history[0].change_details.removed_services[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/services/235"
        )

        assert history[0].date == datetime(
            2024, 4, 15, 3, 26, 57, 257000, tzinfo=tzoffset(None, -25200)
        )
        assert history[0].modified_object.display_name == "Connection 2"
        assert history[0].modified_object.id == 203
        assert (
            history[0].modified_object.link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/203"
        )
        assert history[0].modified_object.name == "Connection 2"
        assert history[0].snapshot.comment == ""
        assert history[0].snapshot.id == 203
        assert history[0].snapshot.name == "Connection 2"

        assert isinstance(history[0].snapshot, HistoryConnectionBaseSnapshot)
        assert history[0].snapshot.xsi_type.value == "historyConnectionDTO"

        assert history[0].type == "Connection"
        assert history[0].user.display_name == "Henry Carr"
        assert history[0].user.id == 4
        assert (
            history[0].user.link.href
            == "https://198.18.0.1/securechangeworkflow/api/securechange/users/4"
        )
        assert history[0].user.name == "Henry Carr"

        assert "Connection changed" in history[3].change_description
        assert history[3].snapshot.id == 236
        assert history[3].snapshot.name == "Connection 3"
        assert history[3].snapshot.services[0].name == "http"
        assert isinstance(history[3].snapshot.services[0], TCPServiceObject)
        assert history[3].snapshot.services[0].min_port == 80
        assert history[3].snapshot.services[0].max_port == 80
        assert history[3].snapshot.services[0].protocol == 6

        assert history[3].snapshot.destinations[0].name == "CRM_01"
        assert history[3].snapshot.destinations[0].ip == IPAddress("192.168.205.33")

        # Covering empty case in find_in_detail_list
        assert history[4].change_details.removed_sources == []

        assert history[4].change_details.added_destinations[0].id == 3245
        assert history[4].change_details.added_destinations[0].name == "EDL_server2"
        assert (
            history[4].change_details.added_destinations[0].display_name
            == "EDL_server2"
        )

        assert history[5].change_details.added_services[0].id == 233
        assert history[5].change_details.added_services[0].name == "amitay5"

        assert history[11].change_details.added_sources[0].id == 3244
        assert history[11].change_details.added_sources[0].name == "EDL_subnet"

    @responses.activate
    def test_application_history_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application_history(60)

    @responses.activate
    def test_get_application_access_requests(
        self, sa: Sa, application_access_requests_mock
    ):
        requests = sa.get_application_access_requests(8)

        assert requests[0].id == 1
        assert requests[0].server_group_id == 412
        assert requests[0].server_group_name == "Sales"
        assert requests[0].server_ip == IPAddress("1.1.1.1")
        assert requests[0].comment == ""
        assert requests[0].action.value == "OPENED"

    @responses.activate
    def test_get_application_access_request(
        self, sa: Sa, application_access_requests_mock
    ):
        request = sa.get_application_access_request(8, 1)

        assert request.id == 1
        assert request.server_group_id == 412
        assert request.server_group_name == "Sales"
        assert request.server_ip == IPAddress("1.1.1.1")
        assert request.comment == ""
        assert request.action.value == "OPENED"

    @responses.activate
    def test_add_application_access_request(
        self, sa: Sa, application_access_requests_mock
    ):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1"
            },
        )

        request = sa.add_application_access_request(
            8, server_group_id=412, server_ip="1.1.1.1"
        )

        assert request.id == 1
        assert request.server_group_id == 412
        assert request.server_group_name == "Sales"

    @responses.activate
    def test_approve_application_access_request(
        self, sa: Sa, application_access_requests_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1",
            status=200,
            body="",
        )

        request = sa.get_application_access_request(8, 1)
        sa.approve_application_access_request(8, 1)
        sa.approve_application_access_request(8, request)

        with pytest.raises(ValueError):
            sa.approve_application_access_request(
                8, ApplicationAccessRequest(action="APPROVE")
            )

    @responses.activate
    def test_reject_application_access_request(
        self, sa: Sa, application_access_requests_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1",
            status=200,
            body="",
        )

        request = sa.get_application_access_request(8, 1)
        sa.reject_application_access_request(8, 1)
        sa.reject_application_access_request(8, request)

        with pytest.raises(ValueError):
            sa.reject_application_access_request(
                8, ApplicationAccessRequest(action="REJECT")
            )

    @responses.activate
    def test_bulk_update_application_access_requests(
        self, sa: Sa, application_access_requests_mock
    ):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests",
            status=200,
            body="",
        )

        sa.bulk_update_application_access_requests(
            8, [ApplicationAccessRequest(id=1, action="APPROVE")]
        )

        with pytest.raises(ValueError):
            sa.bulk_update_application_access_requests(
                8, [ApplicationAccessRequest(id=1, action="OPENED")]
            )

    @responses.activate
    def test_repair_connection(self, sa: Sa, application_connections_mock):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126/repair",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1067"
            },
        )

        with open("tests/securechange/json/ticket/ticket-1067.json") as f:
            ticket_json = json.load(f)

        responses.add(
            responses.GET,
            "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/1067",
            json=ticket_json,
        )

        ticket = sa.repair_connection(
            60, 126, "Firewall Change Request Workflow", "Repairing connection"
        )
        assert ticket.id == 1067
        assert ticket.workflow.name == "Firewall Change Request Workflow"

        assert ticket.last_task.access_request.name == "Required Access"
