from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class Domain(Jsonable):
    id: str = prop("")
    name: str = prop("")
    description: str = prop("")
