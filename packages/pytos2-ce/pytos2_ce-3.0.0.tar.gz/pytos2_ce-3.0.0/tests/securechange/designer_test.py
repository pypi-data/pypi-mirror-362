import pytest  # type: ignore
import json
from pytos2.securechange.designer import (
    DesignerResults,
    DeviceSuggestion,
    BindingSuggestion,
    get_instruction_type,
    classify_object_type,
    classify_service_type,
    NetworkObject,
    HostObject,
    RangeObject,
    SubnetObject,
    GroupObject,
    Instruction,
    AddNetworkObjectInstruction,
    UpdateRuleInstruction,
    AddNewRuleInstruction,
    FullyImplementedInstruction,
    ServiceObject,
    IPService,
    ServiceGroup,
    Rule,
)

from pytos2.securechange.designer_verifier_common import (
    TransportService,
    ICMPService,
)

from pytos2.utils import get_api_node

import responses


# need to load proper json file
@pytest.fixture
def load_instruction_json_by_type():
    def f(instruction_class):
        return instruction_class.kwargify(
            json.load(
                open(
                    f"tests/securechange/json/field/{instruction_class._type.value}-field.json"
                )
            )
        )


class TestDesignerResults:
    @pytest.fixture
    def designer_results(self):
        j = json.load(open("tests/securechange/json/designer/designer_results.json"))
        return DesignerResults.kwargify(j)

    def test_attributes(self, designer_results):
        assert designer_results.id == 1458
        assert hasattr(designer_results, "device_suggestions")
        assert isinstance(designer_results, DesignerResults)

    def test_get_instruction_by_id(self, designer_results):
        instruction_2967 = designer_results.get_instruction_by_id(2967)
        assert instruction_2967.id == 2967
        assert instruction_2967.instruction_type == Instruction.InstructionType.NEW_RULE
        assert isinstance(instruction_2967, Instruction)
        assert isinstance(instruction_2967, AddNewRuleInstruction)


class TestDeviceSuggestion:
    @pytest.fixture
    def suggestion(self):
        j = json.load(open("tests/securechange/json/designer/designer_results.json"))
        device_suggestion_node = get_api_node(
            j, "designer_results.suggestions_per_device.device_suggestion"
        )
        return DeviceSuggestion.kwargify(device_suggestion_node)

    def test_attributes(self, suggestion):
        assert suggestion.id == 815
        assert suggestion.management_name == "DG-B"
        assert suggestion.vendor_name == "PaloAltoNetworks"
        assert suggestion.offline_device is False
        assert suggestion.ancestor_management_name == "PANO-8"


class TestBindingSuggestion:
    @pytest.fixture
    def suggestion(self):
        j = json.load(open("tests/securechange/json/designer/designer_results.json"))
        binding_suggestion_node = get_api_node(
            j,
            "designer_results.suggestions_per_device.device_suggestion.suggestions_per_binding.binding_suggestion",
        )
        return BindingSuggestion.kwargify(binding_suggestion_node)

    def test_attributes(self, suggestion):
        assert suggestion.binding_uid == "{00-FACED0-00}"
        assert type(suggestion.binding_name) is str


class TestFullyImplementedInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open("tests/securechange/json/designer/fully_implemented-instruction.json")
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_FULLY_IMPLEMENTED"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.FULLY_IMPLEMENTED
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is False
        assert hasattr(instruction, "rule") is False or instruction.rule is None

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, FullyImplementedInstruction)
        assert isinstance(instruction, Instruction)


class TestFullyImplementedNoSecurityInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/fully_implemented_since_no_security-instruction.json"
            )
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_FULLY_IMPLEMENTED"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.NO_SECURITY_ON_INTERFACE
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is False
        assert hasattr(instruction, "rule") is False or instruction.rule is None

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, FullyImplementedInstruction)
        assert isinstance(instruction, Instruction)


class TestAddHostObjectInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_host_object-instruction.json"
            )
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.ADD_OBJECT_TO_DEVICE
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is True
        # assert isinstance(instruction.modified_object_name, str)  # not mapped

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, AddNetworkObjectInstruction)
        assert isinstance(instruction, Instruction)


class TestAddedHostObject:
    @pytest.fixture
    def device_added_host_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_host_object-instruction.json"
            )
        )
        device_added_host_object = get_api_node(j, "device_added_network_object")
        return classify_object_type(device_added_host_object)

    def test_attributes(self, device_added_host_object):
        assert device_added_host_object.uid == "-9"
        assert device_added_host_object.name == "Host_172.16.90.5"
        assert device_added_host_object.display_name == "Host_172.16.90.5"
        assert device_added_host_object.origin == "DEVICE"
        assert device_added_host_object.is_global is False
        assert device_added_host_object.implicit is False
        assert device_added_host_object.shared is False
        assert device_added_host_object.id == 3156
        assert device_added_host_object.ip_type == NetworkObject.IPType.IPV4

    def test_object_inheritance(self, device_added_host_object):
        assert isinstance(device_added_host_object, NetworkObject)
        assert isinstance(device_added_host_object, HostObject)


class TestAddRangeObjectInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_range_object-instruction.json"
            )
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.ADD_OBJECT_TO_DEVICE
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is True

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, AddNetworkObjectInstruction)
        assert isinstance(instruction, Instruction)


class TestAddedRangeObject:
    @pytest.fixture
    def device_added_range_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_range_object-instruction.json"
            )
        )
        device_added_range_object = get_api_node(j, "device_added_network_object")
        return classify_object_type(device_added_range_object)

    def test_attributes(self, device_added_range_object):
        assert device_added_range_object.uid == "-13"
        assert device_added_range_object.name == "1.2.3.4-1.2.3.10"
        assert device_added_range_object.display_name == "1.2.3.4-1.2.3.10"
        assert device_added_range_object.origin == "DEVICE"
        assert device_added_range_object.is_global is False
        assert device_added_range_object.implicit is True
        assert device_added_range_object.shared is False
        assert device_added_range_object.id == 3290
        assert device_added_range_object.ip_type == NetworkObject.IPType.IPV4
        assert device_added_range_object.min_ip == "1.2.3.4"
        assert device_added_range_object.max_ip == "1.2.3.10"

    def test_object_inheritance(self, device_added_range_object):
        assert isinstance(device_added_range_object, NetworkObject)
        assert isinstance(device_added_range_object, RangeObject)


class TestAddSubnetObjectInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_subnet_object-instruction.json"
            )
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.ADD_OBJECT_TO_DEVICE
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is True

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, AddNetworkObjectInstruction)
        assert isinstance(instruction, Instruction)


class TestAddedSubnetObject:
    @pytest.fixture
    def device_added_subnet_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_subnet_object-instruction.json"
            )
        )
        device_added_subnet_object = get_api_node(j, "device_added_network_object")
        return classify_object_type(device_added_subnet_object)

    def test_attributes(self, device_added_subnet_object):
        assert device_added_subnet_object.uid == "-1"
        assert device_added_subnet_object.name == "Subnet_9.8.7.0"
        assert device_added_subnet_object.display_name == "Subnet_9.8.7.0"
        assert device_added_subnet_object.origin == "DEVICE"
        assert device_added_subnet_object.is_global is False
        assert device_added_subnet_object.implicit is False
        assert device_added_subnet_object.shared is False
        assert device_added_subnet_object.id == 3305
        assert device_added_subnet_object.ip_type == NetworkObject.IPType.IPV4

    def test_object_inheritance(self, device_added_subnet_object):
        assert isinstance(device_added_subnet_object, NetworkObject)
        assert isinstance(device_added_subnet_object, SubnetObject)


class TestAddGroupObjectInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_subnet_object-instruction.json"
            )
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert (
            instruction.instruction_type
            == Instruction.InstructionType.ADD_OBJECT_TO_DEVICE
        )
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is True

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, AddNetworkObjectInstruction)
        assert isinstance(instruction, Instruction)


class TestAddedGroupObject:
    @pytest.fixture
    def device_added_group_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_network_group_object-instruction.json"
            )
        )
        device_added_group_object = get_api_node(j, "device_added_network_object")
        return classify_object_type(device_added_group_object)

    def test_attributes(self, device_added_group_object):
        assert device_added_group_object.uid == "-17"
        assert device_added_group_object.name == "NetworkGroup_45"
        assert device_added_group_object.display_name == "NetworkGroup_45"
        assert device_added_group_object.origin == "DEVICE"
        assert device_added_group_object.is_global is False
        assert device_added_group_object.implicit is False
        assert device_added_group_object.shared is False
        assert device_added_group_object.id == 3292
        assert device_added_group_object.ip_type == NetworkObject.IPType.OTHER
        assert hasattr(device_added_group_object, "members")
        assert isinstance(device_added_group_object.members, list)

    def test_object_inheritance(self, device_added_group_object):
        assert isinstance(device_added_group_object, NetworkObject)
        assert isinstance(device_added_group_object, GroupObject)

    def test_member_attribute(self, device_added_group_object):
        assert device_added_group_object.members[0].uid == "-13"
        assert device_added_group_object.members[0].name == "1.2.3.4-1.2.3.10"
        assert device_added_group_object.members[0].display_name == "1.2.3.4-1.2.3.10"
        assert device_added_group_object.members[0].origin == "DEVICE"
        assert device_added_group_object.members[0].is_global is False
        assert device_added_group_object.members[0].implicit is True
        assert device_added_group_object.members[0].shared is False
        assert device_added_group_object.members[0].id == 3290
        assert device_added_group_object.members[0].ip_type == NetworkObject.IPType.IPV4
        assert device_added_group_object.members[0].min_ip == "1.2.3.4"
        assert device_added_group_object.members[0].max_ip == "1.2.3.10"

    def test_member_inheritance(self, device_added_group_object):
        assert isinstance(device_added_group_object.members[0], NetworkObject)
        assert isinstance(device_added_group_object.members[0], RangeObject)


class TestAddTransportServiceObject:
    @pytest.fixture
    def device_added_service_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_transport_service_object-instruction.json"
            )
        )
        device_added_service_object = get_api_node(j, "device_added_service_object")
        return classify_service_type(device_added_service_object)

    def test_attributes(self, device_added_service_object):
        assert device_added_service_object.uid == "-21"
        assert device_added_service_object.name == "TCP_1234"
        assert device_added_service_object.display_name == "TCP_1234"
        assert device_added_service_object.origin == "DEVICE"
        assert device_added_service_object.is_global is False
        assert device_added_service_object.implicit is False
        assert device_added_service_object.shared is False
        assert device_added_service_object.id == 1361
        assert device_added_service_object.protocol == 6
        assert device_added_service_object.min_port == 1234
        assert device_added_service_object.max_port == 1234


class TestAddICMPServiceObject:
    @pytest.fixture
    def device_added_service_object(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_icmp_service_object-instruction.json"
            )
        )
        device_added_service_object = get_api_node(j, "device_added_service_object")
        return classify_service_type(device_added_service_object)

    def test_attributes(self, device_added_service_object):
        assert device_added_service_object.uid == "-15"
        assert device_added_service_object.name == "ICMP_253"
        assert device_added_service_object.display_name == "ICMP_253"
        assert device_added_service_object.origin == "DEVICE"
        assert device_added_service_object.is_global is False
        assert device_added_service_object.implicit is False
        assert device_added_service_object.shared is False
        assert device_added_service_object.id == 1435
        assert hasattr(device_added_service_object, "protocol") is False
        assert hasattr(device_added_service_object, "min_port") is False
        assert hasattr(device_added_service_object, "max_port") is False
        assert device_added_service_object.min_icmp_type == 253
        assert device_added_service_object.max_icmp_type == 253


class TestAddServiceGroup:
    @pytest.fixture
    def device_added_service_group(self):
        j = json.load(
            open("tests/securechange/json/designer/add_service_group-instruction.json")
        )
        device_added_service_group = get_api_node(j, "device_added_service_object")
        return classify_service_type(device_added_service_group)

    def test_attributes(self, device_added_service_group):
        assert device_added_service_group.uid == "-33"
        assert device_added_service_group.name == "ServiceGroup_32"
        assert device_added_service_group.display_name == "ServiceGroup_32"
        assert device_added_service_group.origin == "DEVICE"
        assert device_added_service_group.is_global is False
        assert device_added_service_group.implicit is False
        assert device_added_service_group.shared is False
        assert device_added_service_group.id == 1432
        assert hasattr(device_added_service_group, "protocol") is False
        assert hasattr(device_added_service_group, "min_port") is False
        assert hasattr(device_added_service_group, "max_port") is False
        assert hasattr(device_added_service_group, "min_icmp_type") is False
        assert hasattr(device_added_service_group, "max_icmp_type") is False
        assert isinstance(device_added_service_group.members, list)

    def test_object_inheritance(self, device_added_service_group):
        assert isinstance(device_added_service_group, ServiceObject)
        assert isinstance(device_added_service_group, ServiceGroup)

    def test_member_attribute(self, device_added_service_group):
        assert device_added_service_group.members[0].uid == "-29"
        assert device_added_service_group.members[0].display_name == "icmp 253"
        assert device_added_service_group.members[0].origin == "DEVICE"
        assert device_added_service_group.members[0].is_global is False
        assert device_added_service_group.members[0].implicit is True
        assert device_added_service_group.members[0].shared is False
        assert device_added_service_group.members[0].id == 1433
        assert device_added_service_group.members[0].min_icmp_type == 253
        assert device_added_service_group.members[0].max_icmp_type == 253

        assert device_added_service_group.members[1].uid == "-31"
        assert device_added_service_group.members[1].display_name == "udp 343"
        assert device_added_service_group.members[1].origin == "DEVICE"
        assert device_added_service_group.members[1].is_global is False
        assert device_added_service_group.members[1].implicit is True
        assert device_added_service_group.members[1].shared is False
        assert device_added_service_group.members[1].id == 1434
        assert device_added_service_group.members[1].protocol == 17
        assert device_added_service_group.members[1].min_port == 343
        assert device_added_service_group.members[1].max_port == 343


class TestAddNewRuleInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open("tests/securechange/json/designer/add_new_rule-instruction.json")
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert instruction.instruction_type == Instruction.InstructionType.NEW_RULE
        assert instruction.rule_placement.value == "BEFORE"
        assert instruction.change_action.value == "ADD"
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is False
        assert hasattr(instruction, "rule") is True

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, AddNewRuleInstruction)
        assert isinstance(instruction, Instruction)


class TestNewRule:
    @pytest.fixture
    def rule(self):
        j = json.load(
            open("tests/securechange/json/designer/add_new_rule-instruction.json")
        )
        rule_json = get_api_node(j, "rule")
        return Rule.kwargify(rule_json)

    def test_attributes(self, rule):
        assert rule.uid == "-24"
        assert rule.is_disabled is False
        assert rule.from_zone == "Inside"
        assert rule.to_zone == "DMZ"

    def test_object_inheritance(self, rule):
        assert isinstance(rule, Rule)


class TestNewRuleAnyService:
    @pytest.fixture
    def rule(self):
        j = json.load(
            open(
                "tests/securechange/json/designer/add_new_rule_any_service-instruction.json"
            )
        )
        rule_json = get_api_node(j, "rule")
        return Rule.kwargify(rule_json)

    def test_attributes(self, rule):
        assert rule.uid == "-22"
        assert rule.is_disabled is False
        assert rule.from_zone == "any"
        assert rule.to_zone == "any"

    def test_object_inheritance(self, rule):
        assert isinstance(rule, Rule)

    def test_any_service(self, rule):
        assert isinstance(rule.services, list)
        assert rule.services[0].uid == "00000000-0000-0000-0000-000000000000"
        assert rule.services[0].name == "Any"
        assert rule.services[0].origin == "PROVISIONING"
        assert rule.services[0].is_global is False
        assert rule.services[0].implicit is False
        assert rule.services[0].shared is False
        assert rule.services[0].min_protocol == 0
        assert rule.services[0].max_protocol == 255
        assert isinstance(rule.destination_services[0], IPService)


class TestUpdateRuleInstruction:
    @pytest.fixture
    def instruction(self):
        j = json.load(
            open("tests/securechange/json/designer/update_rule-instruction.json")
        )
        return get_instruction_type(j)

    def test_attributes(self, instruction):
        assert instruction.implements_access_requests == ["AR1"]
        assert instruction.status == "DESIGN_SUCCESS"
        assert instruction.instruction_type == Instruction.InstructionType.UPDATE_RULE
        assert hasattr(instruction, "device_added_service_object") is False
        assert hasattr(instruction, "device_added_network_object") is False
        assert hasattr(instruction, "object") is False
        assert hasattr(instruction, "rule") is True
        assert (
            instruction.rule.destination_services[0].referenced
            == ServiceObject.Referenced.UNKNOWN
        )

        assert len(instruction.sources) > 0
        assert len(instruction.destinations) > 0
        assert len(instruction.services) > 0

    def test_object_inheritance(self, instruction):
        assert isinstance(instruction, UpdateRuleInstruction)
        assert isinstance(instruction, Instruction)


@pytest.fixture
def services_mock(st, st_devices_mock):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/1/services",
        json=json.load(open("tests/securetrack/json/services/1.json")),
    )


class TestServiceObjectCasts:
    @responses.activate
    def test_casts(self, st, services_mock):
        services = st.get_services(1)
        assert services is not None

        svc0 = services[0]
        svc = ServiceObject.from_securetrack(svc0)
        assert svc.min_port == 902
        assert svc.max_port == 902
        assert isinstance(svc, TransportService)

        svc419 = services[419]
        svc = ServiceObject.from_securetrack(svc419)
        assert svc.management_domain == "Shared"
        assert isinstance(svc, ICMPService)
