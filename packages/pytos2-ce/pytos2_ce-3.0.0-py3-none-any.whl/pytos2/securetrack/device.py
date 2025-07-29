from enum import Enum
from typing import Optional, List

from netaddr import IPAddress  # type: ignore
from attr.converters import optional
import attr

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, kwargify

from pytos2 import securetrack


@propify
class DeviceLicenseStatus(Jsonable):
    class Prop(Enum):
        TYPE = "type"

    expiration: Optional[str] = prop(None, repr=False)
    used: Optional[int] = prop(None, repr=False)
    status: str = prop("")
    sku: Optional[str] = prop(None, repr=False)
    type: Optional[str] = prop(
        None, key=Prop.TYPE.value, cmp=False, repr=True, init=True
    )


@propify
class Device(Jsonable):
    class Model(Enum):
        CP_CLM = "cp_clm"
        CP_MDS = "cp_mds"
        CP_CMA = "cp_cma"
        CP_DOMAIN_R80PLUS = "cp_domain_r80plus"
        CP_SMC_R80PLUS = "cp_smc_r80plus"
        CP_MDS_R80PLUS = "cp_mds_r80plus"
        CP_SMRT_CNTR = "cp_smrt_cntr"
        CP_SMART_ONE = "cp_smart_one"
        ROUTER = "router"
        XR_ROUTER = "xr_router"
        MODULE = "module"
        MODULE_CLUSTER = "module_cluster"
        NETSCREEN = "netscreen"
        NETSCREEN_CLUSTER = "netscreen_cluster"
        JUNOS = "junos"
        JUNOSSTATELESS = "junosStateless"
        NSM = "nsm"
        NSM_DEVICE = "nsm_device"
        NSM_NETSCREEN_ISG = "nsm_netscreen_isg"
        CSM = "csm"
        CSM_OLD = "csm_old"
        CSM_DEVICE = "csm_device"
        CSM_ASA = "csm_asa"
        CSM_FWSM = "csm_fwsm"
        CSM_ROUTER = "csm_router"
        CSM_NEXUS = "csm_nexus"
        CSM_SWITCH = "csm_switch"
        FWSM = "fwsm"
        NEXUS = "nexus"
        FMG = "fmg"
        FMG_VDOM = "fmg_vdom"
        FMG_FW = "fmg_fw"
        FMG_VDOM_MANAGER = "fmg_vdom_manager"
        ASA = "asa"
        PIX = "pix"
        BIGIP = "bigip"
        NEW_BIGIP = "new_bigip"
        STONESOFT_SMC = "stonesoft_smc"
        SINGLE_FW = "single_fw"
        MASTER_ENGINE = "master_engine"
        VIRTUAL_FW = "virtual_fw"
        FW_CLUSTER = "fw_cluster"
        L3_SWITCH = "L3_switch"
        SWITCH = "switch"
        FORTIGATE = "fortigate"
        PALOALTOFW = "PaloAltoFW"
        PANORAMA = "Panorama"
        PANORAMA_DEVICE = "Panorama_device"
        PANORAMA_DEVICE_CLUSTER = "Panorama_device_cluster"
        PANORAMA_NG = "Panorama_ng"
        PANORAMA_DEVICE_GROUP = "Panorama_device_group"
        PANORAMA_NG_FW = "Panorama_ng_fw"
        MCAFEEFW = "mcafeeFW"
        PROXYSG = "proxysg"
        IPTABLES = "iptables"
        NSX_MANAGER = "nsx_manager"
        NSX_T_MANAGER = "nsx_t_manager"
        NSX_FW = "nsx_fw"
        NSX_LRTR = "nsx_lrtr"
        NSX_EDGE = "nsx_edge"
        AWS_MANAGER = "aws_manager"
        AWS_VPC = "aws_vpc"
        AWS_GW_LB = "aws_gw_lb"
        OPENSTACK_MANAGER = "openStack_manager"
        OPENSTACK_REGION = "openStack_region"
        AZURE_RM_FW = "azure_rm_fw"
        AZURE_RM_FW_POLICY = "azure_rm_fw_policy"
        AZURE_RM_FW_POLICY_ROOT = "azure_rm_fw_policy_root"
        AZURE_RM_LB = "azure_rm_lb"
        AZURE_RM_MANAGER = "azure_rm_manager"
        AZURE_RM_VNET = "azure_rm_vnet"
        AZURE_VHUB = "azure_vhub"
        AZURE_VWAN = "azure_vwan"
        FORTIMANAGER = "fortimanager"
        FMG_ADOM = "fmg_adom"
        FMG_FIREWALL = "fmg_firewall"
        ACI = "aci"
        ACI_TENANT = "aci_tenant"
        FMC = "fmc"
        FIREPOWER = "firepower"
        FMC_DOMAIN = "fmc_domain"
        ZIA_CLOUD_FIREWALL = "zia_cloud_firewall"
        AWS_TRANSITGATEWAY = "aws_transitgateway"
        MERAKI = "meraki"
        MERAKI_ORGANIZATION = "meraki_organization"
        MERAKI_NETWORK = "meraki_network"
        GOOGLE_CLOUD_PLATFORM = "google_cloud_platform"
        GOOGLE_VPC = "gcp_vpc"
        ARISTA_EOS = "arista_eos"
        ARISTA_CVP = "arista_cvp"

    class VirtualType(Enum):
        DEVICE = "device"
        VDOM_MANAGER = "vdom_manager"
        CONTEXT = "context"
        VT_STANDALONE = "vt_standalone"
        MASTERENGINE = "MasterEngine"
        MDOM = "mdom"
        MANAGEMENT = "management"
        VSX = "vsx"
        VSX_ROUTER = "vsx_router"
        VSX_SWITCH = "vsx_switch"
        VSX_BRIDGED = "vsx_bridged"
        VSX_BOX = "vsx_box"

    class Vendor(Enum):
        CISCO = "Cisco"
        FORTINET = "Fortinet"
        NETSCREEN = "Netscreen"
        CHECKPOINT = "Checkpoint"
        PALO_ALTO = "PaloAltoNetworks"
        NEW_F5 = "NewF5"
        F5 = "f5"
        MCAFEE = "Mcafee"
        STONESOFT = "Stonesoft"
        BLUECOAT = "bluecoat"
        GENERIC = "Generic"
        LINUX = "linux"
        VMWARE = "VMware"
        AMAZON = "Amazon"
        OPENSTACK = "OpenStack"
        AZURE = "Azure"
        ZSCALER = "Zscaler"
        GOOGLE = "GoogleCloudPlatform"
        ARISTA = "Arista"

    id: int = prop(0, converter=int)
    installed_policy: Optional[str] = prop(None)
    latest_revision: Optional[int] = prop(None, converter=optional(int), repr=False)
    parent_id: Optional[int] = prop(None, converter=optional(int))
    virtual_type: Optional[VirtualType] = prop(None)
    context_name: Optional[str] = prop(None)
    _ip: Optional[IPAddress] = attr.ib(None, repr=False)
    os_version: Optional[str] = prop(None, key="OS_Version")
    domain_name: str = prop(None)
    model: Optional[Model] = prop(None)
    vendor: Optional[Vendor] = prop(None)
    offline: bool = prop(False)
    topology: bool = prop(False)
    module_uid: Optional[str] = prop(None)
    module_type: Optional[str] = prop(None)
    domain_id: Optional[int] = prop(None, converter=optional(int), repr=False)
    name: Optional[str] = prop(None)
    status: str = prop(None)
    licenses: Optional[List[DeviceLicenseStatus]] = prop(factory=list)

    @property
    def parent(self) -> Optional["Device"]:
        if not self.parent_id:
            return None
        return securetrack.St.default.get_device(self.parent_id)

    @property
    def parents(self) -> List["Device"]:
        d = self
        parents: list = []
        while d.parent:
            d = d.parent
            parents.insert(0, d)

        return parents

    @property
    def children(self):
        return [
            d for d in securetrack.St.default.get_devices() if d.parent_id == self.id
        ]

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        self._ip = IPAddress(val)

    @classmethod
    def kwargify(cls, obj):
        _obj, kwargs = kwargify(cls, obj)

        ip = _obj.get("ip")

        ip = IPAddress(ip) if ip is not None else None
        kwargs["ip"] = ip

        # handle non license device result
        if not _obj.get("licenses"):
            kwargs["licenses"] = list()
        else:
            kwargs["licenses"] = [
                DeviceLicenseStatus.kwargify(lic) for lic in _obj.get("licenses")
            ]

        return cls(**kwargs)

    def get_revisions(self):
        return securetrack.St.default.get_revisions(device=self.id)

    def get_rules(self):
        return securetrack.St.default.get_rules(device=self.id)

    def get_nat_rules(self):
        return securetrack.St.default.get_nat_rules(device=self.id)

    def get_network_objects(self, add_parent_objects: Optional[bool] = None):
        return securetrack.St.default.get_network_objects(
            device=self.id, add_parent_objects=add_parent_objects
        )

    def search_network_objects(self, **kwargs):
        return securetrack.St.default.search_network_objects(device=self.id, **kwargs)

    @property
    def network_objects(self):
        return self.get_network_objects()

    def get_interfaces(self):
        return securetrack.St.default.get_interfaces(device_id=self.id)

    @property
    def interfaces(self):
        return self.get_interfaces()

    def get_topology_interfaces(self):
        return securetrack.St.default.get_topology_interfaces(device_id=self.id)

    @property
    def topology_interfaces(self):
        return self.get_topology_interfaces()

    def get_bindable_objects(self):
        return securetrack.St.default.get_bindable_objects(device_id=self.id)

    @property
    def bindable_objects(self):
        return self.get_bindable_objects()

    def get_time_objects(self):
        return securetrack.St.default.get_time_objects_by_device(self.id)


@propify
class InternetObject(Jsonable):
    class Meta(Enum):
        ROOT = "internet_referral_object"

    class XsiType(Enum):
        INTERNET_REFERRAL_OBJECT_NAME = "internetReferralObjectNameDTO"

    xsi_type: XsiType = prop(XsiType.INTERNET_REFERRAL_OBJECT_NAME)
    device_id: int = prop(converter=int)
    object_name: str = prop(None)
