from os import getenv
from typing import Any, Iterable, Iterator, Optional, TypeVar
from urllib.parse import urljoin, urlparse
import logging
import warnings
import xmltodict

from oauthlib.oauth2 import TokenExpiredError
import requests
from requests import JSONDecodeError, RequestException, Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from traversify import Traverser  # type: ignore

from pytos2.utils import setup_logger, get_api_node
from .models import OAuthToken
from requests_oauthlib import OAuth2Session

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
LOGGER = setup_logger("api")
REQUESTS_LOGGER = logging.getLogger("requests.packages.urllib3")


class SdkError(ValueError):
    def __init__(self, message):
        super().__init__(message)


class ApiError(SdkError):
    def __init__(self, message):
        super().__init__(message)


class GraphqlError(ApiError):
    """
    Thrown when a GraphQL query returns an error

    :param errors: The errors returned by the GraphQL query
    """

    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"GraphQL Error: {errors}")


class BaseAPI:
    def __init__(self, session):
        self.session = session

    def handle_response(self, r, fn_name, action=None, resource=None) -> Response:
        """
        Use this method to handle responses from the API

        :param response: response Object
        :param fn_name: name of the function that made the request
        :param expects_json: if the response is expected to be json
        :return: response or json
        """

        action = action or fn_name.split("_")[0]
        resource = resource or "resource"
        code = ""
        message = ""

        if not r.ok:
            is_no_json = False
            try:
                msg = r.json()
                message = msg.get("result", {}).get("message", "")
                code = msg.get("result", {}).get("code", "")
            except JSONDecodeError:
                is_no_json = True

            if is_no_json and "xml version" in r.text:
                msg = xmltodict.parse(r.text)
                message = msg.get("result", {}).get("message", "")
                code = msg.get("result", {}).get("code", "")
                is_no_json = False

            if is_no_json:
                # If the response is not JSON, raise an error with the response text
                # But we don't need to confuse everybody with a long chain of
                # JSONDecodeErrors.
                err = f"{fn_name}: Failed to {action} {resource} with status {r.status_code}: {r.text}"
                raise ApiError(err)

            err = f"{fn_name}: Failed to {action} {resource} with status {r.status_code}: ({code}) {message}"
            raise ApiError(err)
        return r

    def handle_json(self, r, fn_name, action="get") -> dict:
        r = self.handle_response(r, fn_name, action=action)
        try:
            return r.json()
        except JSONDecodeError as e:
            raise ApiError(f"{fn_name}: Failed to decode response: {r.text}") from e

    def handle_creation(self, r, fn_name, *, cls, action="add", warnme=True) -> Any:
        r = self.handle_response(r, fn_name)
        if r.status_code == 201:
            loc = r.headers["Location"]

            res = self.session.get(loc)
            _json = self.handle_json(res, fn_name, action=action)

            if warnme and (not hasattr(cls, "Meta") or not hasattr(cls.Meta, "ROOT")):
                warnings.warn(
                    f"{cls.__name__} does not have a Meta.ROOT attribute. This may cause issues in handle_creation. If you are seeing this warning, please add a Meta class with a ROOT attribute to {cls.__name__}. If you know what you're doing, you may pass warnme=True to this function."
                )

            if (
                hasattr(cls, "Meta")
                and hasattr(cls.Meta, "ROOT")
                and cls.Meta.ROOT.value in _json
            ):
                _json = _json[cls.Meta.ROOT.value]

            if isinstance(_json, list):
                kwargified = [cls.kwargify(i) for i in _json]
                if len(kwargified) == 1:
                    return kwargified[0]
                return kwargified

            return cls.kwargify(_json)
        else:
            resource_descriptor = getattr(cls.Meta, "ENTITY", "resource")
            err = f"{fn_name}: Failed to add {resource_descriptor} with status {r.status_code}: {r.text}"
            raise ApiError(err)


class APISession(requests.Session):
    """
    Inits a prefixed API session

    :param str base_url: The url for the tos host
    :param str username: username
    :param str password: password
    :param str api_path: api path to prefix all requests
    :param bool verify: sets ssl strict verification for all requests
    """

    def __init__(
        self,
        hostname,
        scheme="https",
        username=None,
        password=None,
        api_path="",
        verify=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if username is not None and password is not None:
            self.auth = (username, password)

        if kwargs.get("headers") is None:
            self.headers.update({"Accept": "application/json, */*"})

        self.verify = verify
        host_base = urlparse(hostname)

        self.base_url = urljoin(
            f"{scheme}://" + (host_base.netloc or host_base.path),
            api_path.strip("/") + "/",
        )

        self.scheme = scheme
        self.hostname = host_base.netloc or host_base.path

    @property
    def username(self):
        if isinstance(self.auth, tuple) and len(self.auth) == 2:
            return self.auth[0]
        return None

    @username.setter
    def username(self, value):
        if isinstance(self.auth, tuple) and len(self.auth) == 2:
            self.auth = (value, self.auth[1])
        else:
            self.auth = (value, None)

    @property
    def password(self):
        if isinstance(self.auth, tuple) and len(self.auth) == 2:
            return self.auth[1]
        return None

    @password.setter
    def password(self, value):
        if isinstance(self.auth, tuple) and len(self.auth) == 2:
            self.auth = (self.auth[0], value)
        else:
            self.auth = (None, value)

    def request(self, method, url, *args, **kwargs):
        """Overrides all requests to prefix url, not intended to be used directly"""

        # Make sure we have a sensible timeout set
        if not kwargs.get("timeout", None):
            kwargs["timeout"] = 300
        REQUESTS_LOGGER.debug(f"Request kwargs {kwargs}")

        try:
            response = super().request(
                method, urljoin(self.base_url, url), *args, **kwargs
            )
        except RequestException as e:
            raise ApiError(f"Failed to make request: {e}") from e
        REQUESTS_LOGGER.debug(f"Response body {response.text}")

        return response


class OAuth2APISession(OAuth2Session):
    """
    Inits a prefixed API session with oauth2 support


    :param str base_url: The url for the tos host
    :param str username: username
    :param str password: password
    :param str api_path: api path to prefix all requests
    :param bool verify: sets ssl strict verification for all requests
    """

    def __init__(
        self,
        hostname,
        scheme="https",
        username=None,
        password=None,
        client_id=None,
        api_path="",
        verify=False,
        **kwargs,
    ):
        super().__init__(client_id, **kwargs)
        if username is not None and password is not None:
            self.username = username
            self.password = password

        if kwargs.get("headers") is None:
            self.headers.update({"Accept": "application/json, */*"})

        self.verify = verify
        host_base = urlparse(hostname)

        self.base_url = urljoin(
            f"{scheme}://" + (host_base.netloc or host_base.path),
            api_path.strip("/") + "/",
        )

        self.scheme = scheme
        self.hostname = host_base.netloc or host_base.path
        self.client_id = client_id

    @property
    def token_url(self) -> str:
        return f"{self.scheme}://{self.hostname}/auth/realms/tufin-realm/protocol/openid-connect/token"

    @property
    def authenticated(self) -> bool:
        return bool(self.access_token)

    def _fetch_token(self) -> OAuthToken:
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        res = requests.post(self.token_url, data=data, headers=headers, verify=False)
        res.raise_for_status()

        self.token = res.json()

        return self.token

    def request(self, method: str, url: str, *args, **kwargs):
        if not self.authenticated:
            self.token = self._fetch_token()

        if self.authenticated:
            kwargs["headers"] = {
                "Authorization": f"Bearer {self.token['access_token']}"
            }

        if not url.startswith("http"):
            url = urljoin(self.base_url, url)

        try:
            response = super().request(
                method, urljoin(self.base_url, url), *args, **kwargs
            )
        except TokenExpiredError:
            self.token = self._fetch_token()
            response = super().request(
                method, urljoin(self.base_url, url), *args, **kwargs
            )

        return response


def get_app_api_session(
    app, hostname=None, username=None, password=None, session_cls=APISession, **kwargs
):
    app_identifier = app.Meta.APP
    if hasattr(app_identifier, "value"):
        app_identifier = app_identifier.value
    app_identifier = app_identifier.upper()
    app_path = app.Meta.PATH
    if hasattr(app_path, "value"):
        app_path = app_path.value

    username_key = "{}_API_USERNAME".format(app_identifier)
    password_key = "{}_API_PASSWORD".format(app_identifier)
    hostname_key = "{}_HOSTNAME".format(app_identifier)

    tos2_envs = app.Meta.TOS2_ENV
    if getattr(tos2_envs, "value", None) is not None:
        tos2_envs = [tos2_envs.value]
    elif not isinstance(tos2_envs, list):
        tos2_envs = [tos2_envs]

    # TODO: Finish env keys
    tos2_env_keys = [(f"{env}_HOST", f"{env}_PORT") for env in tos2_envs]

    tos2_host = None
    tos2_port = 443
    is_tos2 = False

    for host_key, port_key in tos2_env_keys:
        tos2_host = getenv(host_key, None)
        tos2_port = getenv(port_key, None)

        if tos2_host and tos2_port:
            is_tos2 = True
            break

    scheme = "https"

    hostname = hostname or tos2_host or getenv(hostname_key) or getenv("TOS_HOSTNAME")
    if not hostname:
        raise ValueError(
            f"hostname argument must be provided if {hostname_key} or TOS_HOSTNAME environment variable is not set"
        )
    username = username or getenv(username_key)
    if not username:
        raise ValueError(
            f"username argument must be provided if {username_key} environment variable is not set"
        )
    password = password or getenv(password_key)
    if not password:
        raise ValueError(
            f"password argument must be provided if {password_key} environment variable is not set"
        )

    if is_tos2:
        try:
            tos2_port = int(tos2_port)
        except ValueError:
            tos2_port = 443
        scheme = "https" if tos2_port == 443 else "http"

    return (
        hostname,
        username,
        password,
        session_cls(
            hostname=hostname,
            scheme=scheme,
            username=username,
            password=password,
            api_path=app_path,
            **kwargs,
        ),
    )


def resultify_response(response):
    if response.ok:
        return response
    else:
        response.raise_for_status()


def traversify_response(response):
    if response.ok:
        return Traverser(response)
    else:
        response.raise_for_status()


def boolify(params: dict) -> dict:
    return {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}


T = TypeVar("T")


class Pager(Iterable[T]):
    """
    This class abstracts away Tufin's standard pagination. If you are using the SDK,
    this can be consumed like a list.

    User Example:
    ```
    pager = st.get_applications()
    for app in pager:
        pass

    # Or
    pager = st.get_applications()
    apps = pager.fetch_all()
    # apps is now a list of all applications

    # Or
    pager = st.get_applications()
    app = pager[0]
    some_slice = pager[1:10]
    ```

    """

    def __init__(
        self,
        api,
        url,
        api_node,
        fn_name,
        kwargify,
        page_size=2000,
        start=None,
        stop=None,
        step=None,
        params: Optional[dict] = None,
        is_slice=False,
        use_total=True,
    ):
        """
        Create a new Pager object.

        :param api: The API object to use for requests
        :param url: The URL to request: i.e. "applications"
        :param api_node: The root node of the response JSON, i.e. "applications.application"
        :param fn_name: The name of the function that made the request -- This is used for error messages
        :param kwargify: A function to convert an element of the response into a Jsonable object.
        :param page_size: The number of items to request per page, default 2000
        :param start: The index to start at, default 0
        :param stop: The index to stop at, default None. You do not need to set this during regular use. It is used internally for slices.
        :param step: Increment the internal index by this amount, default 1
        :param params: Additional parameters to pass to the request
        :param is_slice: Internal flag to determine if this is a slice, default False
        """

        self.api = api
        self.api_node = api_node
        self.fn_name = fn_name
        self.page_size = page_size
        self.url = url
        self.params = params
        self.use_total = use_total

        self.root_node = api_node.split(".")[0]
        self.kwargify = kwargify

        self.start = start or 0
        self.stop = stop
        self.step = step or 1

        self._items = None
        self._cur_idx = self.start
        self._cur_page_idx = 0
        self._cur_offset = start or 0
        self._next_offset = None
        self._total = None
        self._is_slice = is_slice

        self._accrued = []

        self._prime()

    def __repr__(self):
        item_count = len(self)
        noun = "item" if item_count == 1 else "items"
        length = f"{item_count} {noun}" if self._items is not None else "unknown"
        return f"{self.__class__.__name__}({self.url}, items=[... {length}])"

    def __iter__(self):
        return self

    def _accrue(self):
        if self._items is None or self._cur_page_idx >= len(self._items):
            # Determine whether we should even bother fetching the next page
            if (
                self.use_total
                and self._total is not None
                and self._cur_offset + self._cur_page_idx >= self._total
            ):
                return False
            elif self._items and len(self._items) < self.page_size:
                return False

            self._cur_offset += self._cur_page_idx
            self._items, total = self._fetch_page(self._cur_offset)
            if total and self.use_total:
                self._total = total

            self._cur_page_idx = 0
            if not self._items:
                return False

        if self.stop and self._cur_page_idx + self._cur_offset >= self.stop:
            return False

        item = self._items[self._cur_page_idx]
        self._cur_page_idx += self.step

        if self.kwargify:
            item = self.kwargify(item)

        self._accrued.append(item)
        return True

    def __next__(self) -> T:
        while self._cur_idx - self.start >= len(self._accrued):
            if not self._accrue():
                break

        if (self._cur_idx - self.start) < len(self._accrued):
            item = self._accrued[self._cur_idx - self.start]
            self._cur_idx += 1
            return item
        else:
            raise StopIteration

    def _prime(self):
        self._items, total = self._fetch_page()
        if not self.use_total:
            self.total = -1
        elif total:
            self._total = total

    def __len__(self):
        if self._total is None:
            self._prime()

        if self.use_total and self._total:
            if self.stop and self._total > self.stop:
                return int((self.stop - self.start) / self.step)

            return int((self._total - self.start) / self.step)
        if not self._items:
            return 0

        size = max(len(self._items), len(self._accrued))
        return int(size / self.step)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.fetch_all() == other
        elif isinstance(other, Pager):
            return self.fetch_all() == other.fetch_all()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def _new_pager(self, start, stop, step, is_slice):
        return Pager(
            self.api,
            self.url,
            self.api_node,
            self.fn_name,
            self.kwargify,
            page_size=self.page_size,
            start=start,
            stop=stop,
            step=step,
            params=self.params,
            is_slice=is_slice,
        )

    def __getitem__(self, idx):
        if self._is_slice and isinstance(idx, slice):
            while self._accrue():
                pass

            return self._accrued[idx]

        if isinstance(idx, slice):
            if idx.step and idx.step < 0:
                raise IndexError("Negative steps are not supported")

            if idx.start and idx.start < 0:
                raise IndexError("Negative start indices are not supported")

            if idx.stop and idx.stop < 0:
                raise IndexError("Negative stop indices are not supported")

            return self._new_pager(
                start=self.start + (idx.start or 0),
                stop=idx.stop + self.start if idx.stop else None,
                step=idx.step,
                is_slice=True,
            )

        if idx < 0:
            while self._accrue():
                pass

            return self._accrued[idx]
        if self._total is None:
            self._prime()

        if not self.use_total:
            if idx >= len(self._items) - 1:
                raise IndexError("Index out of range")

        if self._total and idx >= self._total:
            raise IndexError("Index out of range")

        while self._accrue() and idx >= len(self._accrued):
            pass

        if idx >= len(self._accrued):
            raise IndexError("Index out of range")

        return self._accrued[idx]

    def _params(self, start=None):
        params = (self.params or {}).copy()
        params["start"] = start or self.start or 0

        if self.stop and self.stop - self.start < self.page_size:
            params["count"] = (self.stop - self.start) + 1
        else:
            params["count"] = self.page_size

        params["count"] = self.page_size
        if params["start"] == self.start:
            params["get_total"] = "true"
        return params

    def _fetch_page(self, start=None):
        params = self._params(start)

        response = self.api.session.get(self.url, params=params)
        response_json = self.api.handle_json(response, self.fn_name)
        if params["start"] == self.start:
            total = response_json[self.root_node].get("total", None)
        else:
            total = None

        items = get_api_node(response_json, self.api_node, listify=True)
        return items, total

    def fetch_all(self):
        """
        Fetch all items represented by the pager.
        """

        while self._accrue():
            pass

        return self._accrued
