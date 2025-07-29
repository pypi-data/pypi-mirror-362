from typing import Tuple, Any, Optional, Union, List, get_type_hints, Callable
import typing

from requests import JSONDecodeError

try:
    from typing import _ForwardRef as ForwardRef  # type: ignore
except ImportError:  # pragma: no cover
    # python 3.7+ support
    from typing import ForwardRef  # type: ignore

from enum import Enum
from copy import deepcopy

import logging
from logging import NullHandler
from os import getenv
from sys import stdout
from pathlib import Path
import warnings
from datetime import datetime
import re

from dateutil.parser.isoparser import isoparse  # type: ignore
from pythonjsonlogger.json import JsonFormatter  # type: ignore
import attr

LOGGERS: set = set()


class TimeFormat(Enum):
    DATE = "%Y-%m-%d"
    TIME = "%H:%M:%S.%f"
    DATE_TIME = "%Y-%m-%d %H:%M:%S.%f"
    SC_TIME = "%H:%M"
    UTC = "%d-%b-%Y %I:%M:%S%p %z"


def safe_date(exp: str, fmt: TimeFormat) -> Optional[datetime]:
    try:
        return datetime.strptime(exp, fmt.value)
    except (ValueError, TypeError):
        return None


def safe_iso8601_date(d: str) -> Optional[datetime]:
    try:
        return isoparse(d)
    except ValueError:
        return None


def deprecated_property(old_prop, new_prop):
    """
    This function is a helper to reduce boilerplate for deprecated properties.
    """

    def getter(self):
        warnings.warn(f"{old_prop} is deprecated. use {new_prop} instead.")
        return getattr(self, new_prop)

    def setter(self, v):
        warnings.warn(f"{old_prop} is deprecated. use {new_prop} instead.")
        setattr(self, new_prop, v)

    return property(getter, setter)


def propify(cls):
    cls._propify = True
    cls = attr.s(cls, auto_attribs=True, kw_only=True)
    return cls


def prop(
    default=attr.NOTHING,
    validator=None,
    repr=True,
    cmp=True,
    hash=None,
    init=True,
    metadata=None,
    type=None,
    converter=None,
    factory=None,
    kw_only=False,
    key: Optional[str] = None,
    flatify: Optional[str] = None,
    listify: Optional[bool] = None,
    jsonify: Optional[Union[bool, str, Callable]] = True,
    kwargify=None,
    eq=None,
    order=None,
):
    """This function extends attr.ib to to create succint classes that are deserialized
    from and can be serializated to JSON. It adds 4 custom metadata fields that
    control the serialiation flow. These fields end up being stored in the
    `__attrs_attrs__` attribute of the class, and are used by the jsonify and kwargify
    functions below. As with attr.ib it does *NOT* do anything unless the class is
    decorated with @propify

    Args:
        key: The JSON prop value to deserialize / serialize for the attribute.
            Optional if the attribute name matches the value
        flatify: Optional JSON key to remove from the tree (flatten).
            For example, given a JSON object of {"things": {"thing": 123}}, in the
            result object, `obj.things` would equal `123`, rather than {"thing": 123}
        listify: Ensures that the resulting attribute is a list.
            This is useful for  cases where field contains a list when there are
            multiple objects in a results, but does not wrap single objects in a list
            eg. TOS < 19.1
        jsonify: Specifies whether the attribute should be serialized to JSON.
            If the value passed is a string, the value of the attribute with the string
            name if used for the serialized value.

            If the value passed is a callable, the attribute will be run
            through said function and the return value used for the serialized
            value.

    Returns:
        _CountingAttr as returned by attr.ib
    """
    return attr.ib(
        default=default,
        validator=validator,
        repr=repr,
        hash=hash,
        init=init,
        converter=converter,
        factory=factory,
        metadata={
            "key": key,
            "flatify": flatify,
            "listify": listify,
            "jsonify": jsonify,
            "kwargify": kwargify,
            "_propify": True,
        },
        type=type,
        kw_only=kw_only,
        eq=eq or cmp,
        order=order,
    )


class NoInstance:
    """
    Utility class for attributes that should not be accessed with helpful exceptions
    """

    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

    def __getattr__(self, attrib):
        raise RuntimeError(
            "Error accessing {}.{}. {}".format(self.name, attrib, self.message)
        )


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


def snakecase_to_upper_camelcase(name):
    # converts a snake case string to UpperCaseCamelCase
    return "".join((n.capitalize() for n in name.lower().split("_")))


def safe_unwrap_type(attrib, cls):
    if getattr(attrib.type, "__args__", None):
        args = [a for a in attrib.type.__args__ if a is not type(None)]  # noqa

        if len(args) == 1:
            typ = args[0]
            # We do this for performance
            if isinstance(typ, ForwardRef):
                hints = get_type_hints(cls)
                typ = hints.get(attrib.name)
                typ = [a for a in typ.__args__ if a is not type(None)][0]  # noqa
            return typ

        else:
            return None
    else:
        return attrib.type


TYPE_ALIASES = {
    typing.List: list,
    typing.Dict: dict,
}


def classify_attrib(cls, attrib, val, _key=""):
    # If the attrib annotation has __args__, it might be a Union (eg. Optional),
    # so check each of the args to see if it's an Enum
    # This might have to be updated in future versions of Python, as it's an
    # undocumented attribute
    kwargify = attrib.metadata.get("kwargify")
    if kwargify is not None:
        if kwargify is False:
            return val
        return kwargify(val)

    typ = safe_unwrap_type(attrib, cls)
    if typ in TYPE_ALIASES:
        typ = TYPE_ALIASES[typ]

    try:
        if typ and isinstance(typ, type) and issubclass(typ, Enum):
            return typ(val) if any(v.value == val for v in typ) else val
    except TypeError as e:
        raise TypeError(
            f"Error classifying {cls.__name__}.{attrib.name} with value {repr(val)} at key {_key}"
        ) from e

    if hasattr(typ, "kwargify"):
        try:
            return typ.kwargify(val)
        except TypeError as e:
            raise TypeError(
                f"Error kwargifying {cls.__name__}.{attrib.name} with value {repr(val)} at key {_key}"
            ) from e

    if callable(typ):
        # Try to be smart about converting types before it ever gets to attrs, but if it doesn't work, just return the value
        try:
            return typ(val)
        except Exception:
            return val
    # don't classify, return the raw value
    return val


def kwargify(cls: Any, _data: dict, _key="") -> Tuple[dict, dict]:
    """Utility function to assist with deserializing a JSON based dictionary to an
    object. This function only works with classes decorated with @propify, and with
    attributes generated using the propify function. Typical use is in a classmethod to
    create a prepped dictionary that can be used to init a class instance.

    Args:
        cls: class (not instance) that will be deserialized to
        _data: JSON dict to be deserialized

    Returns: a tuple with two items.
        0: a processed version of the _data argument with prop keys translated and
            lists guarenteed
        1: kwargs to init the class instance

    """

    data = deepcopy(_data)
    kwargs = {"data": _data, "flatifies": {}}
    if hasattr(cls, "Meta") and hasattr(cls.Meta, "ROOT"):
        data = data.get(cls.Meta.ROOT.value, data)

    attrs = cls.__attrs_attrs__

    for attrib in attrs:
        meta = attrib.metadata
        # key is the json prop string value
        key = meta.get("key") or attrib.name

        # skip props that aren't in the json, or init is not True
        if not attrib.init:
            continue

        if key not in data:
            default = attrib.default
            if (
                default is attr.NOTHING
                and meta.get("_propify")
                and meta.get("kwargify") is not False
            ):
                raise ValueError(f"key {key} is required to kwargify {cls}")
            elif hasattr(default, "factory") and meta.get("_propify"):
                if isinstance(data, list) and isinstance(key, str):
                    _errkey = f"{cls.__name__}.{_key}" if _key else cls.__name__
                    raise TypeError(
                        f"list indices must be integers or slices, not str, at {_errkey}.{key}"
                    )
                data[key] = default.factory()
            else:  # pragma: no cover
                continue

        # flatify
        flatify = meta.get("flatify")
        if flatify is not None and isinstance(data[key], dict):
            # handle things in flatify that need to be preserved in jsonify
            flatify_xsi_type = data[key].get("@xsi.type")
            if flatify_xsi_type:
                kwargs["flatifies"][key] = {"@xsi.type": flatify_xsi_type}
            data[key] = data[key].get(flatify, data[key])
        # listify
        if meta.get("listify"):
            warnings.warn(
                "The listify argument has been deprecated, use typed attrs instead",
                DeprecationWarning,
            )  # pragma: no cover
        # Convert to lists based on types
        if meta.get("listify") or (
            attrib.type in (List, list)
            or (
                hasattr(attrib.type, "__origin__")
                and attrib.type.__origin__ in (list, List)
            )
        ):
            if not isinstance(data[key], list):
                data[key] = [data[key]] if data[key] else []
            # Check for edge case where list has empty strings
            data[key] = [
                classify_attrib(cls, attrib, val, _key=_key + f".{key}")
                for val in data[key]
                if val
            ]
        else:
            try:
                data[key] = classify_attrib(
                    cls, attrib, data[key], _key=_key + f".{key}"
                )
            except TypeError as e:
                raise TypeError(
                    f"Error classifying {cls.__name__}.{attrib.name} at key {_key}.{key} in {repr(data)}"
                ) from e
        kwargs[attrib.name] = data[key]
    return data, kwargs


def jsonify(obj: Any) -> dict:
    _json = {}
    for cls in type(obj).__mro__:
        attrs = getattr(cls, "__attrs_attrs__", None)
        if not attrs:
            continue
        for _attrib in attrs:
            meta = _attrib.metadata
            jsonify = meta.get("jsonify")
            attrib = (
                jsonify
                if jsonify and jsonify is not True and not callable(jsonify)
                else _attrib.name
            )
            key = meta.get("key") or attrib
            val = getattr(obj, attrib, None)
            if callable(jsonify):
                val = jsonify(val)
            if not meta.get("jsonify") or val is None:
                continue  # pragma: no cover
            if isinstance(val, list):
                val = [
                    getattr(n, "_json", n)
                    for n in val
                    if getattr(n, "_json", n) not in (None, {}, "")
                ]
            elif hasattr(val, "_json"):
                val = val._json
            elif isinstance(val, Enum):
                val = val.value
            flatify = meta.get("flatify")
            if flatify:
                val = {flatify: val, **obj._flatifies.get(key, {})}
            _json[key] = val
    return _json


def get_api_node(obj: dict, path: str, listify: bool = False, default: Any = None):
    """listify=True basically makes default = [].
    See test: TestGetApiNode::test_default for an example"""

    def _listify(obj):
        return [obj] if not isinstance(obj, list) else obj

    def split_escaped(path):
        return [
            k.replace("KQypbNUMED", ".")
            for k in path.replace("..", "KQypbNUMED").split(".")
        ]

    def wrap(val):
        return f"['{val}']"

    node: Union[dict, list, None, str, int] = obj
    nodes: list = []
    for prop in split_escaped(path):
        if isinstance(node, list):
            raise ValueError(
                f"Tried to access key '{prop}' of a list at obj{''.join(wrap(n) for n in nodes)}"
            )
        elif isinstance(node, dict):
            node = node.get(prop)
            nodes.append(prop)
        else:
            node = None
            break

    if node:
        return _listify(node) if listify else node
    else:
        return [] if listify and default is None else default


STDOUT_FORMAT = """%(asctime)s %(funcName)s %(levelname)s %(pathname)s %(lineno)s %(process)s %(message)s"""
JSON_FORMAT = """%(asctime) %(created) %(filename) %(funcName) %(levelname)
    %(levelno) %(lineno) %(module) %(msecs) %(message) %(name) %(pathname)
    %(process) %(processName) %(relativeCreated) %(thread) %(threadName)"""


class DictFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, dict):
            record.msg = record.msg.get("message")
        return super().format(record)


def legacy_setup_logger(name, log_dir=None, to_stdout=None, level=None):
    if to_stdout is None:
        to_stdout = (
            False
            if getenv("PYTOS_LOG_TO_STDOUT", "").lower()
            in ("false", "f", "0", "no", "none", "")
            else True
        )
    logger = logging.getLogger(name)
    if len(logger.handlers):
        return logger

    level = level or getenv(
        f"{name.upper()}_LOG_LEVEL", getenv("PYTOS_LOG_LEVEL", logging.INFO)
    )
    level = logging.getLevelName(level)

    log_dir = log_dir or getenv(f"{name.upper()}_LOG_DIR", getenv("PYTOS_LOG_DIR"))

    if log_dir:
        log_dir = Path(log_dir)
        if log_dir.is_dir():
            log_path = log_dir / f"{name}.log.json"
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(JsonFormatter(JSON_FORMAT))
            logger.addHandler(file_handler)
    if not log_dir or not log_dir.is_dir() or to_stdout or level == logging.DEBUG:
        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setFormatter(DictFormatter(STDOUT_FORMAT))
        logger.addHandler(stdout_handler)

    logger.setLevel(level)
    return logger


def setup_logger(name, log_dir=None, to_stdout=None, level=None):
    logger = logging.getLogger(name)
    if logger not in LOGGERS:
        logger.addHandler(NullHandler())
        LOGGERS.add(logger)
    return logger


__all__ = ["NoInstance"]


def uids_match(uid1, uid2):
    return sanitize_uid(uid1) == sanitize_uid(uid2)


def sanitize_uid(uid):
    return re.sub("({|})", "", uid).lower()


def stringify_optional_obj(obj_to_stringify):
    return None if obj_to_stringify is None else str(obj_to_stringify)


def safe_unwrap_msg(res):
    try:
        j = res.json()
        return j.get("result", {}).get("message", res.text)
    except JSONDecodeError:
        return res.text or "no decodable message"


def multiroot_kwargify(cls, data, _globals=None, _locals=None):
    if _globals is None:
        _globals = globals()
    if _locals is None:
        _locals = locals()

    if hasattr(cls, "Config"):
        cfg = cls.Config

        # has_multi_root is designed for the workflow return.
        # The real data is contained in the root key, which varies depending
        # on the workflow type.
        if getattr(cfg, "has_multi_root", False):
            root_default_cls = getattr(cfg, "root_default_cls", cls)
            root_dict = getattr(cfg, "root_dict", {})

            root_data = None
            root_cls = None
            for root, _cls in root_dict.items():
                root_data = data.get(root, None)
                if root_data:
                    data = root_data
                    root_cls = _cls
                    break

            if not root_data:
                root_data = (
                    data.get(list(data.keys())[0], data) if len(data) == 1 else data
                )
                data = root_data
                root_cls = root_default_cls

            if isinstance(root_cls, str):
                root_cls = ForwardRef(root_cls)
            if isinstance(root_cls, ForwardRef):
                root_cls = root_cls._evaluate(
                    _globals, _locals, recursive_guard=frozenset()
                )

            cls = root_cls
    _obj, kwargs = kwargify(cls, data)
    return cls(**kwargs)
