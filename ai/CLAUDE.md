# assetpy — AI Agent Guide: Writing Validation Rules

This document is the single reference an AI agent needs to add a new validation rule to assetpy. No codebase exploration required.

---

## Step-by-step: Adding a new rule

1. Open `src/assetpy/rules.py`.

2. Copy this template verbatim and fill in the blanks:

```python
class MyRule:
    """One-line description of what this rule checks."""

    severity: Severity = "warning"   # or "error" to make it blocking

    def __init__(self) -> None:      # add constructor params if the rule is configurable
        pass

    def check(self, assets: list[Asset]) -> list[ValidationError]:
        violations = [a.id for a in assets if <YOUR_CONDITION_HERE>]
        if not violations:
            return []
        return [ValidationError(
            code="YOUR_CODE_IN_SCREAMING_SNAKE_CASE",
            message=f"<human-readable explanation>: {violations}",
            asset_ids=violations,
        )]
```

3. The imports already at the top of `rules.py` cover everything needed (`Asset`, `ValidationError`, `Severity`). Add no new imports unless the rule needs the standard library.

4. Export the new class from `src/assetpy/__init__.py` — add it to the `from .rules import ...` line and to `__all__`.

5. Done. The rule is usable immediately:
   ```python
   validator = HierarchyValidator(extra_rules=[MyRule()])
   result = validator.validate(assets)
   ```

---

## Asset fields available inside `check()`

Every `asset` in the list has:

```
asset.id          str           — unique identifier, e.g. "EQP-042"
asset.name        str           — human label
asset.asset_type  AssetType     — ENTERPRISE | SITE | FACILITY | SYSTEM | EQUIPMENT | COMPONENT
asset.status      Status        — OPERATIONAL | DEGRADED | MAINTENANCE | DECOMMISSIONED
asset.criticality Criticality   — CRITICAL | HIGH | MEDIUM | LOW
asset.parent_id   str | None    — None means this asset is the root
asset.metadata    dict[str,str] — arbitrary key/value pairs
```

Enum values are compared as `asset.asset_type == AssetType.EQUIPMENT` or by string `asset.asset_type.value == "EQUIPMENT"`.

---

## `ValidationError` constructor

```python
ValidationError(
    code="MY_CODE",           # str, SCREAMING_SNAKE_CASE — built-in codes are in ErrorCode enum
    message="explanation",    # shown in validation output
    asset_ids=["id1","id2"],  # list of affected IDs; omit or pass [] if not asset-specific
)
```

---

## Severity rules

- `severity = "error"` → findings go to `result.errors`; `result.is_valid` becomes `False`; `AssetGraph.from_assets(validate=True)` raises `ValueError`
- `severity = "warning"` → findings go to `result.warnings`; graph still builds

---

## Key types reference (for type annotations)

```python
from assetpy.models     import Asset, AssetType, Status, Criticality
from assetpy.validation import ValidationError, ValidationResult, ErrorCode
from assetpy.rules      import ValidationRule, Severity
```

---

## Running / testing a new rule

```bash
python - <<'EOF'
from assetpy import HierarchyValidator
from assetpy.demo_data import build_demo_assets
from assetpy.rules import MyRule   # replace with your rule

assets = build_demo_assets()
result = HierarchyValidator(extra_rules=[MyRule()]).validate(assets)
print(result)
EOF
```
