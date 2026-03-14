# assetpy

Enterprise Asset Management (EAM) graph library for modeling and visualizing hierarchical asset structures. Built on [NetworkX](https://networkx.org/) and [Plotly](https://plotly.com/), it provides a validated, traversable directed graph of assets from enterprise down to component level.

---

## Features

- **6-level asset hierarchy** — Enterprise → Site → Facility → System → Equipment → Component
- **Graph-based model** — Uses a NetworkX directed graph for efficient traversal and path-finding
- **Validation engine** — Detects duplicate IDs, missing parents, invalid hierarchy types, cycles, and orphan nodes
- **Traversal API** — Navigate the hierarchy with methods for children, ancestors, descendants, siblings, paths, depth, and subtree size
- **Interactive visualization** — Generates a self-contained HTML file with a zoomable, hoverable Plotly graph
- **Flexible coloring** — Color nodes by asset type or criticality level
- **Demo dataset** — A ~95-node Gulf Coast petroleum refinery hierarchy included out of the box

---

## Requirements

- Python >= 3.11
- [NetworkX](https://networkx.org/) >= 3.2
- [Plotly](https://plotly.com/) >= 5.18
- [Graphviz](https://graphviz.org/) *(optional — improves graph layout)*

---

## Installation

```bash
git clone <repo-url>
cd assetpy
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

---

## Quickstart

### Run the demo

```bash
python main.py
```

This loads a ~95-node refinery hierarchy, validates it, runs sample traversal queries, and opens an interactive graph in your browser.

### CLI options

```bash
assetpy [--color-by {asset_type|criticality}] [--output FILE] [--no-browser]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--color-by` | `asset_type` | Color nodes by `asset_type` or `criticality` |
| `--output` | `asset_graph.html` | Output path for the HTML visualization |
| `--no-browser` | off | Skip auto-opening the file in a browser |

**Examples:**

```bash
# Color by criticality, save to a custom path
assetpy --color-by criticality --output refinery.html

# Generate file without opening browser
assetpy --no-browser --output report.html
```

---

## Using the Library

### Define assets

```python
from assetpy import Asset, AssetType, Status, Criticality

assets = [
    Asset(
        id="ENT-001",
        name="Acme Corporation",
        asset_type=AssetType.ENTERPRISE,
        status=Status.OPERATIONAL,
        criticality=Criticality.CRITICAL,
        parent_id=None,
    ),
    Asset(
        id="SITE-001",
        name="Houston Refinery",
        asset_type=AssetType.SITE,
        status=Status.OPERATIONAL,
        criticality=Criticality.HIGH,
        parent_id="ENT-001",
        metadata={"region": "Gulf Coast", "capacity": "250,000 bpd"},
    ),
    # ...
]
```

### Build and validate the graph

```python
from assetpy import AssetGraph, HierarchyValidator

# Validate before building
validator = HierarchyValidator()
result = validator.validate(assets)

if result.is_valid:
    graph = AssetGraph.from_assets(assets)
else:
    for error in result.errors:
        print(f"[{error.code}] {error.message}")
```

### Traverse the hierarchy

```python
from assetpy import TraversalEngine

engine = TraversalEngine(graph)

# Navigate up
root = engine.get_root("COMP-042")
ancestors = engine.get_ancestors("COMP-042")

# Navigate down
children = engine.get_children("SYS-003")
descendants = engine.get_descendants("FAC-001")

# Filter by type
equipment = engine.get_children_by_type("SYS-003", AssetType.EQUIPMENT)

# Metrics
depth = engine.get_depth("EQUIP-017")
size = engine.get_subtree_size("SITE-001")

# Path between any two nodes
path = engine.find_path("ENT-001", "COMP-042")
```

### Generate a visualization

```python
from assetpy import PlotlyVisualizer

viz = PlotlyVisualizer(graph)

# Color by asset type (default)
viz.render(output_path="asset_graph.html", color_by="asset_type", open_browser=True)

# Color by criticality
viz.render(output_path="criticality_graph.html", color_by="criticality", open_browser=False)
```

---

## Asset Hierarchy

Valid parent-child type relationships:

```
ENTERPRISE
    └── SITE
            └── FACILITY
                    └── SYSTEM
                            └── EQUIPMENT
                                    └── COMPONENT
```

Each asset must have a `parent_id` pointing to a valid asset of the correct parent type, except the single root `ENTERPRISE` node (which has `parent_id=None`).

---

## Validation Rules

| Error Code | Description |
|------------|-------------|
| `EMPTY_GRAPH` | Asset list is empty |
| `DUPLICATE_ID` | Two or more assets share the same ID |
| `MISSING_PARENT` | `parent_id` references a non-existent asset |
| `SELF_REFERENCE` | Asset references itself as parent |
| `MULTIPLE_ROOTS` | More than one asset has `parent_id=None` |
| `INVALID_TYPE_HIERARCHY` | Child type is invalid for the given parent type |
| `CYCLE_DETECTED` | Circular parent-child references exist |
| `ORPHAN_NODE` | *(warning)* Non-enterprise asset has no edges |

---

## Data Models

```python
@dataclass
class Asset:
    id: str                        # Unique identifier
    name: str                      # Human-readable label
    asset_type: AssetType          # ENTERPRISE | SITE | FACILITY | SYSTEM | EQUIPMENT | COMPONENT
    status: Status                 # OPERATIONAL | DEGRADED | MAINTENANCE | DECOMMISSIONED
    criticality: Criticality       # CRITICAL | HIGH | MEDIUM | LOW
    parent_id: str | None          # None for the root enterprise node
    metadata: dict[str, str]       # Arbitrary key-value pairs
```

---

## Project Structure

```
assetpy/
├── main.py                     # CLI entry point and demo runner
├── requirements.txt
├── pyproject.toml
└── src/assetpy/
    ├── models.py               # Asset dataclass and enumerations
    ├── graph.py                # AssetGraph — NetworkX DiGraph wrapper
    ├── traversal.py            # TraversalEngine — hierarchy navigation
    ├── validation.py           # HierarchyValidator — constraint checking
    ├── visualization.py        # PlotlyVisualizer — interactive HTML output
    └── demo_data.py            # build_demo_assets() — sample refinery dataset
```

---

## Demo Dataset

The included demo models a **Gulf Coast Petroleum Group** with ~95 nodes across two sites (Port Arthur and Beaumont), six facilities (CDU, FCC, HDS, Utilities, Wellhead, Water Injection), and realistic equipment metadata such as capacity, design temperature, manufacturer, and installation date.
