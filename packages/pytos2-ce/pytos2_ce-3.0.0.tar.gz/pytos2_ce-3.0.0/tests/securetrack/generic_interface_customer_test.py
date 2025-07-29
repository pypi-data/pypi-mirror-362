import pytest
import json
import responses

from pytos2.securetrack.generic_interface_customer import GenericInterfaceCustomerTag
from pytos2.utils import get_api_node


class TestGenericInterfaceCustomer:
    device = json.load(
        open("tests/securetrack/json/generic_interface_customers/device-5.json")
    )
    interfaces = device["InterfaceCustomerTags"]

    interface_customer = json.load(
        open("tests/securetrack/json/generic_interface_customers/int-cust-74.json")
    )
    interface = interface_customer["InterfaceCustomerTag"]

    @responses.activate
    def test_add_generic_interface_customers_tag_200(self, st):
        """Add one or multiple interface customers"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=201,
        )

        """Add single generic interface customer tag"""
        newRoute = st.add_generic_interface_customer_tag(
            generic=self.interface["generic"],
            device=self.interface["deviceId"],
            interface_name=self.interface["interfaceName"],
            customer_id=self.interface["customerId"],
        )
        assert newRoute is None

    @responses.activate
    def test_add_generic_interface_customer_tags_400(self, st):
        """Add one or multiple interface customer tags"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=400,
        )

        """Add single interface customer tag"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_interface_customer_tag(
                generic=self.interface["generic"],
                device=self.interface["deviceId"],
                interface_name=self.interface["interfaceName"],
                customer_id=self.interface["customerId"],
            )
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_add_generic_interface_customer_tags_404(self, st):
        """Add one or multiple interface customers"""
        responses.add(
            responses.POST,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=404,
        )

        """Add single interface customer"""
        with pytest.raises(ValueError) as exception:
            st.add_generic_interface_customer_tag(
                generic=self.interface["generic"],
                device=self.interface["deviceId"],
                interface_name=self.interface["interfaceName"],
                customer_id=self.interface["customerId"],
            )
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_interface_customer_tag(
        self, st, generic_interface_customer_tag_mock
    ):
        """Get interface by interface id"""
        mockRes = get_api_node(self.interface_customer, "InterfaceCustomerTag")
        interface = GenericInterfaceCustomerTag.kwargify(mockRes)
        interface_customerByInt = st.get_generic_interface_customer_tag(74)
        assert interface_customerByInt == interface

        with pytest.raises(ValueError) as exception:
            st.get_generic_interface_customer_tag(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_get_generic_interface_customer_tags(
        self, st, generic_interface_customer_tag_mock
    ):
        """Get interfaces by device id"""
        interfaces = [
            GenericInterfaceCustomerTag.kwargify(d)
            for d in get_api_node(self.device, "InterfaceCustomerTags", listify=True)
        ]
        interface_customersByInt = st.get_generic_interface_customer_tags(
            5, generic=False
        )
        assert interface_customersByInt == interfaces

        with pytest.raises(ValueError) as exception:
            st.get_generic_interface_customer_tags(404, generic=True)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_update_generic_interface_customers_200(self, st):
        """Update one or multiple interface customers"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=200,
        )

        """Update single interface customer"""
        interface_to_update = GenericInterfaceCustomerTag.kwargify(self.interface)
        newRoute = st.update_generic_interface_customer_tag(interface_to_update)
        assert newRoute is None

    @responses.activate
    def test_update_generic_interface_customers_400(self, st):
        """PUT bad request"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=400,
        )

        with pytest.raises(ValueError) as exception:
            interface_to_update = GenericInterfaceCustomerTag.kwargify(self.interface)
            st.update_generic_interface_customer_tag(interface_to_update)
        assert "Bad Request" in str(exception.value)

    @responses.activate
    def test_update_generic_interface_customers_404(self, st):
        """PUT device id not found"""
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer",
            status=404,
        )

        with pytest.raises(ValueError) as exception:
            interface_to_update = GenericInterfaceCustomerTag.kwargify(self.interface)
            st.update_generic_interface_customer_tag(interface_to_update)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_interface_customer_tag(
        self, st, generic_interface_customer_tag_mock
    ):
        """Delete interface by interface id"""
        interface_customerByInt = st.delete_generic_interface_customer_tag(74)
        assert interface_customerByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_interface_customer_tag(404)
        assert "Not Found" in str(exception.value)

    @responses.activate
    def test_delete_generic_interface_customer_tags(
        self, st, generic_interface_customer_tag_mock
    ):
        """Delete interfaces by device id"""
        interface_customersByInt = st.delete_generic_interface_customer_tags(5)
        assert interface_customersByInt is None

        with pytest.raises(ValueError) as exception:
            st.delete_generic_interface_customer_tags(404)
        assert "Not Found" in str(exception.value)
