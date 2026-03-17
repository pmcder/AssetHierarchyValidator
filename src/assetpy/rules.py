"""
Custom validation rules for assetpy.

Quick-start for AI agents
--------------------------
To add a new rule, copy the template below into this file, fill in the blanks,
export the class from ``src/assetpy/__init__.py``, and use it:

    validator = HierarchyValidator(extra_rules=[MyRule()])
    result = validator.validate(assets)

See ``ai/CLAUDE.md`` for the full step-by-step guide.
"""
from __future__ import annotations

import re
from typing import Literal, runtime_checkable

from typing import Protocol

from .models import Asset
from .validation import ValidationError

Severity = Literal["error", "warning"]


@runtime_checkable
class ValidationRule(Protocol):
    """Protocol that all custom validation rules must satisfy."""

    severity: Severity

    def check(self, assets: list[Asset]) -> list[ValidationError]:
        ...


class NamingConventionRule:
    """Warn when asset IDs do not match a required naming pattern."""

    severity: Severity = "warning"

    def __init__(
        self,
        pattern: str = r"^[A-Z]+-\d{3,}$",
        severity: Severity = "warning",
    ) -> None:
        self._pattern = re.compile(pattern)
        self.severity = severity

    def check(self, assets: list[Asset]) -> list[ValidationError]:
        violations = [a.id for a in assets if not self._pattern.match(a.id)]
        if not violations:
            return []
        return [ValidationError(
            code="NAMING_CONVENTION",
            message=(
                f"{len(violations)} asset ID(s) do not match the required pattern "
                f"'{self._pattern.pattern}': {violations}"
            ),
            asset_ids=violations,
        )]


class MaxDepthRule:
    """Warn when any asset's depth from the root exceeds a maximum."""

    severity: Severity = "warning"

    def __init__(self, max_depth: int = 6, severity: Severity = "warning") -> None:
        self._max_depth = max_depth
        self.severity = severity

    def check(self, assets: list[Asset]) -> list[ValidationError]:
        id_to_parent: dict[str, str | None] = {a.id: a.parent_id for a in assets}
        depth_cache: dict[str, int] = {}

        def depth(asset_id: str, visited: set[str]) -> int:
            if asset_id in depth_cache:
                return depth_cache[asset_id]
            if asset_id in visited:
                # cycle — bail out; cycle checker will catch this
                return 0
            parent_id = id_to_parent.get(asset_id)
            if parent_id is None:
                result = 0
            else:
                result = 1 + depth(parent_id, visited | {asset_id})
            depth_cache[asset_id] = result
            return result

        violations = [
            a.id for a in assets
            if depth(a.id, set()) > self._max_depth
        ]
        if not violations:
            return []
        return [ValidationError(
            code="MAX_DEPTH_EXCEEDED",
            message=(
                f"{len(violations)} asset(s) exceed the maximum hierarchy depth of "
                f"{self._max_depth}: {violations}"
            ),
            asset_ids=violations,
        )]
