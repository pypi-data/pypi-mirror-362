from typing import List, Optional


from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class TimeInterval(Jsonable):
    from_time: str = prop("", key="from")
    to_time: str = prop("", key="to")


@propify
class TimeObject(Jsonable):
    id: int = prop(0, converter=int)
    name: str = prop("")
    uid: str = prop("")
    is_global: bool = prop(None, key="global")
    class_name: str = prop("")
    time_intervals: List[TimeInterval] = prop(
        factory=list,
        key="time_intervals",
        flatify="time_interval",
    )
