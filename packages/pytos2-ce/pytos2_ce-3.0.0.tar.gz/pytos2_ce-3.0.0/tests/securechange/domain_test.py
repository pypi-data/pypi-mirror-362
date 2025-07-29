import json
import pytest
import responses


class TestWorkflows:
    @responses.activate
    def test_get_domains(self, domains_mock, scw):
        domains = scw.get_domains()
        assert domains[8].id == "9"
        assert domains[8].name == "1Toronto BCKP"
        assert domains[8].description == ""

    @responses.activate
    def test_get_domain(self, domains_mock, scw):
        domain = scw.get_domain(2)
        assert domain.id == "2"
        assert domain.name == "Toronto"
        assert domain.description == "Test"
