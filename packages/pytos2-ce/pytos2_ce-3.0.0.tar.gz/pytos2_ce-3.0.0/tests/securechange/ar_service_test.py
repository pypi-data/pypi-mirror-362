import pytest
import json
from pytos2.securechange.fields import (
    classify_service_type,
    AccessRequest,
    MultiAccessRequest,
    Object,
    Service,
    ExistService,
    TCPService,
    UDPService,
    ICMPService,
    OtherService,
    ServiceGroup,
    ExistTCPService,
    ExistUDPService,
    ExistICMPService,
    ExistOtherService,
    PredefinedService,
    PredefinedTCPService,
    PredefinedUDPService,
    PredefinedOtherService,
    ApplicationIdentity,
)
from pytos2.securechange.service import ApplicationIdentityName, PredefinedServiceName


class TestAccessRequest:
    @pytest.fixture
    def access_requests(self):
        j = json.load(
            open(
                "tests/securechange/json/field/multi_access_request_with_all_service_types.json"
            )
        )
        return MultiAccessRequest.kwargify(j)

    def test_ar_inheritance(self, access_requests):
        ar_list = access_requests.access_requests
        assert isinstance(ar_list, list)
        assert isinstance(ar_list[0].services, list)


class TestAccessRequestServices:
    @pytest.fixture
    def ar_services(self):
        j = json.load(
            open(
                "tests/securechange/json/field/multi_access_request_with_all_service_types.json"
            )
        )
        return MultiAccessRequest.kwargify(j).access_requests[0].services

    def test_service_inheritance(self, ar_services):
        assert isinstance(ar_services, list)
        assert isinstance(ar_services[0], TCPService)
        assert isinstance(ar_services[0], Service)

        assert isinstance(ar_services[1], UDPService)
        assert isinstance(ar_services[1], Service)

        assert isinstance(ar_services[2], ICMPService)
        assert isinstance(ar_services[2], Service)

        assert isinstance(ar_services[3], ExistICMPService)
        assert isinstance(ar_services[3], ExistService)
        assert isinstance(ar_services[3], Object)
        assert isinstance(ar_services[3], ICMPService)
        assert isinstance(ar_services[3], Service)

        assert isinstance(ar_services[4], ApplicationIdentity)
        assert isinstance(ar_services[4], Service)
        assert isinstance(ar_services[4].services, list)
        assert isinstance(ar_services[4].services[0], TCPService)
        assert isinstance(ar_services[5], ServiceGroup)
        assert isinstance(ar_services[5], ExistService)
        assert isinstance(ar_services[5], Object)
        assert isinstance(ar_services[5].members, list)

        assert isinstance(ar_services[7], ExistOtherService)
        assert isinstance(ar_services[7], ExistService)
        assert isinstance(ar_services[7], Object)
        assert isinstance(ar_services[7], OtherService)
        assert isinstance(ar_services[7], Service)

        assert isinstance(ar_services[8], ExistOtherService)
        assert isinstance(ar_services[8], ExistService)
        assert isinstance(ar_services[8], Object)
        assert isinstance(ar_services[8], OtherService)
        assert isinstance(ar_services[8], Service)

        assert isinstance(ar_services[9], ExistUDPService)
        assert isinstance(ar_services[9], ExistService)
        assert isinstance(ar_services[9], Object)
        assert isinstance(ar_services[9], UDPService)
        assert isinstance(ar_services[9], Service)

        assert isinstance(ar_services[10], ExistTCPService)
        assert isinstance(ar_services[10], ExistService)
        assert isinstance(ar_services[10], Object)
        assert isinstance(ar_services[10], TCPService)
        assert isinstance(ar_services[10], Service)

        assert isinstance(ar_services[14], PredefinedTCPService)
        assert isinstance(ar_services[14], PredefinedService)
        assert isinstance(ar_services[14], TCPService)
        assert isinstance(ar_services[14], Service)

        assert isinstance(ar_services[15], PredefinedOtherService)
        assert isinstance(ar_services[15], PredefinedService)
        assert isinstance(ar_services[15], OtherService)
        assert isinstance(ar_services[15], Service)

    def test_service_attributes(self, ar_services):
        assert ar_services[0].protocol == "TCP"
        assert ar_services[0].port == "111"
        assert ar_services[0].at_type.value == "PROTOCOL"
        assert ar_services[0].id == 22157

        assert ar_services[1].protocol == "UDP"
        assert ar_services[1].port == "222"
        assert ar_services[1].at_type.value == "PROTOCOL"
        assert ar_services[1].id == 22158

        assert ar_services[2].protocol == "ICMP"
        assert ar_services[2].type == "253"
        assert ar_services[2].at_type.value == "PROTOCOL"
        assert ar_services[2].id == 22870

        assert ar_services[3].at_type.value == "Object"
        assert ar_services[3].id == 22159
        assert ar_services[3].name == "administratively-prohibited"
        assert ar_services[3].management_id == 7
        assert ar_services[3].management_name == "RTR2"
        assert ar_services[3].uid == "{c8944d28-dbef-44ef-a49f-e33a4c09ebca}"
        assert ar_services[3].protocol == "icmp"
        assert ar_services[3].type == "3"
        assert ar_services[3].obj_type == "icmp"

        assert ar_services[4].at_type.value == "APPLICATION_IDENTITY"
        assert ar_services[4].id == 22160
        assert ar_services[4].name == ApplicationIdentityName._BAO
        assert hasattr(ar_services[4], "services")
        assert ar_services[4].services[0].protocol == "TCP"
        assert ar_services[4].services[0].port == "3468"
        assert ar_services[4].services[0].at_type.value == "PROTOCOL"
        assert ar_services[4].services[1].protocol == "TCP"
        assert ar_services[4].services[1].port == "11300"
        assert ar_services[4].services[1].at_type.value == "PROTOCOL"

        assert ar_services[5].at_type.value == "Object"
        assert ar_services[5].id == 22161
        assert ar_services[5].name == "daytime"
        assert ar_services[5].management_id == 243
        assert ar_services[5].management_name == "CMA-R80"
        assert ar_services[5].uid == "{97AEB46F-9AEA-11D5-BD16-0090272CCB30}"
        assert ar_services[5].members[0] == "daytime-tcp"
        assert ar_services[5].members[1] == "daytime-udp"
        assert ar_services[5].obj_type == "group"

        assert ar_services[6].at_type.value == "Object"
        assert ar_services[6].id == 22162
        assert ar_services[6].name == "Data Recovery Appliance"
        assert ar_services[6].management_id == 59
        assert ar_services[6].management_name == "NSX-Distributed Firewall"
        assert ar_services[6].uid == "{32efb97a-bb5c-4bc8-8161-3b1e1846d093}"
        assert ar_services[6].members[0] == "VMware-DataRecovery"
        assert ar_services[6].members[1] == "VMware-ESXi5.x-TCP"
        assert ar_services[6].members[2] == "HTTPS"
        assert ar_services[6].obj_type == "group"

        assert ar_services[7].at_type.value == "Object"
        assert ar_services[7].id == 22163
        assert ar_services[7].name == "ah"
        assert ar_services[7].management_id == 32
        assert ar_services[7].management_name == "RTR4"
        assert ar_services[7].uid == "{3fbd8116-3801-4bee-8593-3cbf999da671}"
        assert ar_services[7].obj_type == "other"
        assert ar_services[7].type == "51"

        assert ar_services[9].at_type.value == "Object"
        assert ar_services[9].id == 22585
        assert ar_services[9].name == "archie"
        assert ar_services[9].management_id == 20
        assert ar_services[9].management_name == "CP SMC"
        assert ar_services[9].uid == "{97AEB3D6-9AEA-11D5-BD16-0090272CCB30}"
        assert ar_services[9].protocol == "udp"
        assert ar_services[9].port == "1525"
        assert ar_services[9].obj_type == "udp"

        assert ar_services[10].at_type.value == "Object"
        assert ar_services[10].id == 22584
        assert ar_services[10].name == "AP-Defender"
        assert ar_services[10].management_id == 20
        assert ar_services[10].management_name == "CP SMC"
        assert ar_services[10].uid == "{97AEB3E9-9AEA-11D5-BD16-0090272CCB30}"
        assert ar_services[10].protocol == "tcp"
        assert ar_services[10].port == "2626"
        assert ar_services[10].obj_type == "tcp"

        assert ar_services[14].protocol == "TCP"
        assert ar_services[14].port == "443"
        assert ar_services[14].at_type.value == "PREDEFINED"
        assert ar_services[14].id == 22168

        assert ar_services[15].type == "51"
        assert ar_services[15].protocol == "OTHER"
        assert ar_services[15].name == PredefinedServiceName.AH
        assert ar_services[15].at_type.value == "PREDEFINED"
        assert ar_services[15].id == 22196
