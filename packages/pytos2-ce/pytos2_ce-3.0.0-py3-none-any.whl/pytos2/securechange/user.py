from typing import Optional, List

from enum import Enum

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify, get_api_node


class UserXsiType(Enum):
    LOCALUSER = "localuser"
    USER = "user"
    GROUP = "group"


class OriginType(Enum):
    LOCAL = "Local"
    LDAP = "LDAP"


@propify
class LDAPConfiguration(Jsonable):
    name: str = prop(None)
    id: int = prop(None)


@propify
class UserDomain(Jsonable):
    name: str = prop()
    id: int = prop()


@propify
class Link(Jsonable):
    class Prop(Enum):
        HREF = "@href"

    href: str = prop(key=Prop.HREF.value)


@propify
class Permission(Jsonable):
    name: Optional[str] = prop(None)
    value: bool = prop(False)
    key: Optional[str] = prop(None, repr=False)


@propify
class UserRole(Jsonable):
    id: int = prop()
    name: str = prop()
    description: Optional[str] = prop(None)
    permissions: List[Permission] = prop(factory=list, flatify="permission", repr=False)
    role_link: Optional[Link] = prop(None, repr=False)


@propify
class UserUpdateRole(Jsonable):
    name: str = prop()


@propify
class SCWPartyLink(Jsonable):
    link: Optional[Link] = prop(None)
    type: Optional[str] = prop(None)
    name: Optional[str] = prop(None)
    id: int = prop(0)
    xsi_type: UserXsiType = prop(UserXsiType.USER, key=Jsonable.Prop.XSI_TYPE.value)


@propify
class SCWParty(Jsonable):
    class Prop(Enum):
        LDAP_DN = "ldapDn"

    class PartyType(Enum):
        USER = "user"
        GROUP = "group"

    class OriginType(Enum):
        LOCAL = "Local"
        LDAP = "LDAP"

    id: int = prop(0)

    xsi_type: UserXsiType = prop(UserXsiType.USER, key=Jsonable.Prop.XSI_TYPE.value)

    email: Optional[str] = prop(None)
    ldap_dn: Optional[str] = prop(None, key=Prop.LDAP_DN.value)
    ldap_configuration: Optional[LDAPConfiguration] = prop(None)
    authentication_method: Optional[str] = prop(None)
    origin_type: Optional[OriginType] = prop(None)
    member_of: List[SCWPartyLink] = prop(factory=list, flatify="user")
    domains: List[UserDomain] = prop(factory=list, flatify="domain")
    name: Optional[str] = prop(None)
    type: Optional[PartyType] = prop(None)
    link: Optional[Link] = prop(None)
    roles: List[UserRole] = prop(factory=list, flatify="role")


@propify
class SCWUser(SCWParty):
    class Meta(Enum):
        ROOT = "user"
        ENTITY = "user"

    out_of_office_from: Optional[str] = prop(None)
    out_of_office_until: Optional[str] = prop(None)
    notes: Optional[str] = prop(None)
    phone: Optional[str] = prop(None)
    send_email: bool = prop(False)
    first_name: Optional[str] = prop(None)
    last_name: Optional[str] = prop(None)
    display_name: Optional[str] = prop(None)


@propify
class SCWLocalUser(SCWParty):
    email: Optional[str] = prop(None)
    first_name: Optional[str] = prop(None)
    last_name: Optional[str] = prop(None)
    password: str = prop("")
    default_authentication: Optional[bool] = prop(False)
    phone: Optional[str] = prop(None)
    notes: Optional[str] = prop(None)
    name: str = prop("")


@propify
class NewLocalUser(SCWLocalUser):
    origin_type: OriginType = prop(OriginType.LOCAL)


@propify
class GroupPermission(Jsonable):
    name: str = prop("")
    value: bool = prop(False)


@propify
class SCWGroup(SCWParty):
    class Meta(Enum):
        ROOT = "group"
        ENTITY = "group"

    class Prop(Enum):
        GROUP_PERMISSIONS = "groupPermissions"
        GROUP_PERMISSION = "groupPermission"

    group_permissions: List[GroupPermission] = prop(
        factory=list,
        key=Prop.GROUP_PERMISSIONS.value,
        flatify=Prop.GROUP_PERMISSION.value,
    )
    description: Optional[str] = prop(None)
    members: List[SCWPartyLink] = prop(factory=list, flatify="user")


def classify_user_object(obj: dict, obj_type: str = None):
    """
    obj is the dictionary fetched from the server.

    obj_type was added because the `users/{id}` endpoint does not have
    an "@xsi.type" defined on the user object like you would expect.
    """

    if not obj_type:
        obj_type = obj[Jsonable.Prop.XSI_TYPE.value]

    cls = {
        UserXsiType.LOCALUSER.value: SCWUser,
        UserXsiType.USER.value: SCWUser,
        UserXsiType.GROUP.value: SCWGroup,
    }.get(obj_type, SCWParty)

    return cls.kwargify(obj)


@propify
class NotificationGroup(Jsonable):
    name: str = prop(None)
    origin_type: OriginType = prop(OriginType.LDAP)
    ldap_configuration: Optional[LDAPConfiguration] = prop(None)


@propify
class LDAPParty(Jsonable):
    ldap_dn: str = prop(None)
    ldap_configuration_name: str = prop(None)


@propify
class LDAPSimulateLogin(NotificationGroup):
    name: str = prop(None)
    origin_type: OriginType = prop(OriginType.LDAP)
    ldap_configuration: Optional[LDAPConfiguration] = prop(None)


@propify
class LDAPUserSimulateLogin(LDAPSimulateLogin):  #
    first_name: Optional[str] = prop(None)
    last_name: Optional[str] = prop(None)
    email: Optional[str] = prop(None)
    phone: Optional[str] = prop(None)
    notes: Optional[str] = prop(None)
