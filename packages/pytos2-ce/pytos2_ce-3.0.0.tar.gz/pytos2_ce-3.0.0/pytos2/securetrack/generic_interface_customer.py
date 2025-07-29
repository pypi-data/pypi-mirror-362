from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericInterfaceCustomerTag(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    generic: Optional[bool] = prop(False)
    device_id: Optional[int] = prop(None, converter=optional(int), key="deviceId")
    interface_name: str = prop(None, key="interfaceName")
    customer_id: Optional[int] = prop(None, converter=optional(int), key="customerId")
