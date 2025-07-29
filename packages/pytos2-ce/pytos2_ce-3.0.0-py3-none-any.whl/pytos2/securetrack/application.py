from enum import Enum
from datetime import date, datetime
from typing import Optional, List

from pytos2.models import Jsonable, ObjectReference, FQDNIp
from pytos2.utils import propify, prop, safe_iso8601_date


def classify_application(obj):
    return get_application_class(obj).kwargify(obj)


def get_application_class(obj):
    if "@xsi.type" in obj:
        mapping = {
            "singleApplicationDTO": SingleApplication,
            "applicationGroupDTO": ApplicationGroup,
        }
        return mapping.get(obj["@xsi.type"], Application)
    else:
        return Application


@propify
class Link(Jsonable):
    href: str = prop("", key="@href")


@propify
class Application(Jsonable):
    name: str = prop("")
    display_name: str = prop("")
    class_name: str = prop("")
    type: str = prop("")
    comment: str = prop("")
    uid: str = prop("")
    overrides: bool = prop(None, repr=False)
    management_domain: str = prop("")
    global_device: bool = prop(None, repr=False)
    device_id: int = prop(None)
    application_id: int = prop("")
    device_name: str = prop("", key="deviceName")


@propify
class SingleApplication(Application):
    services: List[ObjectReference] = prop(factory=list, key="service")


@propify
class ApplicationGroup(Application):
    applications: List[ObjectReference] = prop(factory=list, key="application")
