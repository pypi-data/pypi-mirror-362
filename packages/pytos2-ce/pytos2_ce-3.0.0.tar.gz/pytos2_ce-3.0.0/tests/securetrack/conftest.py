import json
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import re
import os

import pytest
import responses
from responses import matchers

from pytos2.securetrack import StAPI
from pytos2.securetrack.entrypoint import St


@pytest.fixture
def st_api():
    return StAPI(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def st():
    return St(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def st_no_cache():
    return St(
        username="username",
        password="password",
        hostname="198.18.0.1",
        cache=False,
        default=False,
    )


@pytest.fixture
def generic_devices_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/generic_devices",
        json=json.load(
            open("tests/securetrack/json/generic_devices/generic_devices.json")
        ),
        match=[matchers.query_string_matcher("")],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/generic_devices",
        json=json.load(
            open("tests/securetrack/json/generic_devices/generic_devices_filtered.json")
        ),
        match=[matchers.query_string_matcher("name=vm")],
    )

    responses.add(
        responses.POST, "https://198.18.0.1/securetrack/api/generic_devices", status=201
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securetrack/api/generic_devices/2",
        status=204,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/generic_devices/3",
        status=204,
    )


@pytest.fixture
def generic_devices_getter_error(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/generic_devices",
        status=500,
    )


@pytest.fixture
def generic_devices_error_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/generic_devices",
        json=json.load(
            open("tests/securetrack/json/generic_devices/generic_devices.json")
        ),
    )

    responses.add(
        responses.POST, "https://198.18.0.1/securetrack/api/generic_devices", status=400
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securetrack/api/generic_devices/2",
        status=400,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/generic_devices/3",
        match=[matchers.query_string_matcher("update_topology=False")],
        status=400,
    )


@pytest.fixture
def sample_generic_device_csv():
    return open(
        "tests/securetrack/json/generic_devices/sample_generic_device.csv"
    ).read()


@pytest.fixture
def topology_sync_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/topology/synchronize",
        status=200,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/synchronize/status",
        status=200,
        json=json.load(open("tests/securetrack/json/topology/status.json")),
    )


@pytest.fixture
def topology_sync_auth_error_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/topology/synchronize",
        status=401,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/synchronize/status",
        status=401,
    )


@pytest.fixture
def topology_sync_500_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/topology/synchronize",
        status=500,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/synchronize/status",
        status=500,
    )


@pytest.fixture
def topology_sync_502_mock():
    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/topology/synchronize",
        status=502,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/synchronize/status",
        status=502,
    )


@pytest.fixture
def devices_mock(st):
    def device_callback(request):
        parts = request.url.split("/")
        if "show" in parts[-1]:
            _id = parts[-1].split("?", 1)[0]
        else:
            _id = int(parts[-1])

        try:
            _json = json.load(open(f"tests/securetrack/json/devices/device-{_id}.json"))
        except FileNotFoundError:
            return (404, {}, "{}")

        _json = {"device": _json}
        return (200, {}, json.dumps(_json))

    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/devices/(\\d+)$"),
        callback=device_callback,
    )
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/devices/(\\d+)\?show_license=false&show_os_version=false$"
        ),
        callback=device_callback,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices",
        json=json.load(open("tests/securetrack/json/devices/devices.json")),
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/devices/bulk/delete",
        json={"task_uid": "some_guid_here"},
        status=200,
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/devices/bulk/update_topology_data",
        json={"task_uid": "some_guid_here"},
        status=201,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/bulk/tasks/ada853b8-46f7-474b-bb4e-3309a3a9d0af",
        json=json.load(
            open("tests/securetrack/json/devices/get_devices_bulk_task.json")
        ),
        status=200,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/devices/bulk/delete",
        json={"task_uid": "some_guid_here"},
        status=200,
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/devices/bulk/update_topology_data",
        json={"task_uid": "some_guid_here"},
        status=201,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/bulk/tasks/ada853b8-46f7-474b-bb4e-3309a3a9d0af",
        json=json.load(
            open("tests/securetrack/json/devices/get_bulk_device_task.json")
        ),
        status=200,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/bulk/tasks/c878cb8c-6a6d-4939-b20b-550def656ac4",
        json=json.load(
            open("tests/securetrack/json/devices/devices_bulk_delete_task.json")
        ),
    )


@pytest.fixture
def device_rules_mock(st):
    def device_rules_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(open(f"tests/securetrack/json/rules/device-{_id}.json"))
        except FileNotFoundError:
            return (404, {}, "{}")

        return (200, {}, json.dumps(_json))

    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/devices/(\\d+)$"),
        callback=device_rules_callback,
    )


@pytest.fixture
def device_policies_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/20/policies",
        json=json.load(open("tests/securetrack/json/policies/20.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/400000/policies",
        status=404,
    )


@pytest.fixture
def devices_for_rule_test_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices",
        json=json.load(open("tests/securetrack/json/devices/for-rule-test.json")),
    )


@pytest.fixture
def search_rules_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search",
        json=json.load(open("tests/securetrack/json/rules/rule_search-105.json")),
        match=[matchers.query_string_matcher("devices=105&search_text=")],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/105",
        json=json.load(open("tests/securetrack/json/rules/rule_search-105-all-1.json")),
        match=[matchers.query_string_matcher("start=0&count=3000&search_text=")],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/105",
        json=json.load(open("tests/securetrack/json/rules/rule_search-105-all-2.json")),
        match=[matchers.query_string_matcher("start=3000&count=3000&search_text=")],
    )


@pytest.fixture
def rules_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/8/rules",
        json=json.load(open("tests/securetrack/json/rules/device-8.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/20/rules",
        match=[
            matchers.query_string_matcher(
                "add=documentation&uid=%7b3A1BA062-6B19-4C97-8F18-79CBA9EF0AA6%7d"
            )
        ],
        json=json.load(open("tests/securetrack/json/rules/device-20-with-uid.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2285/rules",
        match=[
            matchers.query_string_matcher(
                "add=documentation&uid=Datacenter_access_in_@_8"
            )
        ],
        json=json.load(
            open("tests/securetrack/json/rules/revision-2285-with-uid.json")
        ),
    )

    for i in (1, 5, 7, 20, 21):
        responses.add(
            responses.GET,
            f"https://198.18.0.1/securetrack/api/devices/{i}/rules",
            match=[matchers.query_string_matcher("add=documentation")],
            json=json.load(
                open(f"tests/securetrack/json/rules/device-{i}-add-documentation.json")
            ),
        )
    responses.add(
        responses.GET, "https://198.18.0.1/securetrack/api/devices/10/rules", status=500
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2285/rules",
        json=json.load(open("tests/securetrack/json/rules/device-8.json")),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2226/rules",
        status=500,
    )


@pytest.fixture
def revisions_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/8/latest_revision",
        json=json.load(
            open("tests/securetrack/json/revisions/device-8-latest-revision.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/100000",
        status=404,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/100000/latest_revision",
        status=404,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/100000/revisions",
        status=404,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/8/revisions",
        json=json.load(open("tests/securetrack/json/revisions/device-8.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2226",
        json=json.load(open("tests/securetrack/json/revisions/revision-2226.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2285",
        json=json.load(open("tests/securetrack/json/revisions/revision-2285.json")),
    )

    responses.add(
        responses.GET, "https://198.18.0.1/securetrack/api/revisions/400000", status=404
    )


@pytest.fixture
def network_objects_mock2(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/network_objects/search?device_id=20&filter=text&start=0&count=100&get_total=true",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/search_network_objects_device_id_20.json"
            )
        ),
        status=200,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/network_objects/search?device_id=10000&filter=text&start=0&count=100&get_total=true",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/search_network_objects_empty.json"
            )
        ),
        status=200,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/network_objects/search?name=https&filter=text&start=0&count=100&get_total=true",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/search_network_objects_https.json"
            )
        ),
        status=200,
    )


@pytest.fixture
def network_objects_mock(devices_mock):
    def device_cb(request):
        device_id = request.path_url.split("/")[-2]
        params = parse_qs(urlparse(request.path_url).query)
        if params.get("add_parent_objects", None) == ["true"]:
            postfix = "-add-parent-objects"
        elif params.get("add_parent_objects", None) == ["false"]:
            postfix = "-no-parent-objects"
        else:
            postfix = ""

        fileString = f"tests/securetrack/json/network_objects/{device_id}{postfix}.json"

        if not os.path.exists(fileString):
            return (404, {}, "")
        else:
            return (200, {}, open(fileString).read())

    def search_cb(request):
        # key: value dictionary of params, but the value is a list in case there are multiple values for a single query param
        params = parse_qs(urlparse(request.path_url).query)
        if params.get("filter", [None])[0] == "uid":
            uid = params.get("uid", [None])[0]
            _json = Path(f"tests/securetrack/json/network_objects/{uid}.json")
            if _json.is_file():
                return (200, {}, _json.open().read())
        return (200, {}, json.dumps({"network_objects": {}}))

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/10/network_objects/80681",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/device_10_network_objects_80681.json"
            )
        ),
        status=200,
    )

    responses.add_callback(
        responses.GET,
        re.compile(r"https://198.18.0.1/securetrack/api/devices/\d+/network_objects"),
        callback=device_cb,
    )

    responses.add_callback(
        responses.GET,
        re.compile(r"https://198.18.0.1/securetrack/api/network_objects/search"),
        callback=search_cb,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/24522/network_objects?show_members=true&start=0&count=2000&get_total=true",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/revision_24522_network_objects.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/24522/network_objects/450118?show_members=true",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/revision_24522_network_objects_450118.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/network_objects/15/groups",
        json=json.load(
            open(
                "tests/securetrack/json/network_objects/network_objects_15_groups.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/network_objects/12/rules",
        json=json.load(
            open("tests/securetrack/json/network_objects/network_objects_12_rules.json")
        ),
    )


@pytest.fixture
def services_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/1/services",
        json=json.load(open("tests/securetrack/json/services/1.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/search",
        match=[
            matchers.query_string_matcher(
                "uid=3fbd8116-3801-4bee-8593-3cbf999da671&filter=uid&start=0&count=100&get_total=true"
            ),
        ],
        json=json.load(
            open(
                "tests/securetrack/json/services/search-3fbd8116-3801-4bee-8593-3cbf999da671.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/search",
        match=[
            matchers.query_string_matcher(
                "filter=uid&uid=3fbd8116-3801-4bee-8593-3cbf999da671"
            ),
        ],
        json=json.load(
            open(
                "tests/securetrack/json/services/search-3fbd8116-3801-4bee-8593-3cbf999da671.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/search",
        match=[
            matchers.query_string_matcher(
                "uid=3fbd8116-3801-4bee-8593-3cbf999da671&filter=uid&start=0&count=2000&get_total=true"
            )
        ],
        json=json.load(
            open(
                "tests/securetrack/json/services/search-3fbd8116-3801-4bee-8593-3cbf999da671.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/search",
        match=[
            matchers.query_string_matcher(
                "filter=uid&uid=3fbd8116-3801-4bee-8593-3cbf999da671&device_id=1"
            )
        ],
        json=json.load(
            open(
                "tests/securetrack/json/services/search-device-1-3fbd8116-3801-4bee-8593-3cbf999da671.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/2961503/groups",
        json=json.load(
            open("tests/securetrack/json/services/services_2961503_groups.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/services/2937342/rules",
        json=json.load(
            open("tests/securetrack/json/services/services_2937342_rules.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/8/services?name=daytime&show_members=False&add_parent_objects=True&start=0&count=2000&get_total=true",
        json=json.load(
            open("tests/securetrack/json/services/devices_8_services_daytime.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/24522/services?name=MSExchange&show_members=False&add_parent_objects=True&start=0&count=2000&get_total=true",
        json=json.load(
            open(
                "tests/securetrack/json/services/revisions_24522_services_MSExchange.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/24522/services/3330108?show_members=false",
        json=json.load(
            open(
                "tests/securetrack/json/services/revisions_24522_services_3330108.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/8/services/3099979?show_members=false",
        json=json.load(
            open("tests/securetrack/json/services/devices_8_services_3099979.json")
        ),
    )


@pytest.fixture
def zone_subnets_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones/78/entries",
        json=json.load(open("tests/securetrack/json/zones/zone-entries-78.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones/200/entries",
        status=404,
    )


@pytest.fixture
def zone_descendants_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones/80/descendants",
        json=json.load(open("tests/securetrack/json/zones/zone-descendants-80.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones/200/descendants",
        status=404,
    )


@pytest.fixture
def zones_mock(st):
    def zone_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(open(f"tests/securetrack/json/zones/zone-{_id}.json"))
        except FileNotFoundError:
            return (404, {}, "{}")

        return (200, {}, json.dumps(_json))

    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/zones/(\\d+)$"),
        callback=zone_callback,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones",
        json=json.load(open("tests/securetrack/json/zones/zones.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/zones/internet_representing_address",
        body="8.8.4.4",
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/zones/internet_representing_address",
        status=200,
    )


@pytest.fixture()
def test_post_add_domain_json():
    json.load(open("tests/securetrack/json/domain/post_add_domain.json"))


@pytest.fixture
def domains_mock(st):
    def domain_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(open(f"tests/securetrack/json/domains/domain-{_id}.json"))
        except FileNotFoundError:
            return (404, {}, "{}")

        return (200, {}, json.dumps(_json))

    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/domains/(\\d+)$"),
        callback=domain_callback,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/domains",
        json=json.load(open("tests/securetrack/json/domains/domains.json")),
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/domains/",
        headers={"Location": "https://198.18.0.1/securetrack/api/domains/7"},
    )
    responses.add(responses.PUT, "https://198.18.0.1/securetrack/api/domains/7")


@pytest.fixture
def generic_interfaces_mock(st):
    def interface_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_interfaces/int-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Generic Interface Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    def management_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_interfaces/mgmt-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Management Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Interface by ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interface/(\\d+)$"
        ),
        callback=interface_callback,
    )

    """Get Interfaces by Management ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interface/mgmt/(\\d+)$"
        ),
        callback=management_callback,
    )

    """Delete Interface by ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interface/(\\d+)$"
        ),
        callback=interface_callback,
    )

    """Delete Interfaces by Management ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interface/mgmt/(\\d+)$"
        ),
        callback=management_callback,
    )


@pytest.fixture
def generic_route_mock(st):
    def route_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_routes/route-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Generic Route Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    def management_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_routes/mgmt-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Management Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Route by ID"""
    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/topology/generic/route/(\\d+)$"),
        callback=route_callback,
    )

    """Get Routes by Management ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/route/mgmt/(\\d+)$"
        ),
        callback=management_callback,
    )

    """Delete Route by ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile("https://198.18.0.1/securetrack/api/topology/generic/route/(\\d+)$"),
        callback=route_callback,
    )

    """Delete Routes by Management ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/route/mgmt/(\\d+)$"
        ),
        callback=management_callback,
    )


@pytest.fixture
def generic_vpn_mock(st):
    def vpn_callback(request):
        parsed_url = urlparse(request.url)
        parts = parsed_url.path.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_vpns/vpn-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Generic Vpn Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    def device_callback(request):
        parsed_url = urlparse(request.url)
        parts = parsed_url.path.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/generic_vpns/device-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": "Device Not Found"}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Vpn by ID"""
    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/topology/generic/vpn/(\\d+)$"),
        callback=vpn_callback,
    )

    """Get Vpns by Device ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            r"https://198.18.0.1/securetrack/api/topology/generic/vpn/device/(\d+)\?generic=true$"
        ),
        callback=device_callback,
    )

    """Get Vpns by Device ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            r"https://198.18.0.1/securetrack/api/topology/generic/vpn/device/(\d+)\?generic=false$"
        ),
        callback=device_callback,
    )

    """Delete Vpn by ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile("https://198.18.0.1/securetrack/api/topology/generic/vpn/(\\d+)$"),
        callback=vpn_callback,
    )

    """Delete Vpns by Device ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/vpn/device/(\\d+)$"
        ),
        callback=device_callback,
    )


@pytest.fixture
def generic_transparent_firewall_mock(st):
    def data_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(
                    f"tests/securetrack/json/generic_transparent_firewalls/data-{_id}.json"
                )
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": f"Layer2Data Id {_id} not found"}}),
            )

        return (200, {}, json.dumps(_json))

    def device_callback(request):
        parsed_url = urlparse(request.url)
        parts = parsed_url.path.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(
                    f"tests/securetrack/json/generic_transparent_firewalls/device-{_id}.json"
                )
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": f"DeviceId {_id} not found."}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Transparent Firewalls by Device ID"""
    responses.add_callback(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/generic/transparentfw/device/9",
        match=[matchers.query_string_matcher("generic=false")],
        callback=device_callback,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/generic/transparentfw/device/404",
        match=[matchers.query_string_matcher("generic=false")],
        status=404,
    )

    """Delete Layer 2 Data by ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw/(\\d+)$"
        ),
        callback=data_callback,
    )

    """Delete Transparent Firewalls by Device ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/transparentfw/device/(\\d+)$"
        ),
        callback=device_callback,
    )


@pytest.fixture
def generic_ignored_interface_mock(st):
    def mgmt_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(
                    f"tests/securetrack/json/generic_ignored_interfaces/mgmt-{_id}.json"
                )
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": f"Management Id {_id} not found."}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Ignored Interfaces by Management ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/ignoredinterface/mgmt/(\\d+)$"
        ),
        callback=mgmt_callback,
    )

    """Delete Ignored Interfaces by Management ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/ignoredinterface/mgmt/(\\d+)$"
        ),
        callback=mgmt_callback,
    )


@pytest.fixture
def generic_interface_customer_tag_mock(st):
    def interface_customer_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(
                    f"tests/securetrack/json/generic_interface_customers/int-cust-{_id}.json"
                )
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps(
                    {"result": {"message": f"Interface Customer Tag {_id} not found."}}
                ),
            )

        return (200, {}, json.dumps(_json))

    def device_callback(request):
        parsed_url = urlparse(request.url)
        path_parts = parsed_url.path.split("/")
        _id = int(path_parts[-1])

        try:
            _json = json.load(
                open(
                    f"tests/securetrack/json/generic_interface_customers/device-{_id}.json"
                )
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": f"Device Id {_id} not found."}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Interface Customer Tag by ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer/(\\d+)$"
        ),
        callback=interface_customer_callback,
    )

    """Get Interface Customer Tags by Device ID"""
    responses.add_callback(
        responses.GET,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer/device/(\\d+)\\?generic=(true|false)$"
        ),
        callback=device_callback,
    )

    """Delete Interface Customer Tag by ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer/(\\d+)$"
        ),
        callback=interface_customer_callback,
    )

    """Delete Interface Customer Tags by Device ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile(
            "https://198.18.0.1/securetrack/api/topology/generic/interfacecustomer/device/(\\d+)$"
        ),
        callback=device_callback,
    )


@pytest.fixture
def join_cloud_mock(st):
    def cloud_callback(request):
        parts = request.url.split("/")
        _id = int(parts[-1])

        try:
            _json = json.load(
                open(f"tests/securetrack/json/join_clouds/cloud-{_id}.json")
            )
        except FileNotFoundError:
            return (
                404,
                {},
                json.dumps({"result": {"message": f"Cloud Id {_id} not found."}}),
            )

        return (200, {}, json.dumps(_json))

    """Get Join Cloud by Cloud ID"""
    responses.add_callback(
        responses.GET,
        re.compile("https://198.18.0.1/securetrack/api/topology/join/clouds/(\\d+)$"),
        callback=cloud_callback,
    )

    """Delete Join Cloud by Cloud ID"""
    responses.add_callback(
        responses.DELETE,
        re.compile("https://198.18.0.1/securetrack/api/topology/join/clouds/(\\d+)$"),
        callback=cloud_callback,
    )


@pytest.fixture()
def change_windows_mock_fails():
    responses.add(
        responses.GET, "https://198.18.0.1/securetrack/api/change_windows", status=403
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks",
        status=403,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks/197",
        status=403,
    )


@pytest.fixture()
def change_windows_mock_fails_json():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows",
        body="No no no",
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks",
        body="No no no",
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks/197",
        body="No no no",
    )


@pytest.fixture()
def change_windows_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows?start=0&count=2000&get_total=true",
        json=json.load(
            open("tests/securetrack/json/change_windows/change_windows.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks",
        json=json.load(
            open("tests/securetrack/json/change_windows/change_window_tasks.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/change_windows/07c230ce-2dec-4109-a0db-33ff45ba1057/tasks/197",
        json=json.load(
            open("tests/securetrack/json/change_windows/change_window_task_197.json")
        ),
    )


@pytest.fixture
def applications_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/174/applications?start=0&count=2000&get_total=true",
        json=json.load(open("tests/securetrack/json/applications/174.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/206/applications?start=0&count=2000&get_total=true",
        json={"applications": {"count": 0, "application": []}},
    )


@pytest.fixture
def applications_failed_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/1337/applications?start=0&count=2000&get_total=true",
        body="No no no",
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/1338/applications?start=0&count=2000&get_total=true",
        status=500,
    )


@pytest.fixture
def rule_documentation_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/24522/rules/53419/documentation",
        json=json.load(
            open(
                "tests/securetrack/json/rules/revisions-24522-rules-53419-documentation.json"
            )
        ),
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securetrack/api/revisions/24522/rules/53419/documentation",
        status=200,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/revisions/24522/rules/53419/documentation",
        status=204,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/devices/264/rules/53419/documentation",
        status=204,
    )


@pytest.fixture
def rule_last_usage_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_last_usage/find_all/1",
        json=json.load(open("tests/securetrack/json/rules/rule_last_usage-1.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_last_usage/find/1/d5adc685-6498-47d0-ad62-f7eeae18a069",
        json=json.load(open("tests/securetrack/json/rules/rule_last_usage-1-1.json")),
    )


@pytest.fixture
def rule_search_export_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/export?search_text=shadowed%3Atrue",
        body="Results will be exported as a CSV file in the SecureTrack Reports Repository",
    )


@pytest.fixture
def properties_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/properties",
        json=json.load(open("tests/securetrack/json/properties/properties.json")),
    )

    responses.add(
        responses.PUT,
        "https://198.18.0.1/securetrack/api/properties",
        status=200,
    )


@pytest.fixture
def time_object_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices/1/time_objects",
        json=json.load(open("tests/securetrack/json/time_objects/1.json")),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2812/time_objects",
        json=json.load(open("tests/securetrack/json/time_objects/revision-2812.json")),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2812/time_objects/388",
        json=json.load(
            open("tests/securetrack/json/time_objects/time-objects-388.json")
        ),
    )
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/revisions/2812/time_objects/388,390",
        json=json.load(
            open("tests/securetrack/json/time_objects/time-objects-388-390.json")
        ),
    )


@pytest.fixture
def licenses_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/licenses",
        json=json.load(open("tests/securetrack/json/licenses/licenses.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/licenses/evaluation",
        json=json.load(open("tests/securetrack/json/licenses/license_evaluation.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/licenses/1",
        json=json.load(open("tests/securetrack/json/licenses/license_1.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/licenses/tiered-license",
        json=json.load(open("tests/securetrack/json/licenses/tiered_license.json")),
    )


@pytest.fixture
def security_policy_mock(st):
    def read_plain_text(file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            return f.read()

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies?ignoreSecureTrack2Data=true",
        json=json.load(
            open(
                "tests/securetrack/json/security_policies/security_policies_classic.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies",
        json=json.load(
            open("tests/securetrack/json/security_policies/security_policies.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies/global",
        json=json.load(
            open(
                "tests/securetrack/json/security_policies/security_policies_global.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies/7131354762492230143/export",
        body=read_plain_text(
            "tests/securetrack/json/security_policies/security_policy_export_csv.txt"
        ),
        content_type="text/plain",
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies/404/export",
        status=404,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/security_policies/5/mapping",
        json=json.load(
            open(
                "tests/securetrack/json/security_policies/usp_device_interface_map.json"
            )
        ),
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/security_policies/5/manual_mapping",
        status=200,
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/security_policies/404/manual_mapping",
        status=404,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/security_policies/7131354762492230143",
        status=204,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/security_policies/404",
        status=404,
    )


@pytest.fixture
def search_rules_on_open_tickets_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/devices",
        json=json.load(open("tests/securetrack/json/devices/rule_mod_devices.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search",
        json=json.load(
            open("tests/securetrack/json/rules/search_rules_in_open_tickets.json")
        ),
        match=[
            matchers.query_string_matcher("devices=1&search_text=inprogressticketid:*")
        ],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/",
        json=json.load(
            open("tests/securetrack/json/rules/search_rules_in_open_tickets.json")
        ),
        match=[matchers.query_string_matcher("search_text=inprogressticketid:*")],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/1?start=0&count=3000&search_text=inprogressticketid%3A%2A",
        json=json.load(
            open(
                "tests/securetrack/json/rules/search_rules_in_open_tickets_device_1.json"
            )
        ),
        match=[
            matchers.query_string_matcher(
                "start=0&count=3000&search_text=inprogressticketid%3A%2A"
            )
        ],
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/rule_search/1?start=3000&count=3000&search_text=inprogressticketid%3A%2A",
        json=json.load(
            open(
                "tests/securetrack/json/rules/search_rules_in_open_tickets_device_1.json"
            )
        ),
        match=[
            matchers.query_string_matcher(
                "start=3000&count=3000&search_text=inprogressticketid%3A%2A"
            )
        ],
    )


@pytest.fixture
def internet_objects_mock():
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/internet_referral/264",
        json=json.load(
            open(
                "tests/securetrack/json/internet_objects/internet_object_device_264.json"
            )
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/internet_referral/264/object",
        json=json.load(
            open(
                "tests/securetrack/json/internet_objects/internet_object_device_264_object.json"
            )
        ),
    )

    responses.add(
        responses.POST,
        "https://198.18.0.1/securetrack/api/internet_referral",
        status=201,
        headers={
            "Location": "https://198.18.0.1/securetrack/api/internet_referral/264"
        },
    )

    # The put returns an instance of InternetObject
    responses.add(
        responses.PUT,
        "https://198.18.0.1/securetrack/api/internet_referral/264",
        json=json.load(
            open(
                "tests/securetrack/json/internet_objects/internet_object_device_264.json"
            )
        ),
        status=200,
    )

    responses.add(
        responses.DELETE,
        "https://198.18.0.1/securetrack/api/internet_referral/264",
        status=204,
    )


@pytest.fixture
def topology_subnets_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/subnets",
        json=json.load(open("tests/securetrack/json/topology/topology_subnets.json")),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/subnets/6",
        json=json.load(open("tests/securetrack/json/topology/topology_subnet_6.json")),
    )


@pytest.fixture
def violating_rules_mock(st):
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/violating_rules/264/count",
        json=json.loads('{"count": {"count": 17}}'),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/violating_rules/264/device_violations?ignoreSecureTrack2Data=False&severity=CRITICAL&type=SECURITY_POLICY",
        json=json.load(
            open("tests/securetrack/json/rules/device_264_violating_rules.json")
        ),
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/violating_rules/1/device_violations?ignoreSecureTrack2Data=False&severity=LOW&type=SECURITY_POLICY",
        json=json.load(
            open("tests/securetrack/json/rules/device_1_violating_rules.json")
        ),
    )


@pytest.fixture
def topology_devices_data():
    """Load the sample topology device data from file"""
    return json.load(open("tests/securetrack/json/topology/topology_device.json"))


@pytest.fixture
def topology_device_mock(st):
    """Mock responses for topology device API endpoints"""
    # Mock the GET request for all topology devices
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/device",
        json=json.load(open("tests/securetrack/json/topology/topology_device.json")),
        status=200,
    )

    # Mock the GET request for a single topology device
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/device/716",
        json={
            "TopologyDevice": json.load(
                open("tests/securetrack/json/topology/topology_device.json")
            )["TopologyDevices"][0]
        },
        status=200,
    )

    # Mock error response
    responses.add(
        responses.GET,
        "https://198.18.0.1/securetrack/api/topology/device/999",
        status=404,
        json={"result": {"message": "Topology Device not found"}},
    )
