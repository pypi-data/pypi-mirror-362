from enum import Enum

from typing import Optional, List, Union
from netaddr import IPAddress
from attr.converters import optional

from pytos2.securechange.network_object import classify_object_type
from pytos2.utils import propify, prop, stringify_optional_obj
from pytos2.models import Jsonable

from pytos2.securechange.rule import SlimRule
from pytos2.securechange.designer import DesignerResults
from pytos2.securechange.network_object import NetworkObject

from pytos2.securetrack import St
from pytos2.securetrack.service_object import Service as STService

from pytos2.securetrack.rule import SecurityRule
from pytos2.securetrack.network_object import (
    NetworkObjectXsiType as STNetworkObjectXsiType,
    NetworkObject as STNetworkObject,
)

from .binding import Binding
from . import Designer, Field, FieldXsiType


def _mv_key(j, src, dest):
    if src not in j:
        return

    j[dest] = j[src]
    del j[src]


@propify
class ModificationNetworkObject(Jsonable):
    class XsiType(Enum):
        NETWORK_OBJECT = "ns_sc_policy:network_object"
        SUBNET_NETWORK_OBJECT = "ns_sc_policy:subnet_network_object"
        HOST_NETWORK_OBJECT = "ns_sc_policy:host_network_object"
        RANGE_NETWORK_OBJECT = "ns_sc_policy:range_network_object"
        NETWORK_OBJECT_GROUP = "ns_sc_policy:network_object_group"
        HOST_NETWORK_OBJECT_WITH_INTERFACES = (
            "ns_sc_policy:host_network_object_with_interfaces"
        )

    xsi_type: XsiType = prop(XsiType.NETWORK_OBJECT)
    id: Optional[int] = prop(None)
    comment: Optional[str] = prop(None)
    name: Optional[str] = prop(None)

    def from_securetrack(obj):
        j = dict(obj.data or obj._json)
        if obj.xsi_type == STNetworkObjectXsiType.RANGE_NETWORK_OBJECT:
            _mv_key(j, "first_ip", "min_ip")
            _mv_key(j, "last_ip", "max_ip")

        cls = {
            STNetworkObjectXsiType.HOST_NETWORK_OBJECT: ModificationHostNetworkObject,
            STNetworkObjectXsiType.HOST_NETWORK_OBJECT_WITH_INTERFACES: ModificationHostNetworkObjectWithInterfaces,
            STNetworkObjectXsiType.NETWORK_OBJECT_GROUP: ModificationNetworkObjectGroup,
            STNetworkObjectXsiType.RANGE_NETWORK_OBJECT: ModificationRangeNetworkObject,
            STNetworkObjectXsiType.SUBNET_NETWORK_OBJECT: ModificationSubnetNetworkObject,
        }.get(obj.xsi_type, ModificationNetworkObject)
        return cls.kwargify(j)


@propify
class ModificationHostNetworkObject(ModificationNetworkObject):
    xsi_type: ModificationNetworkObject.XsiType = prop(
        ModificationNetworkObject.XsiType.HOST_NETWORK_OBJECT
    )
    netmask: Optional[IPAddress] = prop(
        IPAddress("255.255.255.255"),
        converter=optional(IPAddress),
        jsonify=stringify_optional_obj,
    )
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )


@propify
class ModificationSubnetNetworkObject(ModificationNetworkObject):
    xsi_type: ModificationNetworkObject.XsiType = prop(
        ModificationNetworkObject.XsiType.SUBNET_NETWORK_OBJECT
    )
    netmask: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )


@propify
class ModificationRangeNetworkObject(ModificationNetworkObject):
    xsi_type: ModificationNetworkObject.XsiType = prop(
        ModificationNetworkObject.XsiType.RANGE_NETWORK_OBJECT
    )
    min_ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    max_ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )


@propify
class ModificationNetworkObjectGroup(ModificationNetworkObject):
    xsi_type: ModificationNetworkObject.XsiType = prop(
        ModificationNetworkObject.XsiType.NETWORK_OBJECT_GROUP
    )


@propify
class ModificationHostNetworkObjectWithInterfaces(ModificationNetworkObject):
    xsi_type: ModificationNetworkObject.XsiType = prop(
        ModificationNetworkObject.XsiType.HOST_NETWORK_OBJECT_WITH_INTERFACES
    )
    netmask: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )
    ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )


@propify
class RangeDTO(Jsonable):
    class Prop(Enum):
        FROM = "from"

    to: int = prop()
    from_: int = prop(key=Prop.FROM.value)


@propify
class ModificationServiceObject(Jsonable):
    class XsiType(Enum):
        SERVICE_OBJECT = "ns_sc_policy:service_object"
        ICMP_SERVICE = "ns_sc_policy:icmp_service"
        IP_SERVICE = "ns_sc_policy:ip_service"
        SERVICE_GROUP = "ns_sc_policy:service_group"
        TRANSPORT_SERVICE = "ns_sc_policy:transport_service"

    xsi_type: XsiType = prop(XsiType.SERVICE_OBJECT, key=Jsonable.Prop.XSI_TYPE.value)

    id: Optional[int] = prop(None)
    comment: Optional[str] = prop(None)
    name: Optional[str] = prop(None)

    def from_securetrack(obj):
        from pytos2.securetrack.service_object import (
            TCPServiceObject,
            UDPServiceObject,
            ICMPServiceObject,
            ServiceGroup,
            OtherIPServiceObject,
        )

        if isinstance(obj, (TCPServiceObject, UDPServiceObject)):
            protos = {6: "TCP", 17: "UDP"}

            proto = protos.get(obj.protocol, obj.protocol)

            return ModificationTransportService(
                comment=obj.comment,
                name=obj.name,
                protocol=proto,
                port=RangeDTO(from_=obj.min_port, to=obj.max_port),
            )
        elif isinstance(obj, (ICMPServiceObject)):
            return ModificationIcmpService(
                comment=obj.comment,
                name=obj.name,
                type=RangeDTO(from_=obj.min_port, to=obj.max_port),
            )
        elif isinstance(obj, (ServiceGroup)):
            return ModificationServiceGroup(comment=obj.comment, name=obj.name)
        elif isinstance(obj, (OtherIPServiceObject)):
            return ModificationIPService(comment=obj.comment, name=obj.name)
        else:
            return ModificationServiceObject(comment=obj.comment, name=obj.name)


@propify
class ModificationIcmpService(ModificationServiceObject):
    xsi_type: ModificationServiceObject.XsiType = prop(
        ModificationServiceObject.XsiType.ICMP_SERVICE, key=Jsonable.Prop.XSI_TYPE.value
    )

    type: Optional[RangeDTO] = prop(None)


@propify
class ModificationIPService(ModificationServiceObject):
    xsi_type: ModificationServiceObject.XsiType = prop(
        ModificationServiceObject.XsiType.IP_SERVICE, key=Jsonable.Prop.XSI_TYPE.value
    )

    protocol: Optional[RangeDTO] = prop(None)


@propify
class ModificationServiceGroup(ModificationServiceObject):
    xsi_type: ModificationServiceObject.XsiType = prop(
        ModificationServiceObject.XsiType.SERVICE_GROUP,
        key=Jsonable.Prop.XSI_TYPE.value,
    )


@propify
class ModificationTransportService(ModificationServiceObject):
    xsi_type: ModificationServiceObject.XsiType = prop(
        ModificationServiceObject.XsiType.TRANSPORT_SERVICE,
        key=Jsonable.Prop.XSI_TYPE.value,
    )

    protocol: Optional[str] = prop(None)
    port: Optional[RangeDTO] = prop(None)


@propify
class RuleOperationBinding(Jsonable):
    binding_uid: str = prop()
    binding: Optional[Binding] = prop(None)
    rules: List[SlimRule] = prop(factory=list, flatify="rule")


@propify
class RuleOperationDevice(Jsonable):
    revision_id: Optional[int] = prop(None)
    management_id: int = prop()

    management_name: str = prop("")
    management_ip: Optional[IPAddress] = prop(
        None, converter=optional(IPAddress), jsonify=stringify_optional_obj
    )

    revision_number: Optional[int] = prop(None)
    number_of_rules: Optional[int] = prop(None)

    bindings: List[RuleOperationBinding] = prop(factory=list, flatify="binding")


@propify
class RuleOperation(Field):
    xsi_type: FieldXsiType = prop(
        FieldXsiType.RULE_RECERTIFICATION, key=Jsonable.Prop.XSI_TYPE.value
    )

    devices: List[RuleOperationDevice] = prop(factory=list, flatify="device")
    _ticketed_rules: Optional[Union[List[SecurityRule], None]] = None

    def get_rules(self):
        rules = []

        for device in self.devices:
            for binding in device.bindings:
                rules += binding.rules

        return rules

    def is_rule_added(self, rule: SecurityRule):
        rules = self.get_rules()
        for slim in rules:
            if slim.uid == rule.uid:
                return True

        return False

    def _add_devices(self, rules: list):
        for rule in rules:
            device = RuleOperationDevice(
                management_id=rule.device.id,
                management_name=rule.device.name,
                revision_id=rule.device.latest_revision,
            )
            if device.management_id not in [d.management_id for d in self.devices]:
                self.devices.append(device)

    def is_invalid_rule(self, rule: SecurityRule):
        def skip_invalid_rule(msg):
            # LOGGER.info(msg)
            return True

        rule_uid = rule.uid

        if self._ticketed_rules is None:
            self._ticketed_rules = St.default.get_rules_on_open_tickets()

        for tr in self._ticketed_rules:
            if rule.id == tr.id:
                return skip_invalid_rule(
                    "Rule {} {} is already in an active ticket, skipping.".format(
                        rule.id, rule.uid
                    )
                )

        if rule.rule_location is not None:
            if rule.rule_location.lower() in ["predefined", "shared"]:
                return skip_invalid_rule(
                    "Rule {} {} has location of {}, skipping.".format(
                        rule.id, rule_uid, rule.rule_location
                    )
                )
        if rule.rule_type is not None:
            if rule.rule_type.value.lower() in ["interzone", "intrazone"]:
                return skip_invalid_rule(
                    "Rule {} {} has type of {}, skipping.".format(
                        rule.id, rule_uid, rule.rule_type
                    )
                )

        if rule.device.model.value.lower() in ["fortimanager", "fmg_adom"]:
            if rule.global_location and rule.global_location.value.lower() in [
                "before",
                "after",
            ]:
                return skip_invalid_rule(
                    "Rule {} {} is global, skipping.".format(rule.id, rule_uid)
                )

        if (
            rule.device.vendor.value.lower() == "paloaltonetworks"
            and rule.global_location
        ):
            if rule.rule_location is not None:
                if rule.rule_location != rule.device.context_name:
                    return skip_invalid_rule(
                        "Rule {} {} is not located on the current device context, skipping.".format(
                            rule.id, rule_uid
                        )
                    )
            elif rule.device.parent is not None:
                if rule.global_location.value.lower() in ["before", "after"]:
                    return skip_invalid_rule(
                        "Rule {} {} is global, skipping.".format(rule.id, rule_uid)
                    )

        if self.xsi_type == FieldXsiType.RULE_RECERTIFICATION:
            if rule.is_disabled:
                return skip_invalid_rule(
                    "Rule {} {} - rule disabled, skipping.".format(rule.id, rule_uid)
                )
            if (
                rule.documentation is not None
                and rule.documentation.certification_status is not None
            ):
                if (
                    rule.documentation.certification_status.value.lower()
                    == "decertified"
                ):
                    return skip_invalid_rule(
                        "Rule {} {} - rule decertified, skipping.".format(
                            rule.id, rule_uid
                        )
                    )
        return False

    def add_rule(
        self,
        rule: SecurityRule,
        skip_invalid_rules: Optional[bool] = False,
    ):
        self.add_rules([rule], skip_invalid_rules)

    def add_rules(
        self,
        rules: List[SecurityRule],
        skip_invalid_rules: Optional[bool] = False,
    ):
        """
        Usage Notes:

        If skip_invalid_rules = True, there will be no checks to see if a rule can be added to a ticket
        and the ticket save/post may cause an error.

        If skip_invalid_rules = False, some attempt will be made to discard rules which cannot be added to tickets.
        """

        self._add_devices(rules)

        for device in self.devices:
            for rule in rules:
                if (
                    device.management_id == rule.device.id
                    and device.revision_id == rule.device.latest_revision
                ):
                    if skip_invalid_rules and self.is_invalid_rule(rule):
                        continue

                    for binding in device.bindings:
                        if binding.binding_uid == rule.bindings[0].uid:
                            break
                    else:
                        binding = RuleOperationBinding(binding_uid=rule.bindings[0].uid)
                        device.bindings.append(binding)

                    slim_rule = SlimRule.kwargify({"uid": rule.uid})
                    binding.rules.append(slim_rule)


@propify
class ObjectStatus(Jsonable):
    class XsiType(Enum):
        EXISTING = "existing"
        NEW = "new"

    xsi_type: XsiType = prop(XsiType.EXISTING, key=Jsonable.Prop.XSI_TYPE.value)
    st_uid: Optional[str] = prop(None)


@propify
class DeviceNetworkObject(Jsonable):
    network_object: List[NetworkObject] = prop(
        factory=list, kwargify=classify_object_type
    )
    device_id: Optional[int] = prop(None)
    status: Optional[ObjectStatus] = prop(None)


@propify
class DeviceServiceObject(Jsonable):
    service_object: List[ModificationServiceObject] = prop(factory=list)
    uid: Optional[str] = prop(None)
    device_id: Optional[int] = prop(None)
    status: Optional[ObjectStatus] = prop(None)
    id: Optional[int] = prop(None)


class CellAction(Enum):
    REMOVE = "REMOVE"
    ADD = "ADD"


@propify
class NetworkObjectCellModification(Jsonable):
    device_network_object: DeviceNetworkObject = prop()
    action: Optional[CellAction] = prop(None)
    id: Optional[int] = prop(None)


@propify
class NetworkObjectCellModifications(Jsonable):
    id: Optional[int] = prop(None)
    network_object_cell_modifications: List[NetworkObjectCellModification] = prop(
        factory=list, flatify="network_object_cell_modification"
    )


@propify
class ServiceObjectCellModification(Jsonable):
    device_service_object: DeviceServiceObject = prop()
    action: Optional[CellAction] = prop(None)
    id: Optional[int] = prop(None)


@propify
class ServiceObjectCellModifications(Jsonable):
    id: Optional[int] = prop(None)
    service_object_cell_modifications: List[ServiceObjectCellModification] = prop(
        factory=list, flatify="service_object_cell_modification"
    )


@propify
class RuleKey(Jsonable):
    device_id: Optional[int] = prop(None)
    binding_uid: Optional[str] = prop(None)
    rule_uid: Optional[str] = prop(None)

    def __eq__(a, b):
        return all(
            [
                a.device_id == b.device_id,
                a.binding_uid == b.binding_uid,
                a.rule_uid == b.rule_uid,
            ]
        )


@propify
class RuleModification(Jsonable):
    class XsiType(Enum):
        RULE_MODIFICATION = "rule_modification"
        MODIFY_RULE_MODIFICATION = "modify_rule_modification"

    rule_key: RuleKey = prop()
    id: Optional[int] = prop(None)
    xsi_type: XsiType = prop(
        XsiType.RULE_MODIFICATION, key=Jsonable.Prop.XSI_TYPE.value
    )

    _rule: SecurityRule = prop(None, jsonify=False)

    @property
    def rule(self):
        if self._rule:
            return self._rule

        rules = St.default.get_rules(
            device=self.rule_key.device_id, rule_uid=self.rule_key.rule_uid
        )
        rule = rules[0]
        self._rule = rule
        return self._rule


@propify
class ModifyRuleModification(RuleModification):
    xsi_type: RuleModification.XsiType = prop(
        RuleModification.XsiType.MODIFY_RULE_MODIFICATION,
        key=Jsonable.Prop.XSI_TYPE.value,
    )
    source_modifications: Optional[NetworkObjectCellModifications] = prop(None)
    destination_modifications: Optional[NetworkObjectCellModifications] = prop(None)
    service_modifications: Optional[ServiceObjectCellModifications] = prop(None)

    def _add_service_obj_mod(self, modlist, objlist, obj, device_id, cell_action):
        if isinstance(obj, str):
            obj = St.default.get_service(obj, device_id)
            _uid = obj.uid

            obj = ModificationServiceObject.from_securetrack(obj)
        elif isinstance(obj, STService):
            _uid = obj.uid

            obj = ModificationServiceObject.from_securetrack(obj)
        else:
            _uid = None

        if not obj:
            return False

        obj_status = ObjectStatus(
            xsi_type=ObjectStatus.XsiType.EXISTING if _uid else ObjectStatus.XsiType.NEW
        )
        if _uid:
            obj_status.st_uid = _uid

        svc_mod = ServiceObjectCellModification(
            action=cell_action,
            device_service_object=DeviceServiceObject(
                device_id=device_id, status=obj_status
            ),
        )

        found = False
        for ref in objlist:
            if obj_status.st_uid and ref.uid == obj_status.st_uid:
                found = True
                break

        if (cell_action == CellAction.REMOVE and found) or (
            cell_action == CellAction.ADD and not found
        ):
            svc_mod.device_service_object.service_object.append(obj)
            modlist.append(svc_mod)
            return True
        else:
            return False

    def _add_net_obj_mod(self, modlist, objlist, obj, device_id, cell_action):
        if isinstance(obj, str):
            obj = St.default.get_network_object(obj, device_id)
            _uid = obj.uid
            obj = ModificationNetworkObject.from_securetrack(obj)
        elif isinstance(obj, STNetworkObject):
            _uid = obj.uid
            obj = ModificationNetworkObject.from_securetrack(obj)
        else:
            _uid = None

        if not obj:
            return False

        obj_status = ObjectStatus(
            xsi_type=ObjectStatus.XsiType.EXISTING if _uid else ObjectStatus.XsiType.NEW
        )
        if _uid:
            obj_status.st_uid = _uid

        net_mod = NetworkObjectCellModification(
            action=cell_action,
            device_network_object=DeviceNetworkObject(
                device_id=device_id, status=obj_status
            ),
        )

        found = False
        for ref in objlist:
            if obj_status.st_uid and ref.uid == obj_status.st_uid:
                found = True
                break

        if (cell_action == CellAction.REMOVE and found) or (
            cell_action == CellAction.ADD and not found
        ):
            net_mod.device_network_object.network_object.append(obj)
            modlist.append(net_mod)
            return True
        else:
            return False

    def add_source(self, obj: Union[str, NetworkObject], device_id):
        if not self.source_modifications:
            self.source_modifications = NetworkObjectCellModifications()

        return self._add_net_obj_mod(
            self.source_modifications.network_object_cell_modifications,
            self.rule.src_networks,
            obj,
            device_id,
            CellAction.ADD,
        )

    def remove_source(self, obj: Union[str, NetworkObject], device_id):
        if not self.source_modifications:
            self.source_modifications = NetworkObjectCellModifications()

        return self._add_net_obj_mod(
            self.source_modifications.network_object_cell_modifications,
            self.rule.src_networks,
            obj,
            device_id,
            CellAction.REMOVE,
        )

    def add_destination(self, obj: Union[str, NetworkObject], device_id):
        if not self.destination_modifications:
            self.destination_modifications = NetworkObjectCellModifications()

        return self._add_net_obj_mod(
            self.destination_modifications.network_object_cell_modifications,
            self.rule.dest_networks,
            obj,
            device_id,
            CellAction.ADD,
        )

    def remove_destination(self, obj: Union[str, NetworkObject], device_id):
        if not self.destination_modifications:
            self.destination_modifications = NetworkObjectCellModifications()

        return self._add_net_obj_mod(
            self.destination_modifications.network_object_cell_modifications,
            self.rule.dest_networks,
            obj,
            device_id,
            CellAction.REMOVE,
        )

    def add_service(self, obj, device_id):
        if not self.service_modifications:
            self.service_modifications = ServiceObjectCellModifications()

        return self._add_service_obj_mod(
            self.service_modifications.service_object_cell_modifications,
            self.rule.src_services + self.rule.dest_services,
            obj,
            device_id,
            CellAction.ADD,
        )

    def remove_service(self, obj, device_id):
        if not self.service_modifications:
            self.service_modifications = ServiceObjectCellModifications()

        return self._add_service_obj_mod(
            self.service_modifications.service_object_cell_modifications,
            self.rule.src_services + self.rule.dest_services,
            obj,
            device_id,
            CellAction.REMOVE,
        )


def classify_rule_modification(obj):
    return (
        {"modify_rule_modification": ModifyRuleModification}
        .get(obj.get(Jsonable.Prop.XSI_TYPE.value))
        .kwargify(obj)
    )


@propify
class RuleModificationField(RuleOperation):
    xsi_type: FieldXsiType = prop(
        FieldXsiType.RULE_MODIFICATION_FIELD, key=Jsonable.Prop.XSI_TYPE.value
    )

    rule_modifications: List[RuleModification] = prop(
        factory=list, flatify="rule_modification", kwargify=classify_rule_modification
    )

    def _get_rule_mod_for_rule(self, rule: SecurityRule):
        rule_key = RuleKey(
            device_id=rule.device.id,
            binding_uid=rule.bindings[0].uid,
            rule_uid=rule.uid,
        )

        for mod in self.rule_modifications:
            if mod.rule_key == rule_key:
                return mod

        mod = ModifyRuleModification(rule_key=rule_key)
        mod._rule = rule

        self.rule_modifications.append(mod)

        return mod

    def add_rule_modification(self, rule: SecurityRule) -> RuleModification:
        if not self.is_rule_added(rule):
            self.add_rule(rule)

        mod = self._get_rule_mod_for_rule(rule)
        return mod

    def add_source_object(self, rule: SecurityRule, obj: Union[str, NetworkObject]):
        return self.add_rule_modification(rule).add_source(obj, rule.device.id)

    def remove_source_object(self, rule: SecurityRule, obj: Union[str, NetworkObject]):
        return self.add_rule_modification(rule).remove_source(obj, rule.device.id)

    def add_destination_object(
        self, rule: SecurityRule, obj: Union[str, NetworkObject]
    ):
        return self.add_rule_modification(rule).add_destination(obj, rule.device.id)

    def remove_destination_object(
        self, rule: SecurityRule, obj: Union[str, NetworkObject]
    ):
        return self.add_rule_modification(rule).remove_destination(obj, rule.device.id)

    def add_service(self, rule: SecurityRule, obj: ModificationServiceObject):
        return self.add_rule_modification(rule).add_service(obj, rule.device.id)

    def remove_service(self, rule: SecurityRule, obj: ModificationServiceObject):
        return self.add_rule_modification(rule).remove_service(obj, rule.device.id)


@propify
class RuleRecertification(RuleOperation):
    xsi_type: FieldXsiType = prop(
        FieldXsiType.RULE_RECERTIFICATION, key=Jsonable.Prop.XSI_TYPE.value
    )


@propify
class RuleDecommission(RuleOperation):
    class Action(Enum):
        DISABLE = "disable"
        REMOVE = "remove"

    xsi_type: FieldXsiType = prop(
        FieldXsiType.RULE_DECOMMISSION, key=Jsonable.Prop.XSI_TYPE.value
    )

    designer_result: Optional[Designer] = prop(None)
    verifier_result: Optional[dict] = prop(None)

    action: Optional[Action] = prop(None)
