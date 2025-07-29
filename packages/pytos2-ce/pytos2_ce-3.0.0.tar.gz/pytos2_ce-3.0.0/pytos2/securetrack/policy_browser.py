from enum import Enum


# Chris cries for `Maybe`!
class Emptiness(Enum):
    EMPTY = ".isempty:true"
    NOT_EMPTY = ".isempty:false"


EMPTY = Emptiness.EMPTY
NOT_EMPTY = Emptiness.NOT_EMPTY
