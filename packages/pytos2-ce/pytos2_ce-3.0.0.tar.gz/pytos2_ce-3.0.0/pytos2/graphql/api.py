from enum import Enum
from typing import Optional

from .base import BaseGql

from ..api import OAuth2APISession
from ..utils import setup_logger
from ..api import get_app_api_session

LOGGER = setup_logger("st_api")


class GqlAPI(BaseGql):
    class Meta:
        APP = "ST"
        PATH = "/v2/api/sync"
        TOS2_ENV = ["TSS_SERVICE", "ST_SERVER_SERVICE"]

    """
    Creates an Oauth2APISession connected to SecureTrack's GraphQL API.   

    By default the value of the "GQL_HOST" environment variable will be used as the hostname. 
    Otherwise, you can provide the hostname argument.

    By default the values of thes "ST_API_USERNAME" and "ST_API_PASSWORD" environment variables 
    will be used for initial oauth2 authentication. Otherwise, you can provide the username and password arguments.

    :param Optional[str] hostname
    :param Optional[str] username
    :param Optional[str] password
    """

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
    ):
        super().__init__()

        self.hostname, self.username, self.password, self.session = get_app_api_session(
            app=self,
            hostname=hostname,
            username=username,
            password=password,
            client_id=client_id,
            session_cls=OAuth2APISession,
        )
