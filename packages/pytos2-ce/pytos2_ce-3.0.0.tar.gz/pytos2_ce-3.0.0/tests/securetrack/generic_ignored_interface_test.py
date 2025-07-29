import pytest
import re
import json
import responses

from pytos2.securetrack.generic_ignored_interface import GenericIgnoredInterface
from pytos2.utils import get_api_node


class TestGenericIgnoredInterface:
    ignored_interfaces = json.load(
        open("tests/securetrack/json/generic_ignored_interfaces/mgmt-10.json")
    )
    interface = ignored_interfaces["IgnoredInterfaces"]

    @responses.activate
    def test_add_generic_ignored_interfaces_200(self, st):
        """Add one or multiple interface"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/ignoredinterface",
            status=201,
        )

        """Add single interface"""
        newInterface = st.add_generic_ignored_interface(
            interface_name=self.interface[0]["interfaceName"],
            device=self.interface[0]["mgmtId"],
            ip=self.interface[0]["ip"],
        )
        assert newInterface is None

    @responses.activate
    def test_add_generic_ignored_interfaces_400(self, st):
        """Add one or multiple interface"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/ignoredinterface",
            status=400,
        )

        """Add single interface"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_ignored_interface(
                interface_name=self.interface[0]["interfaceName"],
                device=self.interface[0]["mgmtId"],
                ip=self.interface[0]["ip"],
            )
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_add_generic_ignored_interfaces_404(self, st):
        """Add one or multiple interface"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/ignoredinterface",
            status=404,
        )

        """Add single interface"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_ignored_interface(
                interface_name=self.interface[0]["interfaceName"],
                device=self.interface[0]["mgmtId"],
                ip=self.interface[0]["ip"],
            )
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_ignored_interfaces(self, st, generic_ignored_interface_mock):
        """Get interface by interface id"""
        interfaces = [
            GenericIgnoredInterface.kwargify(d)
            for d in get_api_node(
                self.ignored_interfaces, "IgnoredInterfaces", listify=True
            )
        ]
        interfaceByInt = st.get_generic_ignored_interfaces(10)
        assert interfaceByInt == interfaces

        with pytest.raises(ValueError) as exception:
            st.get_generic_ignored_interfaces(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_ignored_interfaces(
        self, st, generic_ignored_interface_mock
    ):
        """Delete interface by interface id"""
        interfaceByInt = st.delete_generic_ignored_interfaces(10)
        assert interfaceByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_ignored_interfaces(404)
        assert "Not Found" in str(exception.value)
