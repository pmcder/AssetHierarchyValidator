from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AssetType(str, Enum):
    ENTERPRISE = "ENTERPRISE"
    SITE = "SITE"
    FACILITY = "FACILITY"
    SYSTEM = "SYSTEM"
    EQUIPMENT = "EQUIPMENT"
    COMPONENT = "COMPONENT"


class Status(str, Enum):
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"
    DECOMMISSIONED = "DECOMMISSIONED"


class Criticality(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Asset:
    id: str
    name: str
    asset_type: AssetType
    status: Status
    criticality: Criticality
    parent_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.asset_type, str):
            self.asset_type = AssetType(self.asset_type)
        if isinstance(self.status, str):
            self.status = Status(self.status)
        if isinstance(self.criticality, str):
            self.criticality = Criticality(self.criticality)
