import pytest
from pytos2.utils.cache import Cache, CacheIndex


class Obj:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestCache:
    def test_destruct(self):
        cache = Cache()
        index = cache.make_index("a")

        index.__del__()

    def test_add(self):
        cache = Cache()
        a_index = cache.make_index("a")
        b_index = cache.make_index("b")

        cache.add(Obj(5, 10))
        cache.add(Obj(20, 20))

        assert a_index.get(5).b == 10
        assert b_index.get(10).a == 5
        assert a_index.get(20).b == 20

        cache.add(Obj(5, 20))
        assert a_index.get(5).b == 10
        assert a_index.get(5, 1).b == 20

    def test_is_empty(self):
        cache = Cache()
        index = cache.make_index("a")

        assert cache.is_empty()

        o = Obj(5, 10)
        cache.add(o)

        assert not cache.is_empty()

        cache.remove(o)

        assert cache.is_empty()

    def test_remove(self):
        cache = Cache()
        index = cache.make_index("a")

        o1 = Obj(5, 10)
        o2 = Obj(20, 20)

        cache.add(o1)
        cache.add(o2)

        assert index.get(5).b == 10
        assert index.get(5).a == 5

        cache.remove(o1)
        assert index.get(5) is None

    def test_clear(self):
        cache = Cache()
        index = cache.make_index("a")

        o1 = Obj(5, 10)
        o2 = Obj(20, 20)

        cache.add(o1)
        cache.add(o2)

        assert index.get(5).b == 10
        assert index.get(20).a == 20

        cache.clear()

        assert cache.get_data() == []
        assert cache.is_empty()

    def test_set(self):
        cache = Cache()
        index = cache.make_index("a")

        arr = [Obj(5, 10), Obj(20, 20)]

        cache.set_data(arr)

        assert index.get(5).b == 10
        assert index.get(20).a == 20
