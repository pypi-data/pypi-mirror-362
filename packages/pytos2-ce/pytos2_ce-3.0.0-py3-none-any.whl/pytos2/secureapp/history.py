from datetime import datetime
from enum import Enum

from typing import List, Optional

from ..utils import propify, prop, safe_iso8601_date, kwargify, multiroot_kwargify
from ..models import Jsonable, Link, ObjectReference

from pytos2.secureapp import entrypoint as sa

from pytos2.secureapp.service_object import Service, classify_service_object
from pytos2.secureapp.network_object import NetworkObject, classify_network_object


def classify_history_details(obj):
    _type = {
        "historyConnectionDetailsDTO": HistoryConnectionDetails,
        "historyApplicationDetailsDTO": HistoryApplicationDetails,
        "historyApplicationInterfaceDetailsDTO": HistoryApplicationInterfaceDetails,
        "historyApplicationPackInstanceDetailsDTO": HistoryApplicationPackInstanceDetails,
        "historyNetworkObjectDetailsDTO": HistoryNetworkObjectDetails,
        "historyApplicationInterfaceInstanceDetailsDTO": HistoryApplicationInterfaceInstanceDetails,
        "historyServiceDetailsDTO": HistoryServiceDetails,
    }.get(obj.get("@xsi.type"), HistoryDetails)

    return _type.kwargify(obj)


@propify
class BaseProperties(Jsonable):
    comment: Optional[str] = prop(None)
    name: Optional[str] = prop(None)


@propify
class HistoryDetails(Jsonable):
    class XsiType(Enum):
        HISTORY_CONNECTION_DETAILS_DTO = "historyConnectionDetailsDTO"
        HISTORY_APPLICATION_DETAILS_DTO = "historyApplicationDetailsDTO"
        HISTORY_APPLICATION_INTERFACE_DETAILS_DTO = (
            "historyApplicationInterfaceDetailsDTO"
        )
        HISTORY_APPLICATION_PACK_INSTANCE_DETAILS_DTO = (
            "historyApplicationPackInstanceDetailsDTO"
        )
        HISTORY_NETWORK_OBJECT_DETAILS_DTO = "historyNetworkObjectDetailsDTO"
        HISTORY_APPLICATION_INTERFACE_INSTANCE_DETAILS_DTO = (
            "historyApplicationInterfaceInstanceDetailsDTO"
        )
        HISTORY_SERVICE_DETAILS_DTO = "historyServiceDetailsDTO"

    xsi_type: Optional[XsiType] = prop(None, key="@xsi.type")


@propify
class HistoryApplicationInterfaceDetails(Jsonable):
    new: Optional[BaseProperties] = prop(None)
    previous: Optional[BaseProperties] = prop(None)


@propify
class HistoryApplicationInterfaceInstanceDetails(Jsonable):
    new: Optional[BaseProperties] = prop(None)
    previous: Optional[BaseProperties] = prop(None)


@propify
class HistoryApplicationPackInstanceDetails(Jsonable):
    new: Optional[BaseProperties] = prop(None)
    previous: Optional[BaseProperties] = prop(None)


@propify
class HistoryApplicationDetails(Jsonable):
    ticket: Optional[ObjectReference] = prop(None)
    previous_owner: Optional[ObjectReference] = prop(None)
    new_owner: Optional[ObjectReference] = prop(None)
    removed_editors: List[ObjectReference] = prop(factory=list, flatify="editor")
    removed_viewers: List[ObjectReference] = prop(factory=list, flatify="viewer")


@propify
class ObjectReferenceList(Jsonable):
    source: List[ObjectReference] = prop(factory=list)
    destination: List[ObjectReference] = prop(factory=list)
    service: List[ObjectReference] = prop(factory=list)


def find_in_detail_list(removed, k):
    for r in removed:
        ret = getattr(r, k)
        if ret:
            return ret
    return []


@propify
class HistoryConnectionDetails(HistoryDetails):
    """
    new (BasePropertiesDTO, optional): new base properties,
    previous (BasePropertiesDTO, optional): previous base properties,
    removed ( wrapper,
    source (array[ObjectReferenceDTO], optional): sources removed),
    removed ( wrapper,
    destination (array[ObjectReferenceDTO], optional): destinations removed),
    service (void, optional): services removed
    """

    new: Optional[BaseProperties] = prop(None)
    previous: Optional[BaseProperties] = prop(None)

    added: List[ObjectReferenceList] = prop(factory=list)
    removed: List[ObjectReferenceList] = prop(factory=list)

    @property
    def added_sources(self):
        return find_in_detail_list(self.added, "source")

    @property
    def added_destinations(self):
        return find_in_detail_list(self.added, "destination")

    @property
    def added_services(self):
        return find_in_detail_list(self.added, "service")

    @property
    def removed_sources(self):
        return find_in_detail_list(self.removed, "source")

    @property
    def removed_destinations(self):
        return find_in_detail_list(self.removed, "destination")

    @property
    def removed_services(self):
        return find_in_detail_list(self.removed, "service")


@propify
class HistoryServiceDetails(HistoryConnectionDetails):
    pass


@propify
class HistoryNetworkObjectDetails(HistoryDetails):
    new: Optional[NetworkObject] = prop(None, kwargify=classify_network_object)
    previous: Optional[NetworkObject] = prop(None, kwargify=classify_network_object)
    added: List[ObjectReference] = prop(factory=list)
    removed: List[ObjectReference] = prop(factory=list)


@propify
class HistoryRecord(Jsonable):
    class XsiType(Enum):
        HISTORY_BASE_CONNECTION_DTO = "historyBaseConnectionDTO"
        HISTORY_DEVICE_OBJECT_DTO = "historyDeviceObjectDTO"

    xsi_type: Optional[XsiType] = prop(None, key="@xsi.type")

    date: Optional[datetime] = prop(None, kwargify=safe_iso8601_date)
    object_name: Optional[str] = prop(None)

    # Despite what the API documentation says, this is actually a List of ObjectReference.
    # Make the code we expose to the developer reflect the API documentation.
    user: Optional[ObjectReference] = prop(
        None, kwargify=lambda x: ObjectReference.kwargify(x[0]) if x else None
    )
    type: Optional[str] = prop(None)
    modified_object: Optional[ObjectReference] = prop(None)
    change_description: Optional[str] = prop(None)
    change_details: Optional[HistoryDetails] = prop(
        None, kwargify=classify_history_details
    )

    @classmethod
    def kwargify(cls, obj):
        if obj.get("@xsi.type") == "historyBaseConnectionDTO":
            _obj, kwargs = kwargify(HistoryBaseConnectionRecord, obj)
            return HistoryBaseConnectionRecord(**kwargs)
        elif obj.get("@xsi.type") == "historyDeviceObjectDTO":
            _obj, kwargs = kwargify(HistoryDeviceObjectRecord, obj)
            return HistoryDeviceObjectRecord(**kwargs)
        else:
            _obj, kwargs = kwargify(HistoryRecord, obj)
            return HistoryRecord(**kwargs)
            raise ValueError(
                f"Unknown xsi.type in HistoryRecord: {obj.get('@xsi.type')}"
            )


@propify
class HistoryConnectionBaseSnapshot(Jsonable):
    class XsiType(Enum):
        HISTORY_CONNECTION_DTO = "historyConnectionDTO"

    xsi_type: Optional[XsiType] = prop(None, key="@xsi.type")
    services: List[Service] = prop(
        flatify="service", factory=list, kwargify=classify_service_object
    )
    comment: Optional[str] = prop(None)
    sources: List[NetworkObject] = prop(
        flatify="source", factory=list, kwargify=classify_network_object
    )
    destinations: List[NetworkObject] = prop(
        flatify="destination", factory=list, kwargify=classify_network_object
    )
    name: Optional[str] = prop(None)


@propify
class HistoryBaseConnectionRecord(HistoryRecord):
    xsi_type: Optional[HistoryRecord.XsiType] = prop(
        HistoryRecord.XsiType.HISTORY_BASE_CONNECTION_DTO, key="@xsi.type"
    )

    snapshot: Optional[HistoryConnectionBaseSnapshot] = prop(None)


@propify
class HistoryDeviceObjectRecord(HistoryRecord):
    xsi_type: Optional[HistoryRecord.XsiType] = prop(
        HistoryRecord.XsiType.HISTORY_DEVICE_OBJECT_DTO, key="@xsi.type"
    )

    snapshot: Optional[NetworkObject] = prop(None, kwargify=classify_network_object)
    date: Optional[datetime] = prop(None, kwargify=safe_iso8601_date)
    object_name: Optional[str] = prop(None)
