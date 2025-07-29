from enum import Enum

from typing import List, Optional

from ..utils import propify, prop
from ..models import Jsonable

from pytos2.securechange.service import PredefinedServiceName


@propify
class Layer7ApplicationService(Jsonable):
    name: Optional[PredefinedServiceName] = prop(None)
    protocol: int = prop()
    min: int = prop()
    max: int = prop()


@propify
class ApplicationIdentity(Jsonable):
    class Prop(Enum):
        APPLICATION_IDENTITY_SERVICES = "application_identity_services"

    name: str = prop()
    services: List[Layer7ApplicationService] = prop(
        factory=list,
        key=Prop.APPLICATION_IDENTITY_SERVICES.value,
        flatify="application_identity_service",
    )
