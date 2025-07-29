import pytest
import json
import responses
from netaddr import IPAddress

from pytos2.securetrack.domain import Domain
from pytos2.utils import get_api_node


class TestDomains:
    @responses.activate
    def test_get_domain(self, domains_mock, st):
        domain = st.get_domain(cache=False, identifier=7)
        assert isinstance(domain, Domain)
        assert domain.id == 7
        assert domain.name == "London"
        domain = st.get_domain(cache=False, identifier="London")
        assert isinstance(domain, Domain)
        assert domain.id == 7
        assert domain.name == "London"
        domain_cache = st.get_domain(cache=True, identifier=7)
        assert isinstance(domain_cache, Domain)
        assert st._domains_cache.is_empty() is False
        domain_cache = st.get_domain(cache=True, identifier="London")
        assert isinstance(domain_cache, Domain)
        assert st._domains_cache.is_empty() is False

    @responses.activate
    def test_get_domains(self, domains_mock, st):
        domains = st.get_domains(cache=False)
        assert isinstance(domains, list)
        assert st._domains_cache.is_empty()
        domains_cache = st.get_domains(cache=True)
        assert isinstance(domains_cache, list)
        assert st._domains_cache.is_empty() is False

    @responses.activate
    def test_add_domain(self, domains_mock, st):
        res = st.add_domain("test", "test", "testaddr")
        assert isinstance(res, Domain)
        assert isinstance(res.id, int) and res.id == 7
        assert res.name == "London"

    @responses.activate
    def test_update_domain(self, domains_mock, st):
        res = st.update_domain(7, "test", "test", "testaddr")
        assert isinstance(res, Domain)
