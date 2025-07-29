import pytest
import json

from pytos2.securechange.verifier import (
    VerifierTarget,
    AccessRequestVerifierResult,
    classify_verifier_result,
)

from pytos2.utils import get_api_node


@pytest.fixture
def verifier_result_json():
    return json.load(open("tests/securechange/json/verifier/verifier_result_199.json"))


class TestVerifierResult:
    def test_kwargify(self, verifier_result_json):
        verifier_result = classify_verifier_result(verifier_result_json)
        assert isinstance(verifier_result, AccessRequestVerifierResult)

        targets = verifier_result.verifier_targets
        assert len(targets) == 5

        assert isinstance(targets[0], VerifierTarget)
        assert targets[0].management_id == 32
        assert len(targets[0].verifier_bindings) == 2
