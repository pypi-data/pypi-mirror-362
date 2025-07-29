import pytest
import json
import responses

from pytos2.securechange.user import (
    NewLocalUser,
    LDAPConfiguration,
    LDAPParty,
    LDAPSimulateLogin,
    LDAPUserSimulateLogin,
)


class TestUsers:
    @responses.activate
    def test_add_user_group(self, user_or_group_mock, user_mock, scw):
        res = scw.add_user_group("Group1", "Test Group 1", "group1@contoso.com")
        assert res.email == "contoso@contoso.com"

    @responses.activate
    def test_update_user_group(self, user_or_group_mock, scw):
        res = scw.update_user_group(54, ["70", "96"], ["85", "49"])
        assert res is None

        res = scw.update_user_group(54, ["70", "96"])
        assert res is None

        res = scw.update_user_group(54, None, ["85", "49"])
        assert res is None

    @responses.activate
    def test_delete_user_or_group(self, user_or_group_mock, scw):
        res = scw.delete_user_or_group(70)
        assert res is None

    @responses.activate
    def test_add_user(self, user_or_group_mock, user_mock, scw):
        new_user = NewLocalUser()
        new_user.name = "abaker"
        new_user.first_name = "Aaron"
        new_user.last_name = "Baker"
        new_user.email = "aaron.baker@contoso.com"
        new_user.password = "password"
        new_user.notes = "asdf"
        new_user.default_authentication = False
        res = scw.add_user(new_user)
        assert res.name == "johnny_smith"

    @responses.activate
    def test_user_import_ldap(self, user_or_group_mock, scw):
        ldap = LDAPParty()
        ldap.ldap_configuration_name = "Contoso LDAP"
        ldap.ldap_dn = "CN=abaker,OU=Users,DC=tcse,DC=net"
        res = scw.user_import_ldap(ldap)
        assert res is None

    @responses.activate
    def test_user_login(self, user_or_group_mock, scw):
        user = LDAPUserSimulateLogin()
        user.name = "abaker"
        ldap_config = LDAPConfiguration()
        ldap_config.name = "Contoso LDAP"
        ldap_config.id = 1
        user.ldap_configuration = ldap_config
        res = scw.user_login(user)
        assert res is None

    @responses.activate
    def test_group_login(self, user_or_group_mock, scw):
        group = LDAPSimulateLogin()
        group.name = "Accountants"
        ldap_config = LDAPConfiguration()
        ldap_config.name = "Contoso LDAP"
        ldap_config.id = 1
        group.ldap_configuration = ldap_config
        res = scw.group_login(group)
        assert res is None
