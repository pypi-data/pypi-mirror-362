import pytest
from traversify import Traverser
import responses


class TestRelatedRules:
    @responses.activate
    def test_related_rules_results(self, related_rules_mock, scw):
        ticket = scw.get_ticket(49)
        results = ticket.last_task.access_request.related_rules_result.get_results()

        access_request1 = results.access_requests[0]
        assert len(results.access_requests) == 1
        assert access_request1.ar == 1
        assert len(access_request1.devices) == 1
        assert access_request1.devices[0].management_id == 15

        assert len(access_request1.devices[0].bindings) == 1
        assert len(access_request1.devices[0].bindings[0].related_rules) == 2

        related_rule1 = access_request1.devices[0].bindings[0].related_rules[0]
        assert related_rule1.ignore
        assert related_rule1.rule.uid == "{cc7908e5-8780-4357-a0d2-4fa2fd9180be}"
        assert not related_rule1.rule.is_disabled
        assert related_rule1.rule.rule_number == 140
        assert related_rule1.rule.from_zone == "port3"
        assert related_rule1.rule.to_zone == "port2"
        assert related_rule1.rule.track["track_level"] == "LOG"
        assert related_rule1.rule.install_ons == []
        assert related_rule1.rule.communities == []
        assert related_rule1.rule.times == []

        assert len(related_rule1.rule.sources) == 1
        assert (
            related_rule1.rule.sources[0].uid
            == "{e08566b5-184e-463d-b6f5-de44aeede838}"
        )
        assert related_rule1.rule.sources[0].name == "Host_10.103.0.42"
        assert related_rule1.rule.sources[0].display_name == "Host_10.103.0.42"
        assert related_rule1.rule.sources[0].class_name.value == "host_plain"
        assert related_rule1.rule.sources[0].origin == "DEVICE"
        assert not related_rule1.rule.sources[0].is_global
        assert not related_rule1.rule.sources[0].is_implicit
        assert not related_rule1.rule.sources[0].is_shared
        assert related_rule1.rule.sources[0].comment == ""
        assert related_rule1.rule.sources[0].id == "66c7421a9591a744946348da"
        assert related_rule1.rule.sources[0].version_id == 53
        assert related_rule1.rule.sources[0].device_type.value == "Fortinet"
        assert related_rule1.rule.sources[0].ip_type.value == "IPV4"
        assert related_rule1.rule.sources[0].referenced == "UNKNOWN"
        assert not related_rule1.rule.sources[0].installable_target

        assert len(related_rule1.rule.destinations) == 1
        assert (
            related_rule1.rule.destinations[0].uid
            == "{2c8c67e6-d1c2-48ee-a821-3e79b736d2d7}"
        )
        assert related_rule1.rule.destinations[0].name == "Host_10.234.10.42"
        assert related_rule1.rule.destinations[0].display_name == "Host_10.234.10.42"
        assert related_rule1.rule.destinations[0].class_name.value == "host_plain"
        assert related_rule1.rule.destinations[0].origin == "DEVICE"
        assert not related_rule1.rule.destinations[0].is_global
        assert not related_rule1.rule.destinations[0].is_implicit
        assert not related_rule1.rule.destinations[0].is_shared
        assert related_rule1.rule.destinations[0].comment == ""
        assert related_rule1.rule.destinations[0].id == "66c7421a9591a744946348d6"
        assert related_rule1.rule.destinations[0].version_id == 53
        assert related_rule1.rule.destinations[0].device_type.value == "Fortinet"
        assert related_rule1.rule.destinations[0].ip_type.value == "IPV4"
        assert related_rule1.rule.destinations[0].referenced == "UNKNOWN"
        assert not related_rule1.rule.destinations[0].installable_target

        assert len(related_rule1.rule.destination_services) == 1
        assert (
            related_rule1.rule.destination_services[0].uid
            == "{c75809f4-7e46-4f4b-954d-b46cb86d64fb}"
        )
        assert related_rule1.rule.destination_services[0].name == "TCP_441"
        assert related_rule1.rule.destination_services[0].display_name == "TCP_441"
        assert related_rule1.rule.destination_services[0].origin == "DEVICE"
        assert not related_rule1.rule.destination_services[0].is_global
        assert not related_rule1.rule.destination_services[0].implicit
        assert not related_rule1.rule.destination_services[0].shared
        assert related_rule1.rule.destination_services[0].timeout == 0
        assert related_rule1.rule.destination_services[0].comment == ""
        assert related_rule1.rule.destination_services[0].version_id == 53
        assert related_rule1.rule.destination_services[0].referenced.value == "UNKNOWN"
        assert related_rule1.rule.destination_services[0].type_on_device == ""
        assert not related_rule1.rule.destination_services[0].negate
        assert not related_rule1.rule.destination_services[0].match_for_any

        assert (
            related_rule1.intersecting_objects.found_in_source.uid
            == "{e08566b5-184e-463d-b6f5-de44aeede838}"
        )
        assert (
            related_rule1.intersecting_objects.found_in_destination.uid
            == "{2c8c67e6-d1c2-48ee-a821-3e79b736d2d7}"
        )
        assert (
            related_rule1.intersecting_objects.found_in_service.uid
            == "{c75809f4-7e46-4f4b-954d-b46cb86d64fb}"
        )

        related_rule2 = access_request1.devices[0].bindings[0].related_rules[1]
        assert related_rule2.ignore
        assert related_rule2.rule.uid == "{5fc5ca91-805e-4fe3-baa0-2441f27b1d9a}"
        assert not related_rule2.rule.is_disabled
        assert related_rule2.rule.rule_number == 138
        assert related_rule2.rule.from_zone == "port3"
        assert related_rule2.rule.to_zone == "port2"
        assert related_rule2.rule.track["track_level"] == "LOG"
        assert related_rule2.rule.install_ons == []
        assert related_rule2.rule.communities == []
        assert related_rule2.rule.times == []

        assert len(related_rule2.rule.sources) == 1
        assert (
            related_rule2.rule.sources[0].uid
            == "{e08566b5-184e-463d-b6f5-de44aeede838}"
        )
        assert related_rule2.rule.sources[0].name == "Host_10.103.0.42"
        assert related_rule2.rule.sources[0].display_name == "Host_10.103.0.42"
        assert related_rule2.rule.sources[0].class_name.value == "host_plain"
        assert related_rule2.rule.sources[0].origin == "DEVICE"
        assert not related_rule2.rule.sources[0].is_global
        assert not related_rule2.rule.sources[0].is_implicit
        assert not related_rule2.rule.sources[0].is_shared
        assert related_rule2.rule.sources[0].comment == ""
        assert related_rule2.rule.sources[0].id == "66c7421a9591a744946348e4"
        assert related_rule2.rule.sources[0].version_id == 53
        assert related_rule2.rule.sources[0].device_type.value == "Fortinet"
        assert related_rule2.rule.sources[0].ip_type.value == "IPV4"
        assert related_rule2.rule.sources[0].referenced == "UNKNOWN"
        assert not related_rule2.rule.sources[0].installable_target

        assert len(related_rule2.rule.destinations) == 1
        assert (
            related_rule2.rule.destinations[0].uid
            == "{2c8c67e6-d1c2-48ee-a821-3e79b736d2d7}"
        )
        assert related_rule2.rule.destinations[0].name == "Host_10.234.10.42"
        assert related_rule2.rule.destinations[0].display_name == "Host_10.234.10.42"
        assert related_rule2.rule.destinations[0].class_name.value == "host_plain"
        assert related_rule2.rule.destinations[0].origin == "DEVICE"
        assert not related_rule2.rule.destinations[0].is_global
        assert not related_rule2.rule.destinations[0].is_implicit
        assert not related_rule2.rule.destinations[0].is_shared
        assert related_rule2.rule.destinations[0].comment == ""
        assert related_rule2.rule.destinations[0].id == "66c7421a9591a744946348e0"
        assert related_rule2.rule.destinations[0].version_id == 53
        assert related_rule2.rule.destinations[0].device_type.value == "Fortinet"
        assert related_rule2.rule.destinations[0].ip_type.value == "IPV4"
        assert related_rule2.rule.destinations[0].referenced == "UNKNOWN"
        assert not related_rule2.rule.destinations[0].installable_target

        assert len(related_rule2.rule.destination_services) == 1
        assert (
            related_rule2.rule.destination_services[0].uid
            == "{e28c04b8-cb4b-4f8f-a733-e95e5f654f0f}"
        )
        assert related_rule2.rule.destination_services[0].name == "TCP_442"
        assert related_rule2.rule.destination_services[0].display_name == "TCP_442"
        assert related_rule2.rule.destination_services[0].origin == "DEVICE"
        assert not related_rule2.rule.destination_services[0].is_global
        assert not related_rule2.rule.destination_services[0].implicit
        assert not related_rule2.rule.destination_services[0].shared
        assert related_rule2.rule.destination_services[0].timeout == 0
        assert related_rule2.rule.destination_services[0].comment == ""
        assert related_rule2.rule.destination_services[0].version_id == 53
        assert related_rule2.rule.destination_services[0].referenced.value == "UNKNOWN"
        assert related_rule2.rule.destination_services[0].type_on_device == ""
        assert not related_rule2.rule.destination_services[0].negate
        assert not related_rule2.rule.destination_services[0].match_for_any

        assert (
            related_rule2.intersecting_objects.found_in_source.uid
            == "{e08566b5-184e-463d-b6f5-de44aeede838}"
        )
        assert (
            related_rule2.intersecting_objects.found_in_destination.uid
            == "{2c8c67e6-d1c2-48ee-a821-3e79b736d2d7}"
        )
        assert (
            related_rule2.intersecting_objects.found_in_service.uid
            == "{e28c04b8-cb4b-4f8f-a733-e95e5f654f0f}"
        )
