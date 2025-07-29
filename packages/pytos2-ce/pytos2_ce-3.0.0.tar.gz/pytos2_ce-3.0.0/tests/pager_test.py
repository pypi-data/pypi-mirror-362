from pytos2.api import BaseAPI, Pager
import pytest

PAGER_TEST_LIST = [{"id": idx} for idx in range(10000)]


class _TestResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data

    @property
    def ok(self):
        return True


class _TestSession:
    def __init__(self, emulate_total=True):
        self.emulate_total = emulate_total

    def get(self, *args, params=None, **kwargs):
        params = params or {}

        tlist = PAGER_TEST_LIST[
            params.get("start", 0) : params.get("start", 0) + params.get("count", 0)
        ]
        data = {"data": {"count": len(tlist), "data": tlist}}

        if params.get("get_total", None) == "true" and self.emulate_total:
            data["data"]["total"] = len(PAGER_TEST_LIST)

        return _TestResponse(data)


class _TestAPI(BaseAPI):
    def __init__(self, emulate_total=True):
        super().__init__(_TestSession(emulate_total=emulate_total))


class _TestPager(Pager):
    def __init__(
        self,
        api_node="data.data",
        page_size=2000,
        start=None,
        stop=None,
        step=None,
        is_slice=False,
        emulate_total=True,
    ):
        self.emulate_total = emulate_total

        super().__init__(
            _TestAPI(emulate_total=emulate_total),
            None,
            api_node,
            None,
            None,
            page_size=page_size,
            start=start,
            stop=stop,
            step=step,
            is_slice=is_slice,
        )

    def _new_pager(self, start=None, stop=None, step=None, is_slice=False):
        return _TestPager(
            page_size=self.page_size,
            start=start,
            stop=stop,
            step=step,
            is_slice=is_slice,
            emulate_total=self.emulate_total,
        )


class TestPager:
    def test_basic_pager(self):
        basic = _TestPager()

        assert basic[0]["id"] == 0
        assert basic[2001]["id"] == 2001

        assert isinstance(basic, Pager)

        assert len(basic) == 10000

        # Cover the emulated total instance.
        assert basic.fetch_all()[-1]["id"] == 9999

    def test_one_slice(self):
        basic = _TestPager()
        sliced = basic[5:10]

        assert isinstance(sliced, Pager)
        assert isinstance(sliced, _TestPager)

        assert sliced[0]["id"] == 5
        assert sliced[1]["id"] == 6
        assert sliced[2]["id"] == 7
        assert sliced[3]["id"] == 8
        assert sliced[4]["id"] == 9

        with pytest.raises(IndexError):
            sliced[5]

        assert len(sliced) == 5
        sliced_repr = repr(sliced)
        assert sliced is iter(sliced)

        assert "Pager" in sliced_repr
        assert "5 items" in sliced_repr

    def test_slice_of_slice(self):
        basic = _TestPager()
        sliced = basic[5:10]
        second = sliced[1:3]
        assert isinstance(second, list)
        assert len(second) == 2
        assert second[0]["id"] == 6

    def test_slice_with_step(self):
        basic = _TestPager()
        sliced = basic[5:10:2]
        assert sliced[0]["id"] == 5
        assert sliced[1]["id"] == 7
        assert len(sliced) == 2

        assert isinstance(sliced, Pager)

        sliced = basic[10::2]
        assert sliced[0]["id"] == 10
        assert sliced[-1]["id"] == 9998
        assert len(sliced) == 4995

    def test_slice_with_only_start(self):
        basic = _TestPager()
        sliced = basic[10:]
        assert sliced[0]["id"] == 10
        assert sliced[-1]["id"] == 9999
        assert len(sliced) == 9990

    def test_slice_with_only_stop(self):
        basic = _TestPager()
        sliced = basic[:10]
        assert sliced[0]["id"] == 0
        assert sliced[-1]["id"] == 9
        assert len(sliced) == 10

    def test_slice_with_only_step(self):
        basic = _TestPager()
        sliced = basic[::2]
        assert sliced[0]["id"] == 0
        assert sliced[1]["id"] == 2
        assert sliced[-1]["id"] == 9998
        assert len(sliced) == 5000

    def test_next(self):
        basic = _TestPager()
        first = next(basic)
        assert first["id"] == 0

        last_id = None
        for item in basic:
            last_id = item["id"]

        assert last_id == 9999

    def test_eq(self):
        basic = _TestPager()
        basic2 = _TestPager()

        sliced = basic[5:10]

        assert basic == basic2
        assert sliced == basic2[5:10]
        assert basic != sliced

        assert basic != 0

    def test_invalid_slices(self):
        basic = _TestPager()

        with pytest.raises(IndexError):
            basic[-5:10:2]

        with pytest.raises(IndexError):
            basic[5:-10:2]

        with pytest.raises(IndexError):
            basic[5:10:-2]

    def test_invalid_indices(self):
        basic = _TestPager()

        with pytest.raises(IndexError):
            basic[5:10][10]

        with pytest.raises(IndexError):
            basic[10500]

    def test_no_total_from_api(self):
        basic = _TestPager(emulate_total=False)

        assert len(basic) == 2000
        assert basic.fetch_all()[-1]["id"] == 9999

        assert len(basic) == 10000
