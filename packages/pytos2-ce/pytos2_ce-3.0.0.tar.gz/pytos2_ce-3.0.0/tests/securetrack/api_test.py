import json

import pytest
import responses
from netaddr import IPAddress, IPNetwork

from requests.exceptions import HTTPError

# from result import Result
from typing import Iterator

# from pytos2.securetrack.entrypoint import St
from pytos2.api import Pager
from pytos2.securetrack.rule import BindingPolicy, SecurityRule
from pytos2.securetrack.generic_device import GenericDevice
from pytos2.securetrack.topology import TopologySyncStatus
from pytos2.securetrack.zone import ZoneReference, ZoneEntry
from pytos2.securetrack.revision import Revision
from pytos2.securetrack import St
from pytos2.securetrack.device import Device
from pytos2.securetrack.network_object import HostNetworkObject, BasicNetworkObject
from pytos2.securetrack.service_object import (
    Service,
    OtherIPServiceObject,
    UDPServiceObject,
    AnyIPServiceObject,
)


class TestClient(object):
    def test_with_args(self, st_api):
        assert st_api.hostname == "198.18.0.1"
        assert st_api.username == "username"
        assert st_api.password == "password"

    def test_with_missing_args(self):
        with pytest.raises(ValueError) as e:
            St()
        assert "hostname argument must be provided" in str(e.value)


class TestClientMethods:
    @responses.activate
    def test_get_device(self, devices_mock, st):
        device = st.get_device(8)
        assert device.id == 8
        device = st.get_device("ASAv")
        assert device.name == "ASAv"

    @responses.activate
    def test_get_devices(self, devices_mock, st):
        filter_dict = {"vendor": "Checkpoint", "parent_id": 357}

        devices = st.get_devices(cache=False, filter=filter_dict)
        assert isinstance(st.get_devices(cache=False), list)
        assert st._devices_cache.is_empty()
        assert isinstance(st.get_devices(cache=False, filter=filter_dict), list)
        assert st._devices_cache.is_empty()
        assert isinstance(st.get_devices(), list)
        assert len(devices) == 2
        assert isinstance(st.get_devices(cache=True, filter=filter_dict), list)
        assert st._devices_cache.is_empty() is False
        assert isinstance(st.get_devices(), list)
        assert len(devices) == 2

    @responses.activate
    def test_get_network_objects(self, network_objects_mock, st):
        assert isinstance(st.get_network_objects(device=20), list)
        with pytest.raises(ValueError):
            st.get_network_objects(device=10000)

        device = st.get_device(20)
        network_objs = device.get_network_objects()
        assert isinstance(network_objs, list)
        assert isinstance(network_objs[0], BasicNetworkObject)

        assert isinstance(st.get_network_objects(device=20, cache=False), Pager)

        assert isinstance(
            st.get_network_objects(device=731, add_parent_objects=False), list
        )

        assert isinstance(
            st.get_network_objects(device=731, add_parent_objects=False, cache=False),
            Pager,
        )

    @responses.activate
    def test_get_device_no_cache(self, st_no_cache):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/devices/8\?show_license=false\&show_os_version=false",
            json=json.load(open("tests/securetrack/json/devices/8.json")),
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/devices/8",
            json=json.load(open("tests/securetrack/json/devices/8.json")),
        )
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/devices?name=ASAv",
            json=json.load(open("tests/securetrack/json/devices/ASAv.json")),
        )
        device = st_no_cache.get_device(8)
        assert device.id == 8
        device = st_no_cache.get_device("ASAv")
        assert device.name == "ASAv"

    @responses.activate
    def test_get_rules_for_device(self, devices_for_rule_test_mock, rules_mock, st):
        with pytest.raises(ValueError):
            st.get_rules(device=1, revision=1)

        rules = st.get_rules()

        for rule in rules:
            assert isinstance(rule, SecurityRule)

        st._device_rules_dict = {}
        rules = st.get_rules(rule_uid="{79985494-C73E-11E4-BD2B-7F000001F4F4}")

        for rule in rules:
            assert isinstance(rule, SecurityRule)

        # Test cache if-branch
        rules = st.get_rules(device=20)
        for rule in rules:
            assert isinstance(rule, SecurityRule)

        rules = st.get_rules(
            device=20, rule_uid="{79985494-C73E-11E4-BD2B-7F000001F4F4}"
        )

        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        assert rule.name == "Access to exchange server"

        # Test non-cached if-branch for rule uid
        st._device_rules_dict = {}
        rules = st.get_rules(
            device=20, rule_uid="{79985494-C73E-11E4-BD2B-7F000001F4F4}"
        )

        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        assert rule.name == "Access to exchange server"

        rules = st.get_rules(device=20, uid="{3A1BA062-6B19-4C97-8F18-79CBA9EF0AA6}")
        rule = rules[0]

        assert isinstance(rule, SecurityRule)

        with pytest.raises(ValueError):
            st.get_rules(device=400000)

    @responses.activate
    def test_get_rules_for_revision(self, revisions_mock, rules_mock, st):
        rules = st.get_rules(revision=2285)
        assert isinstance(rules, list)

        rules = st.get_rules(
            revision=2285, rule_uid="{ddf6dfbd-2080-45c9-8476-89a87d0ae5a8}"
        )

        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        assert rule.id == 1617

        rules = st.get_rules(revision=2285, uid="Datacenter_access_in_@_8")
        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        with pytest.raises(ValueError):
            st.get_rules(revision=400000)

        with pytest.raises(ValueError):
            st.get_rules(revision=2226)

        with pytest.raises(ValueError):
            st.get_rules(revision=2226, cache=False)

    @responses.activate
    def test_get_rules_from_device_no_cache(
        self, st_no_cache, devices_mock, rules_mock
    ):
        with pytest.raises(ValueError):
            st_no_cache.get_rules()
            # given conftest.py, will get 500 error on device 10

        rules = st_no_cache.get_rules(device=20)
        assert isinstance(rules[0], SecurityRule)

        rules = st_no_cache.get_rules(
            device=20, rule_uid="{79985494-C73E-11E4-BD2B-7F000001F4F4}"
        )

        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        assert rule.id == 4444

        rules = st_no_cache.get_rules(
            device=20, uid="{3A1BA062-6B19-4C97-8F18-79CBA9EF0AA6}"
        )
        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        with pytest.raises(HTTPError):
            st_no_cache.get_rules(device=400000)

    @responses.activate
    def test_get_rules_from_revision_no_cache(
        self, st_no_cache, revisions_mock, rules_mock
    ):
        rules = st_no_cache.get_rules(revision=2285)
        assert isinstance(rules[0], SecurityRule)

        rules = st_no_cache.get_rules(
            revision=2285, rule_uid="{ddf6dfbd-2080-45c9-8476-89a87d0ae5a8}"
        )
        rule = rules[0]
        assert isinstance(rule, SecurityRule)
        assert rule.id == 1617

        rules = st_no_cache.get_rules(revision=2285, uid="Datacenter_access_in_@_8")
        rule = rules[0]
        assert isinstance(rule, SecurityRule)

        with pytest.raises(ValueError):
            st_no_cache.get_rules(revision=400000)
        with pytest.raises(ValueError):
            st_no_cache.get_rules(revision=2226)

    @responses.activate
    def test_search_rules(self, devices_mock, search_rules_mock, st):
        rules = st.search_rules(devices=105)
        # rules = [r for r in rules]

        assert len(rules) == 3230

    @responses.activate
    def test_get_rules_on_open_tickets(self, search_rules_on_open_tickets_mock, st):
        rules = st.get_rules_on_open_tickets()

        assert len(rules) == 20

    @responses.activate
    def test_get_revision(self, devices_mock, revisions_mock, st):
        revision = st.get_revision(revision=2285)
        assert isinstance(revision, Revision)
        assert revision.revision_id == 135

        # Second time should run through cache
        revision = st.get_revision(revision=2285)
        assert isinstance(revision, Revision)

        with pytest.raises(ValueError):
            st.get_revision(revision=400000)

    @responses.activate
    def test_get_revisions(self, devices_mock, revisions_mock, st):
        revisions = st.get_revisions(device=8)
        assert isinstance(revisions, list)

        assert isinstance(revisions[0], Revision)
        assert revisions[0].revision_id == 135

        revisions = st.get_revisions(device="ASAv")
        assert isinstance(revisions, list)
        with pytest.raises(ValueError):
            st.get_revisions(device="RTR33333")

        device = st.get_device(identifier=8)
        assert isinstance(device.get_revisions(), list)

    @responses.activate
    def test_get_latest_revision(self, devices_mock, revisions_mock, st):
        revision = st.get_latest_revision(device=8)
        assert revision.revision_id == 135
        with pytest.raises(HTTPError):
            st.get_latest_revision(device=100000)

    @responses.activate
    def test_get_revisions_no_cache(self, devices_mock, revisions_mock, st_no_cache):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/devices/8/revisions",
            json=json.load(open("tests/securetrack/json/revisions/device-8.json")),
        )

        revisions = st_no_cache.get_revisions(device=8, cache=False)
        assert isinstance(revisions, list)

        with pytest.raises(HTTPError):
            st_no_cache.get_revisions(device=100000, cache=False)

    @responses.activate
    def test_get_revision_no_cache(self, devices_mock, revisions_mock, st_no_cache):
        responses.add(
            responses.GET,
            "https://198.18.0.1/securetrack/api/revisions/2285",
            json=json.load(open("tests/securetrack/json/revisions/revision-2285.json")),
        )

        revision = st_no_cache.get_revision(2285, cache=False)
        assert isinstance(revision, Revision)

        with pytest.raises(ValueError):
            st_no_cache.get_revision(400000, cache=False)

    @responses.activate
    def test_get_network_object_by_name(self, network_objects_mock, st):
        network_object = st.get_network_object("Subnet_10.3.3.0", 157)
        assert network_object["name"] == "Subnet_10.3.3.0"

    @responses.activate
    def test_get_network_object_by_uid(self, network_objects_mock, st):
        network_object = st.get_network_object(
            uid="{b63f31eb-d8ab-410c-b526-20a48ff9dbd2}"
        )
        assert network_object["name"] == "Subnet_10.2.2.0"

    @responses.activate
    def test_get_network_object_by_uid_cached(self, network_objects_mock, st):
        st.get_network_object(device=181, name="1.1.1.1")
        st.get_network_object(device=174, name="1.1.1.1")
        network_object = st.get_network_object(
            uid="{b17b4120-07d4-0875-d4b2-06227767ff57}", device=174
        )
        assert network_object["name"] == "1.1.1.1"

    @responses.activate
    def test_get_multiple_network_object_by_uid_error(self, network_objects_mock, st):
        with pytest.raises(AssertionError):
            st.get_network_object(uid="{b17b4120-07d4-0875-d4b2-06227767ff57}")

    @responses.activate
    def test_get_multiple_network_object_by_uid(self, network_objects_mock, st):
        network_object = st.get_network_object(
            uid="b17b4120-07d4-0875-d4b2-06227767ff57", device=181
        )
        assert network_object["name"] == network_object.name == "1.1.1.1"

    @responses.activate
    def test_get_multiple_network_object_by_uid_with_device(
        self, network_objects_mock, st
    ):
        network_object = st.get_network_object(
            uid="b17b4120-07d4-0875-d4b2-06227767ff57", device=174
        )
        assert isinstance(network_object, HostNetworkObject)
        assert network_object["name"] == network_object.name == "1.1.1.1"

    @responses.activate
    def test_get_network_object_args(self, network_objects_mock, st):
        with pytest.raises(ValueError):
            st.get_network_object(device=174)

    @responses.activate
    def test_get_multiple_network_object_not_found(self, network_objects_mock, st):
        network_object = st.get_network_object(
            uid="b17b4120-07d4-0875-d4b2-06227767ff57", device=8
        )
        assert network_object is None

    @responses.activate
    def test_prime_services_cache(self, st, services_mock):
        assert len(st._services_by_device_id_by_name.get(1, {})) == 0

        st._prime_services_cache(device_id=1)

        assert len(st._services_by_device_id_by_name[1]) > 0

    @responses.activate
    def test_get_services(self, st, services_mock, devices_mock):
        services = st.get_services(device=1)
        assert isinstance(services, list)

        assert len(services) == 420

        assert services[0].id == 2878000
        assert services[0].name == "902 (tcp)"
        assert services[0].display_name == "902"
        assert services[0].class_name == Service.ClassName.TCP_SERVICE
        assert services[0].type == Service.Type.TCP_SERVICE
        assert not services[0].is_global
        assert services[0].comment == ""
        assert services[0].min_port == 902
        assert services[0].max_port == 902

        with pytest.raises(ValueError):
            st.get_services(device=5000000)

    # test cached service
    @responses.activate
    def test_get_service_preprimed(self, st, services_mock, devices_mock):
        # Prime the cache
        st.get_services(device=1)

        # UID case mismatch? This should still work.
        service = st.get_service(uid="{97aeb369-9aea-11d5-bd16-0090272ccb30}")
        assert isinstance(service, AnyIPServiceObject)
        assert service.id == 2877997
        assert service.name == "Any"
        assert not service.is_global
        assert service.class_name == Service.ClassName.ANY_OBJECT
        assert service.type == Service.Type.IP_SERVICE
        assert service.min_port == 0
        assert service.max_port == 255

    # test uncached service (from device 2 or 3)
    @responses.activate
    def test_get_service(self, st, services_mock, devices_mock):
        with pytest.raises(ValueError):
            service = st.get_service(name="aol")

        # No cache priming this time
        with pytest.raises(AssertionError):
            st.get_service(uid="{3fbd8116-3801-4bee-8593-3cbf999da671}")
        # Test once with caching of this particular UID
        service = st.get_service(uid="{3fbd8116-3801-4bee-8593-3cbf999da671}", device=1)
        assert isinstance(service, OtherIPServiceObject)

        assert service.id == 2878412
        assert service.name == "ah"
        assert service.comment == "Protocol: ah (51)"

        service = st.get_service(
            uid="{3fbd8116-3801-4bee-8593-3cbf999da671}", device=10
        )
        assert service is None

        st._services_by_device_id_by_name[1] = {}
        st._services_by_uid = {}

        # And once without.
        service = st.get_service(uid="{3fbd8116-3801-4bee-8593-3cbf999da671}", device=1)
        assert isinstance(service, OtherIPServiceObject)
        assert service.id == 2878412
        assert service.name == "ah"
        assert service.comment == "Protocol: ah (51)"

        service = st.get_service(device=1, name="aol (udp)")
        assert isinstance(service, UDPServiceObject)

        assert service.id == 2878007
        assert service.type == Service.Type.UDP_SERVICE
        assert service.comment == "America On-line"

        with pytest.raises(ValueError):
            st.get_service(device=50000000, name="aol (udp)")

    @responses.activate
    def test_get_network_object(self, st, network_objects_mock, devices_mock):
        with pytest.raises(ValueError):
            st.get_network_object(device=100000000, uid="nonexistent_uid")

    @responses.activate
    def test_get_device_policies(self, st, device_policies_mock, devices_mock):
        policies = st.get_device_policies(device=20)

        assert isinstance(policies, list)

        policy = policies[0]
        assert policy.name == "Toronto"
        assert isinstance(policy, BindingPolicy)

        policy = policies[1]

        assert policy.name == "Standard"
        assert isinstance(policy, BindingPolicy)

        with pytest.raises(IndexError):
            _ = policies[2]

        with pytest.raises(HTTPError):
            st.get_device_policies(device=400000)

        policies = st.get_device_policies(device="CP SMC")

        policy = policies[0]
        assert isinstance(policy, BindingPolicy)
        assert policy.name == "Toronto"

        with pytest.raises(ValueError):
            st.get_device_policies(device="NONEXISTENT_ABCDEFGH")

    @responses.activate
    def test_get_device_policy(self, st, device_policies_mock, devices_mock):
        policy = st.get_device_policy(device=20, policy="Standard")
        assert isinstance(policy, BindingPolicy)
        assert policy.name == "Standard"

        with pytest.raises(ValueError):
            st.get_device_policy(device=20, policy="Nonexistent")

        with pytest.raises(ValueError):
            st.get_device_policy(device="NONEXISTENT_ABCDEFGH", policy="Nonexistent")

    @responses.activate
    def test_get_generic_devices_error(self, st, generic_devices_getter_error):
        with pytest.raises(ValueError):
            st.get_generic_devices(cache=True)

        with pytest.raises(ValueError):
            st.get_generic_devices(cache=False)

    @responses.activate
    def test_get_generic_devices(self, st, generic_devices_mock):
        devices_list = st.get_generic_devices()
        for d in devices_list:
            assert isinstance(d, GenericDevice)

        assert devices_list[0].name == "Generic02"

        devices = st.get_generic_devices(name="vm", cache=False)
        d = devices[0]
        assert isinstance(d, GenericDevice)
        assert d.name == "vm"
        assert d.id == 5
        with pytest.raises(IndexError):
            devices[1]

        d = st.get_generic_devices(name="vm", cache=True)
        assert isinstance(d, GenericDevice)
        assert d.name == "vm"
        assert d.id == 5

    @responses.activate
    def test_import_generic_device(
        self, st, generic_devices_mock, sample_generic_device_csv
    ):
        res = st.import_generic_device(
            "Generic02", sample_generic_device_csv, customer_id=1
        )
        assert res is None

        res = st.import_generic_device(
            "Nonexistent", sample_generic_device_csv, customer_id=1
        )
        assert res is None

    @responses.activate
    def test_import_generic_device_error(
        self, st, generic_devices_error_mock, sample_generic_device_csv
    ):
        with pytest.raises(ValueError):
            st.import_generic_device(
                "Generic02", sample_generic_device_csv, customer_id=1
            )

        with pytest.raises(ValueError):
            st.import_generic_device(
                "Nonexistent", sample_generic_device_csv, customer_id=1
            )

    @responses.activate
    def test_delete_generic_device(self, st, generic_devices_mock):
        res = st.delete_generic_device(3)
        assert res is None

        res = st.delete_generic_device("Generic01")
        assert res is None

        with pytest.raises(ValueError):
            st.delete_generic_device("nonexistent")

    @responses.activate
    def test_delete_generic_device_error(self, st, generic_devices_error_mock):
        with pytest.raises(ValueError):
            st.delete_generic_device(3)

    @responses.activate
    def test_sync_toplogy(self, st, topology_sync_mock):
        res = st.sync_topology()
        assert res is None

    @responses.activate
    def test_toplogy_status(self, st, topology_sync_mock):
        res = st.get_topology_sync_status()
        assert isinstance(res, TopologySyncStatus)
        assert res.percentage == 100

    @responses.activate
    def test_sync_topology_auth_error(self, st, topology_sync_auth_error_mock):
        with pytest.raises(ValueError) as info:
            st.sync_topology()

        assert "Authentication" in str(info.value)

        with pytest.raises(ValueError) as info:
            st.get_topology_sync_status()

        assert "Authentication" in str(info.value)

    @responses.activate
    def test_sync_topology_500(self, st, topology_sync_500_mock):
        with pytest.raises(ValueError) as info:
            st.sync_topology()

        assert "Error synchronizing" in str(info.value)

        with pytest.raises(ValueError) as info:
            st.get_topology_sync_status()

        assert "Error getting" in str(info.value)

    @responses.activate
    def test_sync_topology_502(self, st, topology_sync_502_mock):
        with pytest.raises(HTTPError):
            st.sync_topology()

        with pytest.raises(HTTPError):
            st.get_topology_sync_status()

    @responses.activate
    def test_get_zone_subnets(self, st, zone_subnets_mock, zones_mock):
        arr1 = st.get_zone_subnets(78)
        subnet0 = arr1[0]

        assert isinstance(subnet0, ZoneEntry)

        assert subnet0.ip == IPAddress("172.16.130.0")
        assert subnet0.netmask == IPAddress("255.255.255.0")
        assert subnet0.prefix == 24
        assert subnet0.subnet == IPNetwork("172.16.130.0/24")

        arr = st.get_zone_subnets("Amsterdam_SiteA")
        subnet = arr[0]

        assert isinstance(subnet, ZoneEntry)
        assert subnet.ip == IPAddress("172.16.130.0")
        assert subnet.netmask == IPAddress("255.255.255.0")
        assert subnet.prefix == 24
        assert subnet.subnet == IPNetwork("172.16.130.0/24")
        assert subnet == subnet0

        with pytest.raises(ValueError):
            st.get_zone_subnets(200)

    @responses.activate
    def test_get_zone_descendants(self, st, zones_mock, zone_descendants_mock):
        arr = st.get_zone_descendants(80)
        zone = arr[0]
        assert isinstance(zone, ZoneReference)
        assert zone.name == "Amsterdam_Ext"
        assert zone.zones[0].name == "Amsterdam_SiteA"

        arr = st.get_zone_descendants("Amsterdam_Ext")
        zone = arr[0]
        assert isinstance(zone, ZoneReference)
        assert zone.name == "Amsterdam_Ext"
        assert zone.zones[0].name == "Amsterdam_SiteA"

        # not exist zone id
        with pytest.raises(ValueError):
            st.get_zone_descendants(200)
