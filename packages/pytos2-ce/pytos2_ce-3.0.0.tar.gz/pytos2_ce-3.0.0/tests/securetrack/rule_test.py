import pytest
import os
import json
from pytos2.securechange.risk_results import SecurityPolicyViolation
import responses

from pytos2.securetrack.rule import (
    Documentation,
    SecurityRule,
    Track,
    PolicyXsiType,
    RuleLastUsage,
)
from pytos2.securetrack.network_object import ObjectReference

from pytos2.utils import get_api_node


class TestRule:
    @pytest.fixture
    def all_rules(self):
        json_dir = "tests/securetrack/json/rules"

        files = os.listdir(json_dir)
        files = [
            name
            for name in files
            if name.startswith("device-") and name.endswith(".json")
        ]

        json_list = []
        for name in files:
            json_list.append(json.load(open(os.path.join(json_dir, name), "r")))
        # json_list = [json.load(open(os.path.join(json_dir, name), "r")) for name in files]
        return json_list

    def get_rules(self, device_id):
        j = json.load(
            open(f"tests/securetrack/json/rules/device-{device_id}.json", "r")
        )

        return get_api_node(j, "rules.rule", listify=True)

    def get_rule(self, device_id, rule_id):
        rules = self.get_rules(device_id)
        for r in rules:
            if int(r["id"]) == int(rule_id):
                return r

        return None

    @pytest.fixture
    def rules_20(self):
        return self.get_rules(20)

    @pytest.fixture
    def rule_174_50(self):
        return self.get_rule(174, 50)

    def test_attributes_2(self, rule_174_50):
        rule = SecurityRule.kwargify(rule_174_50)

        assert rule.name == "Access From AWS"
        assert rule.options[0] == SecurityRule.Option.LOG_FORWARDING
        assert rule.options[1] == SecurityRule.Option.LOG_SESSION

        assert isinstance(rule.applications[0], ObjectReference)
        assert rule.applications[0].uid == "{bf62fdcf-e2c8-442e-a455-8bbc070e1cc3}"
        assert rule.applications[0].display_name == "Any"

        assert isinstance(rule.users[0], ObjectReference)
        assert rule.users[0].uid == "{bf62fdcf-e2c8-442e-a455-8bbc070e1cc3}"
        assert rule.users[0].display_name == "Any"

        assert isinstance(rule.additional_parameters[0], ObjectReference)
        assert (
            rule.additional_parameters[0].uid
            == "{8abbaf52-4dad-f129-c503-4dd83927276d}"
        )
        assert rule.additional_parameters[0].display_name == "Cloud"
        assert rule.additional_parameters[0].name == "Cloud(tag)"

        assert rule.rule_type == SecurityRule.RuleType.UNIVERSAL

        # Another test for
        # time, application, src_service, dst_service, vpn, install,
        # users, user_access, url_category, src_zone, dst_zone, additional_parameter,

    def test_attributes(self, rules_20):
        rule = rules_20[0]
        rule = SecurityRule.kwargify(rule)

        assert rule.id == 1252
        assert rule.cp_uid == "{EA9DB13E-D058-45C6-A2F0-CD731027C22B}"
        assert rule.uid == "{EA9DB13E-D058-45C6-A2F0-CD731027C22B}"
        assert rule.order == 2
        assert rule.name == ""
        assert rule.comment == "Do not touch ! access to CP !"
        assert rule.action == SecurityRule.Action.ACCEPT
        assert not rule.is_implicit
        assert not rule.is_disabled
        assert not rule.is_external
        assert rule.global_location == SecurityRule.GlobalLocation.MIDDLE
        assert not rule.acceleration_breaker
        assert not rule.is_authentication_rule
        assert rule.rule_number == 1
        assert type(rule.track) is Track
        assert rule.track.level is Track.Level.LOG
        assert len(rule.options) == 0
        assert not rule.src_networks_negated
        assert not rule.dest_networks_negated
        assert not rule.src_services_negated
        assert not rule.dest_services_negated
        assert type(rule.src_networks) is list
        assert type(rule.dest_networks) is list
        assert rule.src_networks[0].id == 3865
        assert rule.src_networks[0].display_name == "Any"
        assert rule.dest_networks[0].id == 3886
        assert rule.dest_networks[0].display_name == "SMC_10.100.200.110"

        assert rule.type == SecurityRule.Type.RULE

        # Bindings checking
        policy = rule.bindings[0].policy
        assert policy.xsi_type == PolicyXsiType.MANAGEMENT_POLICY
        assert policy.id == 17
        assert policy.name == "Standard"
        assert policy.itg_id == 20
        assert policy.itg == "ALL"
        assert policy.is_unique_active_in_itg

        binding = rule.bindings[0]
        assert binding.rule_count == 40
        assert binding.security_rule_count == 37
        assert binding.default
        assert binding.uid == "{3A1BA062-6B19-4C97-8F18-79CBA9EF0AA6}"

        # Additional parameters?

    def test_all_kwargify(self, all_rules):
        for i, _rules in enumerate(all_rules):
            if _rules is None:
                continue

            rules = get_api_node(_rules, "rules.rule", listify=True)
            for rule in rules:
                SecurityRule.kwargify(rule)


class TestRuleLastUsage:
    @responses.activate
    def test_rule_last_usage(self, rule_last_usage_mock, st):
        rule_last_usage_list = st.get_device_rule_last_usage(1)

        assert (
            rule_last_usage_list[0].rule_uid == "89e6b631-705d-4631-a92a-7266e8c31b2f"
        )
        assert not rule_last_usage_list[0].applications
        assert not rule_last_usage_list[0].users
        assert (
            rule_last_usage_list[0].rule_last_hit.strftime("%Y-%m-%d") == "2015-09-21"
        )

        assert (
            rule_last_usage_list[1].rule_uid == "d5adc685-6498-47d0-ad62-f7eeae18a069"
        )
        assert rule_last_usage_list[1].applications == {"facebook-chat": "2018-03-12"}
        assert rule_last_usage_list[1].users == {"tcselab\\ateam3": "2018-03-12"}
        assert (
            rule_last_usage_list[1].rule_last_hit.strftime("%Y-%m-%d") == "2018-03-12"
        )

        rule_last_usage = st.get_device_rule_last_usage_for_uid(
            1, "d5adc685-6498-47d0-ad62-f7eeae18a069"
        )

        assert rule_last_usage.rule_uid == "d5adc685-6498-47d0-ad62-f7eeae18a069"
        assert rule_last_usage.applications == {"facebook-chat": "2018-03-12"}
        assert rule_last_usage.users == {"lab\\ateam3": "2018-03-12"}
        assert rule_last_usage.rule_last_hit.strftime("%Y-%m-%d") == "2018-03-12"


class TestRuleDocumentation:
    @responses.activate
    def test_documentation(self, rule_documentation_mock, st):
        doc = st.get_revision_rule_documentation(24522, 53419)
        assert isinstance(doc, Documentation)

        response = st.update_rule_documentation_by_revision(24522, 53419, doc)
        assert response is None

        response = st.delete_rule_documentation_by_revision(24522, 53419)
        assert response is None

        response = st.delete_rule_documentation(264, 53419)
        assert response is None


class TestUSPViolatingRules:
    @responses.activate
    def test_violating_rules(self, violating_rules_mock, st):
        count = st.get_usp_violating_rules_count(264)
        assert count == 17

        violating_rules = st.get_usp_violating_rules(
            1, SecurityPolicyViolation.Severity.LOW
        )
        assert isinstance(violating_rules, list)
        assert violating_rules[0].id == 787
        assert violating_rules[0].order == 14


class TestRuleSearchExport:
    @responses.activate
    def test_rule_search_export(self, rule_search_export_mock, st):
        result_message = st.export_security_rules("shadowed:true")
        assert (
            result_message
            == "Results will be exported as a CSV file in the SecureTrack Reports Repository"
        )
