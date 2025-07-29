from datetime import date, datetime
from typing import Optional, Union, List

from enum import Enum

import attr
from netaddr import IPAddress

from pytos2.utils import jsonify, kwargify, propify, prop

DateFilterType = Union[None, str, datetime, date]


def coerce_date_filter_type(value: DateFilterType) -> Optional[str]:
    if value is None:
        return None

    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        value = value.isoformat()

    return value


@propify
class Jsonable:
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"

    data: Optional[dict] = attr.ib(None, eq=False, repr=False)
    id: Optional[int] = attr.ib(None, eq=False)
    xsi_type: Optional[Union[str, Enum]] = prop(
        None, key=Prop.XSI_TYPE.value, repr=False
    )
    _flatifies: dict = attr.ib(factory=dict, repr=False)

    _json_override: Optional[dict] = attr.ib(None, eq=False, repr=False, init=False)

    @property
    def _json(self) -> dict:
        return self._json_override or jsonify(self)

    @_json.setter
    def _json(self, val):
        self._json_override = val

    @classmethod
    def kwargify(cls, obj: dict):
        _obj, kwargs = kwargify(cls, obj)
        return cls(**kwargs)  # type: ignore

    def __getitem__(self, key):
        return getattr(self, key)


class UnMapped(dict):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self._json = obj
        self.data = obj
        self._type = "UnMapped"

    @classmethod
    def kwargify(cls, obj: dict):
        return cls(obj)


class IPType(Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    OTHER = "OTHER"


@propify
class Link(Jsonable):
    """
    LinkDTO object, common across multiple SDKs.
    """

    class Prop(Enum):
        HREF = "@href"

    href: str = prop("http://", key=Prop.HREF.value)


@propify
class FQDNIp(Jsonable):
    class Prop(Enum):
        SUBNET_MASK = "subnetMask"
        IP = "ip"

    ipType: Optional[IPType] = prop(None)
    subnet_mask: Optional[IPAddress] = prop(None, key=Prop.SUBNET_MASK.value)
    ip: Optional[IPAddress] = prop(None)


def _kwargify_id(value):
    if value is None:
        return value

    try:
        return int(value)
    except ValueError:
        pass

    return value


@propify
class ObjectReference(Jsonable):
    # Added id to ObjectReference because we need to jsonify it in some cases.
    # _kwargify_id is used to convert the id to an int if it is a string.
    id: Union[None, str, int] = prop(None, kwargify=_kwargify_id)
    uid: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)
    management_domain: Optional[str] = prop(None)
    type: str = prop("")
    ips: List[FQDNIp] = prop(factory=list)
    link: Link = prop("")
    members: List["ObjectReference"] = prop(factory=list)
