from enum import Enum

import copy


class CacheEvent(Enum):
    ADD = "add"
    REMOVE = "remove"
    CLEAR = "clear"
    SET = "set"


class Cache:
    def __init__(self):
        self._cache = []
        self._subscribers = {}

    def is_empty(self):
        return len(self._cache) == 0

    def add(self, obj):
        self._cache.append(obj)
        self._trigger_event(CacheEvent.ADD, obj)

    def remove(self, obj):
        self._cache.remove(obj)
        self._trigger_event(CacheEvent.REMOVE, obj)

    def clear(self):
        self._cache = []
        self._trigger_event(CacheEvent.CLEAR, None)

    def set_data(self, data):
        self._cache = copy.copy(data)
        self._trigger_event(CacheEvent.SET, self._cache)

    def _trigger_event(self, event: CacheEvent, param):
        subscribers = self._subscribers.setdefault(event, [])
        for sub in subscribers:
            sub(param)

    def add_event_listener(self, event: CacheEvent, fn):
        self._subscribers.setdefault(event, []).append(fn)

    def remove_event_listener(self, event: CacheEvent, fn):
        arr = self._subscribers.setdefault(event, [])
        self._subscribers[event] = [f for f in arr if f is not fn]

    def make_index(self, prop):
        index = CacheIndex(prop, self)
        index.on_set(self._cache)

        return index

    def get_data(self):
        return self._cache


class CacheIndex:
    def __init__(self, props, cache):
        self._cache = cache
        self.props = props if isinstance(props, list) else [props]

        self.index_map = {}

        cache.add_event_listener(CacheEvent.ADD, self.on_add)
        cache.add_event_listener(CacheEvent.REMOVE, self.on_remove)
        cache.add_event_listener(CacheEvent.CLEAR, self.on_clear)
        cache.add_event_listener(CacheEvent.SET, self.on_set)

    def __del__(self):
        cache = self._cache
        cache.remove_event_listener(CacheEvent.ADD, self.on_add)
        cache.remove_event_listener(CacheEvent.REMOVE, self.on_remove)
        cache.remove_event_listener(CacheEvent.CLEAR, self.on_clear)
        cache.remove_event_listener(CacheEvent.SET, self.on_set)

    def _add_with_prop(self, prop, obj):
        prop_val = getattr(obj, prop, None)

        if prop_val is not None:
            values = self.index_map.setdefault(prop_val, [])
            values.append(obj)

    def _remove_with_prop(self, prop, obj):
        prop_val = getattr(obj, prop, None)

        if prop_val is not None:
            values = self.index_map.setdefault(prop_val, [])
            values.remove(obj)

    def on_add(self, obj):
        for prop in self.props:
            self._add_with_prop(prop, obj)

    def on_remove(self, obj):
        for prop in self.props:
            self._remove_with_prop(prop, obj)

    def on_clear(self, param):
        self.index_map = {}

    def on_set(self, data):
        self.index_map = {}

        for entry in data:
            self.on_add(entry)

    def get(self, key, index=0):
        arr = self.index_map.setdefault(key, [])

        if len(arr) == 0:
            return None

        return arr[index]
