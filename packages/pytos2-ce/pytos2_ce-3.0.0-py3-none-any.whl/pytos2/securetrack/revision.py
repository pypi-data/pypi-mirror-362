from enum import Enum
from typing import Optional, List
from datetime import datetime, date, time
from time import mktime

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify, TimeFormat

from pytos2 import securetrack


@propify
class RevisionTicket(Jsonable):
    class Source(Enum):
        SCW = "scw"

    # id is handled by Jsonable
    source: Optional[Source] = prop(None)


@propify
class RevisionModuleAndPolicy(Jsonable):
    module: Optional[str] = prop(None)
    policy: Optional[str] = prop(None)


@propify
class Revision(Jsonable):
    class Action(Enum):  # tee-hee class action.
        AUTOMATIC = "automatic"
        INSTALLED = "installed"
        SAVED = "saved"

    class Prop(Enum):
        REVISION_ID = "revisionId"
        DATE = "date"
        TIME = "time"
        GUI_CLIENT = "guiClient"
        AUDIT_LOG = "auditLog"
        POLICY_PACKAGE = "policyPackage"
        AUTHORIZATION_STATUS = "authorizationStatus"
        READY = "ready"
        MODULES_AND_POLICY = "modules_and_policy"
        TICKETS = "tickets"

    class AuthorizationStatus(Enum):
        AUTHORIZED = "authorized"
        ERROR = "error"
        N_A = "n_a"
        PENDING = "pending"
        UNAUTHORIZED = "unauthorized"

    revision_id: Optional[int] = prop(
        None, key=Prop.REVISION_ID.value, converter=optional(int)
    )
    action: Optional[Action] = prop(None, repr=False)

    _date: Optional[date] = prop(None, repr=False, jsonify="date_str")
    _time: Optional[time] = prop(None, repr=False, jsonify="time_str")

    admin: Optional[str] = prop(None, repr=False)
    gui_client: Optional[str] = prop(None, repr=False, key=Prop.GUI_CLIENT.value)
    audit_log: Optional[str] = prop(None, repr=False, key=Prop.AUDIT_LOG.value)
    policy_package: Optional[str] = prop(
        None, repr=False, key=Prop.POLICY_PACKAGE.value
    )
    authorization_status: Optional[AuthorizationStatus] = prop(
        None, repr=False, key=Prop.AUTHORIZATION_STATUS.value
    )
    modules_and_policy: List[RevisionModuleAndPolicy] = prop(
        factory=list, flatify="module_and_policy", repr=False
    )

    tickets: List[RevisionTicket] = prop(factory=list, flatify="ticket", repr=False)

    firewall_status: bool = prop(False, repr=False)
    is_ready: bool = prop(False, repr=False, key=Prop.READY.value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, val):
        if type(val) is date:
            self._date = val
        elif type(val) is datetime:
            self._date = val.date()
        elif isinstance(val, str):
            self._date = datetime.strptime(val, TimeFormat.DATE.value).date()
        elif val is None:
            self._date = None
        else:
            raise ValueError("Cannot cast date from instance of '{}'".format(type(val)))

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        if type(val) is time:
            self._time = val
        elif type(val) is datetime:
            self._time = val.time()
        elif isinstance(val, str):
            self._time = datetime.strptime(val, TimeFormat.TIME.value).time()
        elif val is None:
            self._time = None
        else:
            raise ValueError("Cannot cast time from instance of '{}'".format(type(val)))

    @property
    def date_str(self):
        return self._date.strftime(TimeFormat.DATE.value)

    @property
    def time_str(self):
        return self._time.strftime(TimeFormat.TIME.value)[
            :-3
        ]  # Drop the last 3 digits of microseconds to make milliseconds

    @property
    def unix_timestamp(self):
        _timestamp = mktime(self._date.timetuple())
        _timestamp += (
            self._time.hour * 3600 + self._time.minute * 60 + self._time.second
        )
        return _timestamp

    @unix_timestamp.setter
    def unix_timestamp(self, val):
        if not isinstance(val, (float, int)):
            raise ValueError(
                "Cannot cast unix timestamp from instance of '{}'".format(type(val))
            )

        _datetime = datetime.fromtimestamp(val)
        self._date = _datetime.date()
        self._time = _datetime.time()

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)

        _date = _obj.get("date")
        _time = _obj.get("time")

        _date = (
            datetime.strptime(_date, TimeFormat.DATE.value).date()
            if _date is not None
            else None
        )
        _time = (
            datetime.strptime(_time, TimeFormat.TIME.value).time()
            if _time is not None
            else None
        )

        kwargs["date"] = _date
        kwargs["time"] = _time

        return cls(**kwargs)

    def get_rules(self):
        return securetrack.St.default.get_rules(revision=self.id)
