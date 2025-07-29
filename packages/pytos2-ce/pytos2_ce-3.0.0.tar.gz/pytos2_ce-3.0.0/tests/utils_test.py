from enum import Enum
import json

import pytest  # type: ignore
from netaddr import IPNetwork, IPAddress, IPRange  # type: ignore

from pytos2.utils import (
    snakecase_to_upper_camelcase,
    NoInstance,
    singleton,
    setup_logger,
    propify,
    prop,
    kwargify,
    get_api_node,
    deprecated_property,
)
from typing import Dict, List, Optional, Union
from pytos2.models import Jsonable, UnMapped


@propify
class DeprecatedPropertyClass(Jsonable):
    test_property: str = prop("TEST VALUE")

    deprecated_property = deprecated_property("deprecated_property", "test_property")


@propify
class Child(Jsonable):
    name: str = prop()
    nested: List["Child"] = prop(factory=list)


@propify
class DictKwargify(Jsonable):
    name: str = prop()
    properties_dict: Dict = prop(factory=dict)


@propify
class Parent(Jsonable):
    class Meta(Enum):
        ROOT = "root"

    class Things(Enum):
        THIS = "this"
        THAT = "that"

    class Maybe(Enum):
        MAYBE = "MAYBE"

    class Flub(Enum):
        FLARG = "flarg"

    class Prop(Enum):
        FOOBAR = "$#@%$"

    foobar: Optional[str] = prop(key=Prop.FOOBAR.value)
    keys: List[str] = prop(flatify="key")
    empties: List[str] = prop(flatify="empty")
    maybe: Optional[Maybe] = prop()
    thing: Things = prop()
    flub: Flub = prop()
    no_json: Optional[bool] = prop(None, jsonify=False)
    data: Optional[dict] = None
    missing_list: List[str] = prop(factory=list)
    missing: Optional[str] = prop(None)
    wrong: Union[str, int] = prop()
    netty: IPNetwork = prop(kwargify=False)
    addy: IPAddress = prop()
    rangy: IPRange = prop(kwargify=False)
    children: List[Child] = prop(factory=list)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)
        kwargs["netty"] = IPNetwork(f"{_obj['network']}/{_obj['mask']}")
        kwargs["rangy"] = IPRange(*_obj["rangy"].split("-"))
        return cls(**kwargs)


@pytest.fixture
def parent():
    return Parent.kwargify(
        {
            "root": {
                "keys": {"key": "value"},
                "empties": "",
                "$#@%$": "eff word",
                "ignore": "sad, many such cases",
                "no_json": "hare today",
                "flub": "Negatrov",
                "thing": "this",
                "extra": "MIA",
                "maybe": "yes",
                "wrong": 12,
                "network": "1.2.3.0",
                "mask": "255.255.255.0",
                "addy": "1.2.3.4",
                "rangy": "1.1.1.1-2.2.2.2",
                "children": [
                    {
                        "name": "child1",
                        "nested": [{"name": "child2"}, {"name": "child3"}],
                    }
                ],
            }
        }
    )


def test_kwargify(parent):
    assert isinstance(parent.keys, list)
    assert isinstance(parent.empties, list)
    assert parent.foobar == "eff word"
    with pytest.raises(AttributeError):
        parent.ignore
    assert parent.thing is parent.Things.THIS
    assert parent.flub == "Negatrov"
    assert parent["flub"] == "Negatrov"


def test_kwargify_dict(parent):
    # This ensures that the typing.Dict is properly handled.
    dk = DictKwargify.kwargify({"name": "test", "properties_dict": {}})
    assert dk.name == "test"
    assert dk.properties_dict == {}


def test_kwargify_missing_props(parent):
    bad = parent.data
    del bad["root"]["thing"]
    with pytest.raises(ValueError):
        Parent.kwargify(bad)


def test_json(parent):
    assert parent._json == {
        "keys": {"key": ["value"]},
        "empties": {"empty": []},
        "$#@%$": "eff word",
        "thing": "this",
        "maybe": "yes",
        "flub": "Negatrov",
        "missing_list": [],
        "wrong": 12,
        "netty": IPNetwork("1.2.3.0/24"),
        "addy": IPAddress("1.2.3.4"),
        "rangy": IPRange("1.1.1.1", "2.2.2.2"),
        "children": [
            {
                "name": "child1",
                "nested": [
                    {"name": "child2", "nested": []},
                    {"name": "child3", "nested": []},
                ],
            }
        ],
    }


def test_json_override(parent):
    override = {"some": "dic"}
    parent._json = override
    assert parent._json is override


def test_deprecated_property():
    p_class = DeprecatedPropertyClass(test_property="TEST")
    assert p_class.deprecated_property == "TEST"

    p_class.deprecated_property = "ANOTHER VALUE"
    assert p_class.test_property == "ANOTHER VALUE"


@singleton
class Single(object):
    pass


def test_unmapped():
    _json = {"some": "thing"}
    obj = UnMapped.kwargify(_json)
    assert obj._json == _json


class TestHelpers:
    def test_singleton(self):
        single1 = Single()
        single2 = Single()
        assert single1 is single2

    def test_no_instance_obj(self):
        name, msg = "test", "Test error msg"
        no_instance = NoInstance(name, msg)
        with pytest.raises(RuntimeError):
            no_instance.nothing

    def test_snakecase_to_upper_camelcase(self):
        assert (
            snakecase_to_upper_camelcase("snek_case_is_awesome") == "SnekCaseIsAwesome"
        )


class TestGetApiNode:
    empty: dict = {}
    empty_nested: dict = {"things": {}}
    blank_string_nested: dict = {"things": ""}
    flat_nested: dict = {"things": {"thing": {"key": "val"}}}
    list_nested: dict = {"things": {"thing": [{"key": "val"}]}}

    @pytest.mark.parametrize(
        "obj, path, val",
        (
            (empty, "things.thing", None),
            (empty_nested, "things.thing", None),
            (blank_string_nested, "things.thing", None),
            (flat_nested, "things.thing.key", "val"),
        ),
    )
    def test_empty(self, obj, path, val):
        assert get_api_node(obj, path) == val

    @pytest.mark.parametrize(
        "obj, path, val",
        (
            (empty, "things.thing", []),
            (empty_nested, "things.thing", []),
            (blank_string_nested, "things.thing", []),
            (flat_nested, "things.thing", [{"key": "val"}]),
        ),
    )
    def test_listify(self, obj, path, val):
        assert get_api_node(obj, path, listify=True) == val

    @pytest.mark.parametrize(
        "obj, path, val",
        (
            (empty, "things.thing", "default"),
            (empty_nested, "things.thing", "default"),
            (blank_string_nested, "things.thing", "default"),
            (flat_nested, "things.thing", [{"key": "val"}]),
        ),
    )
    def test_default(self, obj, path, val):
        assert get_api_node(obj, path, listify=True, default="default") == val

    def test_list_key_exception(self):
        with pytest.raises(ValueError) as excinfo:
            get_api_node(self.list_nested, "things.thing.key")
        assert "obj['things']['thing']" in str(excinfo.value)


# class TestLogging:
#     def test_with_file_arg(self, tmp_path):
#         lo = setup_logger("test", tmp_path)
#         lo.error("TEST MESSAGE")
#         msg = json.loads(open(tmp_path / "test.log.json").readline())
#         assert msg["message"] == "TEST MESSAGE"
#
#     def test_duplicate_logger(self):
#         lo = setup_logger("test")
#         assert lo == setup_logger("test")
#
#     def test_stdout_logger(self, caplog):
#         lo = setup_logger("out")
#         lo.error("TEST MESSAGE", extra={"ignore": "ignore"})
#         assert "TEST MESSAGE" in caplog.records[0].message
#
#     def test_dict_formatter(self, caplog):
#         lo = setup_logger("out")
#         lo.error({"message": "TEST MESSAGE", "hide": "HIDE"})
#         assert "TEST MESSAGE" in caplog.records[0].message
