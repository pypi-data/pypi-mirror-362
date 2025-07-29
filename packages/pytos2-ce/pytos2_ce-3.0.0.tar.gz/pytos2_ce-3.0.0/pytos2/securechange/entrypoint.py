from datetime import date, datetime
from typing import Union, Optional, Iterable, Iterator, List
from enum import Enum

from pytos2.models import DateFilterType, coerce_date_filter_type
from traversify import Traverser
from pathlib import Path

# avoid circular imports
import pytos2
from .api import ScwAPI
from requests import Response
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
    Timeout,
    JSONDecodeError,
)
from pytos2.securechange.workflow import BasicWorkflowInfo, WorkflowType, FullWorkflow
from pytos2.securechange.user import (
    classify_user_object,
    SCWParty,
    SCWUser,
    SCWGroup,
    UserRole,
    Permission,
    LDAPParty,
    LDAPSimulateLogin,
    LDAPUserSimulateLogin,
    NewLocalUser,
    UserUpdateRole,
    OriginType,
)

from pytos2.securechange.device import DeviceExclusions
from pytos2.securechange.workflow_triggers import WorkflowTrigger
from pytos2.securechange.extension import MarketplaceApp
from pytos2.securechange.saved_search import Query, FreeTextQuery, DetailedQuery
from pytos2.securechange.domain import Domain
from pytos2.securechange.ticket_requests import (
    RequestsSearchList,
    RequestSearch,
    TicketRequestSearch,
    TicketDraftRequestSearch,
)

from pytos2.utils import NoInstance, get_api_node
from pytos2.utils.cache import Cache, CacheIndex
from pytos2.api import Pager


class Scw:
    default: Union["Scw", NoInstance] = NoInstance(
        "Scw.default",
        "No Scw instance has been initialized yet, initialize with `Scw(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
    ):
        self.api: ScwAPI = ScwAPI(hostname, username, password)
        if default:
            Scw.default = self

        self.user_cache = Cache()
        self.users_by_name = self.user_cache.make_index("name")
        self.users_by_id = self.user_cache.make_index("id")

    def ticket_search(
        self,
        subject: Optional[str] = None,
        requester: Optional[str] = None,
        group: Optional[str] = None,
        assigned_to: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[Union[str, "pytos2.securechange.ticket.TicketStatus"]] = None,
        sla_status: Optional[
            Union[str, "pytos2.securechange.ticket.Ticket.SlaStatus"]
        ] = None,
        field_name: Optional[str] = None,
        field_value: Optional[str] = None,
        current_step: Optional[str] = None,
        expiration_date_from: Optional[str] = None,
        expiration_date_to: Optional[str] = None,
        domain_name: Optional[str] = None,
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        """
        Retrieve a list of TicketSearchResult objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/search
        Version: R22-2+

        Usage:
            # Example #1:
            search_results = scw.ticket_search(subject='"Auto Recert Ticket"')

            # Example #2:
            search_results = scw.ticket_search(requester='ateam', assigned_to='api_user')
        """
        from pytos2.securechange.ticket import TicketSearchResult

        # It's clearer to write out the params explicitly than to use locals()
        params = {
            "subject": subject,
            "requester": requester,
            "group": group,
            "assigned_to": assigned_to,
            "priority": priority,
            "status": status,
            "sla_status": sla_status,
            "field_name": field_name,
            "field_value": field_value,
            "current_step": current_step,
            "expiration_date_from": expiration_date_from,
            "expiration_date_to": expiration_date_to,
            "domain_name": domain_name,
        }

        for k, param in params.items():
            if isinstance(param, Enum):
                params[k] = param.value

        r = self.api.session.get("tickets/search", params=params)
        if not r.ok:
            r.raise_for_status()
        else:
            tickets = get_api_node(
                r.json(), "tickets_search_results.ticket_result", listify=True
            )
            return [TicketSearchResult.kwargify(t) for t in tickets]

    def ticket_search_by_details(
        self,
        subject: Optional[str] = None,
        requester: Optional[str] = None,
        group: Optional[str] = None,
        assigned_to: Optional[str] = None,
        priority: Optional[str] = None,
        task_status: Optional[
            Union[str, "pytos2.securechange.ticket.Task.Status"]
        ] = None,
        status: Optional[Union[str, "pytos2.securechange.ticket.TicketStatus"]] = None,
        sla_status: Optional[
            Union[str, "pytos2.securechange.ticket.Ticket.SlaStatus"]
        ] = None,
        sla_outcome: Optional[
            Union[str, "pytos2.securechange.ticket.SlaOutcome"]
        ] = None,
        field_name: Optional[str] = None,
        field_value: Optional[str] = None,
        current_step: Optional[str] = None,
        expiration_date_from: Optional[str] = None,
        expiration_date_to: Optional[str] = None,
        domain_name: Optional[str] = None,
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        """
        Retrieve a list of TicketSearchResult objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/search_by/details
        Version: R23-1+

        Usage:
            # Example #1:
            search_results = scw.ticket_search_by_details(subject='"Auto Recert Ticket"')

            # Example #2:
            search_results = scw.ticket_search_by_details(requester='ateam', assigned_to='api_user')
        """

        from pytos2.securechange.ticket import TicketSearchResult

        # It's clearer to write out the params explicitly than to use locals()
        params = {
            "subject": subject,
            "requester": requester,
            "group": group,
            "assigned_to": assigned_to,
            "priority": priority,
            "task_status": task_status,
            "status": status,
            "sla_status": sla_status,
            "sla_outcome": sla_outcome,
            "field_name": field_name,
            "field_value": field_value,
            "current_step": current_step,
            "expiration_date_from": expiration_date_from,
            "expiration_date_to": expiration_date_to,
            "domain_name": domain_name,
        }

        for k, param in params.items():
            if isinstance(param, Enum):
                params[k] = param.value

        r = self.api.session.get("tickets/search_by/details", params=params)
        r_json = self.api.handle_json(r, "ticket_search_by_details", action="get")
        tickets = get_api_node(
            r_json, "tickets_search_results.ticket_result", listify=True
        )

        return [TicketSearchResult.kwargify(t) for t in tickets]

    def ticket_search_by_saved_search(
        self, saved_search_id: Union[int, Query]
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        """
        Retrieve a list of TicketSearchResult objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/search_by/query
        Version: R23-1+

        Usage:
            # Example #1:
            search_results = scw.ticket_search_by_saved_search(saved_search_id=15)
        """
        from pytos2.securechange.ticket import TicketSearchResult

        if isinstance(saved_search_id, Query):
            saved_search_id = saved_search_id.id
        if not isinstance(saved_search_id, int):
            raise TypeError("saved_search_id must be an int")

        params = {
            "query_id": saved_search_id,
        }

        r = self.api.session.get("tickets/search_by/query", params=params)
        r_json = self.api.handle_json(r, "ticket_search_by_query", action="get")
        tickets = get_api_node(
            r_json, "tickets_search_results.ticket_result", listify=True
        )

        return [TicketSearchResult.kwargify(t) for t in tickets]

    def ticket_search_by_group(
        self, group_id: int
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        """
        Retrieve a list of TicketSearchResult objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/search_by/group
        Version: R23-1+

        Usage:
            # Example #1:
            search_results = scw.ticket_search_by_group(group_id=9)
        """
        from pytos2.securechange.ticket import TicketSearchResult

        params = {
            "group_id": group_id,
        }

        r = self.api.session.get("tickets/search_by/group", params=params)
        r_json = self.api.handle_json(r, "ticket_search_by_free_text", action="get")
        tickets = get_api_node(
            r_json, "tickets_search_results.ticket_result", listify=True
        )

        return [TicketSearchResult.kwargify(t) for t in tickets]

    def ticket_search_by_free_text(
        self, parameter: str
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        """
        Retrieve a list of TicketSearchResult objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/search_by/free_text
        Version: R23-1+

        Usage:
            # Example #1:
            search_results = scw.ticket_search_by_free_text(parameter = "taskstatus:ASSIGNED")

        Parameter reference URL: https://forum.tufin.com/support/kc/R24-2/Content/Suite/2331.htm
        """
        from pytos2.securechange.ticket import TicketSearchResult

        params = {
            "parameter": parameter,
        }

        r = self.api.session.get("tickets/search_by/free_text", params=params)
        r_json = self.api.handle_json(r, "ticket_search_by_free_text", action="get")
        tickets = get_api_node(
            r_json, "tickets_search_results.ticket_result", listify=True
        )

        return [TicketSearchResult.kwargify(t) for t in tickets]

    def get_users(
        self,
        show_indirect_relation: Optional[bool] = None,
        user_name: Optional[str] = None,
        email: Optional[str] = None,
        exact_name: Optional[bool] = None,
    ) -> List[SCWParty]:
        """
        Retrieve a list of SCWParty objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/users
        Version: R22-2+

        Usage:
            # Example #1:
            users = scw.get_users(user_name='ateam')

            # Example #2:
            users = scw.get_users(email='ateam@tufin.com')
        """
        params = {}
        if show_indirect_relation:
            params["showIndirectRelation"] = show_indirect_relation
        if user_name:
            params["user_name"] = user_name
        if email:
            params["email"] = email
        if exact_name:
            params["exact_name"] = exact_name

        response = self.api.session.get("users", params=params)
        if not response.ok:
            response.raise_for_status()
        else:
            _json = response.json()
            users_node = get_api_node(_json, "users.user", listify=True)

            users = []
            self.user_cache.clear()

            for obj in users_node:
                user = classify_user_object(obj)
                users.append(user)

            self.user_cache.set_data(users)
            return users

    def _get_user_from_server(self, identifier: int) -> SCWParty:
        """
        Retrieve a SCWParty object for the given id

        Method: GET
        URL: /securechangeworkflow/api/securechange/users/{id:[0-9]+}
        Version: 22-2+

        Usage:
            user = st._get_user_from_server(5)
        """
        response = self.api.session.get(f"users/{identifier}")

        # if not response.ok:
        response.raise_for_status()
        # else:
        _json = response.json()

        key = ""
        if "group" in _json:
            key = "group"
        elif "user" in _json:
            key = "user"
        else:
            raise KeyError(
                f"Root user class key {_json.keys()} not currently supported by pytos2"
            )

        user_json = _json[key]
        if isinstance(user_json, list):
            user_json = user_json[0]
        return classify_user_object(user_json, obj_type=key)

    def get_user(
        self,
        identifier: Union[str, int],
        expand: bool = False,
        update_cache: Optional[bool] = None,
    ) -> SCWParty:
        """
        Retrieve a SCWParty object for the given id, optionally caching or inclusion of @xsi.type

        Method: GET
        URL: /securechangeworkflow/api/securechange/users (if update_cache is not False)
        URL: /securechangeworkflow/api/securechange/users/{id:[0-9]+} (for including @xsi.type)
        Version: 22-2+

        Usage:
            # Example #1:
            user = scw.get_user(5)

            # Example #2:
            user = scw.get_user(5, expand=True)
        """
        if update_cache is not False and self.user_cache.is_empty():
            _ = self.get_users()  # create or update cache

        if isinstance(identifier, str):
            user = self.users_by_name.get(identifier)
            if not user:
                _ = self.get_users()
                user = self.users_by_name.get(identifier)
                if not user:
                    raise ValueError(f"User with name {identifier} not found")

            if expand:
                # this API only give @xsi.type as additional info
                return self._get_user_from_server(user.id)
            else:
                return user
        else:
            user = self.users_by_id.get(identifier)
            if not user:
                _ = self.get_users()
                user = self.users_by_id.get(identifier)
            if not user:
                raise ValueError(f"User with id {identifier} not found")

            if expand:
                try:
                    return self._get_user_from_server(identifier)
                except HTTPError as e:
                    # wrap the HTTPError into ValueError for consisency
                    raise ValueError(f"User with id {identifier} not found got {e}")
            else:
                return user

    def add_user_group(self, name: str, description: str, email: str) -> SCWGroup:
        """
        Method: POST
        URL: /securechangeworkflow/api/securechange/users/group
        Version: R22-1+

        Usage:
            scw.add_user_group("Group1", "Test Group 1", "group1@contoso.com")
        """
        post_data = {
            "group": {"name": name, "description": description, "email": email}
        }
        response = self.api.session.post("users/group", json=post_data)
        return self.api.handle_creation(response, "add_user_group", cls=SCWGroup)

    def update_user_group(
        self,
        group_id: int,
        member_ids_to_add: Optional[List[int]] = None,
        member_ids_to_remove: Optional[List[int]] = None,
    ) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/users/group/{id:[0-9]+}
        Version: R22-1+

        Usage:
            scw.update_user_group(54, ["70","96"], ["85","49"])
        """
        put_data = {
            "group_change": {
                "member_ids_to_add": member_ids_to_add,
                "member_ids_to_remove": member_ids_to_remove,
            }
        }
        response = self.api.session.put(f"users/group/{group_id}", json=put_data)
        self.api.handle_response(response, "update_user_group", "update")

    def delete_user_or_group(self, identifier: int) -> None:
        """
        URL: /securechangeworkflow/api/securechange/users/{id:[0-9]+}
        Version: R22-1+
        Notes:
            Delete a single user or group from SecureChange Users

        Usage:
            scw.delete_user_or_group(70)
        """
        response = self.api.session.delete(f"users/{identifier}")
        self.api.handle_response(response, "delete_user_or_group", "delete")

    def user_import_ldap(self, ldap: LDAPParty) -> None:
        """
        URL: /securechangeworkflow/api/securechange/users/import
        Version: R22-1+
        Notes:
            Import a single user or group using the LDAP already configured in SecureChange

        Usage:
            ldap = LDAPParty()
            ldap.ldap_configuration_name = "Contoso LDAP" #The name you have configured in the UI under SecureChange LDAP
            ldap.ldap_dn = "CN=abaker,OU=Users,DC=tcse,DC=net"
            scw.user_import_ldap(ldap)
        """
        post_data = {"ldap_party": ldap._json}
        response = self.api.session.post("users/import", json=post_data)
        self.api.handle_response(response, "user_import_ldap", "create/import")

    def user_login(self, user: LDAPUserSimulateLogin):
        """
        This API implicitly imports LDAP users as automatics users to SecureChange by simulating their login.
        To explicitly import LDAP entities, both users and groups, it is recommended to use /users/import API

        URL: /securechangeworkflow/api/securechange/users
        Version: R22-1+
        Notes:
            ldap_configuration is optional and if not supplied, the default ldap config will be used automatically

        Usage:
            user = LDAPUserSimulateLogin()
            user.name = 'abaker'
            ldap_config = LDAPConfiguration()
            ldap_config.name = "Contoso LDAP"
            ldap_config.id = 1
            user.ldap_configuration = ldap_config
            scw.user_login(user)

        """
        if not isinstance(user, LDAPUserSimulateLogin):
            raise TypeError("user argument must be of type LDAPUserSimulateLogin")

        post_data = {"user": user._json}
        response = self.api.session.post("users", json=post_data)
        self.api.handle_response(response, "user_login", "create")

    def add_user(self, new_user: NewLocalUser):
        """
        URL: /securechangeworkflow/api/securechange/users
        Version: R22-1+

        Usage:
            new_user = NewLocalUser()
            new_user.name = 'abaker'
            new_user.first_name = "Aaron"
            new_user.last_name = "Baker"
            new_user.email = "aaron.baker@contoso.com"
            new_user.password = "password"
            new_user.notes = "asdf"
            new_user.default_authentication = False
            scw.user_create(new_user)

        """
        post_data = {"localuser": new_user._json}
        response = self.api.session.post("users", json=post_data)
        return self.api.handle_creation(response, "add_user", cls=SCWUser)

    def group_login(self, group: LDAPSimulateLogin):
        """
        This API implicitly imports LDAP users as automatics users to SecureChange by simulating their login.
        To explicitly import LDAP entities- both users and groups, it is recommended to use /users/import API

        URL: /securechangeworkflow/api/securechange/users
        Version: R22-1+
        Notes:
            ldap_configuration is optional and if not supplied, the default ldap config will be used automatically

        Usage:
            group = LDAPSimulateLogin()
            group.name = 'Accountants'
            ldap_config = LDAPConfiguration()
            ldap_config.name = "Contoso LDAP"
            ldap_config.id = 1
            group.ldap_configuration = ldap_config
            scw.group_login(group)

        """
        if not isinstance(group, LDAPSimulateLogin):
            raise TypeError("group argument must be of type LDAPSimulateLogin")

        post_data = {"group": group._json}
        response = self.api.session.post("users", json=post_data)
        self.api.handle_response(response, "group_login", "import")

    def get_excluded_device_ids(self, show_all: Optional[bool] = None) -> List[int]:
        """
        Retrieve a List of ints that make up the list of excluded device ids

        Method: GET
        URL: /securechangeworkflow/api/securechange/devices/excluded
        URL: /securechangeworkflow/api/securechange/devices/excluded?show_all=true
        Version: 22-2+

        Usage:
            # Example #1:
            excluded_device_ids = scw.get_excluded_device_ids()

            # Example #2:
            excluded_device_ids = scw.get_excluded_device_ids(show_all=True)
        """
        url = "devices/excluded"
        if isinstance(show_all, bool):
            url += "?show_all="
            show_all = str(show_all).lower()
            url += show_all

        r = self.api.session.get(url)
        if r.ok:
            excludes_json = r.json()
            device_ids_model = DeviceExclusions.kwargify(excludes_json)
            return device_ids_model.device_ids
        else:
            r.raise_for_status()

    def get_tickets(
        self,
        status: Optional[
            Union[
                "pytos2.securechange.ticket.TicketStatus",
                List["pytos2.securechange.ticket.TicketStatus"],
            ]
        ] = None,
        start: Optional[int] = None,
        descending: Optional[bool] = None,
        expand_links: Optional[bool] = None,
    ) -> List["pytos2.securechange.ticket.TicketIterator"]:
        """
        Retrieve a list of TicketIterator objects for the given optional search arguments

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets
        Version: R22-2+

        Usage:
            # Example #1:
            ticket_iterators = scw.get_tickets()

            # Example #2:
            ticket_iterators = scw.get_users(descending=True)
        """
        from pytos2.securechange.ticket import TicketStatus, TicketIterator

        params = {}

        if status is not None:
            if isinstance(status, list):
                params["status"] = ",".join([s.value for s in status])
            else:
                params["status"] = status.value
        if start is not None:
            params["start"] = start
        if descending is not None:
            params["desc"] = "true" if descending else "false"
        if expand_links is not None:
            params["expand_links"] = "true" if expand_links else "false"

        return list(TicketIterator(self.api.session, params))

    def get_ticket(self, _id: int) -> "pytos2.securechange.ticket.Ticket":
        """
        Retrieve a Ticket object for the given id

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}
        Version: 22-2+

        Usage:
            ticket = scw.get_ticket(5)
        """
        from pytos2.securechange.ticket import Ticket

        r = self.api.session.get(f"tickets/{_id}")
        if r.ok:
            tkt = Ticket.kwargify(r.json())
            return tkt
        else:
            r.raise_for_status()

    def change_requester(
        self,
        ticket: Union[int, "pytos2.securechange.ticket.Ticket"],
        user: Union[str, int, SCWParty],
        comment="",
    ) -> None:
        """
        Change ticket requester.

        Method: PUT
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/change_requester/{assigneeId:[0-9]+}
        Version: 22-2+

        Usage:
            # Example #1:
            ticket = scw.get_ticket(1)
            user = scw.get_user(5)
            scw.change_requester(ticket, user, 'change requester')

            # Example #2:
            scw.change_requester(1, 5, 'change requester')
        """
        from pytos2.securechange.ticket import Ticket

        if not isinstance(ticket, Ticket):
            ticket = self.get_ticket(ticket)
        if not isinstance(user, SCWUser):
            user = self.get_user(user)

        if isinstance(user, SCWGroup):
            raise ValueError(
                "Error changing requester: Groups not allowed as requesters"
            )

        try:
            url = f"tickets/{ticket.id}/change_requester/{user.id}"
            put_body = {"comment": {"comment": comment if comment else "comment"}}
            response = self.api.session.put(url, json=put_body)
            response.raise_for_status()
        except RequestException as e:
            raise ValueError(f"Error changing requester: {e.response.text}")

    def reassign_ticket(
        self,
        ticket,
        user,
        step: Union[None, "pytos2.securechange.ticket.Step", int, str] = None,
        task: Union[None, "pytos2.securechange.ticket.Task", int] = None,
        comment="",
    ) -> None:
        """
        Reassign a ticket task to the given user, the task defaulting to the last task of the current step.
        Optionally a speficied step or task can be passed as an argument.

        Method: PUT
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/steps/{stepId:[0-9]+}/tasks/{taskId:[0-9]+}/reassign/{assigneeId:[0-9]+}
        Payload:
            {
                "reassign_task_comment": {
                    "comment": comment
                }
            }
        Version: 22-2+

        Usage:
            scw.reassign_ticket(ticket, user)
        """
        from pytos2.securechange.ticket import Step, Task, Ticket

        if not isinstance(ticket, Ticket):
            ticket = self.get_ticket(ticket)

        if not isinstance(user, SCWUser):
            user = Scw.default.get_user(user)

        if step is None:
            step = ticket.current_step

        if not isinstance(step, Step):
            step = ticket.get_step(step)

        if task is None:
            task = step.get_task(0)

        if not isinstance(task, Task):
            task = step.get_task(task)

        try:
            response = self.api.session.put(
                f"tickets/{ticket.id}/steps/{step.id}/tasks/{task.id}/reassign/{user.id}",
                json={"reassign_task_comment": {"comment": comment}},
            )
            if not response.ok:
                msg = response.json().get("result").get("message")
                response.raise_for_status()
        except HTTPError as e:
            raise ValueError(
                f"Got {e}, with Error Message: {msg}. Only tasks under current step can be reassigned"
            )

    def get_attachment(self, file_id: str) -> bytes:
        """
        Retrieve an attachment file's contents (bytes) for the given file_id

        Method: GET
        URL: /securechangeworkflow/api/securechange/attachments/{uid}
        Version: 22-2+

        Usage:
            file_contents = scw.get_attachment('d95d574f-49c0-4c91-b08f-b243735a7501')
        """
        response = self.api.session.get(f"attachments/{file_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Attachment: {e}")
        return response.content

    def add_attachment(self, file: str) -> str:
        """
        Post the contents of the file with the given filename as an attachment

        Method: POST
        URL: /securechangeworkflow/api/securechange/attachments
        Version: 22-2+

        Usage:
            scw.add_attachment('/conf/attachment_file.csv')
        """
        attachment = {"attachment": open(file, "rb")}
        response = self.api.session.post("attachments", files=attachment)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Attachment: {e}")
        return response.text

    def add_comment(
        self,
        ticket_id: Union[int, str],
        step_id: Union[int, str],
        task_id: Union[int, str],
        comment_content: str,
        attachment_uuids: Optional[List[str]],
    ) -> str:
        """
        Post the the given comment_contents and, optionally, file attachments specified by attachment_uuids
        as an attachment to the given ticket, step and task.

        Method: POST
        URL: /securechangeworkflow/api/securechange/attachments
        Version: 22-2+

        Usage:
            # Example #1:
            scw.add_comment(100, 200, 201, 'Thie is a comment')

            # Example #2:
            scw.add_comment(
                100, 200, 201, 'Thie is a comment with an attachment', ['d95d574f-49c0-4c91-b08f-b243735a7501']
            )
        """

        def _format_attachments(uuids: List[str]) -> dict:
            return {"attachment": [{"uid": id} for id in uuids]}

        comment = {"comment": {"content": comment_content}}
        if attachment_uuids:
            comment["comment"]["attachments"] = _format_attachments(attachment_uuids)

        response = self.api.session.post(
            f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/comments",
            json=comment,
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Comment: {e}")

        return response.text

    def delete_comment(
        self,
        ticket_id: Union[int, str],
        comment_id: Union[int, str],
    ) -> None:
        """
        Delete the ticket comment for the given ticket_id, comment_id

        Method: DELETE
        URL: /securechangeworkflow/api/securechange/tickets/{ticketId:[0-9]+}/comments/{commentId:[0-9]+}
        Version: 22-2+

        Usage:
            scw.delete_comment(100, 1)
        """
        response = self.api.session.delete(
            f"tickets/{ticket_id}/comments/{comment_id}",
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Comment: {e}")

    def get_ticket_history(
        self, _id: int
    ) -> "pytos2.securechange.ticket.TicketHistory":
        """
        Retrieve a TicketHistory object for the given ticket id

        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/history
        Version: 22-2+

        Usage:
            # Example #1:
            ticket_history = scw.get_ticket_history(5)

            # Example #2:
            ticket = scw.get_ticket(5)
            ticket_history = ticket.get_history()
        """
        from pytos2.securechange.ticket import TicketHistory

        try:
            response = self.api.session.get(f"tickets/{_id}/history")
            response.raise_for_status()
            response_json = response.json()
            ticket_history = TicketHistory.kwargify(
                response_json["ticket_history_activities"]
            )
            return ticket_history
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except ValueError as e:
            raise ValueError(f"Error creating ticket_history class: {e}")
        except RequestException as e:
            raise ValueError(f"Error retrieving ticket_history: {e}")

    def get_triggers(self) -> List[WorkflowTrigger]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/triggers
        Version: R22-2+

        Usage:
            triggers = scw.get_triggers()

        """
        try:
            url = "triggers"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            api_nodes = get_api_node(
                response_json, "workflow_triggers.workflow_trigger", listify=True
            )
            return [WorkflowTrigger.kwargify(trigger) for trigger in api_nodes]
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except ValueError as e:
            raise ValueError(f"Error creating triggers class: {e}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving triggers: {e}") from e

    def get_trigger(
        self, name: Optional[str] = None, id: Optional[int] = None
    ) -> WorkflowTrigger:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/triggers
        Version: R22-2+

        Usage:
            # Example #1:
            trigger = scw.get_trigger(name='trigger name')

           # Example #2:
            trigger = scw.get_trigger(id=1000)
        """
        if (name and id) or not (name or id):
            raise ValueError("Either name or id (but not both) must be supplied")
        query = f"name={name}" if name else f"id={id}"

        try:
            url = f"triggers?{query}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            api_nodes = get_api_node(
                response_json, "workflow_triggers.workflow_trigger", listify=True
            )
            return WorkflowTrigger.kwargify(api_nodes[0])
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except ValueError as e:
            raise ValueError(f"Error creating triggers class: {e}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving trigger: {e.response.text}") from e

    def add_trigger(self, workflow_trigger: WorkflowTrigger) -> None:
        """
        Method: POST
        URL: /securechangeworkflow/api/securechange/triggers
        Version: R22-2+

        Usage:
            script = Script(path='test-solution/test-solution', arguments='')
            workflow = Workflow(name='test workflow', parent_workflow_id=1)
            trigger = Trigger(name='test trigger', workflow=workflow, events=['CREATE', 'ADVANCE'])
            workflow_trigger = WorkflowTrigger(name='test', script=script, triggers=[trigger])
            scw.add_trigger(workflow_trigger)
        """
        try:
            url = "triggers"
            json_data = {
                "workflow_triggers": {"workflow_trigger": [workflow_trigger._json]}
            }
            response = self.api.session.post(url, json=json_data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error posting trigger: {e.response.text}") from e
        except RequestException as e:
            raise ValueError("Error posting trigger") from e

    def get_ticket_events(
        self,
        type: Optional[str] = None,
        assignee_name: Optional[int] = None,
        assignee_id: Optional[int] = None,
        participant_name: Optional[str] = None,
        participant_id: Optional[int] = None,
        ticket_id: Optional[int] = None,
        workflow_name: Optional[str] = None,
        parent_workflow_id: Optional[int] = None,
        step_name: Optional[str] = None,
        step_id: Optional[int] = None,
        date_from: DateFilterType = None,
        date_to: DateFilterType = None,
    ) -> Iterable["pytos2.securechange.ticket.TicketEvent"]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/lifecycle_events
        Version: R24-1+

        Usage:
            # Example #1:
            ticket_events = scw.get_ticket_events()

            # Example #2:
            ticket_events = scw.get_ticket_events(ticket_id=1031)
        """
        from pytos2.securechange.ticket import TicketEvent

        url = "tickets/lifecycle_events"
        params = {}
        if type:
            params["type"] = type
        if assignee_name:
            params["assignee_name"] = assignee_name
        if assignee_id:
            params["assignee_id"] = assignee_id
        if participant_name:
            params["participant_name"] = participant_name
        if participant_id:
            params["participant_id"] = participant_id
        if ticket_id:
            params["ticket_id"] = ticket_id
        if workflow_name:
            params["workflow_name"] = workflow_name
        if parent_workflow_id:
            params["parent_workflow_id"] = parent_workflow_id
        if step_name:
            params["step_name"] = step_name
        if step_id:
            params["step_id"] = step_id
        if date_from:
            params["date_from"] = coerce_date_filter_type(date_from)
        if date_to:
            params["date_to"] = coerce_date_filter_type(date_to)
        api_node = "ticket_events.ticket_event"
        pager = Pager(
            self.api,
            url,
            api_node,
            "get_ticket_events",
            TicketEvent.kwargify,
            params=params,
        )
        return pager

    def backfill_ticket_events(self, from_date: str) -> None:
        """
        Method: POST
        URL: /securechangeworkflow/api/securechange/tickets/lifecycle_events/historical_events
        Version: R24-1+

        Usage:
            scw.backfill_ticket_events("2023-11-05")
        """
        try:
            url = "tickets/lifecycle_events/historical_events"
            json_data = {"ticket_events_create_history_request": {"from": from_date}}
            response = self.api.session.post(url, json=json_data)
            response.raise_for_status()
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(f"Error retrieving ticket_historical_events_status: {e}")

    def get_ticket_historical_events_status(self) -> str:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/tickets/lifecycle_events/historical_events_status
        Version: R24-1+

        Usage:
            historical_events_status = scw.get_ticket_historical_events_status()
        """
        try:
            url = "tickets/lifecycle_events/historical_events_status"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            return response_json["ticket_events_created_history_status"]["run_status"]
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(f"Error retrieving ticket_historical_events_status: {e}")

    def map_rules(self, ticket_id: int, handler_id: int = None) -> None:
        """
        Method: POST
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/map_rules

        Version: R24-1+

        Usage:
            # Example:
            scw.map_rules(1037)
        """
        try:
            url = f"tickets/{ticket_id}/map_rules"
            if handler_id:
                url += f"?handler_id={handler_id}"
            response = self.api.session.post(url)
            response.raise_for_status()
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error running map_rules: {e} response: {e.response.text}"
            )

    def designer_redesign(
        self, ticket_id: int, step_id: int, task_id: int, field_id: int
    ) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/steps/{stepId:[0-9]+}/tasks/{taskId:[0-9]+}/fields/{fieldId:[0-9]+}/designer/redesign

        Version: R24-1+

        Usage:
            # Example:
            scw.designer_redesign(1037, 5689, 5705, 61671)
        """
        try:
            url = f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/fields/{field_id}/designer/redesign"
            response = self.api.session.put(url)
            response.raise_for_status()
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error running designer redesign: {e} response: {e.response.text}"
            )

    def designer_device_commit(
        self, ticket_id: int, step_id: int, task_id: int, field_id: int, device_id: int
    ) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/steps/{stepId:[0-9]+}/tasks/{taskId:[0-9]+}/fields/{fieldId:[0-9]+}/designer/device/{deviceId:[0-9]+}/commit

        Version: R24-1+

        Usage:
            # Example:
            scw.designer_device_commit(1037, 5689, 5705, 61671, 8)
        """
        try:
            url = f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/fields/{field_id}/designer/device/{device_id}/commit"
            response = self.api.session.put(url)
            response.raise_for_status()
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error running designer device commit: {e} response: {e.response.text}"
            )

    def designer_device_update(
        self,
        ticket_id: int,
        step_id: int,
        task_id: int,
        field_id: int,
        device_id: int,
        force: Optional[bool] = False,
    ) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/tickets/{id:[0-9]+}/steps/{stepId:[0-9]+}/tasks/{taskId:[0-9]+}/fields/{fieldId:[0-9]+}/designer/device/{deviceId:[0-9]+}/update

        Version: R24-1+

        Usage:
            # Example #1:
            scw.designer_device_update(1037, 5689, 5705, 61671, 8)

            # Example #2:
            scw.designer_device_update(1037, 5689, 5705, 61671, 8, True)
        """
        try:
            url = f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/fields/{field_id}/designer/device/{device_id}/update"
            if force:
                url += "?force=true"
            response = self.api.session.put(url)
            response.raise_for_status()
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error running designer device update: {e} response: {e.response.text}"
            )

    def get_workflows(
        self, workflow_type: Optional[WorkflowType] = None
    ) -> List[BasicWorkflowInfo]:
        """
        URL: /securechangeworkflow/api/securechange/workflows/active_workflows
        URL: /securechangeworkflow/api/securechange/workflows/active_workflows?type=ACCESS_REQUEST
        Version: R21-3+

        Usage:
            workflows = scw.get_workflows()
            workflows = scw.get_workflows(WorkflowType.ACCESS_REQUEST)

        """

        try:
            url = (
                f"workflows/active_workflows?type={workflow_type.value}"
                if workflow_type
                else "workflows/active_workflows"
            )
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            return [
                BasicWorkflowInfo.kwargify(wf)
                for wf in get_api_node(
                    response_json, "workflows.workflow", listify=True
                )
            ]
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving workflows: {e}") from e

    def get_workflow(
        self,
        workflow_id: Optional[Union[int, str]] = None,
        workflow_name: Optional[str] = None,
    ) -> FullWorkflow:
        """
        This function returns a FullWorkflow object or a sub-type of it. If something you need is
        not mapped in FullWorkflow, you may use the `data' attribute to access it.

        URL: /securechangeworkflow/api/securechange/workflows?id=588
        URL: /securechangeworkflow/api/securechange/workflows?name=Contoso%20Workflow
        Version:

        Usage:
            workflow = scw.get_workflow(588)
            workflow = scw.get_workflow(workflow_name="Contoso Workflow")

        """
        try:
            url = (
                f"workflows?id={workflow_id}"
                if workflow_id
                else f"workflows?name={workflow_name}"
            )
            response = self.api.session.get(url)
            response.raise_for_status()
            # Returning raw dictionary because we do not yet have models for the entire workflow
            # This is because the name of the first key varies depending on the workflow type
            workflow_data = response.json()
            return FullWorkflow.kwargify(workflow_data)

            # workflow_data = response_json[list(response_json.keys())[0]]
            # return BasicWorkflowInfo.kwargify(workflow_data)
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving workflow by name or id: {e}") from e

    def get_extensions(self) -> List[MarketplaceApp]:
        """
        URL: /securechangeworkflow/api/securechange/extensions
        Version: R23-2+

        Usage:
            apps = scw.get_extensions()

        """

        try:
            response = self.api.session.get("extensions")
            response.raise_for_status()
            response_json = response.json()
            return [
                MarketplaceApp.kwargify(ext)
                for ext in get_api_node(response_json, "extensions")
            ]
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving extensions/marketplaceapps: {e}") from e

    def get_roles(self) -> List[UserRole]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/roles
        Version: R22-2+

        Usage:
            roles = scw.get_roles()

        """
        response = self.api.session.get("roles")
        json = self.api.handle_json(response, "get_roles", "get")
        return [
            UserRole.kwargify(role)
            for role in get_api_node(json, "roles.role", listify=True)
        ]

    def get_role(self, id: Union[int, str]) -> UserRole:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/roles/{id:[0-9]+}
        Version: R22-2+

        Usage:
            role = scw.get_role(8)

        """
        response = self.api.session.get(f"roles/{id}")
        json = self.api.handle_json(response, "get_role", "get")
        return UserRole.kwargify(json["role"])

    def update_user_roles(self, user_id: int, roles_list: List[UserUpdateRole]):
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/users/{id:[0-9]+}/roles
        Version: R21-3+
        Notes:
            Clears existing roles and updates with the new list, except Requestor role will always be present
            User get_user to see what Roles the user is assigned

        Usage:
            roles = []
            roles.append(UserUpdateRole(name="Auditor"))
            sc.user_update_roles(70, roles)

        """
        json_roles = [user_role._json for user_role in roles_list]
        post_data = {"roles": {"role": json_roles}}
        response = self.api.session.put(f"users/{user_id}/roles", json=post_data)
        self.api.handle_response(response, "user_update_roles", "update")

    def get_saved_searches(self) -> List[Query]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/queries
        Version: R24-1+

        Usage:
            # Example #1:
            queries = scw.get_saved_searches()
        """

        try:
            url = "queries"

            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()

            queries = [
                Query.kwargify(query)
                for query in get_api_node(response_json, "queries.query", listify=True)
            ]

            return queries

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error retrieving queries: {e} response: {e.response.text}"
            )

    def get_saved_search(self, id: int) -> List[Query]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/queries/{id:[0-9]+}
        Version: R24-1+

        Usage:
            # Example #1:
            queries = scw.get_saved_search(id=14)
        """

        try:
            url = f"queries/{id}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            queries = []

            if response_json["query"]["type"] == "DETAILED":
                queries = [
                    DetailedQuery.kwargify(query)
                    for query in get_api_node(response_json, "query", listify=True)
                ]

            if response_json["query"]["type"] == "FREE_TEXT":
                queries = [
                    FreeTextQuery.kwargify(query)
                    for query in get_api_node(response_json, "query", listify=True)
                ]

            return queries

        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(
                f"Error retrieving queries: {e} response: {e.response.text}"
            )

    def add_saved_search(self, query: Query) -> None:
        """
        Method: POST
        URL: /securechangeworkflow/api/securechange/queries
        Version: R24-1+

        Usage:
            # Example #1:
            queries = scw.add_saved_search(query)
        """
        try:
            url = "queries/"
            response = self.api.session.post(url, json=query)
            response.raise_for_status()
            return response.status_code
        except (HTTPError, ConnectionError, Timeout) as e:
            raise ValueError(f"Error deleting query: {e} response: {e.response.text}")
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving saved searches: {e}") from e

    def update_saved_search(self, id, query: Query) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/queries/{id}
        Version: R24-1+

        Usage:
            # Example #1:
            queries = scw.update_saved_search(id, query)
        """
        try:
            url = "queries/" + str(id)
            response = self.api.session.put(url, json=query)
            response.raise_for_status()
            return response.status_code
        except (HTTPError, ConnectionError, Timeout) as e:
            raise ValueError(f"Error deleting query: {e} response: {e.response.text}")
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving saved searches: {e}") from e

    def delete_saved_search(self, id) -> None:
        """
        Method: DELETE
        URL: /securechangeworkflow/api/securechange/queries/{id}
        Version: R24-1+

        Usage:
            # Example #1:
            queries = scw.delete_saved_search(id)
        """
        try:
            url = "queries/" + str(id)
            response = self.api.session.delete(url)
            response.raise_for_status()
            return response.status_code
        except (HTTPError, ConnectionError, Timeout) as e:
            raise ValueError(f"Error deleting query: {e} response: {e.response.text}")
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving saved searches: {e}") from e

    def get_domains(self) -> List[Domain]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/domains
        Version: R21-1+

        Usage:
            domains = scw.get_domains()

        """
        response = self.api.session.get("domains")
        json = self.api.handle_json(response, "get_domains", "get")
        return [
            Domain.kwargify(domain)
            for domain in get_api_node(json, "domains.domain", listify=True)
        ]

    def get_domain(self, _id: Union[int, str]) -> Domain:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/domains/{domainId:[0-9]+}
        Version: R21-1+

        Usage:
            domain = scw.get_domain(1)

        """
        response = self.api.session.get(f"domains/{_id}")
        json = self.api.handle_json(response, "get_domain", "get")
        return Domain.kwargify(get_api_node(json, "domain"))

    def synchronize_domains(self):
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/domains/synchronize
        Version: R21-1+

        Usage:
            scw.synchronize_domains()

        """
        response = self.api.session.put("domains/synchronize")
        self.api.handle_response(response, "synchronize_domains", "update")

    def get_requests(
        self,
        view: str,
        group_id: Optional[int] = None,
        request_id: Optional[int] = None,
        type: Optional[str] = None,
        ticket_status: Optional[List[str]] = None,
        ticket_id: Optional[int] = None,
        ticket_requires_attention: Optional[bool] = None,
        logical_operator: Optional[str] = None,
    ) -> List[RequestsSearchList]:
        """
        Method: GET
        URL: /securechangeworkflow/api/securechange/requests/search
        Version: R23-2+

        Usage:
            requests = scw.get_requests(view="ALL_REQUESTS")
            requests = scw.get_requests(view="ALL_REQUESTS",ticketId=815)

        """
        url = "requests/search"
        params = {}
        if view:
            params["view"] = view
        if group_id:
            params["groupId"] = group_id
        if request_id:
            params["requestId"] = request_id
        if type:
            params["type"] = type
        if ticket_status:
            params["ticketStatus"] = ticket_status
        if ticket_id:
            params["ticketId"] = ticket_id
        if ticket_requires_attention:
            params["ticketRequiresAttention"] = ticket_requires_attention
        if logical_operator:
            params["logicalOperator"] = logical_operator

        response = self.api.session.get(url, params=params)
        response_json = self.api.handle_json(response, "get_requests", "get")
        requests_list = get_api_node(response_json, "requests", listify=True)

        queries = [
            (
                TicketRequestSearch.kwargify(request)
                if request["type"] == "TICKET"
                else TicketDraftRequestSearch.kwargify(request)
            )
            for request in requests_list
        ]

        return queries

    def cancel_request(self, id) -> None:
        """
        Method: PUT
        URL: /securechangeworkflow/api/securechange/requests/{id:[0-9]+}/cancel
         Version: R23-2+

        Usage:
            # Example #1:
            request = scw.cancel_request(id)
        """
        url = "requests/" + str(id) + "/cancel"
        response = self.api.session.put(url)
        self.api.handle_response(response, "cancel_request", "cancel")
