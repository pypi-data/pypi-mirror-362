from enum import Enum
from typing import Optional, List

from pytos2.models import Jsonable
from pytos2.utils import prop, propify


@propify
class TopologyDevice(Jsonable):
    """
    Represents a topology device in SecureTrack.

    This model maps to the device objects found in the TopologyDevices API response.
    """

    # Standard device properties
    id: int = prop(0, key="device_id")
    name: str = prop("", key="device_name")
    model: str = prop("", key="device_model")
    domain: int = prop(0, key="device_domain")
    vendor: str = prop("", key="device_vendor")
    virtual_type: str = prop("", key="device_virtual_type")
    topology_enabled: bool = prop(False, key="device_topology_enabled")
    has_dynamic_topology: str = prop("disable", key="device_has_dynamic_topology")

    # Optional device properties
    parent: Optional[int] = prop(None, key="device_parent")
    context_name: Optional[str] = prop(None, key="device_context_name")
    firewall_id: Optional[str] = prop(None, key="device_firewall_id")

    # OPM-related properties
    opm_id: Optional[str] = prop(None, key="opm_device_id")
    opm_system_id: Optional[str] = prop(None, key="opm_system_id")
    opm_type: Optional[str] = prop(None, key="opm_type")
    opm_parent: Optional[str] = prop(None, key="opm_parent")
    opm_vendor: Optional[str] = prop(None, key="opm_vendor")
    opm_model: Optional[str] = prop(None, key="opm_model")
