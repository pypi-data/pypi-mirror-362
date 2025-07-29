from datetime import datetime
from enum import Enum

from typing import List, Optional, Union

from pytos2.api import SdkError
from pytos2.secureapp.network_object import NetworkObject, classify_network_object
from pytos2.secureapp.service_object import Service, classify_service_object
from pytos2.securechange.user import SCWUser

from ..utils import propify, prop, safe_iso8601_date, kwargify
from ..models import Jsonable, Link, ObjectReference


@propify
class ApplicationConnection(Jsonable):
    class Meta(Enum):
        ROOT = "connection"
        ENTITY = "application"

    id: Optional[int] = prop(None)
    services: List[ObjectReference] = prop(flatify="service", factory=list)
    sources: List[ObjectReference] = prop(flatify="source", factory=list)
    destinations: List[ObjectReference] = prop(flatify="destination", factory=list)
    status: Optional[str] = prop(None)
    external: Optional[bool] = prop(None)
    connection_to_application: Optional[ObjectReference] = prop(None)
    comment: Optional[str] = prop(None)
    uid: Optional[str] = prop(None)
    application_id: Optional[str] = prop(None, key="applicationId")
    open_tickets: List[ObjectReference] = prop(flatify="ticket", factory=list)
    name: Optional[str] = prop(None)

    def delete(self):
        from pytos2.secureapp.entrypoint import Sa

        Sa.default.delete_application_connection(int(self.application_id), self.id)

    def update(self):
        if not self.application_id or not self.id:
            raise SdkError(
                "application_id and id are required to update application connection."
            )

        from pytos2.secureapp.entrypoint import Sa

        return Sa.default.update_application_connection(int(self.application_id), self)


@propify
class ExtendedApplicationConnection(ApplicationConnection):
    id: Optional[int] = prop(None)
    services: List[Service] = prop(
        flatify="service", factory=list, kwargify=classify_service_object
    )
    sources: List[NetworkObject] = prop(
        flatify="source", factory=list, kwargify=classify_network_object
    )
    destinations: List[NetworkObject] = prop(
        flatify="destination", factory=list, kwargify=classify_network_object
    )


@propify
class InterfaceConnection(Jsonable):
    class Meta(Enum):
        ROOT = "interface_connection"
        ENTITY = "interface connection"

    name: Optional[str] = prop(None)
    comment: Optional[str] = prop(None)
    open_tickets: List[ObjectReference] = prop(flatify="ticket", factory=list)
    services: List[ObjectReference] = prop(flatify="service", factory=list)
    sources: List[ObjectReference] = prop(flatify="source", factory=list)
    destinations: List[ObjectReference] = prop(flatify="destination", factory=list)
    connected_servers: List[ObjectReference] = prop(flatify="server", factory=list)


@propify
class ApplicationInterface(Jsonable):
    class Meta(Enum):
        ROOT = "application_interface"
        ENTITY = "application interface"

    name: Optional[str] = prop(None)
    comment: Optional[str] = prop(None)
    is_published: Optional[bool] = prop(None)
    application_id: Optional[int] = prop(None)
    interface_connections: List[InterfaceConnection] = prop(
        flatify="interface_connection", factory=list
    )


@propify
class Connection(Jsonable):
    class Prop(Enum):
        APPLICATION_ID = "applicationId"

    class Meta(Enum):
        ROOT = "connection"
        ENTITY = "connection"

    id: Optional[str | int] = prop(None)
    services: List[ObjectReference] = prop(flatify="service", factory=list)
    sources: List[ObjectReference] = prop(flatify="source", factory=list)
    destinations: List[ObjectReference] = prop(flatify="destination", factory=list)
    status: Optional[str] = prop(None)
    external: Optional[bool] = prop(None)
    connection_to_application: Optional[ObjectReference] = prop(None)
    comment: Optional[str] = prop(None)
    name: str = prop()
    uid: Optional[str] = prop(None)
    application_id: Optional[str] = prop(None, key=Prop.APPLICATION_ID.value)
    open_tickets: List[ObjectReference] = prop(flatify="ticket", factory=list)


@propify
class ApplicationInterfaceInstanceGet(Jsonable):
    class Meta(Enum):
        ROOT = "connection_to_application"
        ENTITY = "connection to application"

    id: Optional[str | int] = prop(None)
    uid: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    comment: Optional[str] = prop(None)
    application_id: Optional[str | int] = prop(None)
    connections: List[Connection] = prop(factory=list)
    application_interface_id: Optional[str | int] = prop(None)


@propify
class ApplicationInterfaceInstance(Jsonable):
    comment: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    servers: List[ObjectReference] = prop(flatify="server", factory=list)
    application_interface_id: Optional[str | int] = prop(None)


@propify
class Application(Jsonable):
    class Meta(Enum):
        ROOT = "application"
        ENTITY = "application"

    id: Optional[int] = prop(None)
    comment: Optional[str] = prop(None)
    customer: Optional[ObjectReference] = prop(None)
    status: Optional[str] = prop(None)
    vendors: List[str] = prop(flatify="vendor", factory=list, jsonify=False)
    created: Optional[datetime] = prop(None, kwargify=safe_iso8601_date, jsonify=False)
    connections: List[ObjectReference] = prop(
        flatify="connection", factory=list, jsonify=False
    )
    decommissioned: Optional[bool] = prop(None)
    editors: List[ObjectReference] = prop(factory=list)
    viewers: List[ObjectReference] = prop(factory=list)
    open_tickets: List[ObjectReference] = prop(factory=list, flatify="ticket")
    connection_to_application_packs: List[ObjectReference] = prop(
        factory=list, flatify="connection_to_application_pack", jsonify=False
    )
    name: str = prop()
    owner: Optional[ObjectReference] = prop(None)
    modified: Optional[datetime] = prop(None, kwargify=safe_iso8601_date, jsonify=False)

    def delete(self):
        from pytos2.secureapp.entrypoint import Sa

        Sa.default.delete_application(self.id)

    def update(self):
        from pytos2.secureapp.entrypoint import Sa

        if not self.id:
            raise SdkError("id is required to update application.")

        return Sa.default.update_application(self)
