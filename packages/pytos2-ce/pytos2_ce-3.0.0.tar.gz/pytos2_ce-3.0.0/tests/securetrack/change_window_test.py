import datetime

import pytest
import responses

from pytos2.securetrack.change_window import ChangeWindow


class TestChangeWindows:
    @responses.activate
    def test_get_change_windows(self, change_windows_mock, st):
        change_windows = st.get_change_windows()

        assert change_windows[0].id == "07c230ce-2dec-4109-a0db-33ff45ba1057"
        assert change_windows[0].name == "Panorama - Change Window"
        assert (
            change_windows[0].description
            == "Change window for Panorama devices, will occur every second weekend"
        )
        assert change_windows[0].domain_id == 2
        assert change_windows[0].enabled

        assert change_windows[1].id == "b0dc4034-6d52-4197-8456-eef694b063e3"
        assert change_windows[1].name == "CP R80.10 - Change Window"
        assert change_windows[1].description == "Change window for R80 mgmt. Console"
        assert change_windows[1].domain_id == 9
        assert not change_windows[1].enabled

    @responses.activate
    def test_get_change_windows_fails(self, change_windows_mock_fails, st):
        with pytest.raises(ValueError) as context:
            st.get_change_windows()

        assert "Failed to get resource with status 403" in str(context.value)

        with pytest.raises(ValueError) as context:
            st.get_change_window_tasks("07c230ce-2dec-4109-a0db-33ff45ba1057")

        assert "Error retrieving" in str(context.value)

        with pytest.raises(ValueError) as context:
            st.get_change_window_task("07c230ce-2dec-4109-a0db-33ff45ba1057", 197)

        assert "Error retrieving" in str(context.value)

    @responses.activate
    def test_get_change_windows_fails_json(self, change_windows_mock_fails_json, st):
        with pytest.raises(ValueError) as context:
            st.get_change_windows()

        assert "Failed to decode response" in str(context.value)

        with pytest.raises(ValueError) as context:
            st.get_change_window_tasks("07c230ce-2dec-4109-a0db-33ff45ba1057")

        assert "Error decoding" in str(context.value)

        with pytest.raises(ValueError) as context:
            st.get_change_window_task("07c230ce-2dec-4109-a0db-33ff45ba1057", 197)

        assert "Error decoding" in str(context.value)

    @responses.activate
    def test_get_change_window_tasks(self, change_windows_mock, st):
        change_window_tasks = st.get_change_window_tasks(
            "07c230ce-2dec-4109-a0db-33ff45ba1057"
        )

        assert change_window_tasks[0].start_date == datetime.datetime(
            2024,
            3,
            29,
            0,
            0,
            1,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert change_window_tasks[0].end_date == datetime.datetime(
            2024,
            3,
            29,
            0,
            2,
            1,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert not change_window_tasks[0].errors

        assert change_window_tasks[1].start_date == datetime.datetime(
            2024,
            3,
            15,
            0,
            0,
            0,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert change_window_tasks[1].end_date == datetime.datetime(
            2024,
            3,
            15,
            0,
            2,
            0,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert (
            change_window_tasks[1].errors[0]
            == "Commit not performed as the Device Group monitoring is stopped"
        )

    @responses.activate
    def test_get_change_window_task(self, change_windows_mock, st):
        change_window_task = st.get_change_window_task(
            "07c230ce-2dec-4109-a0db-33ff45ba1057", 197
        )

        assert change_window_task.start_date == datetime.datetime(
            2024,
            3,
            29,
            0,
            0,
            1,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert change_window_task.end_date == datetime.datetime(
            2024,
            3,
            29,
            0,
            2,
            1,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        )
        assert not change_window_task.errors

        assert not change_window_task.device_commits[0].result.errors
        assert change_window_task.device_commits[0].result.device.status == "SUCCESS"
        assert change_window_task.device_commits[0].result.device.revision_id == 264
        assert not change_window_task.device_commits[0].result.device.warnings

        assert not change_window_task.device_commits[1].result.errors
        assert (
            change_window_task.device_commits[1].result.device.status
            == "SUCCESS_WITH_WARNINGS"
        )
        assert change_window_task.device_commits[1].result.device.revision_id == 370
        assert (
            change_window_task.device_commits[1].result.device.warnings[0]
            == "Commit not performed as the Device Group monitoring is stopped"
        )

    def test_change_window_uuid_property(self):
        import uuid

        change_window = ChangeWindow(domain_id=8)

        _id = str(uuid.uuid4())
        change_window.id = _id

        assert change_window.id == _id
        assert change_window.uuid == _id

        _id = str(uuid.uuid4())
        change_window.uuid = _id

        assert change_window.id == _id
