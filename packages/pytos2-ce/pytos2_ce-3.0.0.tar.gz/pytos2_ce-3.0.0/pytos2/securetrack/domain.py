from typing import Optional


from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class Domain(Jsonable):
    id: int = prop(0, converter=int)
    description: Optional[str] = prop("")
    address: Optional[str] = prop("")
    name: str = prop(None)
