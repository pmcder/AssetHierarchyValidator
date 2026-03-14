from __future__ import annotations

import networkx as nx

from .models import Asset
from .validation import HierarchyValidator, ValidationResult


class AssetGraph:
    """Directed graph (parent → child) wrapping nx.DiGraph."""

    def __init__(self, graph: nx.DiGraph) -> None:
        self._graph = graph

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_assets(
        cls,
        assets: list[Asset],
        validate: bool = True,
    ) -> "AssetGraph":
        if validate:
            result: ValidationResult = HierarchyValidator().validate(assets)
            if not result.is_valid:
                raise ValueError(
                    f"Asset hierarchy validation failed:\n{result}"
                )

        g: nx.DiGraph = nx.DiGraph()
        for asset in assets:
            g.add_node(asset.id, asset=asset)
        for asset in assets:
            if asset.parent_id is not None:
                g.add_edge(asset.parent_id, asset.id)

        return cls(g)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def graph(self) -> nx.DiGraph:
        return self._graph

    def get_asset(self, asset_id: str) -> Asset:
        try:
            return self._graph.nodes[asset_id]["asset"]
        except KeyError:
            raise KeyError(f"Asset '{asset_id}' not found in graph.")

    def all_assets(self) -> list[Asset]:
        return [data["asset"] for _, data in self._graph.nodes(data=True)]

    def node_count(self) -> int:
        return self._graph.number_of_nodes()

    def edge_count(self) -> int:
        return self._graph.number_of_edges()
