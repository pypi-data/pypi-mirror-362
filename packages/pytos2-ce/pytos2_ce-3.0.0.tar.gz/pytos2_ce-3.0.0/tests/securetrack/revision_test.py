import pytest
import responses

import json
import os
from datetime import datetime, date, time
from time import mktime
from requests.exceptions import HTTPError
from . import conftest

from pytos2.securetrack.revision import Revision, RevisionTicket
from pytos2.utils import get_api_node


class TestRevision:
    @pytest.fixture
    def all_revisions(self):
        json_dir = "tests/securetrack/json/revisions"

        files = os.listdir(json_dir)
        files = [
            name
            for name in files
            if name.startswith("device-") and name.endswith(".json")
        ]

        json_list = [json.load(open(os.path.join(json_dir, name))) for name in files]
        return json_list

    def get_revision(self, rev_num):
        j = json.load(
            open(f"tests/securetrack/json/revisions/device-{rev_num}.json", "r")
        )
        return get_api_node(j, "revision", listify=True)

    @pytest.fixture
    def revisions_1(self):
        return self.get_revision(1)

    @pytest.fixture
    def revisions_20(self):
        return self.get_revision(20)

    @pytest.fixture
    def revision_with_modules_and_policy(self, revisions_20):
        for r in revisions_20:
            if int(r["id"]) == 118:
                return Revision.kwargify(r)

    @pytest.fixture
    def revision_with_ticket(self, revisions_1):
        for r in revisions_1:
            if int(r["id"]) == 719:
                return Revision.kwargify(r)

        raise ValueError(
            "Revision 719 in device ID 1 revisions no longer has an attached ticket"
        )

    def test_list_attributes(
        self, revision_with_ticket, revision_with_modules_and_policy
    ):
        assert revision_with_ticket.tickets[0].source == RevisionTicket.Source.SCW

        assert len(revision_with_ticket.tickets) == 2
        assert revision_with_ticket.tickets[0].id == 22

        assert revision_with_modules_and_policy.modules_and_policy[0].module == "SMCPM"
        assert (
            revision_with_modules_and_policy.modules_and_policy[0].policy == "Standard"
        )

    def test_attributes(self, revisions_1):
        revision = revisions_1[0]
        revision = Revision.kwargify(revision)

        assert revision.id == 1674
        assert revision.revision_id == 39
        assert revision.action == Revision.Action.AUTOMATIC
        assert revision.date == date(2018, 3, 8)
        assert revision.time == time(12, 47, 17)
        assert revision.admin == "-"
        assert revision.gui_client == "-"
        assert revision.audit_log == "-"
        assert revision.policy_package == "Standard"
        assert revision.authorization_status == Revision.AuthorizationStatus.AUTHORIZED

        assert isinstance(revision.modules_and_policy, list)
        assert len(revision.modules_and_policy) == 0

        assert revision.firewall_status
        assert revision.is_ready

        assert isinstance(revision.tickets, list)
        assert len(revision.tickets) == 0

    def test_set_attributes(self, revisions_1):
        revision = Revision.kwargify(revisions_1[0])

        revision.date = "2015-03-02"
        revision.time = "14:14:50.300"

        assert revision._date == date(2015, 3, 2)
        assert revision._time == time(14, 14, 50, 300000)

        revision.date = date(2014, 4, 12)
        assert revision._date == date(2014, 4, 12)

        revision.date = datetime(2014, 4, 11, 12, 12, 50)
        assert type(revision._date) is date
        assert revision._date == date(2014, 4, 11)
        assert revision.date_str == "2014-04-11"

        with pytest.raises(ValueError) as context:
            revision.date = []

        revision.date = None
        assert revision._date is None

        revision.time = time(12, 30)
        assert revision._time == time(12, 30, 0)

        revision.time = datetime(2013, 3, 2, 12, 50)
        assert revision._time == time(12, 50)
        assert revision.time_str == "12:50:00.000"

        with pytest.raises(ValueError) as context:
            revision.time = []

        revision.time = None
        assert revision._time is None

        _t = datetime(2015, 5, 5, 12, 30)
        _timestamp = mktime(_t.timetuple())

        revision.unix_timestamp = _timestamp
        assert revision.date == date(2015, 5, 5)
        assert revision.time == time(12, 30)
        assert revision.unix_timestamp == _timestamp

        with pytest.raises(ValueError) as context:
            revision.unix_timestamp = "invalid"

    def test_all_kwargify(self, all_revisions):
        for i, _revisions in enumerate(all_revisions):
            if _revisions is None:
                continue

            revisions = get_api_node(_revisions, "revision", listify=True)
            for revision in revisions:
                Revision.kwargify(revision)

    @responses.activate
    def test_revision_error(self, st, revisions_mock):
        temp = st.cache
        st.cache = None  # force cache to be empty
        with pytest.raises(HTTPError):
            st.get_revisions(device=100000)
        st.cache = None
        with pytest.raises(HTTPError):
            st._get_revisions_from_server(100000)
        st.cache = temp
