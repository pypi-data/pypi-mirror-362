import pytest
import json
import responses
from netaddr import IPAddress

from pytos2.securechange.extension import MarketplaceApp
from pytos2.utils import get_api_node


class TestExtensions:
    @responses.activate
    def test_get_extensions(self, extensions_mock, scw):
        exts = scw.get_extensions()
        assert exts[2].app_id == "ipam"
        assert exts[2].name == "IPAM Security Policy App"
        assert exts[2].url == "/apps/ispa"
        assert (
            exts[2].description
            == "The Tufin IPAM sync app integrates Tufin SecureTrack with IP Address Management systems to populate networks zones in order to use the USP in SecureTrack."
        )
        assert exts[2].version == "4.1.5"
        assert exts[2].installed is True
        assert exts[2].upsell is False
