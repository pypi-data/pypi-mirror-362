import pytest
import json


import responses

from netaddr import IPAddress

from typing import List
from pytos2.securetrack.device import Device, InternetObject, DeviceLicenseStatus
from pytos2.securetrack.network_object import NetworkObject
from pytos2.securetrack.managed_devices import (
    BulkOperationTask,
    BulkOperationTaskResult,
    BulkOperationTaskResultDevice,
    BulkOperationTaskStatusList,
)
from pytos2.utils import get_api_node


class TestDevice:
    @pytest.fixture
    def device(self):
        j = json.load(open("tests/securetrack/json/devices/devices.json"))
        device_node = get_api_node(j, "devices.device")[0]
        return Device.kwargify(device_node)

    def test_attributes(self, device):
        assert device.id == 1
        assert device.name == "RTR1"
        assert device.vendor == Device.Vendor.CISCO
        assert device.model == Device.Model.ROUTER
        assert isinstance(device.domain_id, int) and device.domain_id == 1
        assert device.domain_name == "Default"
        assert device.module_uid == ""
        assert device.module_type == "IOS"
        assert device.status == "Stopped"
        assert device.ip == IPAddress("10.100.200.54")
        assert (
            isinstance(device.latest_revision, int) and device.latest_revision == 1674
        )
        assert device.virtual_type == ""
        assert len(device.licenses) == 3
        assert isinstance(device.licenses[0], DeviceLicenseStatus)

    def test_set_attributes(self, device):
        assert device.ip == IPAddress("10.100.200.54")

        device.ip = "1.2.3.4"
        assert device.ip == IPAddress("1.2.3.4")

    @responses.activate
    def test_properties(self, devices_mock, st):
        device = st.get_device(identifier=60)
        assert device
        assert device.name == "NSX-Edge-01"

        parent_device = device.parent
        assert parent_device.id == 58
        assert parent_device.name == "NSX"

        assert len(parent_device.children) == 4

        grandparent = parent_device.parent
        assert grandparent is None

    @responses.activate
    def test_bulk_delete_devices(self, devices_mock, st):
        task: BulkOperationTask = st.bulk_delete_devices([5, 8])
        assert isinstance(task.uid, str)

    @responses.activate
    def test_bulk_update_topology(self, devices_mock, st):
        task: BulkOperationTask = st.bulk_update_topology([5, 8])
        assert isinstance(task.uid, str)

    @responses.activate
    def test_get_devices_bulk_task(self, devices_mock, st):
        task_result: BulkOperationTaskResult = st.get_devices_bulk_task(
            "ada853b8-46f7-474b-bb4e-3309a3a9d0af"
        )
        assert isinstance(task_result.in_progress, BulkOperationTaskStatusList)
        assert all(
            isinstance(item, BulkOperationTaskResultDevice)
            for item in task_result.in_progress.devices
        )

        device = task_result.in_progress.devices[0]
        assert device.id == 1
        assert device.name == "Europe-CMA"
        assert device.ip_address == "192.168.1.1"
        assert (
            device.status == "{}"
        )  # TODO: We should really come up with a way to ensure this is an empty string

        assert isinstance(task_result.succeeded, BulkOperationTaskStatusList)
        assert all(
            isinstance(item, BulkOperationTaskResultDevice)
            for item in task_result.succeeded.devices
        )

        assert isinstance(task_result.failed, BulkOperationTaskStatusList)
        assert all(
            isinstance(item, BulkOperationTaskResultDevice)
            for item in task_result.failed.devices
        )

        assert task_result.total_in_progress == 1
        assert task_result.total_failed == 0
        assert task_result.total_succeeded == 1

        # Check that status.description is used as status properly.
        task_result: BulkOperationTaskResult = st.get_bulk_device_task(
            "c878cb8c-6a6d-4939-b20b-550def656ac4"
        )
        device = task_result.failed.devices[0]
        assert device.status == "Device with id: 998 was not found"


class TestInternetObject:
    @responses.activate
    def test_internet_objects(self, internet_objects_mock, st):
        internet_object = st.get_internet_object(264)
        assert internet_object.device_id == 264
        assert internet_object.object_name == "All internet"

        resolved_internet_object = st.get_internet_resolved_object(264)
        assert isinstance(resolved_internet_object, NetworkObject)

        response = st.add_internet_object(264, "Test Object")
        assert isinstance(response, InternetObject)

        response = st.update_internet_object(264, "Test Object Updated")
        assert isinstance(response, InternetObject)

        response = st.delete_internet_object(264)
        assert response is None
