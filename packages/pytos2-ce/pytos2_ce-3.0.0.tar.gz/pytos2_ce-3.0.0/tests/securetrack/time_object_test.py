import pytest
import json
import responses

from pytos2.securetrack.time_object import TimeObject
from pytos2.utils import get_api_node


class TestTimeObject:
    @responses.activate
    def test_get_time_objects(self, time_object_mock, st):
        time_objects = st.get_time_objects(2812)

        assert isinstance(time_objects[0], TimeObject)
        assert time_objects[0].id == 388
        assert time_objects[0].name == "Any"
        assert time_objects[0].uid == "{97AEB369-9AEA-11D5-BD16-0090272CCB30}"
        assert time_objects[0].is_global is False
        assert time_objects[0].class_name == "any_object"
        assert len(time_objects[0].time_intervals) == 0

        assert isinstance(time_objects[1], TimeObject)
        assert time_objects[1].id == 391
        assert time_objects[1].name == "Off_Work"
        assert time_objects[1].uid == "{4E4A450C-6A62-44A6-B974-AAC64F8B1DD8}"
        assert time_objects[1].is_global is False
        assert time_objects[1].class_name == "time"
        assert len(time_objects[1].time_intervals) == 2

        assert time_objects[1].time_intervals[0].from_time == "00:00"
        assert time_objects[1].time_intervals[0].to_time == "07:00"
        assert time_objects[1].time_intervals[1].from_time == "20:00"
        assert time_objects[1].time_intervals[1].to_time == "23:59"

        assert isinstance(time_objects[2], TimeObject)
        assert time_objects[2].id == 390
        assert time_objects[2].name == "Weekend"
        assert time_objects[2].uid == "{032FBEA8-A4D4-4134-9035-AA2A56091474}"
        assert time_objects[2].is_global is False
        assert time_objects[2].class_name == "time"
        assert len(time_objects[2].time_intervals) == 0

    @responses.activate
    def test_get_time_objects_by_id(self, time_object_mock, st):
        time_objects = st.get_time_objects(2812, [388])

        assert isinstance(time_objects[0], TimeObject)
        assert time_objects[0].id == 388
        assert time_objects[0].name == "Any"
        assert time_objects[0].uid == "{97AEB369-9AEA-11D5-BD16-0090272CCB30}"
        assert time_objects[0].is_global is False
        assert time_objects[0].class_name == "any_object"
        assert len(time_objects[0].time_intervals) == 0

        time_objects = st.get_time_objects(2812, [388, 390])

        assert isinstance(time_objects[0], TimeObject)
        assert time_objects[0].id == 388
        assert time_objects[0].name == "Any"
        assert time_objects[0].uid == "{97AEB369-9AEA-11D5-BD16-0090272CCB30}"
        assert time_objects[0].is_global is False
        assert time_objects[0].class_name == "any_object"
        assert len(time_objects[0].time_intervals) == 0

        assert isinstance(time_objects[1], TimeObject)
        assert time_objects[1].id == 390
        assert time_objects[1].name == "Weekend"
        assert time_objects[1].uid == "{032FBEA8-A4D4-4134-9035-AA2A56091474}"
        assert time_objects[1].is_global is False
        assert time_objects[1].class_name == "time"
        assert len(time_objects[1].time_intervals) == 0

    @responses.activate
    def test_get_time_objects_by_device(self, time_object_mock, st):
        time_objects = st.get_time_objects_by_device(1)

        assert isinstance(time_objects[0], TimeObject)
        assert time_objects[0].id == 83
        assert time_objects[0].name == "All"
        assert time_objects[0].uid == "{97AEB368-9AEA-11D5-BD16-0090272CCB30}"
        assert time_objects[0].is_global is False
        assert time_objects[0].class_name == "any_object"
        assert len(time_objects[0].time_intervals) == 0

        assert isinstance(time_objects[1], TimeObject)
        assert time_objects[1].id == 87
        assert time_objects[1].name == "Off_Work"
        assert time_objects[1].uid == "{4E4A450C-6A62-44A6-B974-AAC64F8B1DD8}"
        assert time_objects[1].is_global is False
        assert time_objects[1].class_name == "time"
        assert len(time_objects[1].time_intervals) == 2

        assert time_objects[1].time_intervals[0].from_time == "00:00"
        assert time_objects[1].time_intervals[0].to_time == "07:00"
        assert time_objects[1].time_intervals[1].from_time == "20:00"
        assert time_objects[1].time_intervals[1].to_time == "23:59"

    @responses.activate
    def test_device_get_time_objects(self, time_object_mock, devices_mock, st):
        device = st.get_device(1)
        time_objects = device.get_time_objects()

        assert isinstance(time_objects[0], TimeObject)
        assert time_objects[0].id == 83
        assert time_objects[0].name == "All"
        assert time_objects[0].uid == "{97AEB368-9AEA-11D5-BD16-0090272CCB30}"
        assert time_objects[0].is_global is False
        assert time_objects[0].class_name == "any_object"
        assert len(time_objects[0].time_intervals) == 0

        assert isinstance(time_objects[1], TimeObject)
        assert time_objects[1].id == 87
        assert time_objects[1].name == "Off_Work"
        assert time_objects[1].uid == "{4E4A450C-6A62-44A6-B974-AAC64F8B1DD8}"
        assert time_objects[1].is_global is False
        assert time_objects[1].class_name == "time"
        assert len(time_objects[1].time_intervals) == 2

        assert time_objects[1].time_intervals[0].from_time == "00:00"
        assert time_objects[1].time_intervals[0].to_time == "07:00"
        assert time_objects[1].time_intervals[1].from_time == "20:00"
        assert time_objects[1].time_intervals[1].to_time == "23:59"
