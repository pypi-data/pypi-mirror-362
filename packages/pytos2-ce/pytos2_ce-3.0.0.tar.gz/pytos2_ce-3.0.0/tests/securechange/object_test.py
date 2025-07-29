import pytest
from netaddr import IPNetwork, IPRange, IPAddress
from . import conftest  # noqa
from pytos2.securechange.fields import MultiAccessRequest


@pytest.fixture
def ars(get_test_field):
    return get_test_field(MultiAccessRequest).access_requests


class TestAccessRequest:
    @pytest.mark.parametrize(
        "attr", ["targets", "users", "sources", "destinations", "services", "labels"]
    )
    def test_list_attrs(self, ars, attr):
        assert isinstance(getattr(ars[0], attr), list)


class TestAccessRequestIP:
    @pytest.fixture
    def subnet(self, ars):
        return ars[1].sources[3]

    def test_subnet(self, subnet):
        assert str(subnet.subnet) == "10.20.50.0/24"

    def test_set_subnet_obj(self, subnet):
        subnet.subnet = IPNetwork("1.2.3.4/31")
        assert subnet.ip_address == "1.2.3.4"
        assert subnet.netmask == "255.255.255.254"
        assert subnet.cidr == 31

    def test_set_subnet_str(self, subnet):
        subnet.subnet = "1.2.3.0/30"
        assert subnet.netmask == "255.255.255.252"
        subnet.subnet = "1.2.3.0/255.255.255.0"
        assert subnet.cidr == 24

    def test_set_invalid_subnet(self, subnet):
        with pytest.raises(ValueError):
            subnet.subnet = "thing"


class TestAccessRequestNatIP:
    @pytest.fixture
    def nat_ip(self, ars):
        return ars[1].sources[4]

    def test_subnet(self, nat_ip):
        assert str(nat_ip.subnet) == "5.6.7.8/32"

    def test_set_subnet_obj(self, nat_ip):
        nat_ip.subnet = IPNetwork("1.2.3.4/31")
        assert nat_ip.ip_address == "1.2.3.4"
        assert nat_ip.netmask == "255.255.255.254"
        assert nat_ip.cidr == 31

    def test_set_nat_subnet_obj(self, nat_ip):
        nat_ip.nat_subnet = IPNetwork("1.2.3.4/31")
        assert nat_ip.nat_ip_address == "1.2.3.4"
        assert nat_ip.nat_netmask == "255.255.255.254"
        assert nat_ip.nat_cidr == 31

    def test_set_subnet_str(self, nat_ip):
        nat_ip.subnet = "1.2.3.0/30"
        assert nat_ip.netmask == "255.255.255.252"
        nat_ip.subnet = "1.2.3.0/255.255.255.0"
        assert nat_ip.cidr == 24

    def test_set_nat_subnet_str(self, nat_ip):
        nat_ip.nat_subnet = "1.2.3.0/30"
        assert nat_ip.nat_ip_address == "1.2.3.0"
        assert nat_ip.nat_netmask == "255.255.255.252"
        assert nat_ip.nat_cidr == 30


class TestAccessRequestRange:
    @pytest.fixture
    def ip_range(self, ars):
        return ars[1].sources[2]

    def test_range(self, ip_range):
        assert str(ip_range.range) == "10.10.10.10-11.1.1.1"

    def test_set_range_obj(self, ip_range):
        ip_range.range = IPRange("1.2.3.4", "1.2.3.6")
        assert ip_range.range_first_ip == "1.2.3.4"
        assert ip_range.range_last_ip == "1.2.3.6"

    def test_set_range_str(self, ip_range):
        ip_range.range = "1.1.1.1-1.2.3.4"
        assert ip_range.range_first_ip == "1.1.1.1"
        assert ip_range.range_last_ip == "1.2.3.4"

    def test_set_range_iter(self, ip_range):
        ip_range.range = ("1.0.0.0", "1.4.3.2")
        assert ip_range.range_first_ip == "1.0.0.0"
        assert ip_range.range_last_ip == "1.4.3.2"

    def test_set_invalid_range(self, ip_range):
        with pytest.raises(ValueError):
            ip_range.range = "thing"


class TestAccessRequestDNS:
    @pytest.fixture
    def dns(self, ars):
        return ars[1].sources[1]

    def test_dns_ip_addresses(self, dns):
        assert all(isinstance(ip, IPAddress) for ip in dns.dns_ip_addresses)

    def test_json_override(self, dns):
        dns._json = {}
        assert dns._json == {}
