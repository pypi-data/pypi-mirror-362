from datetime import date, datetime
from types import EllipsisType
from typing import Union, Optional, List

from netaddr import IPAddress
from requests import Response
from requests.exceptions import HTTPError

# avoid circular imports
import pytos2
from pytos2.api import ApiError, SdkError
from pytos2.models import DateFilterType, coerce_date_filter_type
from pytos2.secureapp.access_requests import ApplicationAccessRequest
from pytos2.securechange.ticket import Ticket  # noqa
from .api import SaAPI
from pytos2.utils import NoInstance, get_api_node
from .application_identities import ApplicationIdentity
from .applications import (
    Application,
    ApplicationConnection,
    ApplicationInterface,
    ApplicationInterfaceInstance,
    ApplicationInterfaceInstanceGet,
    Connection,
    ExtendedApplicationConnection,
    InterfaceConnection,
)
from .network_object import NetworkObject
from .service_object import Service
from .history import HistoryRecord
from pytos2.securechange.user import SCWUser
from pytos2.securechange.fields import Field
from pytos2.models import ObjectReference


class Sa:
    default: Union["Sa", NoInstance] = NoInstance(
        "Sa.default",
        "No Sa instance has been initialized yet, initialize with `Sa(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
    ):
        self.api: SaAPI = SaAPI(hostname, username, password)
        if default:
            Sa.default = self

        self._application_identities: List[ApplicationIdentity] = []

    @property
    def application_identities(self) -> List[ApplicationIdentity]:
        if not self._application_identities:
            res = self._get_application_identities()
            self._application_identities = res
        return self._application_identities

    def _get_application_identities(self, cache=True) -> List[ApplicationIdentity]:
        res = self.api.get_application_identities()
        data = self.api.handle_json(res, "application_identities")
        return [
            ApplicationIdentity.kwargify(a)
            for a in get_api_node(
                data, "application_identities.application_identity", listify=True
            )
        ]

    def get_applications(self) -> List[Application]:
        """
        This function returns a list of all applications in SecureApp.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications

        Usage:
            apps = sa.get_applications()
        """

        res = self.api.get_applications()
        data = self.api.handle_json(res, "get_applications")
        return [
            Application.kwargify(a)
            for a in get_api_node(data, "applications.application", listify=True)
        ]

    def get_application(self, application_id: str) -> Application:
        """
        This function returns a single application by its ID.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            app = sa.get_application(60)
        """

        res = self.api.get_application(application_id)
        data = self.api.handle_json(res, "get_application")
        application = get_api_node(data, "application")
        if isinstance(application, list) and application:
            application = application[0]

        return Application.kwargify(application)

    def add_application(
        self,
        application: Optional[Application] = None,
        /,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        owner: Union[None, SCWUser, int, str] = None,
        editors: Optional[List[Union[SCWUser, int]]] = None,
        viewers: Optional[List[Union[SCWUser, int]]] = None,
        customer: Optional[
            int
        ] = None,  # TODO: Add customer to this once it's implemented.
    ):
        """
        This function creates a new application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications

        Usage:
            Example 1:
            app = sa.add_application(name="My App", comment="This is my app")

            Example 2:
            app = sa.add_application(
                name="My App",
                owner=100,
                editors=[101, 102],
                viewers=[103, 104]
            )
        """

        from pytos2.securechange import Scw

        if not application:
            if isinstance(owner, str):
                owner = Scw.default.get_user(owner)
            if owner:
                owner = owner if isinstance(owner, int) else owner.id

            editors = editors or []
            viewers = viewers or []

            editors = [e if isinstance(e, int) else e.id for e in editors]
            viewers = [v if isinstance(v, int) else v.id for v in viewers]

            application = Application(
                name=name,
                comment=comment,
                owner=ObjectReference(id=owner) if owner else None,
                editors=[ObjectReference(id=e.id) for e in editors],
                viewers=[ObjectReference(id=v.id) for v in viewers],
                customer=ObjectReference(id=customer) if customer else None,
            )

        res = self.api.add_application(application._json)
        return self.api.handle_creation(res, "add_application", cls=Application)

    def update_application(
        self,
        application_id: Union[int, Application],
        name: Optional[str] = None,
        comment: Optional[str] = None,
        owner: Union[None, SCWUser, int] = None,
        editors: Optional[List[Union[SCWUser, int]]] = None,
        viewers: Optional[List[Union[SCWUser, int]]] = None,
    ):
        """
        This function updates an existing application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            Example 1:
            sa.update_application(60, name="My App", comment="This is my app")

            Example 2:
            sa.update_application(
                60,
                name="My App",
                owner=100,
                editors=[101, 102],
                viewers=[103, 104]
            )
        """
        if owner:
            owner = owner if isinstance(owner, int) else owner.id

        editors = (
            [e if isinstance(e, int) else e.id for e in editors] if editors else None
        )
        viewers = (
            [v if isinstance(v, int) else v.id for v in viewers] if viewers else None
        )

        if isinstance(application_id, Application):
            app = application_id
            application_id = app.id
        else:
            app = Application(
                name=name,
                comment=comment,
                owner=ObjectReference(id=owner) if owner else None,
                editors=(
                    [ObjectReference(id=e.id) for e in editors] if editors else None
                ),
                viewers=(
                    [ObjectReference(id=v.id) for v in viewers] if viewers else None
                ),
            )

        res = self.api.update_application(application_id, app._json)
        res = self.api.handle_response(res, "update_application", action="update")

    def delete_application(self, application_id: int):
        """
        This function deletes an application by its ID.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            sa.delete_application(60)
        """

        res = self.api.delete_application(application_id)
        self.api.handle_response(res, "delete_application", action="delete")

    def bulk_update_applications(self, apps: List[Application]):
        res = self.api.update_applications([a._json for a in apps])
        self.api.handle_response(res, "bulk_update_applications", action="update")

    def get_application_connections(
        self, application_id: int
    ) -> List[ApplicationConnection]:
        """
        This function returns a list of all connections for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections

        Usage:
            connections = sa.get_application_connections(60)
        """

        res = self.api.get_application_connections(application_id)
        data = self.api.handle_json(res, "get_application_connections")
        connections = get_api_node(data, "connections.connection", listify=True)
        return [ApplicationConnection.kwargify(c) for c in connections]

    def get_application_connection(
        self, application_id: int, connection_id: int
    ) -> ApplicationConnection:
        """
        This function returns a single connection for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections/100

        Usage:
            connection = sa.get_application_connection(60, 100)
        """

        res = self.api.get_application_connection(application_id, connection_id)
        data = self.api.handle_json(res, "get_application_connection")
        conn = get_api_node(data, "connection")
        return ApplicationConnection.kwargify(conn)

    def get_extended_application_connections(
        self, application_id: int
    ) -> List[ApplicationConnection]:
        """
        This function returns a list of all extended connections for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_extended

        Usage:
            connections = sa.get_extended_application_connections(60)
        """

        res = self.api.get_extended_application_connections(application_id)
        data = self.api.handle_json(res, "get_extended_application_connections")
        connections = get_api_node(
            data, "connections_extended.connection_extended", listify=True
        )
        return [ExtendedApplicationConnection.kwargify(c) for c in connections]

    def add_application_connection(
        self,
        application_id: int,
        connection: Optional[ApplicationConnection] = None,
        /,
        *,
        services: Optional[List[Union[Service, ObjectReference, int]]] = None,
        sources: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        destinations: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        status: Optional[str] = None,
        external: Optional[bool] = None,
        connection_to_application: Union[None, ObjectReference, int] = None,
        comment: Optional[str] = None,
        uid: Optional[str] = None,
        open_tickets: Optional[List[Union[ObjectReference, int]]] = None,
        name: Optional[str] = None,
    ):
        """
        This function creates a new connection for a given application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections

        Usage:
            Example 1:
            sa.add_application_connection(
                60,
                services=[Service(id=1), Service(id=2)],
                sources=[NetworkObject(id=1), NetworkObject(id=2)],
                destinations=[NetworkObject(id=3), NetworkObject(id=4)],
            )

            Example 2:
            sa.add_application_connection(
                60,
                connection=ApplicationConnection(
                    services=[Service(id=1), Service(id=2)],
                    sources=[NetworkObject(id=1), NetworkObject(id=2)],
                    destinations=[NetworkObject(id=3), NetworkObject(id=4)],
                )
            )
        """

        services = (
            [s if isinstance(s, int) else s.id for s in services] if services else []
        )
        sources = (
            [s if isinstance(s, int) else s.id for s in sources] if sources else []
        )
        destinations = (
            [d if isinstance(d, int) else d.id for d in destinations]
            if destinations
            else []
        )
        connection_to_application = (
            (
                connection_to_application.id
                if isinstance(connection_to_application, ObjectReference)
                else connection_to_application
            )
            if connection_to_application
            else []
        )
        open_tickets = (
            [t if isinstance(t, int) else t.id for t in open_tickets]
            if open_tickets
            else []
        )

        if not connection:
            connection = ApplicationConnection(
                services=[ObjectReference(id=s) for s in services],
                sources=[ObjectReference(id=s) for s in sources],
                destinations=[ObjectReference(id=d) for d in destinations],
                status=status,
                external=external,
                connection_to_application=ObjectReference(id=connection_to_application),
                comment=comment,
                uid=uid,
                open_tickets=[ObjectReference(id=t) for t in open_tickets],
                name=name,
            )
        res = self.api.add_application_connection(application_id, connection._json)
        return self.api.handle_creation(
            res, "add_application_connection", cls=ApplicationConnection
        )

    def update_application_connection(
        self,
        application_id: int,
        connection_id: Union[int, ApplicationConnection],
        /,
        *,
        services: Optional[List[Union[Service, ObjectReference, int]]] = None,
        sources: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        destinations: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        status: Optional[str] = None,
        external: Optional[bool] = None,
        connection_to_application: Union[None, ObjectReference, int] = None,
        comment: Optional[str] = None,
        uid: Optional[str] = None,
        open_tickets: Optional[List[Union[ObjectReference, int]]] = None,
        name: Optional[str] = None,
    ):
        """
        This function updates an existing connection for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections/100

        Usage:
            Example 1:
            sa.update_application_connection(
                60,
                100,
                services=[Service(id=1), Service(id=2)],
                sources=[NetworkObject(id=1), NetworkObject(id=2)],
                destinations=[NetworkObject(id=3), NetworkObject(id=4)],
            )

            Example 2:
            sa.update_application_connection(
                60,
                ApplicationConnection(
                    id=100,
                    services=[Service(id=1), Service(id=2)],
                    sources=[NetworkObject(id=1), NetworkObject(id=2)],
                    destinations=[NetworkObject(id=3), NetworkObject(id=4)],
                )
            )
        """

        if isinstance(connection_id, ApplicationConnection):
            conn = connection_id
            connection_id = conn.id
        else:
            conn = ApplicationConnection(
                services=services,
                sources=sources,
                destinations=destinations,
                status=status,
                external=external,
                connection_to_application=connection_to_application,
                comment=comment,
                uid=uid,
                open_tickets=open_tickets,
                name=name,
            )

        res = self.api.update_application_connection(
            application_id, connection_id, conn._json
        )
        self.api.handle_response(res, "update_application_connection")

    def bulk_update_application_connections(
        self, application_id: int, connections: List[ApplicationConnection]
    ):
        """
        This function updates multiple connections for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections

        Usage:
            sa.update_application_connections(60, [ApplicationConnection(id=100, status="ACTIVE")])
        """
        res = self.api.update_application_connections(
            application_id, [c._json for c in connections]
        )
        self.api.handle_response(
            res, "bulk_update_application_connections", action="update"
        )

    def delete_application_connection(self, application_id: int, connection_id: int):
        """
        This function deletes a connection for a given application.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections/100

        Usage:
            sa.delete_application_connection(60, 100)
        """

        res = self.api.delete_application_connection(application_id, connection_id)
        self.api.handle_response(res, "delete_application_connection", action="delete")

    def get_application_interfaces(self, application_id: int):
        """
        This function returns a list of all interfaces for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces

        Usage:
            interfaces = sa.get_application_interfaces(60)

        """

        res = self.api.get_application_interfaces(application_id)
        data = self.api.handle_json(res, "get_application_interfaces")
        interfaces = get_api_node(
            data, "application_interfaces.application_interface", listify=True
        )
        return [ApplicationInterface.kwargify(i) for i in interfaces]

    def get_application_interface(self, application_id: int, interface_id: int):
        """
        This function returns a single interface for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/242/interfaces/31

        Usage:
            interface = sa.get_application_interface(242, 31)
        """

        res = self.api.get_application_interface(application_id, interface_id)
        data = self.api.handle_json(res, "get_application_interface")
        data = get_api_node(data, "application_interface")

        if isinstance(data, list) and data:
            data = data[0]

        return ApplicationInterface.kwargify(data)

    def add_application_interface(
        self,
        application_id: int,
        interface: Optional[ApplicationInterface] = None,
        /,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
    ):
        """
        This function creates a new interface for a given application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces

        Usage:
            Example 1:
            sa.add_application_interface(
                60,
                name="My Interface",
                comment="This is my interface",
            )

            Example 2:
            sa.add_application_interface(
                60,
                ApplicationInterface(
                    name="My Interface",
                    comment="This is my interface",
                )
            )
        """

        interface = (
            ApplicationInterface(
                name=name,
                comment=comment,
            )
            if interface is None
            else interface
        )

        res = self.api.add_application_interface(application_id, interface._json)
        return self.api.handle_creation(
            res, "add_application_interface", cls=ApplicationInterface
        )

    def update_application_interface(
        self,
        application_id: int,
        interface_id: int | ApplicationInterface,
        /,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        is_published: Optional[bool] = None,
    ):
        """
        This function updates an existing interface for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces/31

        Usage:
            Example 1:
            sa.update_application_interface(
                60,
                31,
                name="My Interface",
                comment="This is my interface",
                is_published=True,
            )

            Example 2:
            sa.update_application_interface(
                60,
                ApplicationInterface(
                    id=31,
                    name="My Interface",
                    comment="This is my interface",
                    is_published=True,
                )
            )
        """

        if isinstance(interface_id, ApplicationInterface):
            interface = interface_id
            interface_id = interface_id.id
        else:
            interface = ApplicationInterface(
                name=name,
                comment=comment,
                is_published=is_published,
            )

        res = self.api.update_application_interface(
            application_id, interface_id, interface._json
        )
        self.api.handle_response(res, "update_application_interface", action="update")

    def delete_application_interface(self, application_id: int, interface_id: int):
        """
        This function deletes an interface for a given application.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/242/interfaces/31

        Usage:
            sa.delete_application_interface(242, 31)
        """

        res = self.api.delete_application_interface(application_id, interface_id)
        self.api.handle_response(res, "delete_application_interface", action="delete")

    def get_application_interface_connections(
        self, application_id: int, interface_id: int
    ):
        """
        This function returns a list of all connections for a given interface and application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces/31/connections

        Usage:
            connections = sa.get_application_interface_connections(60, 31)
        """

        res = self.api.get_application_interface_connections(
            application_id, interface_id
        )
        data = self.api.handle_json(res, "get_application_interface_connections")
        connections = get_api_node(
            data, "interface_connections.interface_connection", listify=True
        )
        return [InterfaceConnection.kwargify(c) for c in connections]

    # FIXME: Check all the updates and make sure they actually update like they're supposed to.

    def get_application_interface_connection(
        self, application_id: int, interface_id: int, connection_id: int
    ):
        """
        This function returns a single connection for a given interface and application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/242/interfaces/31/connections/494

        Usage:
            connection = sa.get_application_interface_connection(242, 31, 494)
        """

        res = self.api.get_application_interface_connection(
            application_id, interface_id, connection_id
        )
        data = self.api.handle_json(res, "get_application_interface_connection")
        data = get_api_node(data, "interface_connection")
        if isinstance(data, list) and data:
            data = data[0]

        return InterfaceConnection.kwargify(data)

    def add_application_interface_connection(
        self,
        application_id: int,
        interface_id: int,
        connection: Optional[InterfaceConnection] = None,
        /,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        services: Optional[List[Union[Service, ObjectReference, int]]] = None,
        sources: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        destinations: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        open_tickets: Optional[List[Union[ObjectReference, int]]] = None,
        connected_servers: Optional[List[Union[ObjectReference, int]]] = None,
    ):
        """
        This function creates a new connection for a given interface and application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces/31/connections

        Usage:
            Example 1:
            sa.add_application_interface_connection(
                60,
                31,
                name="My Connection",
                comment="This is my connection",
                services=[1, 2],
                sources=[NetworkObject(id=1), NetworkObject(id=2)],
                destinations=[NetworkObject(id=3), NetworkObject(id=4)],
            )

            Example 2:
            sa.add_application_interface_connection(
                60,
                31,
                InterfaceConnection(
                    name="My Connection",
                    comment="This is my connection",
                    services=[Service(id=1), Service(id=2)],
                    sources=[NetworkObject(id=1), NetworkObject(id=2)],
                    destinations=[NetworkObject(id=3), NetworkObject(id=4)],
                )
            )
        """

        services = (
            [s if isinstance(s, int) else s.id for s in services] if services else []
        )
        sources = (
            [s if isinstance(s, int) else s.id for s in sources] if sources else []
        )
        destinations = (
            [d if isinstance(d, int) else d.id for d in destinations]
            if destinations
            else []
        )
        open_tickets = (
            [t if isinstance(t, int) else t.id for t in open_tickets]
            if open_tickets
            else []
        )
        connected_servers = (
            [s if isinstance(s, int) else s.id for s in connected_servers]
            if connected_servers
            else []
        )

        if not connection:
            connection = InterfaceConnection(
                name=name,
                comment=comment,
                services=[ObjectReference(id=s) for s in services],
                sources=[ObjectReference(id=s) for s in sources],
                destinations=[ObjectReference(id=d) for d in destinations],
                open_tickets=[ObjectReference(id=t) for t in open_tickets],
                connected_servers=[ObjectReference(id=s) for s in connected_servers],
            )

        res = self.api.add_application_interface_connection(
            application_id, interface_id, connection._json
        )
        return self.api.handle_creation(
            res, "add_application_interface_connection", cls=InterfaceConnection
        )

    def update_application_interface_connection(
        self,
        application_id: int,
        interface_id: int,
        connection_id: int | InterfaceConnection,
        /,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        services: Optional[List[Union[Service, ObjectReference, int]]] = None,
        sources: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        destinations: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        open_tickets: Optional[List[Union[ObjectReference, int]]] = None,
        connected_servers: Optional[List[Union[ObjectReference, int]]] = None,
        force_empty_lists: bool = False,
    ):
        """
        This function updates an existing connection for a given interface and application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces/31/connections/494

        Usage:
            Example 1:
            sa.update_application_interface_connection(
                60,
                31,
                494,
                name="My Connection",
                comment="This is my connection",
                services=[1, 2],
                sources=[NetworkObject(id=1), NetworkObject(id=2)],
                destinations=[NetworkObject(id=3), NetworkObject(id=4)],
            )

            Example 2:
            sa.update_application_interface_connection(
                60,
                31,
                InterfaceConnection(
                    id=494,
                    name="My Connection",
                    comment="This is my connection",
                    services=[Service(id=1), Service(id=2)],
                    sources=[NetworkObject(id=1), NetworkObject(id=2)],
                    destinations=[NetworkObject(id=3), NetworkObject(id=4)],
                )
            )
        """

        connection = None
        if isinstance(connection_id, InterfaceConnection):
            connection = connection_id
            connection_id = connection_id.id
        else:
            services = (
                [s if isinstance(s, int) else s.id for s in services]
                if services
                else []
            )
            sources = (
                [s if isinstance(s, int) else s.id for s in sources] if sources else []
            )
            destinations = (
                [d if isinstance(d, int) else d.id for d in destinations]
                if destinations
                else []
            )
            open_tickets = (
                [t if isinstance(t, int) else t.id for t in open_tickets]
                if open_tickets
                else []
            )
            connected_servers = (
                [s if isinstance(s, int) else s.id for s in connected_servers]
                if connected_servers
                else []
            )

            if not force_empty_lists and (
                not services or not sources or not destinations
            ):
                raise ValueError(
                    "services, sources, and destinations should not be empty. They will be overwritten. If this was intentional, set force_empty_lists=True"
                )

            connection = InterfaceConnection(
                name=name,
                comment=comment,
                services=[ObjectReference(id=s) for s in services],
                sources=[ObjectReference(id=s) for s in sources],
                destinations=[ObjectReference(id=d) for d in destinations],
                open_tickets=[ObjectReference(id=t) for t in open_tickets],
                connected_servers=[ObjectReference(id=s) for s in connected_servers],
            )

        res = self.api.update_application_interface_connection(
            application_id, interface_id, connection_id, connection._json
        )
        self.api.handle_response(
            res, "update_application_interface_connection", action="update"
        )

    def delete_application_interface_connection(
        self, application_id: int, interface_id: int, connection_id: int
    ):
        """
        This function deletes a connection for a given interface and application.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/interfaces/31/connections/494

        Usage:
            sa.delete_application_interface_connection(60, 31, 494)
        """

        res = self.api.delete_application_interface_connection(
            application_id, interface_id, connection_id
        )
        self.api.handle_response(
            res, "delete_application_interface_connection", action="delete"
        )

    def get_application_connections_to_applications(self, application_id: int):
        """
        This function returns a list of all connections to other applications for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_to_applications

        Usage:
            connections = sa.get_application_connections_to_applications(60)
        """

        res = self.api.get_application_connections_to_applications(application_id)
        data = self.api.handle_json(res, "get_application_connections_to_applications")
        connections = get_api_node(
            data, "connections_to_applications.connection_to_application", listify=True
        )
        return [ApplicationInterfaceInstanceGet.kwargify(c) for c in connections]

    def get_application_connection_to_application(
        self, application_id: int, connection_id: int
    ):
        """
        This function returns a single connection to another application for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_to_applications/100

        Usage:
            connection = sa.get_application_connection_to_application(60, 100)
        """

        res = self.api.get_application_connection_to_application(
            application_id, connection_id
        )
        data = self.api.handle_json(res, "get_application_connection_to_application")
        data = get_api_node(data, "connection_to_application")
        if isinstance(data, list) and data:
            data = data[0]

        return ApplicationInterfaceInstanceGet.kwargify(data)

    def add_application_connection_to_application(
        self,
        application_id: int,
        conn: ApplicationInterfaceInstance | None = None,
        /,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        servers: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        application_interface_id: Optional[int] = None,
    ):
        """
        This function creates a new connection to another application for a given application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_to_applications

        Usage:
            Example 1:
            sa.add_application_connection_to_application(
                60,
                name="My Connection",
                comment="This is my connection",
                servers=[1],
                application_interface_id=100,
            )

            Example 2:
            sa.add_application_connection_to_application(
                60,
                ApplicationInterfaceInstance(
                    name="My Connection",
                    comment="This is my connection",
                    servers=[ObjectReference(id=1)],
                    application_interface_id=100,
                )
            )
        """

        servers = (
            [s if isinstance(s, int) else s.id for s in servers] if servers else []
        )

        if not conn:
            conn = ApplicationInterfaceInstance(
                comment=comment,
                name=name,
                servers=[ObjectReference(id=s) for s in servers],
                application_interface_id=application_interface_id,
            )

        if not conn.name:
            raise ValueError("name is required")
        if not conn.application_interface_id:
            raise ValueError("application_interface_id is required")

        res = self.api.add_application_connection_to_application(
            application_id, conn._json
        )
        return self.api.handle_creation(
            res,
            "add_application_connection_to_application",
            cls=ApplicationInterfaceInstanceGet,
        )

    def update_application_connection_to_application(
        self,
        application_id: int,
        connection_id: int | ApplicationInterfaceInstance,
        /,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        servers: Optional[List[Union[NetworkObject, ObjectReference, int]]] = None,
        application_interface_id: Optional[int] = None,
        force_empty_servers: bool = False,
    ):
        """
        This function updates an existing connection to another application for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_to_applications/100

        Usage:
            Example 1:
            sa.update_application_connection_to_application(
                60,
                100,
                name="My Connection",
                comment="This is my connection",
                connections=[Connection(services=[ObjectReference(id=1)])],
            )

            Example 2:
            sa.update_application_connection_to_application(
                60,
                ApplicationInterfaceInstance(
                    id=100,
                    name="My Connection",
                    comment="This is my connection",
                    servers=[ObjectReference(id=1)],
                    application_interface_id=100,
                )
            )
        """

        if isinstance(connection_id, ApplicationInterfaceInstanceGet):
            raise ValueError(
                "The SDK does not support updating from an ApplicationInterfaceInstanceGet object fetched from the API. Please use an ApplicationInterfaceInstance object instead."
            )

        if isinstance(connection_id, ApplicationInterfaceInstance):
            connection = connection_id
            connection_id = connection_id.id
        else:
            servers = (
                [s if isinstance(s, int) else s.id for s in servers] if servers else []
            )

            connection = ApplicationInterfaceInstance(
                comment=comment,
                name=name,
                servers=[ObjectReference(id=s) for s in servers],
                application_interface_id=application_interface_id,
            )

            if not connection.servers and not force_empty_servers:
                raise ValueError(
                    "servers is empty. If this is intentional, set force_empty_servers=True"
                )

        if connection.name is None:
            raise ValueError("name is required")

        res = self.api.update_application_connection_to_application(
            application_id, connection_id, connection._json
        )

        self.api.handle_response(
            res, "update_application_connection_to_application", action="update"
        )

    def delete_application_connection_to_application(
        self, application_id: int, connection_id: int
    ):
        """
        This function deletes a connection to another application for a given application.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections_to_applications/100

        Usage:
            sa.delete_application_connection_to_application(60, 100)
        """

        res = self.api.delete_application_connection_to_application(
            application_id, connection_id
        )
        self.api.handle_response(
            res, "delete_application_connection_to_application", action="delete"
        )

    def get_application_history(
        self,
        application_id: int,
        start_date: DateFilterType = None,
        end_date: DateFilterType = None,
        count: Optional[int] = None,
        start: Optional[int] = None,
        type: Optional[str] = None,
        user: Optional[str] = None,
        show_members: Optional[bool] = None,
    ):
        """
        This function returns the history of a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/history

        Usage:
            history = sa.get_application_history(60)
        """

        start_date = coerce_date_filter_type(start_date)
        end_date = coerce_date_filter_type(end_date)

        res = self.api.get_application_history(
            application_id,
            start_date=start_date,
            end_date=end_date,
            count=count,
            start=start,
            type=type,
            user=user,
            show_members=show_members,
        )
        data = self.api.handle_json(res, "get_application_history")
        history = get_api_node(data, "history_records.history_record", listify=True)
        return [HistoryRecord.kwargify(h) for h in history]

    def get_application_access_requests(self, application_id: int):
        """
        This function returns a list of all access requests for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/application_access_requests

        Usage:
            access_requests = sa.get_application_access_requests(60)
        """

        res = self.api.get_application_access_requests(application_id)
        data = self.api.handle_json(res, "get_application_access_requests")
        return [
            ApplicationAccessRequest.kwargify(a)
            for a in get_api_node(
                data,
                "application_access_requests.application_access_request",
                listify=True,
            )
        ]

    def get_application_access_request(self, application_id: int, request_id: int):
        """
        This function returns a single access request for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1

        Usage:
            access_request = sa.get_application_access_request(8, 1)
        """

        res = self.api.get_application_access_request(application_id, request_id)
        data = self.api.handle_json(res, "get_application_access_request")
        data = get_api_node(data, "application_access_request")
        return ApplicationAccessRequest.kwargify(
            data[0] if isinstance(data, list) else data
        )

    def add_application_access_request(
        self,
        application_id: int,
        request: Optional[ApplicationAccessRequest] = None,
        /,
        *,
        comment: Optional[str] = None,
        action: Optional[str] = None,
        server_ip: Optional[str | IPAddress] = None,
        server_group_id: Optional[str | int] = None,
        server_group_name: Optional[str] = None,
    ):
        """
        This function creates a new access request for a given application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/application_access_requests

        Usage:
            Example 1:
            sa.add_application_access_request(
                8,
                comment="Please grant me access to this application",
                server_ip='1.1.2.2',
                server_group_id='1',
            )

            Example 2:
            sa.add_application_access_request(
                8,
                request=ApplicationAccessRequest(
                    comment="Please grant me access to this application",
                    server_ip='1.1.2.2',
                    server_group_id='1',
                ),
            )

        """

        request = (
            ApplicationAccessRequest(
                comment=comment,
                action=action,
                server_ip=server_ip,
                server_group_id=server_group_id,
                server_group_name=server_group_name,
            )
            if request is None
            else request
        )

        res = self.api.add_application_access_request(application_id, request._json)
        return self.api.handle_creation(
            res, "add_application_access_request", cls=ApplicationAccessRequest
        )

    def approve_application_access_request(
        self, application_id: int, request_id: int | ApplicationAccessRequest
    ):
        """
        This function approves an access request for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/application_access_requests/1

        Usage:
            Example 1:
            sa.approve_application_access_request(60, 1)

            Example 2:
            sa.approve_application_access_request(60, ApplicationAccessRequest(id=1))
        """

        if isinstance(request_id, ApplicationAccessRequest):
            request_id = request_id.id
        if request_id is None:
            raise ValueError("request_id is required")

        res = self.api.update_application_access_request(
            application_id, request_id, {"action": "APPROVE"}
        )

        self.api.handle_response(
            res, "approve_application_access_request", action="update"
        )

    def reject_application_access_request(
        self, application_id: int, request_id: int | ApplicationAccessRequest
    ):
        """
        This function rejects an access request for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/application_access_requests/1

        Usage:
            Example 1:
            sa.reject_application_access_request(60, 1)

            Example 2:
            sa.reject_application_access_request(60, ApplicationAccessRequest(id=1))
        """

        if isinstance(request_id, ApplicationAccessRequest):
            request_id = request_id.id
        if request_id is None:
            raise ValueError("request_id is required")

        res = self.api.update_application_access_request(
            application_id, request_id, {"action": "REJECT"}
        )

        self.api.handle_response(
            res, "reject_application_access_request", action="update"
        )

    def bulk_update_application_access_requests(
        self, application_id: int, requests: List[ApplicationAccessRequest]
    ):
        """
        This function updates multiple access requests for a given application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/8/application_access_requests/1

        Usage:
            sa.bulk_update_application_access_requests(
                60,
                [
                    ApplicationAccessRequest(id=1, action="APPROVE"),
                    ApplicationAccessRequest(id=2, action="REJECT"),
                ]
            )
        """

        for r in requests:
            if r.action not in [
                ApplicationAccessRequest.Action.APPROVE,
                ApplicationAccessRequest.Action.REJECT,
            ]:
                raise ValueError(
                    f"Action for application_access_requests must be either 'APPROVE' or 'REJECT'. Got: {r.action}"
                )

        res = self.api.update_application_access_requests(
            application_id, [r._json for r in requests]
        )
        self.api.handle_response(
            res, "update_application_access_requests", action="update"
        )

    def repair_connection(
        self,
        application_id: int,
        connection_id: int,
        workflow: str,
        subject: str,
        fields: Optional[List[Field]] = None,
    ) -> Ticket:
        """
        This function repairs a connection.

        It takes a workflow name, a list of fields, and a subject and produces a new ticket.

        You may need to pass in metadata fields, like TextField or TextArea.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/connections/1/repair

        Usage:
            sa.repair_connection(1, 1, workflow="Firewall Change Request", subject="Repair Connection", fields=[Field(name="Field1", value="Value1")])
        """

        ticket = Ticket.create(workflow, subject)
        step = ticket.create_step(None)
        task = step.create_task()
        task.fields.extend(fields or [])

        res = self.api.repair_connection(
            application_id, connection_id, ticket.post_json
        )
        return self.api.handle_creation(res, "repair_connection", cls=Ticket)
