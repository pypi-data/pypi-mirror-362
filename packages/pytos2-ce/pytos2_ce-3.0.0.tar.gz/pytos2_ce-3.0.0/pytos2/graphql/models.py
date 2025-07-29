from typing import Dict, TypeVar, TypedDict

T = TypeVar("T")
Variables = Dict[str, T]


class GraphResponse(TypedDict):
    data: T
