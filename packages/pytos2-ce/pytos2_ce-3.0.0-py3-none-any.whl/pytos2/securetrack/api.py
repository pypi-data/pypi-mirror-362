from enum import Enum
from typing import Union, Dict, Optional
import json
from io import BytesIO

from requests import Response

from pytos2.api import BaseAPI, get_app_api_session, Pager
from pytos2.utils import setup_logger


LOGGER = setup_logger("st_api")


class StAPI(BaseAPI):
    class Meta:
        PATH = "securetrack/api"
        APP = "ST"
        TOS2_ENV = ["TSS_SERVICE", "ST_SERVER_SERVICE"]

    def __init__(
        self, hostname: Optional[str], username: Optional[str], password: Optional[str]
    ):
        self.hostname, self.username, self.password, session = get_app_api_session(
            app=self, hostname=hostname, username=username, password=password
        )

        super().__init__(session)

    def get_zone_by_id(self, id: int) -> Response:
        return self.session.get(f"zones/{id}")

    def get_zones_by_name(self, name: str) -> Response:
        params = {"name": name}
        return self.session.get("zones", params=params)

    def get_domain_by_id(self, id: int) -> Response:
        return self.session.get(f"domains/{id}")

    def get_domains_by_name(self, name: str) -> Response:
        params = {"name": name}
        return self.session.get("domains", params=params)

    def post_domain(
        self, name: str, description: Optional[str], address: Optional[str]
    ) -> Response:  # pragma: no cover
        LOGGER.info(
            f"POSTing adding domain: {name}, description: {description}, address: {address}"
        )
        domain_body = {
            "domain": {"name": name, "description": description, "address": address}
        }
        res = self.session.post("domains/", json=domain_body)
        if res.ok:
            LOGGER.info(f"Sucessfully added domain {name}")
        else:
            LOGGER.error(
                f"ADD failed for domain, API response: {res.text.strip()}, check /var/log/tomcat/securetrack.log"
            )

        return res

    def put_domain(
        self,
        id: int,
        name: Optional[str],
        description: Optional[str],
        address: Optional[str],
    ) -> Response:
        LOGGER.info(
            f"PUTting update domain: {id}-{name}, description: {description}, address: {address}"
        )
        domain_body = {
            "domain": {"name": name, "description": description, "address": address}
        }
        res = self.session.put(f"domains/{id}", json=domain_body)
        if res.ok:
            LOGGER.info(f"Sucessfully updated domain {id} - {name}")
        else:
            LOGGER.error(
                f"UPDATE failed for domain, API response: {res.text.strip()}, check /var/log/tomcat/securetrack.log"
            )
        return res

    def get_device_by_id(
        self, id: int, license: bool = None, version: bool = None
    ) -> Response:
        params = {}
        params["show_license"] = "true" if license else "false"
        params["show_os_version"] = "true" if version else "false"

        res = self.session.get(f"devices/{id}", params=params)
        if res.ok:
            return res
        else:
            res.raise_for_status()

    def get_devices_by_name(self, name: str) -> Response:
        params = {"name": name}
        return self.session.get("devices", params=params)

    def get_generic_devices(
        self, name: Optional[str] = None, context: Optional[int] = None
    ) -> Response:  # pragma: no cover
        LOGGER.info("GETing generic devices")

        params: Dict[Union[str, int]] = {}
        if name is not None:
            params["name"] = name
        if context is not None:
            params["context"] = context

        return self.session.get("generic_devices", params=params)

    def delete_generic_device(
        self, id: int, update_topology: bool = False
    ) -> Response:  # pragma: no cover
        LOGGER.info(
            f"DELETEing generic device {id}, update_topology: {update_topology}"
        )
        res = self.session.delete(
            f"generic_devices/{id}", params={"update_topology": update_topology}
        )
        if res.ok:
            LOGGER.info("Generic device successfully DELETEed")
        else:
            LOGGER.error(
                f"DELETE failed for generic device, API response: {res.text.strip()}, check /var/log/tomcat/securetrack.log"
            )

        return res

    def put_generic_device(
        self,
        id: int,
        configuration: Union[BytesIO, str],
        name: str,
        update_topology: bool = False,
    ) -> Response:  # pragma: no cover
        files: Dict[str, tuple] = {
            "update_topology": (None, str(update_topology).lower())
        }
        LOGGER.info(f"PUTing generic device {id}, update_topology: {update_topology}")
        if name:
            files["device_data"] = (
                None,
                json.dumps({"generic_device": {"name": name}}),
                "application/json",
            )
            LOGGER.debug(f"Updating device {id} name to {name}")
        if configuration:
            if isinstance(configuration, str):
                configuration = BytesIO(configuration.encode())

            LOGGER.debug(f"Device config: {configuration.read()}")
            configuration.seek(0)
            files["configuration_file"] = (
                "config.txt",
                configuration,
                "application/octet-stream",
            )
        res = self.session.put(
            f"generic_devices/{id}", files=files, headers={"Accept": "*/*"}
        )

        if res.ok:
            LOGGER.info("Generic device successfully PUTed")
        else:
            LOGGER.error(
                f"PUT failed for generic device, API response: {res.text.strip()}, check /var/log/tomcat/securetrack.log"
            )

        return res

    def post_generic_device(
        self,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
        customer_id: Optional[int] = None,
    ) -> Response:  # pragma: no cover
        if isinstance(configuration, str):
            configuration = BytesIO(configuration.encode())
        LOGGER.info(
            f"POSTing generic device {name}, domain: {customer_id}, update_topology: {update_topology}"
        )
        LOGGER.debug(f"Device config: {configuration.read()}")
        configuration.seek(0)

        device_data = {"name": name}
        if customer_id is not None:
            device_data["customer_id"] = customer_id

        res = self.session.post(
            "generic_devices",
            files={
                "configuration_file": (
                    "config.txt",
                    configuration,
                    "application/octet-stream",
                ),
                "device_data": (
                    None,
                    json.dumps({"generic_device": device_data}),
                    "application/json",
                ),
                "update_topology": (None, str(update_topology).lower()),
            },
            headers={"Accept": "*/*"},
        )
        if res.ok:
            LOGGER.info("Generic device successfully POSTed")
        else:
            LOGGER.error(
                f"POST failed for generic device, API response: {res.text.strip()}, check /var/log/tomcat/securetrack.log"
            )

        return res

    def get_rules_from_device_id(
        self, device_id: int, uid: Optional[str] = None, documentation: bool = True
    ) -> Response:
        LOGGER.info(f"GETting rules from device id {device_id}")
        params = {}
        if documentation:
            params["add"] = "documentation"
        if uid:
            params["uid"] = uid

        return self.session.get(f"devices/{device_id}/rules", params=params)

    def get_nat_rules_from_device_id(
        self,
        device_id: int,
        input_interface: str = None,
        output_interface: str = None,
        nat_stage: str = None,
        nat_type: str = None,
    ) -> Response:
        LOGGER.info(f"GETting nat rules from device id {device_id}")
        params = {}
        if input_interface:
            params["input_interface"] = input_interface
        if output_interface:
            params["output_interface"] = output_interface
        if nat_stage:
            params["nat_stage"] = nat_stage
        if nat_type:
            params["nat_type"] = nat_type

        return self.session.get(
            f"devices/{device_id}/nat_rules/bindings", params=params
        )

    def get_rules_from_revision_id(
        self, revision_id: int, uid: Optional[str] = None, documentation: bool = True
    ) -> Response:
        params = {}
        if documentation:
            params["add"] = "documentation"
        if uid:
            params["uid"] = uid

        return self.session.get(f"revisions/{revision_id}/rules", params=params)

    def get_rule_by_id(self, rule_id: int) -> Response:
        LOGGER.info(f"GETting rule by rule id {rule_id}")
        return self.session.get(f"rules/{rule_id}")

    def search_rule(
        self, search_text: Optional[str] = None, devices: list = [], context: int = 0
    ):
        LOGGER.info(
            f"Searching for rules (search_text=`{search_text}', devices=[{', '.join(devices)}], context={context})"
        )

        params = {}

        if search_text is not None:
            params["search_text"] = search_text

        if devices:
            params["devices"] = ",".join(devices)

        if context:
            params["context"] = context

        return self.session.get("rule_search", params=params)

    def get_interfaces_from_device_id(self, device_id: int) -> Response:
        LOGGER.info(f"GETting interfaces for device id: {device_id}")
        return self.session.get(f"devices/{device_id}/interfaces")

    def get_bindable_objects_from_device_id(self, device_id: int) -> Response:
        LOGGER.info(f"GETting bindable objects for device id: {device_id}")
        return self.session.get(f"devices/{device_id}/bindable_objects")

    def get_topology_interfaces_from_device_id(
        self, device_id: int, is_generic: bool = 0
    ) -> Response:
        if is_generic:
            LOGGER.info(
                f"GETting topology interfaces is_generic=true for device id: {device_id}"
            )
            return self.session.get(
                f"devices/topology_interfaces.json?mgmtId={device_id}&is_generic=true"
            )
        else:
            LOGGER.info(f"GETting topology interfaces for device id: {device_id}")
            return self.session.get(
                f"devices/topology_interfaces.json?mgmtId={device_id}"
            )
