from datetime import datetime
from typing import Optional, List

from pytos2.utils import propify, prop, safe_iso8601_date, safe_date, TimeFormat
from pytos2.models import Jsonable


@propify
class ChangeWindow(Jsonable):
    # Rekeying uuid to Jsonable.id, since that's our standard ID prop.
    id: str = prop("", key="uuid")
    name: str = prop("")
    description: str = prop("")
    domain_id: int = prop()
    enabled: bool = prop(False)

    @property
    def uuid(self):
        return self.id

    @uuid.setter
    def uuid(self, v):
        self.id = v


@propify
class DeviceCommitDevice(Jsonable):
    status: str = prop("")
    revision_id: int = prop()
    warnings: List[str] = prop(factory=list, flatify="warning")


@propify
class DeviceCommitResult(Jsonable):
    errors: List[str] = prop(factory=list, flatify="error")
    device: DeviceCommitDevice = prop()


@propify
class DeviceCommit(Jsonable):
    result: DeviceCommitResult = prop()


@propify
class ChangeWindowTask(Jsonable):
    start_date: Optional[datetime] = prop(
        None,
        repr=False,
        jsonify=False,
        kwargify=lambda val: safe_date(val, TimeFormat.UTC),
    )
    end_date: Optional[datetime] = prop(
        None,
        repr=False,
        jsonify=False,
        kwargify=lambda val: safe_date(val, TimeFormat.UTC),
    )
    errors: List[str] = prop(factory=list, flatify="error")
    device_commits: List[DeviceCommit] = prop(factory=list, flatify="device_commit")
