"""CLI demo script for the assetpy EAM Network Graph Application."""
from __future__ import annotations

import argparse
import sys

# Support both installed-package and src-layout direct invocation
try:
    from assetpy import (
        AssetGraph,
        Asset,
        AssetType,
        Criticality,
        HierarchyValidator,
        PlotlyVisualizer,
        Status,
        TraversalEngine,
    )
    from assetpy.demo_data import build_demo_assets
except ModuleNotFoundError:
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    from assetpy import (  # type: ignore[assignment]
        AssetGraph,
        Asset,
        AssetType,
        Criticality,
        HierarchyValidator,
        PlotlyVisualizer,
        Status,
        TraversalEngine,
    )
    from assetpy.demo_data import build_demo_assets  # type: ignore[assignment]


DIVIDER = "-" * 60


def main() -> None:
    parser = argparse.ArgumentParser(
        description="assetpy — EAM Network Graph demo"
    )
    parser.add_argument(
        "--color-by",
        choices=["asset_type", "criticality"],
        default="asset_type",
        help="Color scheme for the graph visualization (default: asset_type)",
    )
    parser.add_argument(
        "--output",
        default="asset_graph.html",
        help="Output HTML file path (default: asset_graph.html)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the HTML in the browser after rendering",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 1. Load demo data
    # ------------------------------------------------------------------
    print(DIVIDER)
    print("1. LOADING DEMO DATA")
    print(DIVIDER)
    assets = build_demo_assets()
    print(f"   Loaded {len(assets)} assets from build_demo_assets()")

    # ------------------------------------------------------------------
    # 2. Validate
    # ------------------------------------------------------------------
    print()
    print(DIVIDER)
    print("2. VALIDATION")
    print(DIVIDER)
    validator = HierarchyValidator()
    result = validator.validate(assets)
    print(f"   {result}")

    # ------------------------------------------------------------------
    # 3. Build graph
    # ------------------------------------------------------------------
    print()
    print(DIVIDER)
    print("3. BUILD ASSET GRAPH")
    print(DIVIDER)
    ag = AssetGraph.from_assets(assets, validate=False)  # already validated above
    print(f"   Nodes : {ag.node_count()}")
    print(f"   Edges : {ag.edge_count()}")

    # ------------------------------------------------------------------
    # 4. Traversal demos
    # ------------------------------------------------------------------
    print()
    print(DIVIDER)
    print("4. TRAVERSAL DEMOS")
    print(DIVIDER)
    te = TraversalEngine(ag)

    # 4a. Root lookup
    root = te.get_root("CMP-001")
    print(f"   Root of CMP-001          : {root.id} — {root.name}")

    # 4b. Ancestors chain
    ancestors = te.get_ancestors("CMP-001")
    chain = " → ".join(f"{a.id}({a.asset_type.value[:3]})" for a in ancestors)
    print(f"   Ancestors of CMP-001     : {chain}")

    # 4c. Children of a facility
    children = te.get_children("FAC-002")
    print(f"   Children of FAC-002      : {[c.id for c in children]}")

    # 4d. Descendant count
    desc_count = len(te.get_descendants("SITE-001"))
    print(f"   Descendants of SITE-001  : {desc_count}")

    # 4e. Path finding
    path = te.find_path("ENT-001", "CMP-011")
    path_str = " → ".join(a.id for a in path)
    print(f"   Path ENT-001 → CMP-011   : {path_str}")

    # 4f. Subtree size
    subtree_sz = te.get_subtree_size("FAC-003")
    print(f"   Subtree size of FAC-003  : {subtree_sz}")

    # 4g. Depth
    depth = te.get_depth("CMP-001")
    print(f"   Depth of CMP-001         : {depth}")

    # ------------------------------------------------------------------
    # 5. Intentional validation failure demo
    # ------------------------------------------------------------------
    print()
    print(DIVIDER)
    print("5. INTENTIONAL VALIDATION FAILURE DEMO")
    print(DIVIDER)
    bad_assets = list(assets)
    # Duplicate ID
    bad_assets.append(Asset(
        id="ENT-001",                    # duplicate
        name="Fake Duplicate Enterprise",
        asset_type=AssetType.ENTERPRISE,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id=None,
    ))
    # Missing parent reference
    bad_assets.append(Asset(
        id="SYS-999",
        name="Orphaned System",
        asset_type=AssetType.SYSTEM,
        status=Status.OPERATIONAL,
        criticality=Criticality.LOW,
        parent_id="FAC-999",             # non-existent
    ))
    bad_result = validator.validate(bad_assets)
    print(f"   {bad_result}")

    # ------------------------------------------------------------------
    # 6. Render Plotly HTML
    # ------------------------------------------------------------------
    print()
    print(DIVIDER)
    print("6. RENDER PLOTLY HTML")
    print(DIVIDER)
    viz = PlotlyVisualizer(ag)
    out = viz.render(
        color_by=args.color_by,
        output_path=args.output,
        title="Gulf Coast Petroleum Group — Asset Hierarchy",
        open_browser=not args.no_browser,
    )
    print(f"   Graph written to: {out}")
    if not args.no_browser:
        print("   Opening in browser...")
    print()
    print(DIVIDER)
    print("DONE")
    print(DIVIDER)


if __name__ == "__main__":
    main()
