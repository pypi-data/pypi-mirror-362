from typing import List
import pytest
import json

from pytos2.api import Pager
from pytos2.securetrack.rule import SecurityRule
from . import conftest

from pytos2.securetrack.service_object import (
    Service,
    ServiceXsiType,
    ServiceObjectReference,
    TCPServiceObject,
    UDPServiceObject,
    ICMPServiceObject,
    IPServiceObject,
    PortServiceObject,
    ICMPV6ServiceObject,
    ICMPV6IPServiceObject,
    OtherServiceObject,
    OtherIPServiceObject,
    AnyObject,
    AnyIPServiceObject,
    ServiceGroup,
    RPCServiceObject,
    DCERPCService,
    DefaultService,
    classify_service_object,
)
import responses
from pytos2.utils import get_api_node


class TestAuroraService:
    @pytest.fixture
    def services_list(self):
        j = json.load(open("tests/securetrack/json/services/aurora339.json"))
        service_node = get_api_node(j, "services.service")
        return [classify_service_object(service) for service in service_node]

    def test_service_objects(self, services_list):
        assert len(services_list) == 325

    @responses.activate
    def test_various_services_endpoints(self, services_mock, st):
        pager = st.search_services(uid="3fbd8116-3801-4bee-8593-3cbf999da671")
        assert isinstance(pager, Pager)
        services = pager.fetch_all()
        assert len(services) == 13
        assert isinstance(services[0], Service)

        assert isinstance(services[12], ServiceGroup)
        assert hasattr(services[12], "members")
        assert len(services[12].members) == 2

        groups = st.get_service_groups(2961503)
        assert isinstance(groups, list)
        assert len(groups) == 2
        assert isinstance(groups[0], ServiceGroup)

        pager = st.get_service_rules(2937342)
        assert isinstance(pager, Pager)
        rules = pager.fetch_all()
        assert len(rules) == 6
        assert isinstance(rules[0], SecurityRule)

        pager = st.get_services(8, name="daytime")
        assert isinstance(pager, Pager)
        services = pager.fetch_all()
        assert len(services) == 2
        assert isinstance(services[0], Service)

        pager = st.get_services(revision=24522, name="MSExchange")
        assert isinstance(pager, Pager)
        services = pager.fetch_all()
        assert len(services) == 1
        assert isinstance(services[0], Service)

        services = st.get_services(revision=24522, object_ids=[3330108])
        assert len(services) == 4
        assert isinstance(services[0], Service)

        services = st.get_services(8, object_ids=[3099979])
        assert len(services) == 1
        assert isinstance(services[0], Service)


class TestService:
    @pytest.fixture
    def services_list(self):
        j = json.load(open("tests/securetrack/json/services/1.json"))
        service_node = get_api_node(j, "services.service")
        return [classify_service_object(service) for service in service_node]

    def test_attributes(self, services_list):
        assert services_list[0].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[0].id == 2878000
        assert services_list[0].name == "902 (tcp)"
        assert services_list[0].display_name == "902"
        assert services_list[0].class_name == Service.ClassName.TCP_SERVICE
        assert services_list[0].type == Service.Type.TCP_SERVICE
        assert services_list[0].is_global is False
        assert services_list[0].comment == ""
        assert services_list[0].uid == "{4647cde8-ba3f-4721-b40b-818545261f1a}"
        assert services_list[0].overrides is False
        assert services_list[0].min_port == 902
        assert services_list[0].max_port == 902
        assert services_list[0].protocol == Service.Protocol.TCP.value
        assert services_list[0].negate is False
        assert services_list[0].timeout == "0"
        assert services_list[0].is_implicit is True

        assert services_list[2].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[2].id == 2877997
        assert services_list[2].name == "Any"
        assert services_list[2].display_name == "Any"
        assert services_list[2].class_name == Service.ClassName.ANY_OBJECT
        assert services_list[2].type == Service.Type.IP_SERVICE
        assert services_list[2].is_global is False
        assert services_list[2].comment is None
        assert services_list[2].uid == "{97AEB369-9AEA-11D5-BD16-0090272CCB30}"
        assert services_list[2].overrides is False
        assert services_list[2].min_port == 0
        assert services_list[2].max_port == 255
        assert services_list[2].negate is False
        assert services_list[2].timeout == "0"
        assert services_list[2].is_implicit is False

        assert services_list[5].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[5].id == 2878002
        assert services_list[5].name == "administratively-prohibited (icmp)"
        assert services_list[5].display_name == "administratively-prohibited"
        assert services_list[5].class_name == Service.ClassName.ICMP_SERVICE
        assert services_list[5].type == Service.Type.ICMP_SERVICE
        assert services_list[5].is_global is False
        assert services_list[5].comment == ""
        assert services_list[5].uid == "{ba7802ac-0d69-4ffe-8b5f-30a36e518e9f}"
        assert services_list[5].overrides is False
        assert services_list[5].protocol == Service.Protocol.ICMP.value
        assert services_list[5].min_port == 3
        assert services_list[5].max_port == 3
        assert services_list[5].negate is False
        assert services_list[5].timeout == "0"
        assert services_list[5].is_implicit is False

        assert services_list[6].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[6].id == 2878003
        assert services_list[6].name == "ah"
        assert services_list[6].display_name == "ah"
        assert services_list[6].class_name == Service.ClassName.OTHER_SERVICE
        assert services_list[6].type == Service.Type.IP_SERVICE
        assert services_list[6].is_global is False
        assert services_list[6].comment == "Protocol: ah (51)"
        assert services_list[6].uid == "{3fbd8116-3801-4bee-8593-3cbf999da671}"
        assert services_list[6].overrides is False
        assert services_list[6].min_port == 51
        assert services_list[6].max_port == 51
        assert services_list[6].negate is False
        assert services_list[6].timeout == "0"
        assert services_list[6].is_implicit is False

        assert services_list[10].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[10].id == 2878007
        assert services_list[10].name == "aol (udp)"
        assert services_list[10].display_name == "aol"
        assert services_list[10].class_name == Service.ClassName.UDP_SERVICE
        assert services_list[10].type == Service.Type.UDP_SERVICE
        assert services_list[10].is_global is False
        assert services_list[10].comment == "America On-line"
        assert services_list[10].uid == "{7c8de56b-cdd4-4983-91fc-333402a8e93d}"
        assert services_list[10].overrides is False
        assert services_list[10].protocol == Service.Protocol.UDP.value
        assert services_list[10].min_port == 5190
        assert services_list[10].max_port == 5190
        assert services_list[10].negate is False
        assert services_list[10].timeout == "0"
        assert services_list[10].is_implicit is False

        assert services_list[65].xsi_type == ServiceXsiType.SERVICE_GROUP_OBJECT
        assert services_list[65].id == 2878062
        assert services_list[65].name == "group_ServiceGroup_1"
        assert services_list[65].display_name == "ServiceGroup_1"
        assert services_list[65].class_name == Service.ClassName.SERVICE_GROUP
        assert services_list[65].type == Service.Type.GROUP
        assert services_list[65].is_global is False
        assert services_list[65].comment == ""
        assert services_list[65].uid == "{d199bdbd-2309-4f8e-9695-4cfc8aeec90c}"
        assert services_list[65].is_implicit is False
        assert services_list[65].members[0].id == 2878000
        assert (
            services_list[65].members[0].uid == "{4647cde8-ba3f-4721-b40b-818545261f1a}"
        )
        assert services_list[65].members[0].name == "902 (tcp)"
        assert services_list[65].members[0].display_name == "902"

        assert services_list[414].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[414].id == 2973376
        assert services_list[414].uid == "{97AEB3C6-9AEA-11D5-BD16-0090272CCB30}"
        assert services_list[414].name == "nisplus"
        assert services_list[414].display_name == "nisplus"
        assert services_list[414].class_name == Service.ClassName.RPC_SERVICE
        assert services_list[414].type == Service.Type.RPC_SERVICE
        assert services_list[414].is_global is False
        assert (
            services_list[414].comment
            == "NIS+ later version provides additional security and other facilities"
        )
        assert services_list[414].uid == "{97AEB3C6-9AEA-11D5-BD16-0090272CCB30}"
        assert services_list[414].is_implicit is False

        assert services_list[415].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[415].id == 2981341
        assert services_list[415].uid == "{06179529-f281-4596-bb8f-dcbc63cccf9e}"
        assert services_list[415].name == "application-421"
        assert services_list[415].display_name == "s7"
        assert services_list[415].class_name == Service.ClassName.OTHER_SERVICE
        assert services_list[415].type == Service.Type.OTHER_SERVICE
        assert services_list[415].comment == "Protocol: ARP"
        assert services_list[415].is_global is False
        assert services_list[415].timeout == "never"

        assert services_list[416].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[416].id == 2973422
        assert services_list[416].uid == "{3D0D46B6-4DDB-43E0-9FAA-C969DBC3E19F}"
        assert services_list[416].name == "ALL_DCE_RPC"
        assert services_list[416].display_name == "ALL_DCE_RPC"
        assert services_list[416].class_name == Service.ClassName.DCERPC_SERVICE
        assert services_list[416].type == Service.Type.OTHER_SERVICE
        assert (
            services_list[416].comment
            == "Special Service For Allowing All DCE-RPC Services"
        )
        assert services_list[416].is_global is False
        assert services_list[416].timeout == "never"
        assert services_list[416].is_implicit is False

        assert services_list[417].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[417].id == 3000911
        assert services_list[417].uid == "{5a49039f-15b3-4db0-a05f-c83cfc4e4f33}"
        assert services_list[417].name == "/Common/any_any"
        assert services_list[417].display_name == "any_any"
        assert services_list[417].class_name == Service.ClassName.PORT_SERVICE
        assert services_list[417].type == Service.Type.PORT_SERVICE
        assert services_list[417].comment == ""
        assert services_list[417].is_global is False
        assert services_list[417].min_port == 0
        assert services_list[417].max_port == 65535
        assert services_list[417].timeout == "0"

        assert services_list[418].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[418].id == 3014849
        assert services_list[418].uid == "{70ec3e84-daff-40d0-9d9d-63f2aec64aa5}"
        assert services_list[418].name == "ALL_ICMP6"
        assert services_list[418].display_name == "ALL_ICMP6"
        assert services_list[418].class_name == Service.ClassName.ICMPV6_SERVICE
        assert services_list[418].type == Service.Type.IP_SERVICE
        assert services_list[418].comment == ""
        assert services_list[418].is_global is False
        assert services_list[418].min_port == 58
        assert services_list[418].max_port == 58
        assert services_list[418].timeout == "0"
        assert services_list[418].management_domain == "Amsterdam"
        assert services_list[418].management_domain_securetrack_name == "Amsterdam"

        assert services_list[419].xsi_type == ServiceXsiType.SINGLE_SERVICE_OBJECT
        assert services_list[419].id == 3242792
        assert services_list[419].uid == "{B114786F-03CD-AB2E-0B2F-EF9376CBB3E0}"
        assert services_list[419].name == "st_implicit_app_ping6"
        assert services_list[419].display_name == "st_implicit_app_ping6"
        assert services_list[419].class_name == Service.ClassName.ICMP_V6_SERVICE
        assert services_list[419].type == Service.Type.OTHER_SERVICE
        assert services_list[419].comment == ""
        assert services_list[419].is_global is False
        assert services_list[419].timeout == "never"
        assert services_list[419].management_domain == "Shared"
        assert services_list[419].management_domain_securetrack_name == "QA Pano"

    def test_set_attributes(self, services_list):
        services_list[0].max_port = 904

        j = services_list[0]._json
        assert j["max"] == 904
