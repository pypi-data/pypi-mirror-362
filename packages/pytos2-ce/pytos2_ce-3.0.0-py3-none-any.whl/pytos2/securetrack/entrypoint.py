from collections import OrderedDict
from datetime import date
from typing import Dict, Iterable, Iterator, List, Tuple, Optional, Union
from enum import Enum
from io import BytesIO
import typing
import warnings

from requests.exceptions import HTTPError, JSONDecodeError, RequestException
from requests import Response
from netaddr import IPAddress

from pytos2.securetrack.generic_transparent_firewall import GenericTransparentFirewall
from pytos2.securetrack.security_policy import (
    CSVData,
    SecurityZoneMatrix,
    SecurityPolicyDeviceMapping,
    SecurityPolicyInterface,
    InterfacesManualMappings,
    InterfaceUserMapping,
    ZoneUserAction,
)
from .api import StAPI
from .device import Device, InternetObject
from .domain import Domain
from .network_object import classify_network_object, NetworkObject
from .policy_browser import Emptiness
from .revision import Revision
from .rule import (
    BindingPolicy,
    Documentation,
    SecurityRule,
    RuleLastUsage,
    SecurityPolicyViolation,
    SecurityPolicyViolationType,
)
from .time_object import TimeObject
from pytos2.utils import (
    NoInstance,
    get_api_node,
    sanitize_uid,
    uids_match,
    setup_logger,
    safe_unwrap_msg,
)
from pytos2.utils.cache import Cache
from .application import classify_application, Application
from .service_object import ServiceGroup, classify_service_object, Service
from .zone import Zone, ZoneReference, ZoneEntry
from .interface import Interface, BindableObject, TopologyInterface
from .generic_device import GenericDevice
from .generic_ignored_interface import GenericIgnoredInterface
from .generic_interface_customer import GenericInterfaceCustomerTag
from .generic_interface import GenericInterface
from .generic_route import GenericRoute
from .generic_vpn import GenericVpn
from .change_window import ChangeWindow, ChangeWindowTask
from .properties import Properties, Property
from .license import License, TieredLicense
from .cloud import (
    JoinCloud,
    RestCloud,
    RestAnonymousSubnet,
    SuggestedCloud,
)
from .topology import (
    TopologyMode,
    TopologySubnetDetailed,
    TopologySyncStatus,
    TopologySubnet,
)
from .topology_device import TopologyDevice
from .managed_devices import BulkOperationTask, BulkOperationTaskResult
from pytos2.graphql.api import GqlAPI
from pytos2.api import Pager, boolify


LOGGER = setup_logger("st_entrypoint")


def _bool(x: bool) -> str:
    return "true" if x else "false"


def _querify(k: str, v: Union[str, bool, List[Union[str, bool]]]) -> str:
    # Used in `St.search_rules`. See that method for more details.

    # `search_text` params (key:values pairs with semantic key meanings to
    # Policy Browser, such as `'action:accept'`) are specified in the URI in
    # the format: `'key:value+key:value+...'`.  (e.g.:
    # `uid:123+action:accept`), so we have to marshal the given params into
    # said format.
    #
    # `strs remains strings, `bool`s are converted to the string `"true"` or
    # `"false"` respectively, and array values are converted to look like:
    # `'key:value1+key:value2+...'`.
    if isinstance(v, list):
        return " ".join([_querify(k, v_) for v_ in v])
    elif isinstance(v, bool):
        return f"{k}:{_bool(v)}"
    else:
        return f"{k}:{v}"


class St:
    default: Union["St", NoInstance] = NoInstance(
        "St.default",
        "No St instance has been initialized yet, initialize with `St(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = "admin-cli",
        default=True,
        cache=True,
    ):
        self.api: StAPI = StAPI(hostname, username, password)
        if client_id:
            self.graphql = GqlAPI(hostname, username, password, client_id=client_id)
        else:
            warnings.warn("No client_id provided, GraphQL API will not be available")

        if default:
            St.default = self
        self.cache = cache

        self._devices_cache = Cache()
        self._devices_cache_params = {}
        self._devices_index = self._devices_cache.make_index(["name", "id"])

        self._network_objects_by_device_id_by_name: dict = {}
        self._network_objects_by_uid: dict = {}
        self._services_by_uid: dict = {}
        self._services_by_device_id_by_name: dict = {}
        self._device_rules_dict: dict = {}
        self._revision_rules_dict: dict = {}
        self._revisions_dict: dict = {}
        self._device_revisions_dict: dict = {}
        self._rules_dict: dict = {}
        self._zones_cache = Cache()
        self._zones_index = self._zones_cache.make_index(["name", "id"])
        self._zones: list = []
        self._zones_dict: dict = {}
        self._domains_cache = Cache()
        self._domains_index = self._domains_cache.make_index(["name", "id"])
        self._domains: list = []
        self._domains_dict: dict = {}

        self._generic_devices_cache = Cache()
        self._generic_devices_index = self._generic_devices_cache.make_index(
            ["name", "id"]
        )

    def _prime_generic_devices_cache(self):
        generic_devices = self.get_generic_devices(cache=False)

        self._generic_devices_cache.clear()
        for d in generic_devices:
            self._generic_devices_cache.add(d)

    def _prime_domains_cache(self):
        domains = self.api.session.get("domains").json()

        self._domains_cache.clear()
        for domain in get_api_node(domains, "domain", listify=True):
            domain_obj = Domain.kwargify(domain)
            self._domains_cache.add(domain_obj)

    def _prime_zones_cache(self):
        zones = self.api.session.get("zones").json()

        self._zones_cache.clear()
        for zone in get_api_node(zones, "zones.zone", listify=True):
            zone_obj = Zone.kwargify(zone)
            self._zones_cache.add(zone_obj)

    def _get_all_devices_json(self, license=False, version=False):
        params = {}
        params["show_license"] = "true" if license else "false"
        params["show_os_version"] = "true" if version else "false"

        return self.api.session.get("devices", params=params).json()

    def _prime_devices_cache(self, license=False, version=False):
        devices = self._get_all_devices_json(license=license, version=version)

        self._devices_cache_params = {"license": license, "version": version}
        self._devices_cache.clear()
        for device in get_api_node(devices, "devices.device", listify=True):
            device_obj = Device.kwargify(device)
            self._devices_cache.add(device_obj)

    def _filter_device_result(self, device_data, filter):
        filtered_results = []
        for d in device_data:
            # Remove licenses list from object, as it is not hashable
            licenses = ...

            if d.data and "licenses" in d.data:
                licenses = d.data["licenses"]
                del d.data["licenses"]

            if set(filter.items()).issubset(set(d.data.items())):
                filtered_results.append(d)

            if licenses is not ...:
                d.data["licenses"] = licenses

        return filtered_results

    def get_devices(
        self,
        cache: Optional[bool] = None,
        filter: Optional[dict] = None,
        license: bool = False,
        version: bool = False,
    ):
        if cache is not False and self.cache:
            if self._devices_cache.is_empty():
                self._prime_devices_cache(license=license, version=version)
            elif self._devices_cache_params != {"license": license, "version": version}:
                self._prime_devices_cache(license=license, version=version)

            if not filter:
                return self._devices_cache.get_data()
            else:
                return self._filter_device_result(
                    self._devices_cache.get_data(), filter
                )
        else:
            devices = self._get_all_devices_json(license=license, version=version)

            d_list = [
                Device.kwargify(d)
                for d in get_api_node(devices, "devices.device", listify=True)
            ]
            if not filter:
                return d_list
            else:
                return self._filter_device_result(d_list, filter)

    def _resolve_device_id(self, device: Union[int, str, Device]) -> int:
        if isinstance(device, str):
            device_obj = self.get_device(device)
            if not device_obj:
                raise ValueError(f"Cannot find device {device}")

            return device_obj.id
        elif isinstance(device, Device):
            return device.id
        elif isinstance(device, int):
            return device
        else:
            raise ValueError(
                "Device argument not recognized. Accepted value types are int, str, and Device object."
            )

    def get_zones(self, cache: Optional[bool] = None):
        if cache is not False and self.cache:
            if self._zones_cache.is_empty():
                self._prime_zones_cache()
            return self._zones_cache.get_data()
        else:
            zones = self.api.session.get("zones").json()
            return [
                Zone.kwargify(d)
                for d in get_api_node(zones, "zones.zone", listify=True)
            ]

    def _resolve_zone_from_name(self, name: Union[str, List[str]]):
        zones = self.get_zones()
        if isinstance(name, str):
            name = [name]

        objects = []

        for n in name:
            for zone in zones:
                if zone.name == n:
                    objects.append(zone)

        return objects

    def get_zone_subnets(
        self, identifier: Union[int, str, List[int]]
    ) -> List[ZoneEntry]:
        def _send_request(id_list):
            _identifier = ",".join([str(i) for i in id_list])
            response = self.api.session.get(f"zones/{_identifier}/entries")
            if not response.ok:
                try:
                    msg = response.json().get("result").get("message")
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"wrong zone identifier, got '{msg}' from API Error: {e}"
                    )
            else:
                zone_entries = get_api_node(
                    response.json(), "zone_entries.zone_entry", listify=True
                )
                zone_subnets = []
                for entry in zone_entries:
                    zone_subnets.append(ZoneEntry.kwargify(entry))

                return zone_subnets

        def _get(_identifier):
            if isinstance(_identifier, str):
                _identifier = [z.id for z in self._resolve_zone_from_name(_identifier)]

            if isinstance(_identifier, (list, int)):
                if isinstance(_identifier, int):
                    _identifier = [_identifier]

                if isinstance(_identifier, list):
                    i = 0
                    length = len(_identifier)
                    res_subnets = []
                    while i < length:
                        id_list = _identifier[i : i + 10]
                        i += 10

                        for entry in _send_request(id_list):
                            res_subnets.append(entry)
                            # yield entry

                    return res_subnets  # noqa
            else:
                raise TypeError(
                    f"input identifier can only be list, int, str or list[int]] but got {_identifier}"
                )

        zone_subnets = []
        for entry in _get(identifier):
            zone_subnets.append(entry)
        return zone_subnets

    def get_zone_descendants(
        self, identifier: Union[int, str, List[int]]
    ) -> List[Zone]:
        def _send_request(id_list):
            _identifier = ",".join([str(i) for i in id_list])

            response = self.api.session.get(f"zones/{_identifier}/descendants")
            if not response.ok:
                try:
                    msg = response.json().get("result").get("message")
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"wrong zone identifier, got '{msg}' from API Error: {e}"
                    )
            else:
                zones = get_api_node(response.json(), "zones.zone", listify=True)
                if not zones:
                    raise ValueError(f"can not find zones by given ids: {_identifier}")
                zone_ref = []
                for zone in zones:
                    zone_ref.append(ZoneReference.kwargify(zone))

                return zone_ref

        def _get(_identifier):
            if isinstance(_identifier, str):
                _identifier = [z.id for z in self._resolve_zone_from_name(_identifier)]

            if isinstance(_identifier, (list, int)):
                if isinstance(_identifier, int):
                    _identifier = [_identifier]

                if isinstance(_identifier, list):
                    i = 0
                    length = len(_identifier)
                    res_descendants = []
                    while i < length:
                        id_list = _identifier[i : i + 10]
                        i += 10

                        for zone in _send_request(id_list):
                            res_descendants.append(zone)

                    return res_descendants
            else:
                raise TypeError(
                    f"input identifier can only be list, int, str or list[int]] but got {_identifier}"
                )

        zone_descendants = []
        for zone in _get(identifier):
            zone_descendants.append(zone)
        return zone_descendants

    def get_zone(
        self, identifier: Union[int, str], cache: Optional[bool] = None
    ) -> Optional[Zone]:
        def _get(_identifier):
            if isinstance(_identifier, int):
                zone = get_api_node(self.api.get_zone_by_id(_identifier).json(), "zone")
                return Zone.kwargify(zone) if zone else None
            else:
                for zone in get_api_node(
                    self.api.get_zones_by_name(_identifier).json(),
                    "zones.zone",
                    default=[],
                ):
                    zone_obj = Zone.kwargify(zone)
                    if zone_obj.name == _identifier:
                        return zone_obj

        if cache is not False and self.cache:
            if self._zones_cache.is_empty():
                self._prime_zones_cache()
            return self._zones_index.get(identifier)
        else:
            return _get(identifier)

    def get_domains(self, cache: Optional[bool] = None):
        if cache is not False and self.cache:
            if self._domains_cache.is_empty():
                self._prime_domains_cache()
            return self._domains_cache.get_data()
        else:
            domains = self.api.session.get("domains").json()

            return [
                Domain.kwargify(d)
                for d in get_api_node(domains, "domain", listify=True)
            ]

    def get_domain(
        self, identifier: Union[int, str], cache: Optional[bool] = None
    ) -> Optional[Domain]:
        def _get(_identifier):
            if isinstance(_identifier, int):
                domain = get_api_node(
                    self.api.get_domain_by_id(_identifier).json(), "domain"
                )
                return Domain.kwargify(domain) if domain else None
            else:
                for domain in get_api_node(
                    self.api.get_domains_by_name(_identifier).json(),
                    "domain",
                    default=[],
                ):
                    domain_obj = Domain.kwargify(domain)
                    if domain_obj.name == _identifier:
                        return domain_obj

        if cache is not False and self.cache:
            if self._domains_cache.is_empty():
                self._prime_domains_cache()
            return self._domains_index.get(identifier)
        else:
            return _get(identifier)

    def _get_domain_id(self, domain_input):
        if not domain_input:
            return None

        if isinstance(domain_input, int):
            domain = self.get_domain(domain_input)
            if domain:
                return domain.id
            else:
                raise ValueError(f"Domain with id '{domain_input}' not found.")
        elif isinstance(domain_input, str):
            domain = self.get_domain(domain_input)
            if domain:
                return domain.id
            else:
                raise ValueError(f"Domain with name '{domain_input}' not found.")
        elif isinstance(domain_input, Domain):
            return domain_input.id
        raise ValueError(f"Invalid input type: {type(domain_input)}")

    def add_domain(
        self,
        name: str,
        description: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[Domain]:
        res = self.api.post_domain(name=name, description=description, address=address)
        if res.ok:
            created_url = res.headers.get("Location", "")
            did = int(created_url.split("/")[-1])
            new_domain = get_api_node(self.api.get_domain_by_id(did).json(), "domain")
            if new_domain:
                domain = Domain.kwargify(new_domain)
                self._domains_cache.add(domain)
                return domain
            else:
                raise ValueError(
                    f"domain id: {did} not found by GET call after POSTing to SecureTrack"
                )

        else:  # pragma: no cover
            try:
                msg = res.json().get("result").get("message")
                res.raise_for_status()
            except HTTPError as e:
                raise ValueError(
                    f"unable to POST new domain :{name} to SecureTrack, got {msg} from API Error: {e}"
                )

    def update_domain(
        self,
        identifier: Union[int, str, Domain],
        name: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[Domain]:
        modify_domain = None
        if isinstance(identifier, Domain):
            modify_domain = identifier
            identifier = identifier.id

        if self._domains_cache.is_empty():
            self._prime_domains_cache()
        if not modify_domain:
            modify_domain = self._domains_index.get(identifier)
        res = self.api.put_domain(
            id=modify_domain.id,
            name=name or modify_domain.name,
            description=description or modify_domain.description,
            address=address or modify_domain.address,
        )
        if res.ok:
            modified_domain_json = get_api_node(
                self.api.get_domain_by_id(modify_domain.id).json(), "domain"
            )
            modified_domain = Domain.kwargify(modified_domain_json)
            self._domains_dict[identifier] = modified_domain
            return modified_domain

        else:
            try:
                msg = res.json().get("result").get("message")
                res.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got {e}, with Error Message: {msg}")

    def get_device(
        self,
        identifier: Union[int, str],
        cache: Optional[bool] = None,
        license: Optional[bool] = False,
        version: Optional[bool] = False,
    ) -> Optional[Device]:
        opts = {"license": license, "version": version}

        def _get(_identifier):
            if isinstance(_identifier, int):
                device = get_api_node(
                    self.api.get_device_by_id(identifier, **opts).json(), "device"
                )
                return Device.kwargify(device) if device else None
            else:
                for device in get_api_node(
                    self.api.get_devices_by_name(_identifier).json(),
                    "devices.device",
                    default=[],
                ):
                    device_obj = Device.kwargify(device)
                    if device_obj.name == _identifier:
                        return device_obj

        if cache is not False and self.cache:
            if self._devices_cache.is_empty():
                self._prime_devices_cache()
            return self._devices_index.get(identifier)
        else:
            return _get(identifier)

    def _get_network_objects(
        self,
        device_id: Optional[int] = None,
        revision_id: Optional[int] = None,
        **params,
    ):
        if device_id:
            pager = Pager(
                self.api,
                f"devices/{device_id}/network_objects",
                "network_objects.network_object",
                "get_network_objects",
                classify_network_object,
                params=boolify(params),
            )
            return pager
        elif revision_id:
            pager = Pager(
                self.api,
                f"revisions/{revision_id}/network_objects",
                "network_objects.network_object",
                "get_network_objects",
                classify_network_object,
                params=boolify(params),
            )
            return pager
        else:
            raise ValueError("Either device_id or revision_id must be provided")

    def _prime_network_objects_cache(
        self, device_id: int, add_parent_objects: Optional[bool] = None
    ):
        # bust existing cache for device_id
        self._network_objects_by_device_id_by_name[device_id] = {}
        self._network_objects_by_uid = {
            u: [o for o in objs if o.device_id != device_id]
            for u, objs in self._network_objects_by_uid.items()
        }

        network_objects = self._get_network_objects(
            device_id, add_parent_objects=add_parent_objects
        )
        for obj in network_objects:
            self._network_objects_by_device_id_by_name.setdefault(device_id, {})[
                str(obj["name"])
            ] = obj
            self._network_objects_by_uid.setdefault(
                sanitize_uid(obj["uid"]), []
            ).append(obj)

    def _prime_services_cache(self, device_id: int):
        # bust existing cache for device_id
        self._services_by_device_id_by_name[device_id] = {}
        self._services_by_uid = {
            u: [o for o in objs if o.device_id != device_id]
            for u, objs in self._services_by_uid.items()
        }

        services = self.api.session.get(f"devices/{device_id}/services").json()
        for obj in get_api_node(services, "services.service", listify=True):
            obj = classify_service_object(dict(**obj, device_id=device_id))
            self._services_by_device_id_by_name.setdefault(device_id, {})[
                str(obj["name"])
            ] = obj
            self._services_by_uid.setdefault(sanitize_uid(obj["uid"]), []).append(obj)

    def get_shadowing_rules_for_device(
        self: "St", device: str, rules: Iterator[str]
    ) -> List[Tuple[SecurityRule, List[SecurityRule]]]:
        rules = self.api.session.get(
            f"devices/{device}/shadowing_rules",
            params={"shadowed_uids": ",".join(rules)},
        )

        if not rules.ok:
            try:
                msg = rules.json().get("result").get("message")
                rules.raise_for_status()
            except HTTPError as e:
                raise ValueError(
                    f"Unable to get shadowing rules got '{msg}' from API Error: {e}"
                )
        rules_json = (
            rules.json()
            .get("cleanup_set")
            .get("shadowed_rules_cleanup")
            .get("shadowed_rules")
            .get("shadowed_rule")
        )
        result_rules = []
        for rule in rules_json:
            rule_and_shadowing_rules_pair = (
                SecurityRule.kwargify(rule.get("rule")),
                [
                    SecurityRule.kwargify(r)
                    for r in rule.get("shadowing_rules").get("rule")
                ],
            )
            result_rules.append(rule_and_shadowing_rules_pair)
        return result_rules

    def search_network_objects(
        self,
        *,
        name: Optional[str] = None,
        ip: Optional[Union[str, IPAddress]] = None,
        any_field: Optional[str] = None,
        device: Optional[Union[int, str, Device]] = None,
        comment: Optional[str] = None,
        uid: Optional[str] = None,
        contained_in: Optional[str] = None,
        contains: Optional[str] = None,
        exact_subnet: Optional[str] = None,
        exact_match: Optional[bool] = False,
        identity_awareness: Optional[Union[str, bool]] = None,
        type_on_device: Optional[Union[str, bool]] = None,
        context: Optional[int] = None,
    ) -> Pager:
        """
        Search network objects filtered by name, ip, comment, device, uid, subnet (not all can be combined)

        Method: GET
        URL: /securetrack/api/network_objects/search
        Version: 21+

        Notes:
            Arguments are not positional and must be explicitly declared using their names.

            Most filters cannot be combined. However, device can be combined with
            all filters.

            If your environment is multi-domain, you may filter by domain id
            using the context argument

        Usage:

            !!IMPORTANT!!
            Unless you use fetch_all(), you will get back an instance
            of a Pager class. It has iteration, length, automatic paging, etc.

            from pytos2.api import Pager

            netobjs: Pager = st.search_network_objects(name="https")
            print len(netobjs)
            for obj in netobjs:
                print(obj)

            # fetch_all() will generally have poorer performance since it has to fetch everything
            all_https = st.search_network_objects(name="https").fetch_all()

            netobjs: Pager = st.search_network_objects(name="https", device=553)

            netobjs: Pager = st.search_network_objects(name="https", exact_match=True)

            netobjs: Pager = st.search_network_objects(comment="DHCP server")

            netobjs: Pager = st.search_network_objects(ip="91.199")

            netobjs: Pager = st.search_network_objects(ip="91.199.100.249")

            netobjs: Pager = st.search_network_objects(device=8)

            netobjs: Pager = st.search_network_objects(any_field="1.1.1.1")

            netobjs: Pager = st.search_network_objects(any_field="1.1", device="ASAv")

            netobjs: Pager = st.search_network_objects(contained_in="91.199.0.0")

            netobjs: Pager = st.search_network_objects(contains="91.199.100.249")

            netobjs: Pager = st.search_network_objects(exact_subnet="65.55.88.0")

            netobjs: Pager = st.search_network_objects(type_on_device=True)

        """
        filter = "text"  # Must be: text, subnet or uid
        params = {}

        # We must check for filters that are combined which cannot be combined.
        # TOS does not always return errors for these use cases but rather
        # ignores the filter which was not specified in the "filter" property
        # and returns all network objects.

        locals_ = (
            locals()
        )  # a necessary work-around for using "locals" in list comprehensions

        exclusive_text_filters = ["name", "ip", "any_field", "uid", "comment"]
        text_fil_count = sum([bool(locals_.get(f)) for f in exclusive_text_filters])

        exclusive_subnet_filters = ["contained_in", "contains", "exact_subnet"]
        sub_fil_count = sum(bool(locals_.get(f)) for f in exclusive_subnet_filters)

        if text_fil_count + sub_fil_count > 1:
            raise ValueError(
                """
Please specify exactly one of: 
name, ip, any_field, uid, comment,
contains, contained_in or exact_subnet.
These arguments cannot be combined. 
"""
            )

        if text_fil_count > 0:
            if exact_match:
                params["exact_match"] = "true"
        elif sub_fil_count > 0:
            filter = "subnet"
            if exact_match:
                raise ValueError(
                    'Exact match only applies to name, ip, and comment "text" filters.'
                )

        for var_name in exclusive_text_filters + exclusive_subnet_filters:
            value = locals().get(var_name)
            if value:
                # This is convert things like netaddr objects
                if not isinstance(locals().get(var_name), str):
                    params[var_name] = str(value)
                else:
                    params[var_name] = value
                break

        if uid:
            filter = "uid"
            params["uid"] = uid.replace("{", "").replace("}", "")

        if device:
            device_id = self._resolve_device_id(device)
            if device_id:
                params["device_id"] = device_id

        if context:
            params["context"] = context
        if identity_awareness:
            params["identity_awareness"] = "supported"
        if type_on_device:
            params["typeOnDevice"] = "edl_ip_list"

        params["filter"] = filter

        pager = Pager(
            self.api,
            "network_objects/search",
            "network_objects.network_object",
            "search_network_objects",
            classify_network_object,
            params=params,
            page_size=100,
        )
        return pager

    def get_network_objects(
        self,
        device: Union[int, str, None] = None,
        *,
        revision: Optional[int] = None,
        name: Optional[str] = None,
        type: Optional[NetworkObject.Type] = None,
        show_members: Optional[bool] = True,
        contains_ip: Optional[str] = None,
        identity_awareness: Optional[str] = None,
        type_on_device: Optional[str] = None,
        add_parent_objects: Optional[bool] = None,
        uids: Optional[str] = None,
        cache: Optional[bool] = None,
        object_ids: Optional[List[int]] = None,
    ):
        if device and object_ids:
            return self._get_network_objects_for_device_and_object_ids(
                device=device,
                object_ids=object_ids,
                show_members=show_members,
                identity_awareness=identity_awareness,
            )
        if revision and object_ids:
            return self._get_network_objects_for_revision_and_object_ids(
                revision_id=revision,
                object_ids=object_ids,
                show_members=show_members,
                identity_awareness=identity_awareness,
            )

        params = {}
        if name:
            params["name"] = name
        if type:
            params["type"] = type.value
        if show_members is not None:
            params["show_members"] = str(show_members).lower()
        if contains_ip:
            params["contains_ip"] = contains_ip
        if identity_awareness:
            params["identity_awareness"] = identity_awareness
        if type_on_device:
            params["type_on_device"] = type_on_device
        if add_parent_objects is not None:
            params["add_parent_objects"] = str(add_parent_objects).lower()
        if uids:
            params["uids"] = uids

        if device:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
            device_id = device_obj.id

            # If any other key besides show_members or add_parent_objects is passed, we won't use the cache,
            # as the cache doesn't support filtering on other keys properly.
            cache_compat = (
                len(
                    set(params.keys()).difference(
                        {"show_members", "add_parent_objects"}
                    )
                )
                == 0
            )

            if cache is not False and self.cache and cache_compat:
                if device_id not in self._network_objects_by_device_id_by_name:
                    self._prime_network_objects_cache(
                        device_id, add_parent_objects=add_parent_objects
                    )

                objs = list(
                    self._network_objects_by_device_id_by_name[device_id].values()
                )
                for obj in objs:
                    obj.device_id = device_id
            else:
                objs = self._get_network_objects(device_id, **params)

            return objs
        elif revision:
            return self._get_network_objects(revision_id=revision, **params)

    def get_network_object(
        self,
        name: Optional[str] = None,
        device: Union[int, str, None] = None,
        uid: Optional[str] = None,
        cache=True,
    ) -> NetworkObject:
        device_obj = None
        if device:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
        if self.cache and cache:
            if uid:
                uid = sanitize_uid(uid)
                if uid not in self._network_objects_by_uid:
                    objs = self.api.session.get(
                        "network_objects/search", params={"filter": "uid", "uid": uid}
                    ).json()

                    for obj_json in get_api_node(
                        objs, "network_objects.network_object", listify=True
                    ):
                        obj = classify_network_object(obj_json)
                        self._network_objects_by_uid.setdefault(
                            sanitize_uid(obj["uid"]), []
                        ).append(obj)
                        self._network_objects_by_device_id_by_name.setdefault(
                            obj["device_id"], {}
                        )[obj["name"]] = obj

                objs = self._network_objects_by_uid.get(uid, [None])
                if len(objs) > 1:
                    if device_obj is None:
                        raise AssertionError(
                            f"More than one object found for uid {uid}, device argument must be passed"
                        )
                    else:
                        for obj in objs:
                            if obj.device_id == device_obj.id:
                                objs = [obj]
                                break
                        else:
                            objs = [None]
                return objs[0]

            elif not name or device_obj is None:
                raise ValueError(
                    "name and device arguments must be passed if uid is None"
                )
            device_id = device_obj.id
            if device_id not in self._network_objects_by_device_id_by_name:
                network_objects = self.api.session.get(
                    f"devices/{device_id}/network_objects"
                ).json()
                for obj_json in get_api_node(
                    network_objects, "network_objects.network_object", listify=True
                ):
                    obj = classify_network_object(obj_json)
                    self._network_objects_by_device_id_by_name.setdefault(
                        device_id, {}
                    )[str(obj["name"])] = obj
                    obj.device_id = device_id
                    self._network_objects_by_uid.setdefault(
                        sanitize_uid(obj["uid"]), []
                    ).append(obj)
            return self._network_objects_by_device_id_by_name[device_id].get(name)
        else:
            raise NotImplementedError(
                "Non-caching mode is not supported...yet"
            )  # pragma: no cover

    def get_services(
        self,
        device: Union[int, str, None] = None,
        *,
        revision: Optional[int] = None,
        name: Optional[str] = None,
        protocol: Optional[Union[str, int, Service.Protocol]] = None,
        port: Optional[int] = None,
        type: Optional[str] = None,
        icmp_type: Optional[int] = None,
        add_parent_objects: Optional[bool] = True,
        show_members: Optional[bool] = False,
        context: Optional[int] = None,
        object_ids: Optional[List[int]] = None,
        cache: Optional[bool] = None,
    ):
        params = {}

        if name:
            params["name"] = name
        if protocol is not None:
            if isinstance(protocol, str):
                params["protocol"] = Service.Protocol[protocol.upper()].value
            elif isinstance(protocol, int) and protocol >= 0 and protocol <= 255:
                params["protocol"] = protocol
            else:
                params["protocol"] = protocol.value
        if port is not None:
            params["port"] = port
        if type:
            if type.lower() in ["tcp", "udp", "ip", "icmp", "group"]:
                params["type"] = type.lower()
            else:
                raise ValueError(
                    f"Invalid value for 'type' filter: {type}. Allowed values are: tpc, udp, ip, icmp, group"
                )
        if icmp_type is not None:
            if icmp_type >= 0 and icmp_type <= 255:
                params["icmp_type"] = icmp_type
        params["show_members"] = show_members
        params["add_parent_objects"] = add_parent_objects
        if context:
            params["context"] = context

        if device:
            if not isinstance(device, int):
                device_obj = self.get_device(device)
                if device_obj is None:
                    raise ValueError(f"Device {device} not found")
                device = device_obj.id
        if object_ids:
            if device:
                return self._get_services_by_device_and_id(
                    device, object_ids, show_members=show_members, context=context
                )
            if revision:
                return self._get_services_by_revision_and_id(
                    revision, object_ids, show_members=show_members, context=context
                )

        # Services cache does not support any of the filters
        cache_compat = len(params) == 2 and device

        if cache is not False and self.cache and cache_compat:
            if device not in self._services_by_device_id_by_name:
                self._prime_services_cache(device)
            objs = list(self._services_by_device_id_by_name[device].values())
            for obj in objs:
                obj.device_id = device
            return objs

        if device:
            pager = Pager(
                self.api,
                f"devices/{device}/services",
                "services.service",
                "get_services_by_device",
                classify_service_object,
                params=params,
            )
            return pager
        elif revision:
            pager = Pager(
                self.api,
                f"revisions/{revision}/services",
                "services.service",
                "get_services_by_revision",
                classify_service_object,
                params=params,
            )
            return pager
        else:
            raise ValueError("Either device or revision must be provided")

    def get_service(
        self,
        name: Optional[str] = None,
        device: Union[int, str, None] = None,
        uid: Optional[str] = None,
        cache=True,
    ) -> Service:
        device_obj = None
        if device:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
        if self.cache and cache:
            if uid:
                uid = sanitize_uid(uid)
                if uid not in self._services_by_uid:
                    params = {"filter": "uid", "uid": uid}

                    if device_obj:
                        params["device_id"] = device_obj.id

                    objs = self.api.session.get("services/search", params=params).json()

                    for obj_json in get_api_node(
                        objs, "services.service", listify=True
                    ):
                        obj = classify_service_object(obj_json)
                        self._services_by_uid.setdefault(
                            sanitize_uid(obj["uid"]), []
                        ).append(obj)

                        self._services_by_device_id_by_name.setdefault(
                            obj.device_id or device_obj.id, {}
                        )[obj["name"]] = obj

                objs = self._services_by_uid.get(uid, [None])
                if len(objs) > 1:
                    if device_obj is None:
                        raise AssertionError(
                            "More than one object found for uid {uid}, device argument must be passed"
                        )
                    else:
                        for obj in objs:
                            if obj.device_id == device_obj.id:
                                objs = [obj]
                                break
                        else:
                            objs = [None]
                return objs[0]

            elif not name or device_obj is None:
                raise ValueError(
                    "name and device arguments must be passed if uid is None"
                )
            device_id = device_obj.id
            if (
                device_id not in self._services_by_device_id_by_name
                or name not in self._services_by_device_id_by_name[device_id]
            ):
                services = self.api.session.get(f"devices/{device_id}/services").json()
                for obj_json in get_api_node(
                    services, "services.service", listify=True
                ):
                    obj = classify_service_object(obj_json)
                    self._services_by_device_id_by_name.setdefault(device_id, {})[
                        str(obj["name"])
                    ] = obj
                    obj.device_id = device_id
                    self._services_by_uid.setdefault(
                        sanitize_uid(obj["uid"]), []
                    ).append(obj)

            return self._services_by_device_id_by_name[device_id].get(name)
        else:
            raise NotImplementedError(
                "Non-caching mode is not supported...yet"
            )  # pragma: no cover

    def _prime_rules_cache(self):
        self._device_rules_dict = {}
        self._revision_rules_dict = {}

    def _transform_rules_response(self, rules_response: Response) -> Iterator:
        if not rules_response.ok:
            try:
                msg = rules_response.text
                rules_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got '{msg}' from Error :{e}")

        rules_json = rules_response.json()
        rules_json = get_api_node(rules_json, "rules.rule", listify=True)
        rules = [SecurityRule.kwargify(rule) for rule in rules_json]
        return rules

    def _transform_nat_rules_response(self, nat_rules_response: Response) -> Iterator:
        if not nat_rules_response.ok:
            try:
                msg = nat_rules_response.json().get("result").get("message")
                nat_rules_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got '{msg}' from Error: {e}")

        nat_rules_json = nat_rules_response.json()
        nat_rules_json = get_api_node(nat_rules_json, "nat_rule", listify=True)
        nat_rules = [SecurityRule.kwargify(nat_rule) for nat_rule in nat_rules_json]
        return nat_rules

    def _filter_rule_uid(self, rules, rule_uid):
        if rule_uid:
            mat_rules = [rule for rule in rules if uids_match(rule.uid, rule_uid)]
            return mat_rules
        else:
            return rules

    def _get_rules_by_revision(
        self,
        revision: int,
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ):
        revision_obj = self.get_revision(revision=revision)
        revision_id = revision_obj.id
        if cache and self.cache:
            if not self._revision_rules_dict:
                self._prime_rules_cache()

            if revision_id in self._revision_rules_dict:
                rules = self._revision_rules_dict[revision_id]

                if rule_uid is not None:
                    return self._filter_rule_uid(rules, rule_uid)
                else:
                    return rules
            else:
                rules_response = self.api.get_rules_from_revision_id(
                    revision_id, uid=uid, documentation=documentation
                )
                rules = self._transform_rules_response(rules_response)

                self._revision_rules_dict[revision_id] = rules
                return self._filter_rule_uid(rules, rule_uid)
        else:
            rules_response = self.api.get_rules_from_revision_id(
                revision_id, uid=uid, documentation=documentation
            )
            rules = self._transform_rules_response(rules_response)

            return self._filter_rule_uid(rules, rule_uid)

    def _get_rules_by_device(
        self,
        device: Union[str, int],
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ):
        device_obj = self.get_device(device)

        if device_obj is None:
            raise ValueError(f"Device {device} not found")

        latest_revision_id = device_obj.latest_revision
        device_id = device_obj.id
        if cache and self.cache:
            if not self._device_rules_dict:
                self._prime_rules_cache()

            if device_id in self._device_rules_dict:
                return self._filter_rule_uid(
                    self._device_rules_dict[device_id], rule_uid
                )

            else:
                rules_response = self.api.get_rules_from_device_id(
                    device_id, uid=uid, documentation=documentation
                )
                rules = self._transform_rules_response(rules_response)

                for rule in rules:
                    rule.device = device_obj

                self._device_rules_dict[device_id] = rules

                if latest_revision_id is not None:
                    self._revision_rules_dict[latest_revision_id] = rules

                if rule_uid:
                    return self._filter_rule_uid(rules, rule_uid)
                else:
                    return rules
        else:
            rules_response = self.api.get_rules_from_device_id(
                device_id, uid=uid, documentation=documentation
            )
            rules = self._transform_rules_response(rules_response)

            for rule in rules:
                rule.device = device_obj

            return rules

    def _get_nat_rules_by_device(self, device: Union[str, int]):
        def _get_response(device_obj, interface_name=None):
            device_id = device_obj.id

            nat_rules_response = self.api.get_nat_rules_from_device_id(
                device_id, input_interface=interface_name
            )
            if not nat_rules_response.ok:
                try:
                    msg = nat_rules_response.json().get("result").get("message")
                    nat_rules_response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(f"got '{msg}' from Error {e}")

            nat_rules = self._transform_nat_rules_response(nat_rules_response)

            for rule in nat_rules:
                rule.device = device_obj

            return nat_rules

        should_iterate_interfaces = False

        device_obj = self.get_device(device)

        if device_obj is None:
            raise ValueError(f"Device {device} not found")

        if device_obj.vendor in [Device.Vendor.CISCO]:
            should_iterate_interfaces = True

        device_id = device_obj.id

        interfaces = None
        rules = []
        if should_iterate_interfaces:
            interfaces = self.get_interfaces(device_id)
            for interface in interfaces:
                iface_nat_rules = _get_response(device_obj, interface.name)
                for rule in iface_nat_rules:
                    rules.append(rule)
            return rules
        else:
            nat_rules = _get_response(device_obj, None)

            for rule in nat_rules:
                rules.append(rule)
            return rules

    def get_nat_rules(self, device: Union[str, int, None] = None) -> List[SecurityRule]:
        if device is None:
            raise NotImplementedError(
                "Current SDK does not support NAT rules for all devices"
            )
        elif device is not None:
            device_obj = self.get_device(device)
            to_return_nat_rules = []
            nat_rules = self._get_nat_rules_by_device(device=device)
            nat_rule_map = {}
            for n in nat_rules:
                nat_rule_map[n.id] = n

            for nat_rule in nat_rule_map.values():
                nat_rule.device = device_obj
                to_return_nat_rules.append(nat_rule)
            return to_return_nat_rules

    def get_rules_on_open_tickets(
        self,
        devices: Union[Union[str, int], List[Union[str, int]]] = None,
        context: int = 0,
    ) -> List[SecurityRule]:
        return self.search_rules(
            devices=devices, context=context, **{"inprogressticketid": "*"}
        )

    def get_rules(
        self,
        device: Union[str, int, None] = None,
        revision: Union[int, None] = None,
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ) -> List[SecurityRule]:
        match_rules = []
        if device is None and revision is None:
            for device in self.get_devices():
                rules = self._get_rules_by_device(
                    device=device.id,
                    rule_uid=rule_uid,
                    uid=uid,
                    documentation=documentation,
                    cache=cache,
                )
                for rule in rules:
                    rule.device = device

                    if rule_uid is not None and uids_match(rule.uid, rule_uid):
                        match_rules.append(rule)
                    elif rule_uid is None:
                        match_rules.append(rule)
        elif device is not None and revision is not None:
            raise ValueError(
                "You cannot specify both revision and device arguments for the same call"
            )

        elif device is not None:
            rules = self._get_rules_by_device(
                device=device,
                rule_uid=rule_uid,
                uid=uid,
                documentation=documentation,
                cache=cache,
            )
            device_obj = self.get_device(device)
            for rule in rules:
                rule.device = device_obj
                match_rules.append(rule)

        elif revision is not None:
            rules = self._get_rules_by_revision(
                revision=revision,
                rule_uid=rule_uid,
                uid=uid,
                documentation=documentation,
                cache=cache,
            )
            for rule in rules:
                match_rules.append(rule)
        return match_rules

    def get_rule_documentation(
        self: "St", device: Union[str, int], rule: Union[int, SecurityRule]
    ) -> Documentation:
        """
        Get rule documentation for a single rule given by device ID and rule ID

        Method: GET
        URL: /securetrack/api/devices/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: R22-2+

        Usage:
            doc = st.get_rule_documentation(8, 234)
        """
        device_obj = self.get_device(device)
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        r = self.api.session.get(
            f"devices/{device_obj.id}/rules/{rule_id}/documentation"
        )
        if not r.ok:
            r.raise_for_status()  # no detail msg in response
        return Documentation.kwargify(r.json()["rule_documentation"])

    def update_rule_documentation(
        self,
        device: Union[str, int],
        rule: Union[int, SecurityRule],
        rule_documentation: Documentation,
    ) -> None:
        """
        Update rule documentation for a single rule given by device ID and rule ID

        Method: POST
        URL: /securetrack/api/devices/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: R22-2+

        Usage:
            doc = st.get_rule_documentation(8, 234)
            doc.comment = doc.comment + " | Some new comment here"
            st.update_rule_documentation(8, 234, doc)
        """
        if isinstance(device, str):
            device_obj = self.get_device(device)
            device = device_obj.id
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        documentation_body = {"rule_documentation": rule_documentation._json}

        r = self.api.session.put(
            f"devices/{device}/rules/{rule_id}/documentation", json=documentation_body
        )

        if not r.ok:
            r.raise_for_status()

    def get_revision_rule_documentation(
        self: "St", revision_id: int, rule: Union[int, SecurityRule]
    ) -> Documentation:
        """
        Get rule documentation for a single rule given by revision ID and rule ID

        Method: GET
        URL: /securetrack/api/revisions/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: R22-2+

        Usage:
            doc = st.get_revision_rule_documentation(24522, 53419)
        """
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        r = self.api.session.get(
            f"revisions/{revision_id}/rules/{rule_id}/documentation"
        )
        if not r.ok:
            r.raise_for_status()  # no detail msg in response
        return Documentation.kwargify(r.json()["rule_documentation"])

    def update_rule_documentation_by_revision(
        self,
        revision_id: int,
        rule: Union[int, SecurityRule],
        rule_documentation: Documentation,
    ) -> None:
        """
        Update rule documentation for a single rule given by revision ID and rule ID

        Method: POST
        URL: /securetrack/api/revisions/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: R22-2+

        Usage:
            doc = st.get_revision_rule_documentation(24522, 53419)
            doc.comment = doc.comment + " | Some new comment here"
            st.update_rule_documentation_by_revision(24522, 53419, doc)
        """
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        documentation_body = {"rule_documentation": rule_documentation._json}
        r = self.api.session.put(
            f"revisions/{revision_id}/rules/{rule_id}/documentation",
            json=documentation_body,
        )
        self.api.handle_response(r, "update_rule_documentation_by_revision", "update")

    def delete_rule_documentation(
        self, device: Union[int, str], rule: Union[int, SecurityRule]
    ):
        """
        Delete specified rule documentation using device id and rule info

        Method: DELETE
        URL: /securetrack/api/devices/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: 21+

        Usage:
            st.delete_rule_documentation(264, 53419)
        """
        device_id = self._resolve_device_id(device)
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        url = f"devices/{device_id}/rules/{rule_id}/documentation"
        response = self.api.session.delete(url)
        self.api.handle_response(response, "delete_rule_documentation", "delete")

    def delete_rule_documentation_by_revision(
        self, revision_id: int, rule: Union[int, SecurityRule]
    ):
        """
        Delete specified rule documentation using revision id and rule info

        Method: DELETE
        URL: /securetrack/api/revisions/{id:[0-9]+}/rules/{rule_id:[0-9]+}/documentation
        Version: 21+

        Usage:
            st.delete_rule_documentation_by_revision(24522, 53419)
        """
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        url = f"revisions/{revision_id}/rules/{rule_id}/documentation"
        response = self.api.session.delete(url)
        self.api.handle_response(
            response, "delete_rule_documentation_by_revision", "delete"
        )

    def _prime_revisions_cache(self):
        self._revisions_dict = {}
        self._device_revisions_dict = {}

    def _get_revision_from_cache(self, revision_id: int):
        revision = self._revisions_dict.get(revision_id, None)
        if not revision:
            raise TypeError("No revision found in cache")
        return revision

    def _get_revision_from_server(self, revision_id: int):
        revision_response = self.api.session.get(f"revisions/{revision_id}")
        if not revision_response.ok:
            try:
                msg = (
                    revision_response.json().get("result").get("message")
                    if revision_response.text
                    else f"Generic API Error {revision_response.status_code}"
                )
                revision_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from Error :{e}")

        revision_json = revision_response.json()
        revision_json = get_api_node(revision_json, "revision")
        return Revision.kwargify(revision_json)

    def get_revision(self, revision: int, cache: bool = True) -> Revision:
        if cache and self.cache:
            if not self._revisions_dict:
                self._prime_revisions_cache()
            try:
                revision_obj = self._get_revision_from_cache(revision)
            except TypeError as e:
                try:
                    revision_obj = self._get_revision_from_server(revision)
                except HTTPError as e:
                    raise ValueError(f"got error :{e}")
            self._revisions_dict[revision] = revision_obj
            return revision_obj
        else:
            return self._get_revision_from_server(revision)

    def get_latest_revision(self, device: Union[str, int]):
        device_id = self.get_device(device).id if isinstance(device, str) else device
        revision_response = self.api.session.get(f"devices/{device_id}/latest_revision")
        # API return can not be JSON Decoded - use generic error
        if not revision_response.ok:
            revision_response.raise_for_status()

        revision_json = revision_response.json()
        revision_json = get_api_node(revision_json, "revision")

        revision_obj = Revision.kwargify(revision_json)
        return revision_obj

    def _get_revisions_from_cache(self, device_id: int):
        revisions = self._device_revisions_dict.get(device_id, None)
        if revisions:
            return revisions
        else:
            return False

    def _get_revisions_from_server(self, device_id: int):
        revisions_response = self.api.session.get(f"devices/{device_id}/revisions")
        if not revisions_response.ok:
            revisions_response.raise_for_status()

        revisions_json = revisions_response.json()
        revisions_json = get_api_node(revisions_json, "revision", listify=True)

        revisions = [Revision.kwargify(revision) for revision in revisions_json]
        return revisions

    def get_revisions(self, device: Union[str, int], cache: bool = True):
        device_obj = self.get_device(identifier=device)
        if not device_obj:
            raise ValueError(f"Device {device} not found")
        device_id = device_obj.id

        if cache and self.cache:
            if not self._device_revisions_dict:
                self._prime_revisions_cache()

            revisions = self._get_revisions_from_cache(device_id)
            if revisions:
                return revisions
            else:
                revisions = self._get_revisions_from_server(device_id)
                self._device_revisions_dict[device_id] = revisions
                return revisions
        else:
            return self._get_revisions_from_server(device_id)

    def search_rules(
        self: "St",
        text: Optional[str] = None,
        devices: Union[Union[str, int], List[Union[str, int]]] = None,
        context: Optional[int] = None,
        # The list of known rule search parameters that have been encoded (so
        # far):
        shadowed: Optional[bool] = None,
        expiration_date: Optional[Union[Emptiness, date]] = None,
        certification_expiration_date: Optional[Union[Emptiness, date]] = None,
        comment: Optional[Emptiness] = None,
        # The unknowns (dun dun dun):
        #
        # (N.B. that search params passed by name in the type signature
        # (`shadowed`, etc.) will overwrite any params inside of
        # `search_text_params` (actually, if you try to call the function like:
        # `st.search_rules(shadowed=True, **{"shadowed": True})` it will crash),
        # so please prefer passing search query params by name if you can.)
        **search_text_params: Dict[str, Union[str, bool, List[Union[str, bool]]]],
    ) -> List[SecurityRule]:
        # This function operates in two stages:
        #
        # 1. First it calls the base "/rule_search" endpoint with your given
        # device list (or all devices if no device list was passed) and search
        # queries to see which devices will be sub-queried.
        #
        # 1. Next, it consecutively calls the "/rule_search/{device_id}"
        # endpoint per device, and returns every rule that matches your query.

        # For whatever reason, rule_search supports a format that wants you to
        # put your search text and your other queries all together in the same
        # `search_text` URI parameter. However, actual search `str` *text* must
        # be specified first. So instead of something like this:
        #
        #     ?search_text=my cool search text&shadowed=true&action=accept
        #
        # We have to do this:
        #
        #     ?search_text=my cool search text shadowed:true action:accept
        #
        # N.B.: It seems that the API parses ':' and '%3A' into the same value,
        # so it currently unknown to me how to include a literal `':'` in the
        # text portion of an programmatic hit of this endpoint (without that
        # text portion being treated as a key:value pair).
        devices_cache = {d.id: d for d in self.get_devices()}
        if devices is None:
            devices = devices_cache.keys()
        if not isinstance(devices, Iterable):
            devices = [devices]
        _search_text_params = []
        for k, v in search_text_params.items():
            if k == "uid":
                v = sanitize_uid(v)
            _search_text_params.append(_querify(k, v))
        search_text_params = _search_text_params
        search_text_string = " ".join(search_text_params)
        if expiration_date is not None:
            if isinstance(expiration_date, Emptiness):
                string = f"{expiration_date.value}"
            else:
                string = f":{expiration_date.strftime('%Y%m%d')}"
            search_text_params.append("expirationdate" + string)

        if certification_expiration_date is not None:
            if isinstance(certification_expiration_date, Emptiness):
                string = f"{certification_expiration_date.value}"
            else:
                string = f":{certification_expiration_date.strftime('%Y%m%d')}"
            search_text_params.append("certificationexpirationdate" + string)

        if comment is not None:
            search_text_params.append(f"comment{comment.value}")

        def _chunked_rule_search(devices):
            LOGGER.debug(f"Running chunked rule search for devices: {devices}")

            params = OrderedDict(
                {
                    "devices": ",".join(str(d) for d in devices),
                    "search_text": text + " " if text is not None else "",
                }
            )
            if context:
                params["context"] = context

            params["search_text"] += search_text_string

            if shadowed is not None:
                search_text_params.append(f"shadowed:{_bool(shadowed)}")

            # N.B.: It *is* possible to save one HTTP request here if we only have
            # a single device id in `devices`, as we can skip the `/rule_search`
            # hit and just request `/rule_search/{devices[0]}` immediately, but it
            # wasn't worth the complexity of implementation as `/rule_search` is
            # plenty fast.
            rule_search_info = self.api.session.get("rule_search", params=params)

            if not rule_search_info.ok:
                try:
                    msg = rule_search_info.json().get("result").get("message")
                    rule_search_info.raise_for_status()
                except HTTPError as e:
                    raise ValueError(f"got '{msg}' from API Error: {e}")

            rule_search_info = rule_search_info.json()

            # Walrus, come save me.
            rule_search_info = rule_search_info.get("device_list")
            if rule_search_info is None:
                return
            rule_search_info = rule_search_info.get("device")
            if rule_search_info is None:
                return

            # Save me twice.
            devices = [
                {
                    "rule_count": device_info["rule_count"],
                    "device_id": device_info["device_id"],
                }
                for device_info in rule_search_info
                if device_info.get("device_id") is not None
                and device_info.get("rule_count", 0) > 0
            ]

            return devices

        total_rule_count = 0

        devices = list(devices)  # Turn dict_keys() into list for chunking below
        i = 0
        found_rules = []
        while i < len(devices):
            device_ids = devices[i : i + 50]
            i += 50

            _devices_chunk = _chunked_rule_search(device_ids)

            total_rule_count += sum([d["rule_count"] for d in _devices_chunk])

            for device_info in _devices_chunk:
                device_id = device_info["device_id"]
                device_rule_count = device_info["rule_count"]

                device = devices_cache.get(device_id)
                if device is None:
                    LOGGER.warning(
                        {
                            "message": f"There is no device known to SecureTrack with id {device_id}; perhaps it was deleted? Skipping.",
                            "device": {"id": device_id},
                        }
                    )
                    continue

                # N.B.: API results are 0-based, not one-based. So passing in a
                # `count` of 3000 will return items starting from the 3001st and so
                # forth (passing in 0 will return starting from item #1).
                params = OrderedDict(
                    {"start": 0, "count": 3000, "search_text": search_text_string}
                )
                rules_retrieved_for_this_device = 0

                while rules_retrieved_for_this_device < device_rule_count:
                    rules = self.api.session.get(
                        f"rule_search/{device.id}", params=params
                    )
                    params["start"] += params["count"]

                    if not rules.ok:
                        try:
                            msg = rules.json().get("result").get("message")
                            rules.raise_for_status()
                        except HTTPError as e:
                            raise ValueError(f"got '{msg}' from API error: {e}")
                    rules = rules.json()

                    if rules.get("rules") is None:
                        break
                    if rules["rules"].get("rule") is None:
                        break
                    if rules["rules"].get("count") is None:
                        break

                    for rule in rules["rules"]["rule"]:
                        rule = SecurityRule.kwargify(rule)
                        rule.total_rule_count = total_rule_count
                        rule.device_rule_count = device_rule_count
                        rule.device = device
                        found_rules.append(rule)

                    rules_retrieved_for_this_device += rules["rules"]["count"]
        return found_rules

    def rule_search(self, *args: tuple, **kwargs: dict) -> List[SecurityRule]:
        return self.search_rules(*args, **kwargs)

    def update_documentation(
        self, device_id: int, rule_id: int, rule_doc: Documentation
    ):
        response = self.api.session.put(
            f"devices/{device_id}/rules/{rule_id}/documentation", json=rule_doc._json
        )

        if not response.ok:
            response.raise_for_status()

    def get_device_policies(self, device: Union[int, str]) -> List[BindingPolicy]:
        device_id = self._resolve_device_id(device)

        response = self.api.session.get(f"devices/{device_id}/policies")
        if not response.ok:
            response.raise_for_status()

        _json = response.json()

        policies = get_api_node(_json, "policies", listify=True)
        to_return_policies = []
        for policy in policies:
            try:
                policy_obj = BindingPolicy.kwargify(policy)
                to_return_policies.append(policy_obj)
            except Exception as e:  # pragma: no cover
                raise ValueError(
                    f"unable to kwargify policy_json: {policy}, got error: {e}"
                )
        return to_return_policies

    def get_device_policy(self, device: Union[int, str], policy: str) -> BindingPolicy:
        policies = self.get_device_policies(device)

        for policy_obj in policies:
            if policy_obj.name == policy:
                return policy_obj

        raise ValueError("No matching policy found in given device.")

    def get_interfaces(self, device_id: int) -> List[Interface]:
        device_info = self.default.get_device(device_id)

        if device_info and device_info.vendor.name == "CHECKPOINT":
            interfaces = self.api.get_topology_interfaces_from_device_id(device_id)
            base_id = "interface"
        else:
            interfaces = self.api.get_interfaces_from_device_id(device_id)
            base_id = "interfaces.interface"

        if interfaces.status_code == 404:
            raise ValueError(f"Device {device_id} not found")
        elif interfaces.status_code == 400:
            # checkpoint devices unsupported returns 400
            raise ValueError(
                f"CheckPoint Device {device_id} not supported, use topology_interfaces"
            )
        else:
            return [
                Interface.kwargify(d)
                for d in get_api_node(interfaces.json(), base_id, listify=True)
            ]

    def get_bindable_objects(self, device_id: int) -> List[BindableObject]:
        objects = self.api.get_bindable_objects_from_device_id(device_id)
        if objects.status_code == 404:
            raise ValueError(f"Device {device_id} not found")
        else:
            return [
                BindableObject.kwargify(d)
                for d in get_api_node(objects.json(), "bindable_objects", listify=True)
            ]

    def get_topology_interfaces(
        self, device_id: int, is_generic: Optional[int] = 0
    ) -> List[TopologyInterface]:
        interfaces = self.api.get_topology_interfaces_from_device_id(
            device_id, is_generic=is_generic
        )

        return [
            TopologyInterface.kwargify(d)
            for d in get_api_node(interfaces.json(), "interface", listify=True)
        ]

    def get_generic_devices(
        self,
        name: Optional[str] = None,
        context: Optional[int] = None,
        cache: bool = True,
    ) -> List[GenericDevice]:
        if not cache:
            response = self.api.get_generic_devices(name=name, context=context)
            if not response.ok:
                try:
                    msg = response.text
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"Got {e}, with Error Message: {msg} from generic_devices API"
                    )
            else:
                generic_devices = get_api_node(
                    response.json(), "generic_devices.device", listify=True
                )
                return [GenericDevice.kwargify(d) for d in generic_devices]
        else:
            if self._generic_devices_cache.is_empty():
                self._prime_generic_devices_cache()

            if name is None:
                return self._generic_devices_cache.get_data()
            else:
                for d in self._generic_devices_cache.get_data():
                    if name == d.name:
                        return d

    def delete_generic_device(
        self, identifier: Union[int, str], update_topology: bool = False
    ) -> None:
        if isinstance(identifier, str):
            if self._generic_devices_cache.is_empty():
                self._prime_generic_devices_cache()

            device = self._generic_devices_index.get(identifier)
            if device is None:
                raise ValueError("Could not find device with specified name")

            identifier = device.id

        response = self.api.delete_generic_device(
            id=identifier, update_topology=update_topology
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error: {e}")

    def add_generic_device(
        self,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
        customer_id: Optional[int] = None,
    ) -> None:
        response = self.api.post_generic_device(
            name=name,
            configuration=configuration,
            update_topology=update_topology,
            customer_id=customer_id,
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error: {e}")

    def update_generic_device(
        self,
        id: int,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
    ) -> None:
        response = self.api.put_generic_device(
            id=id,
            configuration=configuration,
            name=name,
            update_topology=update_topology,
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error :{e}")

    def import_generic_device(
        self,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
        customer_id: Optional[int] = None,
    ):
        if self._generic_devices_cache.is_empty():
            self._prime_generic_devices_cache()

        existing_device = self._generic_devices_index.get(name)

        if existing_device is None:
            return self.add_generic_device(
                name=name,
                configuration=configuration,
                update_topology=update_topology,
                customer_id=customer_id,
            )
        else:
            return self.update_generic_device(
                id=existing_device.id,
                name=name,
                configuration=configuration,
                update_topology=False,
            )

    def sync_topology(self, full_sync: bool = False):
        response = self.api.session.post(
            "topology/synchronize", params={"full_sync": full_sync}
        )

        if response.ok:
            return
        elif response.status_code == 401:
            raise ValueError("Authentication error")
        elif response.status_code == 500:
            raise ValueError("Error synchronizing topology model")
        else:
            response.raise_for_status()

    def get_topology_sync_status(self) -> TopologySyncStatus:
        response = self.api.session.get("topology/synchronize/status")

        if response.ok:
            status = get_api_node(response.json(), "status")
            status = TopologySyncStatus.kwargify(status)
            return status
        elif response.status_code == 401:
            raise ValueError("Authentication error")
        elif response.status_code == 500:
            raise ValueError("Error getting synchronization process")
        else:
            response.raise_for_status()

    def add_generic_interface(
        self,
        device: Union[str, int, Device],
        name: str,
        vrf: str,
        mpls: bool,
        unnumbered: bool,
        type: Union[str, None] = None,
        ip: Optional[str] = None,
        mask: Optional[str] = None,
    ) -> None:
        """
        Add a generic interface

        Method: POST
        URL: /securetrack/api/topology/generic/interface
        Version: 20+

        Notes:
            None is an acceptable value for the property named "type"
            When unnumbered = True, ip and mask should be empty/None

        Usage:
            # Example #1:
            st.add_generic_interface(
                device=1,
                name="newApo1",
                vrf="V101-PAL",
                mpls=False,
                unnumbered=False,
                type="external",
                ip="100.103.33.33",
                mask="255.255.255.0",
            )

            # Example #2:
            st.add_generic_interface(
                device=1,
                name="newApo1",
                vrf="V101-PAL",
                mpls=False,
                unnumbered=True,
                type="internal"
            )
        """
        try:
            device_id = self._resolve_device_id(device)
            if unnumbered:
                if ip or mask:
                    raise ValueError(
                        "Unnumbered interfaces cannot contain an ip or mask."
                    )
            else:
                if not ip or not mask:
                    raise ValueError("Numbered interfaces must have an ip and mask.")
            interface = GenericInterface(
                device_id=device_id,
                name=name,
                ip=IPAddress(ip) if ip else None,
                mask=IPAddress(mask) if mask else None,
                vrf=vrf,
                mpls=mpls,
                unnumbered=unnumbered,
                type=type,
            )
            data = {"GenericInterfaces": [interface._json]}
            response = self.api.session.post("topology/generic/interface", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic Interface(s): {e}")

    def get_generic_interface(self, int_id: int) -> GenericInterface:
        """
        Get a GenericInterface object by interface id

        Method: GET
        URL: /securetrack/api/topology/generic/interface/{inId}
        Version: 20+

        Usage:
            generic_interface = st.get_generic_interface(42)

        """
        try:
            response = self.api.session.get(f"topology/generic/interface/{int_id}")
            response.raise_for_status()
            interface = get_api_node(response.json(), "GenericInterface")
            return GenericInterface.kwargify(interface)
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic Interface: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Interface: {e}")

    def get_generic_interfaces(
        self, device: Union[str, int, Device]
    ) -> List[GenericInterface]:
        """
        Get a list of GenericInterface objects using management id

        Method: GET
        URL: /securetrack/api/topology/generic/interface/mgmt/{mgmtId}
        Version: 20+

        Usage:
            generic_interfaces = st.get_generic_interfaces(1)

        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                f"topology/generic/interface/mgmt/{device_id}"
            )
            response.raise_for_status()
            return [
                GenericInterface.kwargify(d)
                for d in get_api_node(
                    response.json(), "GenericInterfaces", listify=True
                )
            ]
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic Interface: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Interfaces: {e}")

    def update_generic_interface(self, interface: GenericInterface) -> None:
        """
        Update a GenericInterface object

        Method: PUT
        URL: /securetrack/api/topology/generic/interface
        Version: 20+

        Usage:
            interface1 = st.get_generic_interface(42)
            interface1.ip = IPAddress("100.103.33.34")
            st.update_generic_interface(interface1)

        """
        try:
            data = {"GenericInterfaces": [interface._json]}
            response = self.api.session.put("topology/generic/interface", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Generic Interface(s): {e}")

    def delete_generic_interface(self, int_id: Union[int, str]) -> None:
        """
        Delete a generic interface

        Method: DELETE
        URL: /securetrack/api/topology/generic/interface/{inId}
        Version: 20+

        Usage:
            st.delete_generic_interface(42)

        """
        try:
            response = self.api.session.delete(f"topology/generic/interface/{int_id}")
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Interface: {e}")

    def delete_generic_interfaces(self, device: Union[str, int, Device]) -> None:
        """
        Delete a list generic interfaces for a specific management id

        Method: DELETE
        URL: /securetrack/api/topology/generic/interface/mgmt/{mgmtId}
        Version: 20+

        Usage:
            st.delete_generic_interfaces(1)

        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/interface/mgmt/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Interfaces: {e}")

    def add_generic_route(
        self,
        device: Union[str, int, Device],
        destination: str,
        mask: str,
        interface_name: str,
        next_hop: str,
        next_hop_type: str,
        vrf: str,
    ) -> None:
        """
        Add a generic route

        Method: POST
        URL: /securetrack/api/topology/generic/route/
        Version: 20+

        Usage:
            st.add_generic_route(
                device=2,
                destination="10.4.4.4",
                mask="255.0.0.0",
                interface_name="",
                next_hop="AA",
                next_hop_type="VR",
                vrf="V102-YO"
            )
        """
        try:
            device_id = self._resolve_device_id(device)
            if next_hop_type == "IP":
                try:
                    next_hop = str(IPAddress(next_hop))
                except Exception:
                    raise ValueError(
                        "'next_hop' must be a valid IP Address when next_hop_type is 'IP'"
                    )

            route = GenericRoute(
                device_id=device_id,
                destination=IPAddress(destination),
                mask=IPAddress(mask),
                interface_name=interface_name,
                next_hop=next_hop,
                next_hop_type=next_hop_type,
                vrf=vrf,
            )
            data = {"GenericRoutes": [route._json]}
            response = self.api.session.post("topology/generic/route", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic Routes: {e}")

    def get_generic_route(self, int_id: int) -> GenericRoute:
        """
        Get a GenericRoute object by route id

        Method: GET
        URL: /securetrack/api/topology/generic/route/{routeId}
        Version: 20+

        Usage:
            generic_route = st.get_generic_route(1)
        """
        try:
            response = self.api.session.get(f"topology/generic/route/{int_id}")
            response.raise_for_status()
            route = get_api_node(response.json(), "GenericRoute")
            return GenericRoute.kwargify(route)
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic Route: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Route: {e}")

    def get_generic_routes(self, device: Union[str, int, Device]) -> List[GenericRoute]:
        """
        Get a list of GenericRoute objects by management id

        Method: GET
        URL: /securetrack/api/topology/generic/route/mgmt/{mgmtId}
        Version: 20+

        Usage:
            generic_route = st.get_generic_routes(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(f"topology/generic/route/mgmt/{device_id}")
            response.raise_for_status()
            return [
                GenericRoute.kwargify(d)
                for d in get_api_node(response.json(), "GenericRoutes", listify=True)
            ]
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic Route: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Routes: {e}")

    def update_generic_route(self, route: GenericRoute) -> None:
        """
        Update a GenericRoute object

        Method: PUT
        URL: /securetrack/api/topology/generic/route/
        Version: 20+

        Usage:
            route = st.get_generic_route(1)
            route.destination = IPAddress("10.4.4.5")
            st.update_generic_route(route)
        """
        try:
            data = {"GenericRoutes": [route._json]}
            response = self.api.session.put("topology/generic/route", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Generic Routes: {e}")

    def delete_generic_route(self, int_id: int) -> None:
        """
        Delete a generic route

        Method: DELETE
        URL: /securetrack/api/topology/generic/route/
        Version: 20+

        Usage:
            st.delete_generic_route(1)
        """
        try:
            response = self.api.session.delete(f"topology/generic/route/{int_id}")
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Route: {e}")

    def delete_generic_routes(self, device: Union[str, int, Device]) -> None:
        """
        Delete generic routes for a specified management id

        Method: DELETE
        URL: /securetrack/api/topology/generic/route/mgmt/{mgmtId}
        Version: 20+

        Usage:
            st.delete_generic_routes(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/route/mgmt/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Routes: {e}")

    def add_generic_vpn(
        self,
        generic: bool,
        device: Union[str, int, Device],
        interface_name: str,
        vpn_name: str,
        tunnel_source_ip_addr: str,
        tunnel_dest_ip_addr: str,
    ) -> None:
        """
        Add a generic vpn

        Method: POST
        URL: /securetrack/api/topology/generic/vpn
        Version: 20+

        Usage:
            st.add_generic_vpn(
                generic=True,
                device=1,
                interface_name="new33",
                vpn_name=None,
                tunnel_source_ip_addr="3.3.3.33",
                tunnel_dest_ip_addr="1.1.1.11"
            )
        """
        try:
            device_id = self._resolve_device_id(device)
            vpn = GenericVpn(
                generic=generic,
                device_id=device_id,
                interface_name=interface_name,
                vpn_name=vpn_name,
                tunnel_source_ip_addr=IPAddress(tunnel_source_ip_addr),
                tunnel_dest_ip_addr=IPAddress(tunnel_dest_ip_addr),
            )
            data = {"GenericVpns": [vpn._json]}
            response = self.api.session.post("topology/generic/vpn", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic VPN: {e}")

    def get_generic_vpn(self, int_id: int) -> GenericVpn:
        """
        Get a GenericVpn object by id

        Method: GET
        URL: /securetrack/api/topology/generic/vpn/{vpnId}
        Version: 20+

        Usage:
            vpn = st.get_generic_vpn(1)
        """
        try:
            response = self.api.session.get(f"topology/generic/vpn/{int_id}")
            response.raise_for_status()
            vpn = get_api_node(response.json(), "GenericVpn")
            return GenericVpn.kwargify(vpn)
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic VPN: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic VPN: {e}")

    def get_generic_vpns(
        self, device: Union[str, int, Device], generic: bool
    ) -> List[GenericVpn]:
        """
        Get a list of GenericVpn objects for management/genericDevice Id.

        Method: GET
        URL: /securetrack/api/topology/generic/vpn/device/{deviceId}
        Version: 20+

        Usage:
            vpns = st.get_generic_vpns(1, generic=True)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                f"topology/generic/vpn/device/{device_id}",
                params={"generic": str(generic).lower()},
            )
            response.raise_for_status()
            return [
                GenericVpn.kwargify(d)
                for d in get_api_node(response.json(), "GenericVpns", listify=True)
            ]
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Generic VPN(s): {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic VPNs: {e}")

    def update_generic_vpn(self, vpn: GenericVpn) -> None:
        """
        Update a generic vpn

        Method: PUT
        URL: /securetrack/api/topology/generic/vpn
        Version: 20+

        Usage:
            generic_vpn = st.get_generic_vpn(1)
            generic_vpn.tunnel_source_ip_addr = IPAddress("3.3.3.34")
            st.update_generic_vpn(generic_vpn)
        """
        try:
            data = {"GenericVpns": [vpn._json]}
            response = self.api.session.put("topology/generic/vpn", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Generic Vpns: {e}")

    def delete_generic_vpn(self, int_id: int) -> None:
        """
        Delete a generic vpn by id

        Method: DELETE
        URL: /securetrack/api/topology/generic/vpn/{vpnId}
        Version: 20+

        Usage:
            st.delete_generic_vpn(1)
        """
        try:
            response = self.api.session.delete(f"topology/generic/vpn/{int_id}")
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Vpn: {e}")

    def delete_generic_vpns(self, device: Union[str, int, Device]) -> None:
        """
        Delete a list of generic vpn's by management/genericDevice id

        Method: DELETE
        URL: /securetrack/api/topology/generic/vpn/device/{deviceId}
        Version: 20+

        Usage:
            st.delete_generic_vpns(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/vpn/device/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Vpns: {e}")

    def add_generic_transparent_firewall(
        self,
        output_l3_device_id: int,
        output_l3_is_generic_device: bool,
        output_l3_interface_name: str,
        layer2_device_id: int,
        input_l2_interface_name: str,
        output_l2_interface_name: str,
        input_l3_device_id: int,
        input_l3_is_generic_device: bool,
        input_l3_interface_name: str,
    ) -> None:
        """
        Add a generic transparent firewall

        Method: POST
        URL: /securetrack/api/topology/generic/transparentfw
        Version: 20+

        Usage:
            st.add_generic_transparent_firewalls(
                output_l3_device_id=22,
                output_l3_is_generic_device=False,
                output_l3_interface_name="FastEthernet0/0",
                layer2_device_id=21,
                input_l2_interface_name="inside",
                output_l2_interface_name="outside",
                input_l3_device_id=20,
                input_l3_is_generic_device=False,
                input_l3_interface_name="Loopback0")
        """
        try:
            firewall = GenericTransparentFirewall(
                output_l3_device_id=output_l3_device_id,
                output_l3_is_generic_device=output_l3_is_generic_device,
                output_l3_interface_name=output_l3_interface_name,
                layer2_device_id=layer2_device_id,
                input_l2_interface_name=input_l2_interface_name,
                output_l2_interface_name=output_l2_interface_name,
                input_l3_device_id=input_l3_device_id,
                input_l3_is_generic_device=input_l3_is_generic_device,
                input_l3_interface_name=input_l3_interface_name,
            )
            data = {"TransparentFirewalls": [firewall._json]}
            response = self.api.session.post(
                "topology/generic/transparentfw", json=data
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic Transparent Firewalls: {e}")

    def get_generic_transparent_firewalls(
        self, device: Union[str, int, Device], generic: bool
    ) -> List[GenericTransparentFirewall]:
        """
        Get a list of GenericTransparentFirewall objects for a generic or monitored device using device id

        Method: GET
        URL: /securetrack/api/topology/generic/transparentfw/device/{deviceId}
        Version: 20+

        Usage:
            # Example #1: Get generic transparent firewalls for a monitored device
            firewalls = st.get_generic_transparent_firewalls(1, False)

            # Example #2: Get generic transparent firewalls for a generic device
            firewalls = st.get_generic_transparent_firewalls(1, True)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                f"topology/generic/transparentfw/device/{device_id}",
                params={"generic": str(generic).lower()},
            )
            response.raise_for_status()
            return [
                GenericTransparentFirewall.kwargify(d)
                for d in get_api_node(
                    response.json(), "TransparentFirewalls", listify=True
                )
            ]
        except JSONDecodeError as e:
            raise ValueError(
                f"Error converting JSON to Generic Transparent firewall: {e}"
            )
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Transparent Firewalls: {e}")

    def update_generic_transparent_firewalls(
        self, firewalls: List[GenericTransparentFirewall]
    ) -> None:
        """
        Update a list of generic transparent firewall

        Method: PUT
        URL: /securetrack/api/topology/generic/transparentfw
        Version: 20+

        Usage:
            edited_firewalls = []
            firewall = st.get_generic_transparent_firewalls(1, generic=False)[0]
            firewall.output_l3_interface_name = "10GBEthernet0/0"
            edited_firewalls.append(firewall)
            st.update_generic_transparent_firewalls(edited_firewalls)
        """
        try:
            data = {"TransparentFirewalls": [fw._json for fw in firewalls]}
            response = self.api.session.put("topology/generic/transparentfw", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Generic Transparent Firewalls: {e}")

    def delete_generic_transparent_firewall(self, layer_2_data_id: int) -> None:
        """
        Delete a generic transparent firewall by layer2DataId

        Method: DELETE
        URL: /securetrack/api/topology/generic/transparentfw/{layer2DataId}
        Version: 20+

        Usage:
            st.delete_generic_transparent_firewall(17)
        """
        try:
            response = self.api.session.delete(
                f"topology/generic/transparentfw/{layer_2_data_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Transparent Firewall: {e}")

    def delete_generic_transparent_firewalls(
        self, device: Union[str, int, Device]
    ) -> None:
        """
        Delete a list of generic transparent firewalls for a specific device by device id

        Method: DELETE
        URL: /securetrack/api/topology/generic/transparentfw/device/{deviceId}
        Version: 20+

        Usage:
            st.delete_generic_transparent_firewalls(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/transparentfw/device/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Transparent Firewalls: {e}")

    def add_generic_ignored_interface(
        self, interface_name: str, device: Union[str, int, Device], ip: str
    ) -> None:
        """
        Add a generic ignored interface

        Method: POST
        URL: /securetrack/api/topology/generic/ignoredinterface
        Version: 20+

        Usage:
            st.add_generic_ignored_interface(
                interface_name="eth2",
                device=10,
                ip="0.0.0.0"
            )
        """
        try:
            device_id = self._resolve_device_id(device)
            interface = GenericIgnoredInterface(
                interface_name=interface_name, device_id=device_id, ip=IPAddress(ip)
            )
            data = {"IgnoredInterfaces": [interface._json]}
            response = self.api.session.post(
                "topology/generic/ignoredinterface", json=data
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic Ignored Interfaces: {e}")

    def get_generic_ignored_interfaces(
        self, device: Union[str, int, Device]
    ) -> List[GenericIgnoredInterface]:
        """
        Get a list of GenericIgnoredInterface objects by management id

        Method: GET
        URL: /securetrack/api/topology/generic/ignoredinterface/mgmt/{mgmtId}
        Version: 20+

        Usage:
            generic_ignored_interfaces = st.get_generic_ignored_interfaces(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                f"topology/generic/ignoredinterface/mgmt/{device_id}"
            )
            response.raise_for_status()
            return [
                GenericIgnoredInterface.kwargify(d)
                for d in get_api_node(
                    response.json(), "IgnoredInterfaces", listify=True
                )
            ]
        except JSONDecodeError as e:
            raise ValueError(
                f"Error converting JSON to Generic Ignored Interface(s): {e}"
            )
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Ignored Interfaces: {e}")

    def delete_generic_ignored_interfaces(
        self, device: Union[str, int, Device]
    ) -> None:
        """
        Delete all GenericIgnoredInterface objects for a specific management id

        Method: DELETE
        URL: /securetrack/api/topology/generic/ignoredinterface/mgmt/{mgmtId}
        Version: 20+

        Usage:
            st.delete_generic_ignored_interfaces(1)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/ignoredinterface/mgmt/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Ignored Interfaces: {e}")

    def add_generic_interface_customer_tag(
        self,
        generic: bool,
        device: Union[str, int, Device],
        interface_name: str,
        customer_id: int,
    ) -> None:
        """
        Add a generic interface customer tag

        Method: POST
        URL: /securetrack/api/topology/generic/interfacecustomer
        Version: 20+

        Usage:
            st.add_generic_interface_customer_tag(
                generic=False,
                device=5,
                interface_name="port4.1",
                customer_id=3
            )
        """
        try:
            device_id = self._resolve_device_id(device)
            interface_customer_tag = GenericInterfaceCustomerTag(
                generic=generic,
                device_id=device_id,
                interface_name=interface_name,
                customer_id=customer_id,
            )
            data = {"InterfaceCustomerTags": [interface_customer_tag._json]}
            response = self.api.session.post(
                "topology/generic/interfacecustomer", json=data
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Generic Interface Customer Tags: {e}")

    def get_generic_interface_customer_tag(
        self, int_cust_id: int
    ) -> GenericInterfaceCustomerTag:
        """
        Get a GenericInterfaceCustomer object for a specified customer id

        Method: GET
        URL:  /securetrack/api/topology/generic/interfacecustomer/{interfaceCustomerId}
        Version: 20+

        Usage:
            generic_interface_customer_tag = st.get_generic_interface_customer_tag(1)
        """
        try:
            response = self.api.session.get(
                f"topology/generic/interfacecustomer/{int_cust_id}"
            )
            response.raise_for_status()
            interface_customer = get_api_node(response.json(), "InterfaceCustomerTag")
            return GenericInterfaceCustomerTag.kwargify(interface_customer)
        except JSONDecodeError as e:
            raise ValueError(
                f"Error converting JSON to Generic Interface Customer: {e}"
            )
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Interface Customer Tag: {e}")

    def get_generic_interface_customer_tags(
        self, device: Union[str, int, Device], generic: bool
    ) -> List[GenericInterfaceCustomerTag]:
        """
        Get a list of GenericInterfaceCustomerTag objects for a specified device id

        Method: GET
        URL:  /securetrack/api/topology/generic/interfacecustomer/device/{deviceId}
        Version: 20+

        Usage:
            # Example #1: Get tags for a generic device
            generic_interface_customer_tags = st.get_generic_interface_customer_tags(5, True)

            # Example #2: Get tags for a monitored device
            generic_interface_customer_tags = st.get_generic_interface_customers_tags(8, False)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                f"topology/generic/interfacecustomer/device/{device_id}",
                params={"generic": str(generic).lower()},
            )
            response.raise_for_status()
            return [
                GenericInterfaceCustomerTag.kwargify(d)
                for d in get_api_node(
                    response.json(), "InterfaceCustomerTags", listify=True
                )
            ]
        except JSONDecodeError as e:
            raise ValueError(
                f"Error converting JSON to Generic Interface Customer Tags: {e}"
            )
        except HTTPError as e:
            raise ValueError(f"Error Getting Generic Interface Customer Tags: {e}")

    def update_generic_interface_customer_tag(
        self, interface_customer_tag: GenericInterfaceCustomerTag
    ) -> None:
        """
        Update a GenericInterfaceCustomerTag object

        Method: PUT
        URL: /securetrack/api/topology/generic/interfacecustomer
        Version: 20+

        Usage:
            gen_interface_customer_tag = st.get_generic_interface_customer_tag(73)
            gen_interface_customer_tag.interface_name = "port7"
            st.update_generic_interface_customer_tag(gen_interface_customer_tag)
        """
        try:
            data = {"InterfaceCustomerTags": [interface_customer_tag._json]}
            response = self.api.session.put(
                "topology/generic/interfacecustomer", json=data
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Generic Interface Customer Tag: {e}")

    def delete_generic_interface_customer_tag(self, int_cust_id: int) -> None:
        """
        Delete a GenericInterfaceCustomerTag object for a specified interface customer id

        Method: DELETE
        URL:  /securetrack/api/topology/generic/interfacecustomer/{interfaceCustomerId}
        Version: 20+

        Usage:
            st.delete_generic_interface_customer_tag(1)
        """
        try:
            response = self.api.session.delete(
                f"topology/generic/interfacecustomer/{int_cust_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Interface Customer Tag: {e}")

    def delete_generic_interface_customer_tags(
        self, device: Union[str, int, Device]
    ) -> None:
        """
        Delete all GenericInterfaceCustomerTags objects for a specified device id

        Method: DELETE
        URL: /securetrack/api/topology/generic/interfacecustomer/device/{deviceId}
        Version: 20+

        Usage:
            st.delete_generic_interface_customer_tags(5)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.delete(
                f"topology/generic/interfacecustomer/device/{device_id}"
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Generic Interface Customer Tags: {e}")

    def get_topology_mode(self, device: Union[int, str, Device]) -> TopologyMode:
        """
        Get a TopologyMode object for specified device using device id, device name, or device object

        Method: GET
        URL:  /securetrack/api/topology/topology_mode
        Version: 23-1+

        Usage:
            topology_mode = st.get_topology_mode(5)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.get(
                "topology/topology_mode",
                params={"mgmtId": device_id},
            )
            response.raise_for_status()
            response_json = response.json()
            return [TopologyMode.kwargify(response_json["topology_mode"])]
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Topology Mode: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Topology Mode: {e}")

    def update_topology_mode(
        self, device: Union[int, str, Device], is_enabled: bool
    ) -> TopologyMode:
        """
        Update (Enable or Disable) Topology Mode for the specified device

        Method: PUT
        URL:  /securetrack/api/topology/topology_mode
        Version: 23-1+

        Usage:
           st.update_topology_mode(5, True)
        """
        try:
            device_id = self._resolve_device_id(device)
            response = self.api.session.put(
                "topology/topology_mode",
                params={"mgmtId": device_id, "isEnabled": str(is_enabled).lower()},
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Topology Mode: {e}")

    def add_join_cloud(self, name: str, clouds: List[int]) -> None:
        """
        Add a JoinCloud object

        Method: POST
        URL:  /securetrack/api/topology/join/clouds/
        Version: 20+

        Usage:
            st.add_join_cloud(
                name="Yami2",
                clouds=[12,30,46]
            )
        """
        try:
            join_cloud = JoinCloud(name=name, clouds=clouds)
            data = {"JoinCloud": join_cloud._json}
            response = self.api.session.post("topology/join/clouds", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Adding Join Cloud: {e}")

    def get_join_cloud(self, cloud_id: Union[int, str]) -> JoinCloud:
        """
        Get a JoinCloud object for a specified cloud id

        Method: GET
        URL:  /securetrack/api/topology/join/clouds/{cloudId}
        Version: 20+

        Usage:
            join_cloud = st.get_join_cloud(67)
        """
        try:
            response = self.api.session.get(f"topology/join/clouds/{cloud_id}")
            response.raise_for_status()
            return JoinCloud.kwargify(response.json())
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Join Cloud: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Join Cloud: {e}")

    def update_join_cloud(self, join_cloud: JoinCloud) -> None:
        """
        Update a JoinCloud object

        Method: PUT
        URL:  /securetrack/api/topology/join/clouds/
        Version: 20+

        Usage:
            join_cloud = st.get_join_cloud(67)
            join_cloud.name = "Yami2"
            st.update_join_cloud(join_cloud)
        """
        try:
            data = {"JoinCloud": join_cloud._json}
            response = self.api.session.put("topology/join/clouds", json=data)
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Updating Join Cloud: {e}")

    def delete_join_cloud(self, cloud_id: Union[int, str]) -> None:
        """
        Delete a JoinCloud object

        Method: DELETE
        URL:  /securetrack/api/topology/join/clouds/{cloudId}
        Version: 20+

        Usage:
            st.delete_join_cloud(67)
        """
        try:
            response = self.api.session.delete(f"topology/join/clouds/{cloud_id}")
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error Deleting Join Cloud: {e}")

    def get_change_windows(
        self, context: Optional[int] = None
    ) -> Iterable[ChangeWindow]:
        """
        Method: GET
        URL: /securetrack/api/change_windows
        Version: R22-2+

        Usage:
            change_windows = st.get_change_windows()
        """

        url = "change_windows"
        api_node = "change_windows.change_window"
        if context:
            params = {"context": context}
        else:
            params = None
        pager = Pager(
            self.api,
            url,
            api_node,
            "get_change_windows",
            ChangeWindow.kwargify,
            params=params,
        )
        return pager

    def get_change_window_tasks(
        self, uid: str, context: Optional[int] = None
    ) -> List[ChangeWindowTask]:
        """
        Method: GET
        URL: /securetrack/api/change_windows/{uid}/tasks
        Version: R22-2+

        Usage:
            change_window_tasks = st.get_change_window_tasks('07c230ce-2dec-4109-a0db-33ff45ba1057')
        """
        try:
            url = f"change_windows/{uid}/tasks"
            response = self.api.session.get(url, params={"context": context})
            response.raise_for_status()
            response_json = response.json()
            api_node = get_api_node(response_json, "commit_tasks.commit_task")
            change_window_tasks = [ChangeWindowTask.kwargify(node) for node in api_node]
            return change_window_tasks
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving change_window_tasks: {e}") from e

    def get_change_window_task(self, uid: str, task_id: int) -> ChangeWindowTask:
        """
        Method: GET
        URL: /securetrack/api/change_windows/{uid}/tasks/{task_id}
        Version: R22-2+

        Usage:
            change_window_task = st.get_change_window_task('07c230ce-2dec-4109-a0db-33ff45ba1057', 197)
        """
        try:
            url = f"change_windows/{uid}/tasks/{task_id}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            api_node = get_api_node(response_json, "commit_task")
            change_window_task = ChangeWindowTask.kwargify(api_node)
            return change_window_task
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving change_window_task: {e}") from e

    def get_device_applications(
        self, device: Union[int, str], context: Union[int, str, Domain, None] = None
    ) -> Iterable[Application]:
        """
        Method: GET
        URL: /securetrack/api/devices{id}/applications
        Version: R22-2+

        Usage:
            applications = st.get_device_applications(8)

        Notes:
            Fetches list of applications defined on device given by ID. This API is currently supported for Palo Alto Networks firewalls.
            In Panorama NG, overrides property in returned ApplicationDTO will be set to true, if the application overrides an original value.
        """
        context = self._get_domain_id(context)
        device_id = self._resolve_device_id(device)
        url = f"devices/{device_id}/applications"
        api_node = "applications.application"
        pager = Pager(
            self.api,
            url,
            api_node,
            "get_device_applications",
            classify_application,
            params={"context": context} if context else {},
        )
        return pager

    def get_device_rule_last_usage(
        self, device: Union[int, str]
    ) -> List[RuleLastUsage]:
        """
        Get last hit dates for all rules in a given device.
        For Palo Alto firewalls, this also returns last hits for users and applications in the rule.

        Method: GET
        URL: /securetrack/api/rule_last_usage/find_all/{device_id}
        Version: R22-2+

        Usage:
        device_findall_last_usage = st.get_device_rule_last_usage(20)
        """
        device_id = self._resolve_device_id(device)

        try:
            url = f"rule_last_usage/find_all/{device_id}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            rule_last_usage_list = [
                RuleLastUsage.kwargify(item)
                for item in response_json["rule_last_usage"]
            ]
            return rule_last_usage_list
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except RequestException as e:
            raise ValueError(f"Error retrieving rule_last_usage: {e}") from e

    def get_device_rule_last_usage_for_uid(
        self, device: Union[int, str], uid: str
    ) -> RuleLastUsage:
        """
        Get last hit dates for all rules in a given device.
        For Palo Alto firewalls, this also returns last hits for users and applications in the rule.
        The rule_uid is the value from the uid field returned by the /rules API: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

        Method: GET
        URL: /securetrack/api/rule_last_usage/find/{device_id}/{rule_uid}
        Version: R22-2+

        Usage:
            device_find_last_usage = st.get_device_rule_last_usage_for_uid(20,"ea9db13e-d058-45c6-a2f0-cd731027c22b")
        """
        device_id = self._resolve_device_id(device)

        try:
            url = f"rule_last_usage/find/{device_id}/{uid}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            rule_last_usage = RuleLastUsage.kwargify(response_json["rule_last_usage"])
            return rule_last_usage
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except RequestException as e:
            raise ValueError(f"Error retrieving rule_last_usage: {e}")

    def get_properties(self) -> Properties:
        """
        Method: GET
        URL: /securetrack/api/properties
        Version: R22-2+

        Usage:
            properties = st.get_properties()
        """
        try:
            url = "properties"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            api_node = get_api_node(response_json, "properties")
            return Properties.kwargify(api_node)
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving properties: {e}") from e

    def set_license_notification_days(self, days):
        """
        Method: PUT
        URL: /securetrack/api/properties
        Version: R22-2+

        Usage:
            st.set_license_notification_days(100)
        """
        property = Property(key="LICENSE_ABOUT_TO_EXPIRE_THRESHOLD", value=days)
        properties = Properties(general_properties=[property])
        try:
            url = "properties"
            properties_body = {
                "properties": {
                    "general_properties": properties._json["general_properties"]
                },
            }
            response = self.api.session.put(url, json=properties_body)
            response.raise_for_status()
        except RequestException as e:
            raise ValueError(f"Error putting properties: {e}") from e

    def _generic_list_fetch(self, url, cls, key, entity_name):
        try:
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            objects = [cls.kwargify(obj) for obj in response_json[key]]
            return objects
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except HTTPError as e:
            try:
                msg = e.response.json()
                message = msg.get("result", {}).get("message", "")
                code = msg.get("result", {}).get("code", "")

                if message and code:
                    raise ValueError(
                        f"Error retrieving {entity_name}: ({code}) {message}"
                    ) from e
                else:
                    raise ValueError(f"Error retrieving {entity_name}: {e}") from e
            except JSONDecodeError:
                raise ValueError(f"Error retrieving {entity_name}: {e}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving {entity_name}: {e}")

    def get_time_objects(
        self, revision: int, time_ids: List[int] = None
    ) -> List[TimeObject]:
        """
        Retrieve a list of TimeObject objects for a given revision id, optionally specifying which time object ids

        Method: GET
        URL: /securetrack/api/revisions/{id:[0-9]+}/time_objects
        Version: R22-2+

        Usage:
            # Example #1:
            time_objects = st.get_time_objects(2812)

            # Example #2:
            time_objects = st.get_time_objects(2812, [388, 390])
        """
        url = f"revisions/{revision}/time_objects"
        if time_ids:
            ids = ",".join([str(time_id) for time_id in time_ids])
            url += "/{}".format(ids)

        return self._generic_list_fetch(url, TimeObject, "time_object", "time_objects")

    def get_time_objects_by_device(self, device_id: int) -> List[TimeObject]:
        """
        Retrieve a list of TimeObject objects for a device id

        Method: GET
        URL: /securetrack/api/devices/{id:[0-9]+}/time_objects
        Version: R22-2+

        Usage:
            # Example #1:
            time_objects = st.get_time_objects_by_device(5)

            # Example #2:
            device = st.get_device(5)
            time_objects = device.get_time_objects()
        """

        return self._generic_list_fetch(
            f"devices/{device_id}/time_objects",
            TimeObject,
            "time_object",
            "time_objects",
        )

    def get_licenses(self) -> Union[List[License], TieredLicense]:
        """
        Gets a TieredLicense object or a List of License objects

        URL: /securetrack/api/licenses
        Version: R21-3+

        Usage:
            licenses = st.get_licenses()

        """
        try:
            license = self.get_tiered_license()
            return license
        except Exception as e:
            # We get a 404 here when there is no tiered license
            pass

        try:
            url = "licenses"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            if "license" in response_json:
                # When this happens it contains an error telling you to call Tiered license instead
                return []
            elif "licenses" in response_json:
                return [
                    License.kwargify(lic)
                    for lic in get_api_node(
                        response_json, "licenses.license", listify=True
                    )
                ]
            else:
                return []
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving licenses: {e}") from e

    def get_license(
        self, license_type: Union[int, str] = "full", sku: Optional[str] = None
    ) -> Union[TieredLicense, License, None]:
        """
        URL: /securetrack/api/licenses/{id:[0-9]+|current|full|audit|evaluation}
        Version: R21-3+

        Usage:
            license = st.get_license("full")

        """
        if license_type == "tiered-license":
            if sku:
                raise ValueError(
                    "sku is not supported when license_type is 'tiered-license'"
                )

            return self.get_tiered_license()

        try:
            url = f"licenses/{license_type}"
            response = self.api.session.get(
                url, params={"sku": sku}, headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            response_json = response.json()
            license = response_json["license"]
            if license and "unsupportedLicense" not in license:
                return License.kwargify(response_json["license"])

            return None
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving license: {e}") from e

    def get_tiered_license(self) -> TieredLicense:
        """
        URL: /securetrack/api/licenses/tiered-license
        Version: R23-2+

        Usage:
            tiered_license = st.get_tiered_license()

        """
        try:
            url = "licenses/tiered-license"
            response = self.api.session.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            response_json = response.json()
            return TieredLicense.kwargify(response_json)
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding json: {response.text}") from e
        except RequestException as e:
            raise ValueError(f"Error retrieving license: {e}") from e

    def get_usp_policies(
        self,
        context: Optional[int] = None,
        get_global: Optional[bool] = False,
        aurora_data: bool = True,
    ) -> List[SecurityZoneMatrix]:
        """
        Method: GET
        URL: /securetrack/api/security_policies
        URL: /securetrack/api/security_policies/global
        Version: 20+, aurora_data/ignoreSecureTrack2Data supported from 21+

        Notes:
            The aurora_data parameter when set to False returns data that was migrated from a TOS Classic installation.

        Usage:
            # Example 1:
            usp_policies = st.get_usp_policies()

            # Example 2:
            global_usp_policies = st.get_usp_policies(get_global=True)
        """
        try:
            ignoreSecureTrack2Data = not aurora_data
            if get_global is False:
                response = self.api.session.get(
                    "security_policies",
                    params={
                        "context": context,
                        "ignoreSecureTrack2Data": str(ignoreSecureTrack2Data).lower(),
                    },
                )
            else:
                # ignore context because it isn't needed/supported by this API endpoint
                response = self.api.session.get(
                    "security_policies/global",
                    params={
                        "ignoreSecureTrack2Data": str(ignoreSecureTrack2Data).lower()
                    },
                )
            response.raise_for_status()
            json = response.json()
            usp_list = [
                SecurityZoneMatrix.kwargify(usp)
                for usp in get_api_node(
                    json,
                    "SecurityPolicyList.securityPolicies.securityPolicy",
                    listify=True,
                )
            ]
            return usp_list
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except RequestException as e:
            raise ValueError(f"Error retrieving USP Policies : {e}")

    def export_usp_policy(
        self,
        identifier: int,
        context: Optional[int] = None,
        aurora_data: Optional[bool] = True,
    ) -> CSVData:
        """
        Method: GET
        URL: /securetrack/api/security_policies/{id:[0-9]+}/export
        Version: 20+, aurora_data/ignoreSecureTrack2Data supported from 21+

        Notes:
            The aurora_data parameter when set to False returns data that was migrated from a TOS Classic installation.

            Lines are new line delimited, and each line is comma delimitted
            First line will be column headers. Here's example output:
                from domain,from zone,to domain,to zone,severity,access type,services/applications,rule properties,flows,description
                All Domains,Amsterdam,All Domains,AWS_DB,critical,allow only,tcp 161;tcp 162;tcp 10161;tcp 10162;udp 161;udp 162;udp 10161;udp 10162,IS_LOGGED,,

        Usage:
            csv_string = st.export_usp_policy(5)
            #implement your own "write to file" or "download" code here
        """
        try:
            ignoreSecureTrack2Data = not aurora_data
            response = self.api.session.get(
                f"security_policies/{identifier}/export",
                params={
                    "context": context,
                    "ignoreSecureTrack2Data": str(ignoreSecureTrack2Data).lower(),
                },
            )
            response.raise_for_status()
            return response.text
        except RequestException as e:
            raise ValueError(f"Error getting string/csv export of USP Policy: {e}")

    def delete_usp_policy(
        self,
        id: int,
        context: Optional[int] = None,
        aurora_data: Optional[bool] = True,
    ) -> None:
        """
        Method: DELETE
        URL: /securetrack/api/security_policies/{id:[0-9]+}/
        Version: 20+

        Notes:
            The aurora_data parameter when set to False determines which table entries will be deleted from.

        Usage:
            # Example #1:
            st.delete_usp_policy(7131354762492230143)

            # Example #2:
            st.delete_usp_policy(id=1, aurora_data=False)
        """
        try:
            ignoreSecureTrack2Data = not aurora_data
            response = self.api.session.delete(
                f"security_policies/{id}",
                params={
                    "context": context,
                    "ignoreSecureTrack2Data": str(ignoreSecureTrack2Data).lower(),
                },
            )
            response.raise_for_status()
        except RequestException as e:
            raise ValueError(f"Error deleting USP Policy: {e}")

    def get_usp_map(
        self, device: Union[str, int], context: Optional[int] = None
    ) -> SecurityPolicyDeviceMapping:
        """
        Method: GET
        URL: /securetrack/api/security_policies/{id:[0-9]+}/mapping
        Version: 20+

        Usage:
           interface_map = st.get_usp_map(5)
        """
        try:
            device_id = self._resolve_device_id(device)

            url = f"security_policies/{device_id}/mapping"
            response = self.api.session.get(url, params={"context": context})
            response.raise_for_status()
            json = response.json()
            security_policy_device_mapping = SecurityPolicyDeviceMapping.kwargify(
                get_api_node(json, "security_policy_device_mapping")
            )
            return security_policy_device_mapping
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except RequestException as e:
            raise ValueError(f"Error retrieving USP device interface map: {e}")

    def _update_usp_map(
        self,
        device_id: int,
        interface_name: str,
        zone_id: int,
        add_or_remove: str,
        context: Optional[int] = None,
    ):
        try:
            user_mapping = InterfaceUserMapping(interface_name=interface_name)
            user_mapping.zones_user_actions.append(
                ZoneUserAction(zone_id=zone_id, action=add_or_remove)
            )
            mapping = InterfacesManualMappings(interface_manual_mapping=[user_mapping])
            url = f"security_policies/{device_id}/manual_mapping"
            dict_data = mapping if isinstance(mapping, dict) else mapping._json
            data = {"interfaces_manual_mappings": dict_data}
            response = self.api.session.post(
                url, params={"context": context}, json=data
            )
            response.raise_for_status()
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except RequestException as e:
            raise ValueError(
                f"Error trying to post a USP interface manual mapping: {e}"
            )

    def _get_zone_id_from_zone_name(self, name: str):
        zone_matches = self._resolve_zone_from_name(name)
        if len(zone_matches) == 1:
            return zone_matches[0].id
        elif len(zone_matches) == 0:
            raise ValueError("No matching zones were found.")
        else:
            raise ValueError(
                "Too many matching zones were found. Please specify a Zone ID instead of a Zone Name."
            )

    def add_usp_map(
        self,
        device: Union[str, int],
        interface_name: str,
        zone: Union[int, str],
        context: Optional[int] = None,
    ):
        """
        Method: POST
        URL: /securetrack/api/security_policies/{deviceId:[0-9]+}/manual_mapping
        Version: 20-1+

        Usage:
            st.add_usp_map(
                device_id=5,
                interface_name="ge-0/0/0.0",
                zone=147
            )
        """
        if isinstance(zone, int):
            zone_id = zone
        else:
            zone_id = self._get_zone_id_from_zone_name(zone)

        device_id = self._resolve_device_id(device)

        self._update_usp_map(
            device_id=device_id,
            interface_name=interface_name,
            zone_id=zone_id,
            add_or_remove="add",
            context=context,
        )

    def delete_usp_map(
        self,
        device: Union[str, int],
        interface_name: str,
        zone: Union[int, str],
        context: Optional[int] = None,
    ):
        """
        Method: POST
        URL: /securetrack/api/security_policies/{deviceId:[0-9]+}/manual_mapping
        Version: 20-1+

        Usage:
            st.delete_usp_map(
                device=5,
                interface_name="ge-0/0/0.0",
                zone=147
            )
        """
        if isinstance(zone, int):
            zone_id = zone
        else:
            zone_id = self._get_zone_id_from_zone_name(zone)

        device_id = self._resolve_device_id(device)

        self._update_usp_map(
            device_id=device_id,
            interface_name=interface_name,
            zone_id=zone_id,
            add_or_remove="remove",
            context=context,
        )

    def get_clouds(
        self,
        type: str = "joined",
        name: Optional[str] = None,
        context: Optional[int] = None,
    ) -> Iterable[RestCloud]:
        """
        Get a list of Cloud objects by type and optionally filter by name

        Method: GET
        URL: /securetrack/api/topology/clouds
        Version: 21+

        Usage:
            # Example #1:
            # gets joined clouds
            clouds = st.get_clouds()

            # Example #2:
            clouds = st.get_clouds(type="non-joined")

            # Example #3:
            clouds = st.get_clouds(type="non-joined", name="192.")
        """
        if type not in ["joined", "non-joined"]:
            raise ValueError(
                "Error: 'type' argument must be 'joined' or 'non-joined'. 'joined' is default."
            )

        params = {"type": type, "name": name, "context": context}
        pager = Pager(
            self.api,
            "topology/clouds",
            "topology_clouds.topology_cloud",
            "get_clouds",
            RestCloud.kwargify,
            params=params,
        )
        return pager

    def get_cloud(self, cloud_id: int) -> RestCloud:
        """
        Get a Cloud by id

        Method: GET
        URL: /securetrack/api/topology/clouds/{id}
        Version: 21+

        Usage:
            cloud = st.get_cloud(56)

        """
        try:
            response = self.api.session.get(f"topology/clouds/{cloud_id}")
            response.raise_for_status()
            cloud = get_api_node(response.json(), "topology_cloud")
            return RestCloud.kwargify(cloud)
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Cloud: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Cloud: {e}")

    def get_cloud_internal_networks(
        self, cloud_management_id: int
    ) -> List[RestAnonymousSubnet]:
        """
        Get a list of Cloud Internal Networks by cloud management id

        Method: GET
        URL: /securetrack/api/topology/cloud_internal_networks/{id}
        Version: 21+

        Usage:
            cloud_networks = st.get_cloud_internal_networks(58)

        """
        try:
            url = f"topology/cloud_internal_networks/{cloud_management_id}"
            response = self.api.session.get(url)
            response.raise_for_status()
            response_json = response.json()
            api_node = get_api_node(response_json, "network_list.network")
            cloud_networks = [RestAnonymousSubnet.kwargify(item) for item in api_node]
            return cloud_networks
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON to Cloud: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Cloud: {e}")

    def add_topology_cloud(
        self,
        cloud_members: List[int],
        cloud_name: str,
        force_topology_init: Optional[bool] = False,
        context: Optional[int] = None,
    ):
        """
        Creates a new topology cloud in the Interactive Map by joining existing non-joined clouds together.

        Method: POST
        URL: /securetrack/api/topology/clouds
        Version: 21+

        Notes:
            Cloud Members must contain at least two cloud IDs, which cannot be already joined
            If the context parameter is not provided, then the API will use the context id of the first member of the members list in the body.
            Clouds included in the members list of the body must not be joined clouds or members of another joined cloud.
            If the provided body does not specify a joined cloud name, the newly created topology cloud will be given the name of the first member of the members list in the body.

        Usage:

            st.add_topology_cloud(cloud_name="Cloud 888", cloud_members=[49,51])

        """
        try:
            params = {}
            if context:
                params["context"] = context
            params["forceTopologyInit"] = force_topology_init
            data = {
                "cloud_data": {"cloud_name": cloud_name, "cloud_members": cloud_members}
            }
            response = self.api.session.post(
                "topology/clouds", json=data, params=params
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(f"Error adding a Topology Cloud: {e}")

    def update_topology_cloud(
        self,
        cloud_id: int,
        cloud_members: Optional[List[int]] = None,
        cloud_name: Optional[str] = None,
        action: Optional[str] = None,
        force_topology_init: Optional[bool] = False,
    ):
        """
        Modify the name of a topology cloud, and add/remove members of a joined cloud.

        Method: PUT
        URL: /securetrack/api/topology/clouds/{id}
        Version: 21+

        Notes:
            To change the name of a topology cloud, enter a value in the name field of the cloud_data and leave the cloud_members empty.
            To add/remove members of a joined cloud, specify the action and specify the clouds by id in the cloud_members list.
            The action is used only if the body contains a members list. If a members list is provided but no actions is specified, then the default action is 'add'.
            When adding cloud members, clouds included in the members list must not be joined clouds or members of another joined cloud.
            When removing cloud members, if only zero or one member remains in the joined cloud, it will be deleted from the Interactive Map.

        Usage:
            # Example #1: Change/update the cloud name:
            st.update_topology_cloud(105, cloud_name="Cloud 888")

            # Example #2:
            # Default action, if not specified, is "add"
            st.update_topology_cloud(105, cloud_members=[52], action="add")

            # Example #3:
            st.update_topology_cloud(105, cloud_members=[52], action="remove")
        """
        try:
            params = {}
            if not cloud_members and not cloud_name:
                raise ValueError(
                    "This method requires at least one of 'cloud_members' or 'cloud_name' have some data."
                )
            data = {
                "cloud_data": {"cloud_members": cloud_members, "cloud_name": cloud_name}
            }
            if action is None:
                params["action"] = "add"
            else:
                params["action"] = action
            if force_topology_init is not None:
                params["forceTopologyInit"] = force_topology_init
            response = self.api.session.put(
                f"topology/clouds/{cloud_id}", json=data, params=params
            )
            response.raise_for_status()
        except HTTPError as e:
            raise ValueError(
                f"Error updating a Topology Cloud: {response} {response.text}"
            )

    def get_cloud_suggestions(
        self, context: Optional[int] = None
    ) -> Iterable[SuggestedCloud]:
        """
        Get a list of SuggestedCloud objects

        Method: GET
        URL: /securetrack/api/topology/cloud_suggestions
        Version: 21+

        Notes:
            Returns information about all clouds in the topology.
            This API includes the ID of the cloud, the number of routes that point to the cloud, and the relevant devices (including the management_id) that have routes that point to the cloud.
            This information can be used to identify missing devices that may need to be added to the topology or to identify clouds that are candidates for being joined.

        Usage:


        """
        url = "topology/cloud_suggestions"
        api_node = "suggested_clouds.cloud"
        if context:
            params = {"context": context}
        else:
            params = None

        pager = Pager(
            self.api,
            url,
            api_node,
            "get_cloud_suggestions",
            SuggestedCloud.kwargify,
            params=params,
        )
        return pager

    def get_cloud_suggestions_by_id(
        self, cloud_id: int, context: Optional[int] = None
    ) -> Iterable[SuggestedCloud]:
        """
        Get a SuggestedCloud objects

        Method: GET
        URL: /securetrack/api/topology/cloud_suggestions/{cloud_id}
        Version: 21+

        Notes:
            Returns information about a specific cloud in the topology.
            This API includes the ID of the cloud, the number of routes that point to the cloud, and the relevant devices (including the management_id) that have routes that point to the cloud.
            This information can be used to identify missing devices that may need to be added to the topology or to identify clouds that are candidates for being joined.

        Usage:


        """
        url = f"topology/cloud_suggestions/{cloud_id}"
        api_node = "suggested_clouds.cloud"
        if context:
            params = {"context": context}
        else:
            params = None

        pager = Pager(
            self.api,
            url,
            api_node,
            "get_cloud_suggestions_by_id",
            SuggestedCloud.kwargify,
            params=params,
        )
        return pager

    def get_bulk_device_task(self, task_uid: str) -> BulkOperationTaskResult:
        """Track In-Progress Tasks involving Monitored Devices

        Method: POST
        URL: /securetrack/api/devices/bulk/tasks/{id}
        Version: R22-1+
        Notes:
            A list of devices and their status is displayed.
            Tasks are created by:
                bulk_update_topology
                bulk_delete_devices

        Usage:
            uid = "ada853b8-46f7-474b-bb4e-3309a3a9d0af"
            task = st.get_device_bulk_task(uid)
        """
        response = self.api.session.get(f"devices/bulk/tasks/{task_uid}")
        json = self.api.handle_json(response, "get_bulk_device_task", action="get")
        return BulkOperationTaskResult.kwargify(get_api_node(json, "task_result"))

    def get_devices_bulk_task(self, task_uid: str) -> BulkOperationTaskResult:
        """Track In-Progress Tasks involving Monitored Devices

        Method: POST
        URL: /securetrack/api/devices/bulk/tasks/{id}
        Version: R22-1+
        Notes:
            A list of devices and their status is displayed.
            Tasks are created by:
                bulk_add_devices
                bulk_update_devices
                bulk_import_devices
                bulk_update_topology
                bulk_delete_devices

        Usage:
            uid = "ada853b8-46f7-474b-bb4e-3309a3a9d0af"
            task = st.get_device_bulk_task(uid)
        """
        response = self.api.session.get(f"devices/bulk/tasks/{task_uid}")
        json = self.api.handle_json(response, "get_devices_bulk_task", action="get")
        return BulkOperationTaskResult.kwargify(get_api_node(json, "task_result"))

    def bulk_delete_devices(self, device_ids: List[int]) -> BulkOperationTask:
        """Delete One or More SecureTrack Devices

        Method: DELETE
        URL: /securetrack/api/devices/bulk
        Version: R23-1+
        Notes:
            This function is supported for ALL devices.
            The input for API is the Management ID (mgmt_ID).
            Use the mgmt_ID of a management device to delete it and its managed devices.
            Use multiple mgmt_IDs to delete individual devices in bulk.

            After the task status is complete, run Fast Topology Sync to see the changes to topology.

        Usage:
            devices = [194, 196, 198]
            task = st.bulk_delete_devices(devices)
        """
        data = {"devices_list": {"devices": [{"device_id": d} for d in device_ids]}}
        response = self.api.session.delete("devices/bulk/delete", json=data)
        json = self.api.handle_json(
            response, "bulk_delete_devices", action="bulk delete"
        )
        return BulkOperationTask.kwargify(json)

    def bulk_update_topology(self, devices: List[int]) -> BulkOperationTask:
        """Manually trigger retrieval of topology data collection

        Method: POST
        URL: /securetrack/api/devices/bulk/update_topology_data
        Version: R23-2+
        Notes:
            This functionality is applicable to all root devices with dynamic topology setting enabled.
            The topology data will be retrieved for the root device and all of its managed devices.

            The input for API is the Management ID (mgmt_ID).
            Use the mgmt_ID of a management device to update it and its managed devices.
            Use multiple mgmt_IDs to update individual devices in bulk.

            After the task status is complete, run Fast Topology Sync to see the updated device topology on the map.

        Usage:

            devices = [194, 196, 198]
            task = st.bulk_update_topology(devices)
        """
        data = {"devices_list": {"devices": [{"device_id": d} for d in devices]}}
        response = self.api.session.post("devices/bulk/update_topology_data", json=data)
        json = self.api.handle_json(
            response, "bulk_update_topology", action="bulk update"
        )
        return BulkOperationTask.kwargify(json)

    def get_internet_object(self, device: Union[int, str]) -> InternetObject:
        """
        Get Internet representation or "internet referral configuration" for device

        Method: GET
        URL: /securetrack/api/internet_referral/{deviceId:[0-9]+}
        Version: 21+

        Usage:

        """
        device_id = self._resolve_device_id(device)
        response = self.api.session.get(f"internet_referral/{device_id}")
        json = self.api.handle_json(response, "get_internet_representation", "get")
        return InternetObject.kwargify(get_api_node(json, "internet_referral_object"))

    def get_internet_resolved_object(self, device: Union[int, str]) -> NetworkObject:
        """
        Get resolved Internet representation, aka Network Object for device

        Method: GET
        URL: /securetrack/api/internet_referral/{deviceId:[0-9]+}/object
        Version: 21+

        Usage:

        """
        device_id = self._resolve_device_id(device)
        url = f"internet_referral/{device_id}/object"
        response = self.api.session.get(url)
        json = self.api.handle_json(
            response, "get_internet_representation_resolved_object", "get"
        )
        return NetworkObject.kwargify(get_api_node(json, "network_object"))

    def add_internet_object(
        self, device: Union[int, str], object_name: str
    ) -> InternetObject:
        """
        Add/Create Internet representation or "internet referral configuration" for device

        Method: POST
        URL: /securetrack/api/internet_referral/{deviceId:[0-9]+}
        Version: 21+

        Usage:

        """
        device_id = self._resolve_device_id(device)
        body = {
            "internet_referral": {
                "device_id": device_id,
                "object_name": object_name,
                "@xsi.type": "internetReferralObjectNameDTO",
            }
        }
        response = self.api.session.post("internet_referral", json=body)
        return self.api.handle_creation(
            response, "add_internet_object", cls=InternetObject
        )

    def update_internet_object(
        self, device: Union[int, str], object_name: str
    ) -> InternetObject:
        """
        Update Internet representation or "internet referral configuration" for device

        Method: PUT
        URL: /securetrack/api/internet_referral/{deviceId:[0-9]+}
        Version: 21+

        Usage:

        """
        device_id = self._resolve_device_id(device)
        url = f"internet_referral/{device_id}"
        body = {
            "internet_referral": {
                "device_id": device_id,
                "object_name": object_name,
                "xsi.type": "internetReferralObjectNameDTO",
            }
        }
        response = self.api.session.put(url, json=body)
        # self.api.handle_response(response, "update_internet_object", "update")
        json = self.api.handle_json(response, "update_internet_object", "update")
        return InternetObject.kwargify(get_api_node(json, "internet_referral_object"))

    def delete_internet_object(self, device: Union[int, str]):
        """
        Delete Internet representation or "internet referral configuration" for device

        Method: DELETE
        URL: /securetrack/api/internet_referral/{deviceId:[0-9]+}
        Version: 21+

        Usage:

        """
        device_id = self._resolve_device_id(device)
        url = f"internet_referral/{device_id}"
        response = self.api.session.delete(url)
        self.api.handle_response(response, "delete_internet_representation", "delete")

    def get_topology_subnets(
        self, name: str = None, ip: str = None, context: Optional[int] = None
    ) -> Pager:
        """Returns a list of the topology subnets for all the domains for which the user has permission to access.

        Method: GET
        URL: /securetrack/api/topology/subnets
        Version: R22-1+
        Notes:
            This API requires either 'Super admin' or 'Multi-Domain admin' privileges.
            For users with "Super admin" permission, the context parameter is optional. If a context is not specified, the Global context will be used.
            For users with "Multi-Domain" privilege, the context parameter is required.
            To get the context parameter, call the /domains/ API and use the id included in the returned domain DTO.
            Use the optional name parameter to restrict the results to topology subnet names that match the search criteria provided, as follows:
            1. If you provide only a mask, then an exact match search is done on the mask portion of the name
            e.g. if name=/2, the results will include 1.2.3.4/2, but not 1.2.3.4/22
            2. If you provide only a partial or complete IP address, then a contains search is done in the IPv4 block portion of the name
            e.g. name=32, the results will include 192.168.205.32/24 and 55.192.32.22/16, but will not include 55.168.205.5/32
            3. If you provide both an IPv4 address (either partial or complete) and a mask, then an exact match search is done
            e.g. if name=23.4/2, then the results will include 192.168.23.4/2, but will not include 192.168.23.4/23 or 23.4.192.168/2

            Use the optional ip parameter to restrict the results to topology subnets that contain this ip, see example below.

            User can use ip or name parameter, not both.

        Usage:
            subnets = st.get_topology_subnets()

            # Pager is intended to be used exactly like a list.
            for subnet in subnets:
                pass

            # Example #2:
            # If you want a real list type, you can call fetch_all() to get all data
            # from the endpoint. This can be very slow and is not recommended.
            subnets = st.get_topology_subnets().fetch_all()

        """
        url = "topology/subnets"
        api_node = "topology_subnets.subnets"
        params = {}
        if context:
            params["context"] = context
        if name and ip:
            raise ValueError(
                "You may use name or ip parameters, but not both at the same time."
            )
        if name:
            params["name"] = name
        elif ip:
            params["ip"] = ip

        pager = Pager(
            self.api,
            url,
            api_node,
            "get_topology_subnets",
            TopologySubnet.kwargify,
            params=params,
        )
        return pager

    def get_topology_subnet(self, id: int) -> TopologySubnetDetailed:
        """Returns the subnet for the specified id, including information regarding attached devices and join candidates.

        Method: GET
        URL: /securetrack/api/topology/subnets/{id}
        Version: R22-1+
        Notes:
            This API requires 'Super admin' or 'Multi-Domain admin' privileges.
            Multi-Domain user must have access permission to the domain where the subnet resides.

        Usage:
            subnet = st.get_topology_subnet(1687)

        """
        response = self.api.session.get(f"topology/subnets/{id}")
        json = self.api.handle_json(response, "get_topology_subnet", action="get")
        return TopologySubnetDetailed.kwargify(get_api_node(json, "subnet"))

    def search_services(
        self,
        name: Optional[str] = None,
        protocol: Optional[Union[str, Service.Protocol]] = None,
        port: Optional[int] = None,
        device: Optional[Union[int, str, Device]] = None,
        comment: Optional[str] = None,
        uid: Optional[str] = None,
        context: Optional[int] = None,
    ) -> Pager:
        """
        Search services on devices filtered by name, comment, protocol, port, and device

        Method: GET
        URL: /securetrack/api/services/search
        Version: 21+

        Notes:
            Filters cannot be combined except "device" and "context" can be added to any filter and "name" and "comment" can be combined.
            If your environment is multi-domain, a valid domain id can be added via the context filter

        Usage:

            # Example #1:
            service_objects = st.search_services(protocol="tcp")

            # Example #2:
            service_objects = st.search_services(port=22)

            # Example #3:
            service_objects = st.search_services(port=22, device_id=8)

            # Example #4:
            service_objects = st.search_services(name="Remote Desktop")

            # Example #5:
            service_objects = st.search_services(name="Remote Desktop", device_id=8)

            # Example #6, combine both text filters and device:
            service_objects = st.search_services(name="h323", comment="call signaling", device_id=8)

        """
        filter = "text"  # Must be one of: protocol, port, text, or uid
        params = {}

        # Check for filters that are combined which cannot be combined. TOS does not return errors for these use cases but
        # rather ignores the filter which was not specified in the "filter" property
        if protocol and port:
            raise ValueError(
                "Protocol and port filters cannot be used together. Use only one of these."
            )
        if (protocol or port) and (name or comment):
            raise ValueError(
                "Protocol, port, and text filters (name or comment) are each exclusive and cannot be combined."
            )
        if uid and (protocol or port or name or comment):
            raise ValueError(
                "uid filter is exclusive and cannot be combined with any other filters."
            )

        if protocol:
            filter = "protocol"
            if isinstance(protocol, str):
                params["protocol"] = Service.Protocol[protocol.upper()].value
            else:
                params["protocol"] = protocol.value
        elif port:
            filter = "port"
            params["port"] = port
        elif uid:
            filter = "uid"
            params["uid"] = uid

        if filter == "text" and (name or comment):
            if name:
                params["name"] = name
            if comment:
                params["comment"] = comment
        if device:
            device_id = self._resolve_device_id(device)
            if device_id:
                params["device_id"] = device_id
            else:
                raise ValueError(f"Device '{device}' was not found.")
        if context:
            params["context"] = context

        params["filter"] = filter

        pager = Pager(
            self.api,
            "services/search",
            "services.service",
            "search_services",
            classify_service_object,
            params=params,
            page_size=100,
            use_total=False,
        )
        return pager

    def get_service_groups(
        self, service_id: int, context: Optional[int] = None
    ) -> List[ServiceGroup]:
        """
        Get all ServiceGroup objects for a specific service using service ID

        Method: GET
        URL: /securetrack/api/services/{id:[0-9]+}/groups
        Version: 21+

        Usage:
            groups = st.get_service_groups(2961503)

        """
        if context:
            params = {"context": context}
        else:
            params = None

        response = self.api.session.get(f"services/{service_id}/groups", params=params)
        json = self.api.handle_json(response, "get_services_groups", "get")
        sg_list = get_api_node(json, "services.service")
        if sg_list:
            return [ServiceGroup.kwargify(obj) for obj in sg_list]
        else:
            return []

    def get_service_rules(
        self,
        service_id: int,
        include_groups: bool = False,
        context: Optional[int] = None,
    ) -> Pager:
        """
        Get all rules for a specified service using service ID

        Method: GET
        URL: /securetrack/api/services/{id:[0-9]+}/rules
        Version: 21+

        Usage:
            rules = st.get_service_rules(2961503)

        """
        url = f"services/{service_id}/rules"
        api_node = "rules.rule"
        params = {}
        if context:
            params["context"] = context
        if include_groups:
            params["include_groups"] = "true"
        pager = Pager(
            self.api,
            url,
            api_node,
            "get_service_rules",
            SecurityRule.kwargify,
            params=params,
        )
        return pager

    def _get_services_by_revision_and_id(
        self,
        revision_id: int,
        service_ids: Union[List[str], List[int], str, int],
        show_members: Optional[bool] = False,
        context: Optional[int] = None,
    ) -> List[Service]:
        """
        Get specified services for specified revision using revision ID and a list of service IDs

        Method: GET
        URL: /securetrack/api/revisions/{revision_id:[0-9]+}/services/{ids:(([0-9]+,)*[0-9]+|\\*)}
        Version: 21+

        Notes:

        Usage:
            services = st.get_services_by_revision_and_id(239534, [23689,23743])
        """
        params = {}
        params["show_members"] = str(show_members).lower()
        if context:
            params["context"] = context

        if isinstance(service_ids, (str, int)):
            service_ids = [service_ids]

        url = f"revisions/{revision_id}/services/{','.join(str(sid) for sid in service_ids)}"
        response = self.api.session.get(url, params=params)
        json = self.api.handle_json(response, "get_services_by_revision_and_id", "get")
        services = get_api_node(json, "services.service")
        if services:
            return [classify_service_object(svc) for svc in services]
        else:
            return []

    def _get_services_by_device_and_id(
        self,
        device: Union[int, str, Device],
        service_ids: Union[List[str], List[int], str, int],
        show_members: Optional[bool] = False,
        context: Optional[int] = None,
    ) -> List[Service]:
        """
        Get specified services for specified device using device info and a list of service IDs

        Method: GET
        URL: /securetrack/api/devices/{device_id:[0-9]+}/services/{ids:(([0-9]+,)*[0-9]+|\\*)}
        Version: 21+

        Notes:

        Usage:
            services = st.get_services_by_device_and_id(8, [23689,23743])
        """
        device_id = self._resolve_device_id(device)
        params = {}
        params["show_members"] = str(show_members).lower()
        if context:
            params["context"] = context

        if isinstance(service_ids, (str, int)):
            service_ids = [service_ids]

        url = (
            f"devices/{device_id}/services/{','.join(str(sid) for sid in service_ids)}"
        )
        response = self.api.session.get(url, params=params)
        json = self.api.handle_json(response, "get_services_by_device_and_id", "get")
        services = get_api_node(json, "services.service")
        if services:
            return [classify_service_object(svc) for svc in services]
        else:
            return []

    def _get_network_objects_for_revision_and_object_ids(
        self,
        revision_id: int,
        object_ids: List[int],
        show_members: Optional[bool] = True,
        identity_awareness: Optional[str] = None,
    ) -> List[NetworkObject]:
        """
        Get a list of network objects by revision ID and specified object ID's

        Method: GET
        URL: /securetrack/api/revisions/{revision_id:[0-9]+}/network_objects/{ids:(([0-9]+,)*[0-9]+|\\*)}
        Version: 21+

        Usage:
            network_objects = st._get_network_object_for_revision(24522, [222,238,243])

        """
        params = {}
        if show_members is not None:
            params["show_members"] = str(show_members).lower()
        if identity_awareness:
            params["identity_awareness"] = identity_awareness

        response = self.api.session.get(
            f"revisions/{revision_id}/network_objects/{','.join(map(str, object_ids))}",
            params=params,
        )
        json = self.api.handle_json(
            response, "get_network_objects_for_revision_and_object_ids", "get"
        )
        return [
            NetworkObject.kwargify(obj)
            for obj in get_api_node(json, "network_objects.network_object")
        ]

    def _get_network_objects_for_device_and_object_ids(
        self,
        device: Union[int, str],
        object_ids: List[int],
        show_members: Optional[bool] = True,
        identity_awareness: Optional[str] = None,
    ) -> List[NetworkObject]:
        """
        Get a list of network objects by device info and specified object ID's

        Method: GET
        URL: /securetrack/api/devices/{device_id:[0-9]+}/network_objects/{ids:(([0-9]+,)*[0-9]+|\\*)}
        Version: 21+

        Usage:
            network_objects = st._get_network_objects_for_device_and_object_ids(254, [222,238,243])

        """
        device_id = self._resolve_device_id(device)
        params = {}
        if show_members is not None:
            params["show_members"] = str(show_members).lower()
        if identity_awareness:
            params["identity_awareness"] = identity_awareness

        url = f"devices/{device_id}/network_objects/{','.join(map(str, object_ids))}"
        response = self.api.session.get(url, params=params)
        json = self.api.handle_json(
            response, "get_network_objects_for_device_and_object_ids", "get"
        )
        return [
            NetworkObject.kwargify(obj)
            for obj in get_api_node(json, "network_objects.network_object")
        ]

    def get_network_object_groups(
        self, object_id: int, context: Optional[int] = None
    ) -> List[NetworkObject]:
        """
        Get a list of network groups that contain the specified Network Object ID

        Method: GET
        URL: /securetrack/api/network_objects/69577/groups
        Version: 21+

        Usage:
            groups = st.get_network_object_groups(69577)
        """
        if context:
            params = {"context": context}
        else:
            params = None

        response = self.api.session.get(
            f"network_objects/{object_id}/groups", params=params
        )
        json = self.api.handle_json(response, "get_network_object_groups", "get")
        nog_list = get_api_node(json, "network_objects.network_object")
        if nog_list:
            return [NetworkObject.kwargify(obj) for obj in nog_list]
        else:
            return []

    def get_network_object_rules(
        self,
        object_id: int,
        include_groups: bool = False,
        context: Optional[int] = None,
    ) -> Pager:
        """
        Get a list of rules that contain the specified Network Object ID

        Method: GET
        URL: /securetrack/api/network_objects/65078/rules?include_groups=true
        Version: 21+

        Usage:
            rules = st.get_network_object_rules(69577, include_groups=True)

        """
        url = f"network_objects/{object_id}/rules"
        api_node = "rules.rule"
        params = {}
        if context:
            params["context"] = context
        if include_groups:
            params["include_groups"] = "true"
        pager = Pager(
            self.api,
            url,
            api_node,
            "get_network_object_rules",
            SecurityRule.kwargify,
            params=params,
        )
        return pager

    def get_internet_representing_address(
        self, context: Optional[int] = None
    ) -> IPAddress:
        """
        Get the internet representing address value for network simulations

        Method: GET
        URL: /securetrack/api/zones/internet_representing_address
        Version: R23-1+
        Notes:
            Internet representing address will be used for network path simulation when:
                (1) An access request uses Internet object as either a source or a destination
                (2) An access request uses Url Category as a destination and no Url-Category zone is defined.

        Usage:
            ip_address = st.get_internet_representing_address()

        """
        params = {}
        if context:
            params["context"]
        response = self.api.session.get("zones/internet_representing_address")
        if not response.ok:
            msg = safe_unwrap_msg(response)
            raise ValueError(
                f"Got error: {msg} with status code {response.status_code}"
            )
        else:
            return IPAddress(response.text)

    def set_internet_representing_address(
        self, ip_address: Union[str, IPAddress], context: Optional[int] = None
    ) -> IPAddress:
        """
        Set the internet representing address value for network simulations

        Method: POST
        URL: /securetrack/api/zones/internet_representing_address
        Version: R23-1+
        Notes:
            Internet representing address will be used for network path simulation when:
                (1) An access request uses Internet object as either a source or a destination
                (2) An access request uses Url Category as a destination and no Url-Category zone is defined.

        Usage:
            st.set_internet_representing_address("8.8.4.4")

        """
        query_string = ""
        if isinstance(ip_address, str):
            ip_address = IPAddress(ip_address)
        query_string = "ipAddress=" + str(ip_address)
        if context:
            query_string += f"&context={context}"
        response = self.api.session.post(
            f"zones/internet_representing_address?{query_string}"
        )
        self.api.handle_response(response, "set_internet_representing_address", "set")

    def get_usp_violating_rules_count(
        self,
        device: Union[int, str, Device],
        aurora_data: bool = True,
    ) -> int:
        """Returns a count of USP violating rules

        Method: GET
        URL: /securetrack/api/violating_rules/{deviceId:[0-9]+}/count
        Version: R22-1+

        Notes:
            The aurora_data parameter when set to False returns data that was migrated from a TOS Classic installation.

        Usage:
            count = st.get_usp_violating_rules_count(264)

        """
        params = {}
        device_id = self._resolve_device_id(device)
        ignoreSecureTrack2Data = not aurora_data
        params["ignoreSecureTrack2Data"] = ignoreSecureTrack2Data
        url = f"violating_rules/{device_id}/count"
        response = self.api.session.get(url, params=params)
        json = self.api.handle_json(response, "get_usp_violating_rules_count", "get")
        count = get_api_node(json, "count.count")
        return count

    def get_usp_violating_rules(
        self,
        device: Union[int, str, Device],
        severity: Union[SecurityPolicyViolation.Severity, str],
        violation_type: Optional[
            Union[SecurityPolicyViolationType, str]
        ] = SecurityPolicyViolationType.SECURITY_POLICY,
        policy_name: Optional[str] = None,
        aurora_data: bool = True,
    ) -> List[SecurityRule]:
        """Returns a list of USP violating rules

        Method: GET
        URL: /securetrack/api/violating_rules/{deviceId:[0-9]+}/count
        Version: R22-1+

        Notes:
            The aurora_data parameter when set to False returns data that was migrated from a TOS Classic installation.

        Usage:
            rules = st.get_usp_violating_rules(264, SecurityPolicyViolation.Severity.CRITICAL, SecurityPolicyViolationType.SECURITY_POLICY)

        """

        severity = (
            SecurityPolicyViolation.Severity(severity)
            if isinstance(severity, str)
            else severity
        )
        violation_type = (
            SecurityPolicyViolationType(violation_type)
            if isinstance(violation_type, str)
            else violation_type
        )

        params = {}
        device_id = self._resolve_device_id(device)
        ignoreSecureTrack2Data = not aurora_data
        params["ignoreSecureTrack2Data"] = ignoreSecureTrack2Data
        params["severity"] = severity.value
        params["type"] = violation_type.value
        if policy_name:
            params["policy_name"] = policy_name
        url = f"violating_rules/{device_id}/device_violations"
        response = self.api.session.get(url, params=params)
        json = self.api.handle_json(response, "get_usp_violating_rules", "get")
        rules = get_api_node(
            json, "security_policy_device_violations.violating_rules.violating_rule"
        )
        if rules:
            return [SecurityRule.kwargify(rule) for rule in rules]
        else:
            return []

    def export_security_rules(
        self,
        search_text: str,
        context: Optional[int] = None,
    ) -> str:
        """
        Initiates a filtered export of Security Rules to the SecureTrack Reports Repository

        Method: GET
        URL: /securetrack/api/rule_search/export
        Version: 22-1+

        Notes:
            The search_text parameter provides the same capabilities as the Policy Browser feature in SecureTrack.
            You can search for a string across all rule fields, or you can search for a combination of specific strings in specific fields.
            The text format for a field is : for example uid:9259f6ee-47a0-4996-a214-ab7edc14a916.
            See the search info documentation in Securetrack Policy Browser page for more information.
            This API exports the results data as a CSV file in the SecureTrack Reports Repository.

        Usage:
            result_message = st.export_security_rules("mail")
            # Success will return this message: Results will be exported as a CSV file in the SecureTrack Reports Repository
        """
        try:
            response = self.api.session.get(
                "rule_search/export",
                params={
                    "context": context,
                    "search_text": search_text,
                },
            )
            response.raise_for_status()
            return response.text
        except RequestException as e:
            raise ValueError(f"Error getting string/csv export of Security Rules: {e}")

    def get_topology_device(self, device_id: Union[int, str]) -> TopologyDevice:
        """
        Get a specific topology device by ID.

        Method: GET
        URL: /securetrack/api/topology/device/{device_id}
        Version: R23-1+

        Args:
            device_id: The ID of the device to retrieve

        Returns:
            TopologyDevice: The requested topology device

        Raises:
            ValueError: If the device cannot be found or there's an error

        Usage:
            device = st.get_topology_device(123)
        """
        try:
            response = self.api.session.get(f"topology/device/{device_id}")
            if not response.ok:
                response.raise_for_status()

            data = response.json()
            device_data = get_api_node(data, "TopologyDevice", default=None)

            return TopologyDevice.kwargify(device_data)

        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Topology Device {device_id}: {e}")
        except Exception as e:
            raise ValueError(f"Error retrieving topology device {device_id}: {e}")

    def get_topology_devices(
        self, context: Optional[int] = None
    ) -> List[TopologyDevice]:
        """
        Get all topology devices.

        Method: GET
        URL: /securetrack/api/topology/device
        Version: 23-1+

        Returns:
            List[TopologyDevice]: List of topology device objects

        Usage:
            devices = st.get_topology_devices()
        """
        try:
            response = self.api.session.get("topology/device")
            if not response.ok:
                response.raise_for_status()

            data = response.json()
            devices = []
            for device in get_api_node(data, "TopologyDevices", listify=True):
                devices.append(TopologyDevice.kwargify(device))
            return devices
        except JSONDecodeError as e:
            raise ValueError(f"Error converting JSON: {e}")
        except HTTPError as e:
            raise ValueError(f"Error Getting Topology Devices: {e}")
        except Exception as e:
            raise ValueError(f"Error retrieving topology devices: {e}")
