import json
from datetime import datetime, time as datetime_time
from typing import List, Union
from unittest import mock

from netaddr import IPNetwork, IPAddress, IPRange  # type: ignore
import pytest  # type: ignore
import responses  # type: ignore


from pytos2.securechange.fields import (
    AtType,
    AccessRequest,
    CloneServerPolicyRequest,
    Field,
    IPObject,
    MultiAccessRequest,
    MultiServerDecommissionRequest,
    MultiGroupChange,
    Target,
    TextField,
    TextArea,
    MultiTextField,
    MultiTextArea,
    Manager,
    Hyperlink,
    MultiHyperlink,
    MultiTarget,
    MultiService,
    MultiNetworkObject,
    Date,
    Time,
    ApproveReject,
    Checkbox,
    DropDownList,
    MultipleSelection,
    Zone,
    classify_group_change_member_from_api,
    GroupChange,
    GroupChangeMember,
    GroupChangeMemberHost,
    GroupChangeMemberNetwork,
    GroupChangeMemberRange,
    RuleModificationField,
    RuleRecertification,
)
from pytos2.models import UnMapped
from pytos2.securechange.ticket import Ticket
from pytos2.securechange.designer import DesignerResults
from pytos2.securechange.service import PredefinedServiceName
from pytos2.securechange.fields import Service
from pytos2.securechange.fields.rule_operation import RuleKey
from pytos2.securechange.rule import SlimRule
from pytos2.securechange.network_object import HostNetworkObject
from pytos2.securechange.fields.rule_operation import (
    ModificationTransportService,
    ModificationServiceObject,
    ModificationIcmpService,
    ModificationIPService,
    RangeDTO,
)

from pytos2.securetrack.device import Device
from pytos2.securetrack.rule import SecurityRule, BindingPolicy
from pytos2.securetrack.service_object import (
    TCPServiceObject,
    ICMPServiceObject,
    Service as STService,
    OtherIPServiceObject,
)


@pytest.fixture
def mgc(get_test_field):
    return get_test_field(MultiGroupChange)


class TestField:
    @pytest.fixture
    def generic_field(self):
        return Field.kwargify({"name": "name", "id": 123})

    def test_json_override(self, generic_field):
        assert generic_field._json == generic_field.data
        generic_field._json = {}
        assert generic_field._json == {}

    def test_read_only(self):
        field = TextArea.kwargify(
            json.load(open("tests/securechange/json/field/read_only-field.json"))
        )
        assert len(field._json) == 0

    def test_dirty(self, generic_field):
        generic_field.id = 124
        assert generic_field._dirty


class TestMultiAccessRequest:
    @pytest.fixture
    def ar(self, get_test_field):
        return get_test_field(MultiAccessRequest)

    def test_attrs(self, ar):
        assert hasattr(ar, "designer_result")
        assert isinstance(ar.access_requests, list)

    @responses.activate
    def test_designer_results(self, ar, ar_with_designer_results):
        responses.add(
            responses.GET,
            "https://10.20.50.192/securechangeworkflow/api/securechange/tickets/251/steps/1242/tasks/1254/fields/21516/designer",
            json=json.load(
                open("tests/securechange/json/designer/designer_result_251.json")
            ),
        )

        assert isinstance(
            ar_with_designer_results.designer_result.get_results(), DesignerResults
        )

        assert ar.designer_result.get_results() is None

    def test_add_arr(self, ar):
        new_ar = ar.add_ar()
        assert new_ar.sources == []


class TestAccessRequest:
    @pytest.fixture
    def ar1(self, get_test_field):
        return get_test_field(MultiAccessRequest).access_requests[0]

    def test_add_source(self, ar1):
        src = ar1.add_source("1.2.3.4")
        assert src.ip_address == "1.2.3.4"
        assert ar1.comment == "test comment mapping"

    def test_add_destination(self, ar1):
        dst = ar1.add_destination("4.3.2.1")
        assert dst.ip_address == "4.3.2.1"

    def test_add_tcp_service(self, ar1):
        svc = ar1.add_service("tcp 443")
        assert svc.port == "443"
        assert svc.protocol == Service.Protocol.TCP

    def test_add_predefined_service(self, ar1):
        svc = ar1.add_service("https")
        assert svc.name == PredefinedServiceName.HTTPS

    def test_add_invalid_predefined_service(self, ar1):
        with pytest.raises(ValueError):
            ar1.add_service("httpoo")

    @responses.activate
    def test_add_object(self, ar1, network_objects_mock):
        dst = ar1.add_destination(name="192.168.1.82V", device=174)
        assert dst.type.value == "host"

    @responses.activate
    def test_add_target(self, st, ar1, mock_devices, devices_mock):
        policy_name = "Standard"

        def test_target(target: Target, target_name: str, type: Target.ObjectType):
            assert target.type.value == type.value
            assert target.name == target_name

        def test_policy(device: Device, target_name: str, type: Target.ObjectType):
            policy = st.get_device_policy(device=device.id, policy=policy_name)
            assert isinstance(policy, BindingPolicy)
            target = ar1.add_target(device=device, policy=policy)
            test_target(target, target_name, type)

        def add_target(
            device: Device,
            target_name: str,
            type: Target.ObjectType,
        ):
            t1 = ar1.add_target(device=device, policy=policy_name)
            t2 = ar1.add_target(device=device.id, policy=policy_name)
            t3 = ar1.add_target(device=device.name, policy=policy_name)
            test_target(t1, target_name, type)
            test_target(t2, target_name, type)
            test_target(t3, target_name, type)

            if device.model is not Device.Model.ASA:
                test_policy(device, target_name, type)

            ar1.targets = []

        def device_not_found():
            target = ar1.add_target(device="Nonexistent", policy="Test")
            assert target is None

        def expect_exception(device, error, policy=policy_name):
            with pytest.raises(ValueError) as exception:
                ar1.add_target(device=device, policy=policy)

            assert error in str(exception.value)

        def test_devices(devices):
            for d in devices:
                responses.add(
                    responses.GET,
                    f"https://198.18.0.1/securetrack/api/devices/{d.id}/policies",
                    json=json.load(open("tests/securetrack/json/policies/20.json")),
                )
                device = st.get_device(d.id)
                assert isinstance(device, Device)

                name = ""
                type = None
                if device.model is Device.Model.ASA:
                    ar1.use_topology = False
                    assert ar1.use_topology is False
                    error = f"ACL name must be specified in the policy argument to add a {device.model.value} target to an AR with topology disbaled"
                    expect_exception(device, error, "")

                    name = policy_name
                    type = Target.ObjectType.ACL
                    add_target(device, name, type)

                    ar1.use_topology = True
                    assert ar1.use_topology is True
                    name = device.name
                    type = Target.ObjectType.FIREWALL
                    add_target(device, name, type)

                elif device.model in (
                    Device.Model.PANORAMA_NG_FW,
                    Device.Model.FMG_FIREWALL,
                ):
                    ar1.use_topology = False
                    assert ar1.use_topology is False
                    error = f"Cannot add a {device.model.value} target to an AR with topology disabled"
                    expect_exception(device, error)

                    ar1.use_topology = True
                    assert ar1.use_topology is True
                    name = device.name
                    type = Target.ObjectType.FIREWALL
                    add_target(device, name, type)

                elif device.model in (Device.Model.PANORAMA_DEVICE_GROUP,):
                    ar1.use_topology = True
                    assert ar1.use_topology is True
                    error = f"Cannot add a {device.model.value} target to an AR with topology enabled"
                    expect_exception(device, error)

                    ar1.use_topology = False
                    assert ar1.use_topology is False

                    name = f"{None}>{None}"
                    type = Target.ObjectType.ZONE_TO_ZONE
                    add_target(device, name, type)

                elif device.model in (Device.Model.FMG_ADOM, Device.Model.FMG_VDOM):
                    ar1.use_topology = True
                    assert ar1.use_topology is True
                    error = f"Cannot add a {device.model.value} target to an AR with topology enabled"
                    expect_exception(device, error)

                    # test for pytos2/securechange/fields/__init__.py line 767
                    # when no policy is provided this is
                    # unreachable since value error will be thrown
                    # after not finding a policy with get_policy

                    ar1.use_topology = False
                    assert ar1.use_topology is False
                    # error = "policy argument must be specified to add this type of target to this AR"
                    # expect_exception(device, error, "")

                    name = f"{None}>{None}"
                    type = Target.ObjectType.ZONE_TO_ZONE
                    add_target(device, name, type)

                elif device.model in (Device.Model.MODULE, Device.Model.MODULE_CLUSTER):
                    name = device.name
                    type = Target.ObjectType.FIREWALL
                    add_target(device, name, type)

                elif device.model in (Device.Model.CP_CMA, Device.Model.CP_SMRT_CNTR):
                    name = policy_name
                    type = Target.ObjectType.POLICY
                    add_target(device, name, type)

                else:
                    error = f"Support for {device.model.value} type targets is not been implemented."
                    expect_exception(device, error)
                    continue

        device_not_found()
        test_devices(mock_devices)

        # Testing ASA
        device = st.get_device(8)

        ar1.use_topology = True
        o = ar1.add_target(device=device)
        assert o.name == "ASAv"
        assert o.type is Target.ObjectType.FIREWALL

        # Testing ASA with use_topology off
        ar1.use_topology = False
        o = ar1.add_target(device=device, policy="TESTME")
        assert o.name == "TESTME"
        assert o.management_name == "ASAv"
        assert o.type is Target.ObjectType.ACL

    def test_jsonify(self):
        ar = AccessRequest()
        assert "sources" not in ar._json

    @responses.activate
    def test_target_count(self, st, ar1, mock_devices, devices_mock):
        policy_name = "Standard"

        def check_target_count(targets: List[Target]):
            assert len(targets) == len(ar1.targets)

        def add_targets(devices):
            targets = []
            ar1.targets = []
            for d in devices:
                responses.add(
                    responses.GET,
                    f"https://198.18.0.1/securetrack/api/devices/{d.id}/policies",
                    json=json.load(open("tests/securetrack/json/policies/157.json")),
                )
                device = st.get_device(d.id)
                assert isinstance(device, Device)

                if device.model in (
                    Device.Model.PANORAMA_NG_FW,
                    Device.Model.FMG_FIREWALL,
                ):
                    ar1.use_topology = True
                else:
                    ar1.use_topology = False

                target = ar1.add_target(
                    device=device,
                    policy="FG_SITE-A-POLICY",
                    source_zone="any",
                    destination_zone="port2",
                )
                target = ar1.add_target(
                    device=device,
                    policy="FG_SITE-B-POLICY",
                    source_zone="any",
                    destination_zone="port2",
                )
                targets.append(target)

            check_target_count(targets)

        pan = [
            d
            for d in mock_devices
            if (
                d.id in (174, 179, 180, 181, 182)
                and d.model is not Device.Model.PANORAMA_NG
            )
        ]
        add_targets(pan)

        fm = [d for d in mock_devices if d.id in (157, 159, 160, 161)]
        add_targets(fm)


class TestCloneServerPolicyRequest:
    @pytest.fixture
    def server_policy_request(self, get_test_field):
        return get_test_field(CloneServerPolicyRequest)

    def test_attrs(self, server_policy_request):
        assert isinstance(server_policy_request.to_servers, list)
        assert isinstance(server_policy_request.to_servers[0], IPObject)
        assert server_policy_request.from_server.ip_address == "192.168.2.200"


class TestMultiServerDecommissionRequest:
    @pytest.fixture
    def server_decom(self, get_test_field):
        return get_test_field(MultiServerDecommissionRequest)

    def test_attrs(self, server_decom):
        assert isinstance(server_decom.server_decommission_requests, list)
        assert (
            server_decom.server_decommission_requests[0].comment
            == "Example Server Decom"
        )

    def test_add_server(self, server_decom):
        server_decom.server_decommission_requests[0].add_server("1.2.3.4")
        assert (
            server_decom.server_decommission_requests[0].servers[-1].ip_address
            == "1.2.3.4"
        )

    def test_add_bad_server(self, server_decom):
        with pytest.raises(ValueError):
            server_decom.server_decommission_requests[0].add_server("foobar")

    def test_kwargify_ticket(self, ticket_488):
        ticket = Ticket.kwargify(ticket_488)
        assert ticket.id == 488


class TestMultiGroupChange:
    def test_attrs(self, mgc):
        assert hasattr(mgc, "group_changes")
        assert isinstance(mgc.group_changes, list)

    def test_delete_member(self, mgc):
        member = mgc.group_changes[7].members[0]
        with pytest.raises(AssertionError):
            member.delete()
        member = mgc.group_changes[2].members[0]
        deleted_member = member.delete()
        assert isinstance(deleted_member, GroupChangeMemberHost)
        assert deleted_member.id == 1130
        assert deleted_member.management_id == 5
        assert str(deleted_member.ip) == "10.10.20.50"
        assert deleted_member.status.value == "DELETED"
        re_deleted_member = member.delete()
        assert re_deleted_member == deleted_member


class TestGroupChange:
    def test_address_book(self, mgc):
        assert str(mgc.group_changes[3].address_book) == "global"

    def test_zone(self, mgc):
        assert str(mgc.group_changes[7].zone) == "ssl.External"


class TestAddGroupChange:
    def test_bad_args(self, mgc):
        with pytest.raises(ValueError):
            mgc.add_group_change("thing")

    @responses.activate
    def test_bad_device(self, network_objects_mock, mgc):
        with pytest.raises(ValueError):
            mgc.add_group_change("bad", 1000000)

    @responses.activate
    def test_new_group(self, network_objects_mock, mgc: MultiGroupChange):
        res = mgc.add_group_change("new_group", 157)
        assert isinstance(res, GroupChange)

    @responses.activate
    def test_bad_uid(self, network_objects_mock, mgc):
        with pytest.raises(ValueError):
            mgc.add_group_change(uid="afb2d78d-356a-4a86-805a-000000000000")

    @responses.activate
    def test_bad_object_type(self, network_objects_mock, mgc):
        with pytest.raises(ValueError):
            mgc.add_group_change(uid="afb2d78d-356a-4a86-805a-c80afee8e338")

    @responses.activate
    def test_existing_group(self, network_objects_mock, mgc):
        res = mgc.add_group_change("New_group", 243)
        assert isinstance(res, GroupChange)


class TestAddMember:
    @pytest.fixture
    def gc(self, get_test_field):
        return get_test_field(MultiGroupChange).group_changes[9]

    @pytest.fixture
    def gc1(self, get_test_field):
        return get_test_field(MultiGroupChange).group_changes[0]

    @pytest.fixture
    def gc2(self, get_test_field):
        return get_test_field(MultiGroupChange).group_changes[2]

    @pytest.mark.parametrize(
        "name, details_arg, details, at_type, type",
        [
            (
                "newhost",
                "1.2.3.4",
                "1.2.3.4",
                GroupChangeMemberHost,
                GroupChangeMember.ObjectType.HOST,
            ),
            (
                "newnetwork",
                "1.2.3.0/24",
                "1.2.3.0/255.255.255.0",
                GroupChangeMemberNetwork,
                GroupChangeMember.ObjectType.NETWORK,
            ),
            (
                "newrange",
                "2.2.2.2-3.3.3.3",
                "[ 2.2.2.2 - 3.3.3.3 ]",
                GroupChangeMemberRange,
                GroupChangeMember.ObjectType.ADDRESS_RANGE,
            ),
        ],
    )
    def test_new(self, gc, name, details_arg, details, at_type, type):
        member = gc.add_member(name=name, details=details_arg)
        assert isinstance(member, GroupChangeMember)
        assert member.details == details
        assert isinstance(member, at_type)
        assert member.type is type

    def test_existing(self, gc):
        add_res = gc.add_member(name="new_net", details="1.3.4.0/255.255.255.0")
        assert add_res is None

    @responses.activate
    def test_uid(self, gc, network_objects_mock):
        add_res = gc.add_member(uid="20dcde39-b1ac-4013-adbb-81a5a705801d")
        assert isinstance(add_res, GroupChangeMember)
        assert add_res.uid == "20dcde39-b1ac-4013-adbb-81a5a705801d"

    @responses.activate
    def test_already_added_uid(self, gc2, network_objects_mock):
        add_res = gc2.add_member(uid="b4e77d4c-f471-4bb2-bfff-69503bdd6669")
        assert add_res is None

    @responses.activate
    def test_deleted_uid(self, gc1, network_objects_mock):
        add_res = gc1.add_member(uid="b17b4120-07d4-0875-d4b2-06227767ff57")
        assert isinstance(add_res, GroupChangeMember)

    @responses.activate
    def test_uid_missing(self, gc1, network_objects_mock):
        with pytest.raises(ValueError):
            gc1.add_member(uid="b17b4120-07d4-0875-d4b2-000000000000")

    @responses.activate
    def add_target_missing(self, mgc, network_objects_mock):
        group_change = GroupChange(name="moo", management_id=100000000)
        with pytest.raises(ValueError):
            group_change.add_member(uid="1111111111111111111111111111")

    def test_new_from_other_group(self, gc):
        add_res = gc.add_member(name="nost", details="3.3.3.3")
        assert isinstance(add_res, GroupChangeMember)
        assert add_res.at_type is AtType.OBJECT
        add_res = gc.add_member(name="nost", details="3.3.3.3")
        assert add_res is None

    def test_existing_mismatch(self, gc):
        with pytest.raises(ValueError):
            gc.add_member(name="nost", details="2.2.2.2")
        with pytest.raises(ValueError):
            gc.add_member(name="new_net", details="1.3.5.0/24")

    def test_bad_member(self, gc):
        with pytest.raises(ValueError):
            gc.add_member(name="bad", details="300.10.10.0")

    def test_args(self, gc):
        with pytest.raises(TypeError):
            gc.add_member(name="thing")


class TestGroupChangeMember:
    @pytest.fixture
    def mgc(self, get_test_field):
        return get_test_field(MultiGroupChange)

    def test_host(self, mgc):
        member = mgc.group_changes[0].members[0]
        assert member.details == "1.1.1.1"
        assert member.ip == IPAddress("1.1.1.1")
        member.ip = IPAddress("1.2.3.5")
        assert member.details == "1.2.3.5"
        with pytest.raises(ValueError):
            member.ip = "garbage"

    def test_network(self, mgc):
        member = mgc.group_changes[5].members[0]
        assert member.details == "10.10.103.0/255.255.255.0"
        assert member.network == IPNetwork("10.10.103.0/24")
        member.network = IPNetwork("10.12.14.0/24")
        assert member.details == "10.12.14.0/255.255.255.0"
        with pytest.raises(ValueError):
            member.network = "garbage"

    def test_range(self, mgc):
        member = mgc.group_changes[6].members[3]
        assert member.details == "[ 127.0.0.1 - 127.255.255.255 ]"
        assert member.range == IPRange("127.0.0.1", "127.255.255.255")
        member.range = "6.6.6.20-6.6.6.40"
        assert member.details == "[ 6.6.6.20 - 6.6.6.40 ]"
        with pytest.raises(ValueError):
            member.range = "garbage"

    def test_classify(self):
        assert isinstance(
            classify_group_change_member_from_api({"some": "field"}), UnMapped
        )


def test_approve_reject(get_test_field):
    field = get_test_field(ApproveReject)
    assert field.approved is bool(field) is True
    field.reject()
    assert field.approved is False
    assert field.reason == "None provided"
    field.approve("because")
    assert field.approved is True
    assert field.reason == "because"


def test_check_box(get_test_field):
    field = get_test_field(Checkbox)
    assert field.value is field.checked is bool(field) is True
    field.uncheck()
    assert field.value is False
    field.check()
    assert field.value is True
    field.toggle()
    assert field.value is False


class TestDate:
    @pytest.fixture
    def date(self, get_test_field):
        return get_test_field(Date)

    def test_value(self, date):
        assert date.value == "2019-05-08"

    def test_set_date(self, date):
        date.date = datetime(1988, 9, 11)
        assert date.value == "1988-09-11"

    def test_set_str_date(self, date):
        date.date = "1988-09-11"
        assert date.date == datetime(1988, 9, 11).date()

    def test_invalid_set_date(self, date):
        with pytest.raises(TypeError):
            date.date = "198-9-11"


class TestTime:
    @pytest.fixture
    def time(self, get_test_field):
        return get_test_field(Time)

    def test_value(self, time):
        assert time.value == "12:00"

    def test_set_time(self, time):
        time.time = datetime_time(5, 30)
        assert time.value == "05:30"

    def test_invalid_set_time(self, time):
        with pytest.raises(TypeError):
            time.time = "05:30"


class TestRuleRecertification:
    @responses.activate
    def test_is_invalid_rule(
        self, device_20_rules, device_1_rules, search_rules_on_open_tickets_mock
    ):
        recert = RuleRecertification()

        rules = [device_20_rules[0], device_20_rules[1], device_1_rules[0]]

        for rule in rules:
            recert.add_rule(rule)

        for rule in rules:
            is_invalid = recert.is_invalid_rule(rule)
            assert is_invalid is False

    def test_add_rule(self, device_20_rules, device_1_rules):
        recert = RuleRecertification()

        rule = device_20_rules[0]
        rule2 = device_20_rules[1]
        rule3 = device_1_rules[0]

        recert.add_rule(rule)
        recert.add_rule(rule2)
        recert.add_rule(rule3)

        rules = recert.get_rules()
        assert len(rules) == 3

    def test_add_rules(self, device_20_rules, device_1_rules):
        recert = RuleRecertification()

        rules = [device_20_rules[0], device_20_rules[1], device_1_rules[0]]

        recert.add_rules(rules)

        rules = recert.get_rules()
        assert len(rules) == 3


class TestRuleModification:
    @pytest.fixture
    def rule_mod(self, get_test_field):
        return get_test_field(RuleModificationField)

    def test_id(self, rule_mod):
        assert rule_mod.id == 24670
        assert rule_mod.rule_modifications[0].id == 3
        assert rule_mod.rule_modifications[0].source_modifications.id == 4

    def test_rule_key(self, rule_mod):
        rule_modification = rule_mod.rule_modifications[0]
        assert isinstance(rule_modification.rule_key, RuleKey)
        assert rule_modification.rule_key == RuleKey(
            device_id=20,
            binding_uid="{3A1BA062-6B19-4C97-8F18-79CBA9EF0AA6}",
            rule_uid="{C610F0C8-C339-11E4-9E5F-7F0000011414}",
        )

    def test_get_rules(self, rule_mod):
        rules = rule_mod.get_rules()
        assert len(rules) == 1
        assert isinstance(rules[0], SlimRule)

    def test_is_rule_added(self, rule_mod):
        rule = SecurityRule(uid="{C610F0C8-C339-11E4-9E5F-7F0000011414}")
        rule2 = SecurityRule(uid="{C610F0C8-C339-11E4-9E5F-7F0000011434}")

        assert rule_mod.is_rule_added(rule)
        assert not rule_mod.is_rule_added(rule2)

    def test_add_rule(self, device_20_rules, device_20_network_objects):
        rule_mod = RuleModificationField()

        rule = device_20_rules[0]

        rule_mod.add_destination_object(
            rule, HostNetworkObject(id=0, name="TestObject", ip="1.2.3.4")
        )

        rules = rule_mod.get_rules()
        assert len(rules) == 1

        rule_mod.add_source_object(device_20_rules[1], device_20_network_objects[0])

        rules = rule_mod.get_rules()
        assert len(rules) == 2

        rule_mod.add_service(
            device_20_rules[1],
            ModificationTransportService(
                name="Test", comment="Test2", port=RangeDTO(from_=443, to=448)
            ),
        )

    def test_removes(self, device_20_rules, device_20_network_objects):
        rule_mod = RuleModificationField()

        rule = device_20_rules[0]

        # 84 = SMCPM
        rule_mod.remove_destination_object(rule, device_20_network_objects[84])
        assert len(rule_mod.get_rules()) == 1

        # Some random network object that isn't included in the rule
        assert not rule_mod.remove_destination_object(
            device_20_rules[1], device_20_network_objects[50]
        )

        # 137 = m01
        rule_mod.remove_source_object(
            device_20_rules[1], device_20_network_objects[137]
        )
        assert len(rule_mod.get_rules()) == 2

    @responses.activate
    def test_rule_prop(self, device_20_rules, device_20_rules_mock):
        rule = device_20_rules[0]
        rule_mod = RuleModificationField()

        rule_mod.add_destination_object(
            rule, HostNetworkObject(id=0, name="TestObject", ip="1.2.3.4")
        )

        mod = rule_mod.rule_modifications[0]
        assert mod.rule.uid == rule.uid
        mod._rule = None
        assert mod.rule.uid == rule.uid

    def test_from_securetrack(self):
        obj = TCPServiceObject(
            comment="Hello Comment",
            name="Hello Name",
            protocol=6,
            min_port=443,
            max_port=443,
        )
        o = ModificationServiceObject.from_securetrack(obj)

        assert o.port.from_ == 443
        assert o.port.to == 443
        assert o.protocol == "TCP"
        assert isinstance(o, ModificationTransportService)

        obj = ICMPServiceObject(
            comment="icmp", name="icmp srvc", min_port=40, max_port=40
        )
        o = ModificationServiceObject.from_securetrack(obj)

        assert o.type.from_ == 40
        assert o.type.to == 40
        assert isinstance(o, ModificationIcmpService)

        obj = STService(comment="hello test", name="blah blah")
        o = ModificationServiceObject.from_securetrack(obj)
        assert isinstance(o, ModificationServiceObject)

        obj = OtherIPServiceObject(name="other ip server object")
        o = ModificationServiceObject.from_securetrack(obj)
        assert isinstance(o, ModificationIPService)


def test_drop_down_list(get_test_field):
    field = get_test_field(DropDownList)
    assert isinstance(field.options, list)


def test_hyperlink(get_test_field):
    field = get_test_field(Hyperlink)
    assert field.url == "http://"


def test_multi_hyperlink(get_test_field):
    field = get_test_field(MultiHyperlink)
    assert all(isinstance(h, Hyperlink) for h in field.hyperlinks)


def test_manager(get_test_field):
    field = get_test_field(Manager)
    assert isinstance(field.text, str)


def test_multiple_selection(get_test_field):
    field = get_test_field(MultipleSelection)
    # TODO test comparison
    assert isinstance(field.options, list) and isinstance(field.selected_options, list)


def test_multi_network_object(get_test_field):
    field = get_test_field(MultiNetworkObject)
    assert isinstance(field.network_objects, list)


def test_multi_service(get_test_field):
    field = get_test_field(MultiService)
    assert isinstance(field.services, list)


def test_multi_target(get_test_field):
    field = get_test_field(MultiTarget)
    assert isinstance(field.targets, list)


def test_text_field(get_test_field):
    field = get_test_field(TextField)
    assert field.text == "test"


def test_multi_text_field(get_test_field):
    field = get_test_field(MultiTextField)
    assert [t.text for t in field.text_fields] == ["a", "b"]


def test_text_area(get_test_field):
    field = get_test_field(TextArea)
    assert field.text == "test"


def test_multi_text_area(get_test_field):
    field = get_test_field(MultiTextArea)
    assert [t.text for t in field.text_areas] == ["1", "2"]
