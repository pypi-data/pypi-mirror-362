from enum import Enum
from typing import List, Optional, Union
from attr.converters import optional

from ..utils import propify, prop
from ..models import Jsonable


@propify
class BulkOperationTaskResultDevice(Jsonable):
    id: int = prop(key="device_id", converter=int)
    status: Optional[str] = prop(None, key="status", flatify="description")
    name: Optional[str] = prop("", key="display_name")
    ip_address: Optional[str] = prop(None)


@propify
class BulkOperationTaskStatusList(Jsonable):
    count: int = prop(converter=int)
    devices: List[BulkOperationTaskResultDevice] = prop(flatify="devices", factory=list)


@propify
class BulkOperationTaskResult(Jsonable):
    in_progress: BulkOperationTaskStatusList = prop(key="in_progress", factory=list)
    succeeded: BulkOperationTaskStatusList = prop(key="succeeded", factory=list)
    failed: BulkOperationTaskStatusList = prop(key="failed", factory=list)
    total_in_progress: int = prop(0, converter=int)
    total_succeeded: int = prop(0, converter=int)
    total_failed: int = prop(0, converter=int)

    @property
    def count(self):
        return self.total_in_progress + self.total_succeeded + self.total_failed


@propify
class BulkOperationTask(Jsonable):
    uid: str = prop(key="task_uid")

    def get_result(self) -> BulkOperationTaskResult:
        from pytos2.securetrack.entrypoint import St

        if self.task_result:
            return self.task_result

        bulk_operation_task_result = St.default.get_devices_bulk_task(self.uid)
        return bulk_operation_task_result.result
