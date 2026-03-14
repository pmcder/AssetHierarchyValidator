from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

import networkx as nx

from .models import Asset, AssetType

if TYPE_CHECKING:
    pass


VALID_PARENT_TYPES: dict[AssetType, set[AssetType]] = {
    AssetType.ENTERPRISE: {AssetType.SITE},
    AssetType.SITE: {AssetType.FACILITY},
    AssetType.FACILITY: {AssetType.SYSTEM},
    AssetType.SYSTEM: {AssetType.EQUIPMENT},
    AssetType.EQUIPMENT: {AssetType.COMPONENT},
    AssetType.COMPONENT: set(),
}


class ErrorCode(str, Enum):
    DUPLICATE_ID = "DUPLICATE_ID"
    MISSING_PARENT = "MISSING_PARENT"
    CYCLE_DETECTED = "CYCLE_DETECTED"
    ORPHAN_NODE = "ORPHAN_NODE"
    INVALID_TYPE_HIERARCHY = "INVALID_TYPE_HIERARCHY"
    SELF_REFERENCE = "SELF_REFERENCE"
    MULTIPLE_ROOTS = "MULTIPLE_ROOTS"
    EMPTY_GRAPH = "EMPTY_GRAPH"


@dataclass
class ValidationError:
    code: ErrorCode
    message: str
    asset_ids: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)

    def __str__(self) -> str:
        status = "PASSED" if self.is_valid else "FAILED"
        lines = [f"Validation: {status} ({len(self.errors)} errors, {len(self.warnings)} warnings)"]
        for err in self.errors:
            ids = f" [{', '.join(err.asset_ids)}]" if err.asset_ids else ""
            lines.append(f"  ERROR  [{err.code}]{ids}: {err.message}")
        for warn in self.warnings:
            ids = f" [{', '.join(warn.asset_ids)}]" if warn.asset_ids else ""
            lines.append(f"  WARN   [{warn.code}]{ids}: {warn.message}")
        return "\n".join(lines)


class HierarchyValidator:
    def validate(self, assets: list[Asset]) -> ValidationResult:
        errors: list[ValidationError] = []
        warnings: list[ValidationError] = []

        empty_error = self._check_empty(assets)
        if empty_error:
            errors.append(empty_error)
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        errors.extend(self._check_duplicate_ids(assets))
        errors.extend(self._check_missing_parent_refs(assets))
        errors.extend(self._check_self_references(assets))
        errors.extend(self._check_multiple_roots(assets))
        errors.extend(self._check_type_hierarchy(assets))
        errors.extend(self._check_cycles(assets))
        warnings.extend(self._check_orphan_nodes(assets))

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _check_empty(self, assets: list[Asset]) -> ValidationError | None:
        if not assets:
            return ValidationError(
                code=ErrorCode.EMPTY_GRAPH,
                message="Asset list is empty — nothing to build a graph from.",
            )
        return None

    def _check_duplicate_ids(self, assets: list[Asset]) -> list[ValidationError]:
        counts = Counter(a.id for a in assets)
        dupes = [asset_id for asset_id, count in counts.items() if count > 1]
        if not dupes:
            return []
        return [ValidationError(
            code=ErrorCode.DUPLICATE_ID,
            message=f"Duplicate asset IDs found: {dupes}",
            asset_ids=dupes,
        )]

    def _check_missing_parent_refs(self, assets: list[Asset]) -> list[ValidationError]:
        id_set = {a.id for a in assets}
        missing = [
            a.id for a in assets
            if a.parent_id is not None and a.parent_id not in id_set
        ]
        if not missing:
            return []
        return [ValidationError(
            code=ErrorCode.MISSING_PARENT,
            message=f"Assets reference non-existent parent IDs: {missing}",
            asset_ids=missing,
        )]

    def _check_self_references(self, assets: list[Asset]) -> list[ValidationError]:
        self_refs = [a.id for a in assets if a.parent_id == a.id]
        if not self_refs:
            return []
        return [ValidationError(
            code=ErrorCode.SELF_REFERENCE,
            message=f"Assets reference themselves as parent: {self_refs}",
            asset_ids=self_refs,
        )]

    def _check_multiple_roots(self, assets: list[Asset]) -> list[ValidationError]:
        roots = [a.id for a in assets if a.parent_id is None]
        if len(roots) == 1:
            return []
        if len(roots) == 0:
            return [ValidationError(
                code=ErrorCode.MULTIPLE_ROOTS,
                message="No root node found (every asset has a parent_id — cycle or missing root).",
            )]
        return [ValidationError(
            code=ErrorCode.MULTIPLE_ROOTS,
            message=f"Expected exactly 1 root (parent_id=None), found {len(roots)}: {roots}",
            asset_ids=roots,
        )]

    def _check_type_hierarchy(self, assets: list[Asset]) -> list[ValidationError]:
        id_to_asset = {a.id: a for a in assets}
        violations: list[str] = []
        for asset in assets:
            if asset.parent_id is None:
                continue
            parent = id_to_asset.get(asset.parent_id)
            if parent is None:
                continue  # already caught by missing_parent check
            allowed_child_types = VALID_PARENT_TYPES.get(parent.asset_type, set())
            if asset.asset_type not in allowed_child_types:
                violations.append(asset.id)
        if not violations:
            return []
        return [ValidationError(
            code=ErrorCode.INVALID_TYPE_HIERARCHY,
            message=(
                f"{len(violations)} asset(s) violate the type hierarchy "
                f"(e.g. COMPONENT cannot have children, or wrong level ordering): {violations}"
            ),
            asset_ids=violations,
        )]

    def _check_cycles(self, assets: list[Asset]) -> list[ValidationError]:
        g: nx.DiGraph = nx.DiGraph()
        for asset in assets:
            g.add_node(asset.id)
        for asset in assets:
            if asset.parent_id is not None:
                g.add_edge(asset.parent_id, asset.id)
        try:
            cycle = nx.find_cycle(g)
            cycle_ids = list({node for edge in cycle for node in edge})
            return [ValidationError(
                code=ErrorCode.CYCLE_DETECTED,
                message=f"Cycle detected among assets: {cycle_ids}",
                asset_ids=cycle_ids,
            )]
        except nx.NetworkXNoCycle:
            return []

    def _check_orphan_nodes(self, assets: list[Asset]) -> list[ValidationError]:
        id_set = {a.id for a in assets}
        # Build in/out degree maps
        in_degree: dict[str, int] = {a.id: 0 for a in assets}
        out_degree: dict[str, int] = {a.id: 0 for a in assets}
        for asset in assets:
            if asset.parent_id in id_set:
                in_degree[asset.id] += 0   # child doesn't get in-degree from parent ref
                out_degree[asset.parent_id] = out_degree.get(asset.parent_id, 0) + 1
        # Recompute properly: in_degree = number of parents pointing to this node
        in_degree = {a.id: 0 for a in assets}
        for asset in assets:
            if asset.parent_id in id_set:
                in_degree[asset.id] += 1

        orphans = [
            a.id for a in assets
            if in_degree[a.id] == 0
            and out_degree.get(a.id, 0) == 0
            and a.parent_id is None
            and a.asset_type != AssetType.ENTERPRISE
        ]
        if not orphans:
            return []
        return [ValidationError(
            code=ErrorCode.ORPHAN_NODE,
            message=f"Orphan nodes detected (no parent, no children, not ENTERPRISE): {orphans}",
            asset_ids=orphans,
        )]
