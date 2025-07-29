from enum import Enum
from typing import List, Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class GenericTransparentFirewall(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    output_l3_device_id: Optional[int] = prop(
        None, converter=optional(int), key="outputL3DeviceId"
    )
    output_l3_is_generic_device: Optional[bool] = prop(
        None, key="outputL3IsGenericDevice"
    )
    output_l3_interface_name: Optional[str] = prop(None, key="outputL3InterfaceName")
    layer2_device_id: Optional[int] = prop(
        None, converter=optional(int), key="layer2DeviceId"
    )
    input_l2_interface_name: Optional[str] = prop(None, key="inputL2InterfaceName")
    output_l2_interface_name: Optional[str] = prop(None, key="outputL2InterfaceName")
    input_l3_device_id: Optional[int] = prop(
        None, converter=optional(int), key="inputL3DeviceId"
    )
    input_l3_is_generic_device: Optional[bool] = prop(
        None, key="inputL3IsGenericDevice"
    )
    input_l3_interface_name: Optional[str] = prop(None, key="inputL3InterfaceName")
