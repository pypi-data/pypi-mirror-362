from enum import Enum

import pytest
import requests
import responses
import attr
from requests.exceptions import HTTPError
from traversify import Traverser

from pytos2.api import (
    APISession,
    get_app_api_session,
    resultify_response,
    boolify,
    traversify_response,
)


class TestAPISession:
    @responses.activate
    def test_get_json(self):
        client = APISession(
            hostname="test",
            username="user",
            password="password",
            api_path="api",
            verify=False,
        )
        responses.add(
            responses.GET, "https://test/api/thing", json={"k": "v"}, status=200
        )

        r = client.get("thing")
        assert r.json() == {"k": "v"}

    @responses.activate
    def test_post_json(self):
        client = APISession(
            hostname="test",
            username="user",
            password="password",
            api_path="api",
            verify=False,
        )
        responses.add(
            responses.POST, "https://test/api/thing", json={"k": "v"}, status=200
        )

        p = client.post("thing", json={})
        assert p.json()["k"] == "v"


class TestGetAppSession(object):
    @attr.s(auto_attribs=True)
    class App:
        class Meta(Enum):
            APP = "app"
            PATH = "/app"
            TOS2_ENV = "TSS_SERVICE"

    @attr.s(auto_attribs=True)
    class App2:
        class Meta:
            APP = "app2"
            PATH = "/app2"
            TOS2_ENV = ["TSS_SERVICE", "ST_SERVER_SERVICE"]

    app = App()
    app2 = App2()

    def test_with_args(self):
        hostname, username, password, session = get_app_api_session(
            self.app, "hostname", "username", "password"
        )
        assert hostname == "hostname"
        assert username == "username"
        assert password == "password"
        assert session.base_url.startswith("https:")

    def test_with_env(self, monkeypatch):
        monkeypatch.setenv("APP_API_USERNAME", "env_username")
        monkeypatch.setenv("APP_API_PASSWORD", "env_password")
        monkeypatch.setenv("APP_HOSTNAME", "198.18.0.2")

        hostname, username, password, session = get_app_api_session(self.app)
        assert hostname == "198.18.0.2"
        assert username == "env_username"
        assert password == "env_password"
        assert session.base_url.startswith("https:")
        assert not session.verify

    def test_with_tos2_env(self, monkeypatch):
        monkeypatch.setenv("APP_API_USERNAME", "env_username")
        monkeypatch.setenv("APP_API_PASSWORD", "env_password")
        monkeypatch.setenv("TSS_SERVICE_HOST", "198.18.0.3")
        monkeypatch.setenv("TSS_SERVICE_PORT", "80")

        hostname, username, password, session = get_app_api_session(self.app)
        assert hostname == "198.18.0.3"
        assert username == "env_username"
        assert password == "env_password"
        assert session.base_url.startswith("http:")
        assert not session.verify

    def test_with_tos2_env_without_enum(self, monkeypatch):
        monkeypatch.setenv("APP2_API_USERNAME", "env_username")
        monkeypatch.setenv("APP2_API_PASSWORD", "env_password")
        monkeypatch.setenv("ST_SERVER_SERVICE_HOST", "198.18.0.3")
        monkeypatch.setenv("ST_SERVER_SERVICE_PORT", "80")

        hostname, username, password, session = get_app_api_session(self.app2)
        assert hostname == "198.18.0.3"
        assert username == "env_username"
        assert password == "env_password"
        assert session.base_url.startswith("http:")
        assert not session.verify

    def test_with_tos2_env_without_enum2(self, monkeypatch):
        monkeypatch.setenv("APP2_API_USERNAME", "env_username")
        monkeypatch.setenv("APP2_API_PASSWORD", "env_password")
        monkeypatch.setenv("ST_SERVER_SERVICE_HOST", "198.18.0.3")
        monkeypatch.setenv("ST_SERVER_SERVICE_PORT", "80")
        monkeypatch.setenv("TSS_SERVICE_HOST", "198.18.0.4")
        monkeypatch.setenv("TSS_SERVICE_PORT", "81")

        hostname, username, password, session = get_app_api_session(self.app2)
        assert hostname == "198.18.0.4"
        assert username == "env_username"
        assert password == "env_password"
        assert session.base_url.startswith("http:")
        assert not session.verify

    def test_with_missing_args(self):
        with pytest.raises(ValueError) as e:
            get_app_api_session(self.app)
        assert "hostname argument must be provided" in str(e.value)
        with pytest.raises(ValueError) as e:
            get_app_api_session(self.app, "hostname")
        assert "username argument must be provided" in str(e.value)
        with pytest.raises(ValueError) as e:
            get_app_api_session(self.app, "hostname", "password")
        assert "password argument must be provided" in str(e.value)


@responses.activate
def test_resultify_response():
    client = APISession(hostname="test", username="", password="")
    responses.add(responses.GET, "https://test/thing", json={"k": "v"}, status=200)
    responses.add(responses.GET, "https://test/thong", json={"k": "v"}, status=404)

    r = resultify_response(client.get("thing"))
    assert r and isinstance(r, requests.Response)

    with pytest.raises(HTTPError):
        resultify_response(client.get("thong"))
    # assert not r.is_ok() and isinstance(r.value, requests.Response)


@responses.activate
def test_traversify_response():
    client = APISession(hostname="test", username="", password="")
    responses.add(responses.GET, "https://test/thing", json={"k": "v"}, status=200)
    responses.add(responses.GET, "https://test/thong", json={"k": "v"}, status=404)

    r = traversify_response(client.get("thing"))
    assert r and isinstance(r, Traverser)

    with pytest.raises(HTTPError):
        traversify_response(client.get("thong"))


def test_boolify():
    assert boolify(
        {"True": True, "False": False, "None": None, "ignore": "ignore"}
    ) == {"True": "true", "False": "false", "None": None, "ignore": "ignore"}
