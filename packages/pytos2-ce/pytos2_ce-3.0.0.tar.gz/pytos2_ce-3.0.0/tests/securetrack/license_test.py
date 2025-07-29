import pytest
import json
import responses
from netaddr import IPAddress

from pytos2.securetrack.license import License, Customer, SKU, SKUDevice
from pytos2.utils import get_api_node, safe_iso8601_date


class TestLicenses:
    @responses.activate
    def test_get_licenses(self, licenses_mock, st):
        license = st.get_licenses()
        assert license.supported is True
        assert license.version == "3.1"
        assert license.customer_id == "0012000001KFH3bAAH"
        assert license.customer_name == "RND License Testing"
        assert license.license_file_id == "1e54d2c3-e2b4-41e6-ad83-1153b68b17a0"
        assert license.site_name == "Eval"
        assert license.site_type.value == "production"
        assert license.installed == safe_iso8601_date("2023-10-02T03:21:02Z")
        assert license.expires == safe_iso8601_date("2024-03-05T22:00:00Z")
        assert license.status.value == "expired"
        assert license.type.value == "evaluation"

        message = license.messages[0]
        assert message.category == "LICENSE_AUDIT"
        assert message.severity == "warning"
        assert message.code == "LICENSE_USAGE_WARN_STRONG"
        assert (
            message.message
            == "License usage report must be submitted within $1 days. After this time, you will not be able to upgrade TOS."
        )
        assert message.params[0] == "27"

    @responses.activate
    def test_get_license(self, licenses_mock, st):
        license = st.get_license(license_type=1)

        assert license.id == "1"
        assert license.type == "full"
        assert license.uid == "595e0a9d-6c9e-4a42-b488-cbccb802e567"
        assert license.issued == safe_iso8601_date("2022-06-20")
        assert license.expiration == safe_iso8601_date("2024-06-17")
        assert license.customer.id == "012345678ZZZZZZXXX"
        assert license.customer.name == "Contoso"
        assert license.customer.site == "Production"
        assert license.skus[1].name == "TS-SECTRK-FW-CLS"
        assert (
            license.skus[1].description
            == "Subscribed physical, Virtual Context, or Virtual Cloud Firewall Cluster"
        )
        assert license.skus[1].quantity == 15
        assert license.skus[1].expiration == safe_iso8601_date("2024-06-18")
        assert license.skus[1].devices[0].id == "5"
        assert license.skus[1].devices[0].name == "SRX"
        assert license.skus[1].devices[0].consumed == 1

        assert license.type == "full"

        license = st.get_license(license_type="evaluation")
        assert license.type == "evaluation"

    @responses.activate
    def test_get_tiered_license(self, licenses_mock, st):
        license = st.get_tiered_license()

        assert license.supported is True
        assert license.version == "3.1"
        assert license.customer_id == "0012000001KFH3bAAH"
        assert license.customer_name == "RND License Testing"
        assert license.license_file_id == "1e54d2c3-e2b4-41e6-ad83-1153b68b17a0"
        assert license.site_name == "Eval"
        assert license.site_type.value == "production"
        assert license.installed == safe_iso8601_date("2023-10-02T03:21:02Z")
        assert license.expires == safe_iso8601_date("2024-03-05T22:00:00Z")
        assert license.status.value == "expired"
        assert license.type.value == "evaluation"

        message = license.messages[0]
        assert message.category == "LICENSE_AUDIT"
        assert message.severity == "warning"
        assert message.code == "LICENSE_USAGE_WARN_STRONG"
        assert (
            message.message
            == "License usage report must be submitted within $1 days. After this time, you will not be able to upgrade TOS."
        )
        assert message.params[0] == "27"
