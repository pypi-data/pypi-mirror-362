from typing import Optional, TypedDict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pytos2.secureapp.entrypoint import Sa
    from pytos2.securechange.entrypoint import Scw
    from pytos2.securetrack.entrypoint import St

Apps = Union["Sa", "Scw", "St"]


class APISessionKwargs(TypedDict):
    app: Apps
    hostname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    scheme: Optional[str]
    verify: Optional[bool]


class OAuthToken(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: str
    expires_at: str
    mac_key: str
    mac_algorithm: str
