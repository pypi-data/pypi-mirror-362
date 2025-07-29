from enum import Enum
from datetime import date, datetime
from typing import Optional, List

from pytos2.models import Jsonable
from pytos2.utils import propify, prop, safe_iso8601_date


@propify
class Customer(Jsonable):
    id: str = prop("", repr=False)
    site_id: Optional[str] = prop(None, repr=False)
    site: Optional[str] = prop(None)
    name: str = prop("")


@propify
class SKUDevice(Jsonable):
    id: str = prop("")
    consumed: int = prop(0)
    name: str = prop("")


@propify
class SKU(Jsonable):
    name: str = prop("")
    description: Optional[str] = prop(None, repr=False)
    quantity: int = prop(0)
    expiration: Optional[datetime] = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )
    devices: List[SKUDevice] = prop(factory=list, key="devices", repr=False)


@propify
class License(Jsonable):
    id: str = prop("")
    expiration: datetime = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )
    uid: Optional[str] = prop(None, repr=False)
    customer: Customer = prop(None)
    issued: Optional[datetime] = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )
    skus: List[SKU] = prop(factory=list, repr=False, flatify="sku")
    type: str = prop("")


@propify
class TieredLicenseMessage(Jsonable):
    category: str = prop(None)
    severity: str = prop(None)
    code: str = prop(None)
    message: str = prop(None)
    params: List[str]


@propify
class TieredLicense(Jsonable):
    class LicenseType(Enum):
        EVALUATION = "evaluation"
        FULL = "full"

    class Status(Enum):
        VALID = "valid"
        EXPIRED = "expired"

    class SiteType(Enum):
        PRODUCTION = "production"
        LAB = "lab"

    supported: bool = prop(None)
    version: str = prop(None)
    tier: str = prop(None)
    customer_id: str = prop(None)
    customer_name: str = prop(None)
    license_file_id: str = prop(None)
    site_name: str = prop(None)
    site_type: SiteType = prop(None)
    site_id: str = prop(None)
    installed: datetime = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )
    expires: datetime = prop(
        None, kwargify=safe_iso8601_date, jsonify=lambda d: d.isoformat() if d else None
    )
    status: Status = prop(None)
    type: LicenseType = prop(None)
    messages: List[TieredLicenseMessage] = prop(list)
