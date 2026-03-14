from __future__ import annotations

import networkx as nx

from .graph import AssetGraph
from .models import Asset, AssetType


class TraversalEngine:
    """High-level traversal operations over an AssetGraph."""

    def __init__(self, asset_graph: AssetGraph) -> None:
        self._ag = asset_graph

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _asset(self, asset_id: str) -> Asset:
        return self._ag.get_asset(asset_id)

    def _g(self) -> nx.DiGraph:
        return self._ag.graph

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_parent(self, asset_id: str) -> Asset | None:
        predecessors = list(self._g().predecessors(asset_id))
        if not predecessors:
            return None
        return self._asset(predecessors[0])

    def get_children(self, asset_id: str) -> list[Asset]:
        return sorted(
            [self._asset(n) for n in self._g().successors(asset_id)],
            key=lambda a: a.id,
        )

    def get_siblings(self, asset_id: str) -> list[Asset]:
        parent = self.get_parent(asset_id)
        if parent is None:
            return []
        return [a for a in self.get_children(parent.id) if a.id != asset_id]

    def get_ancestors(self, asset_id: str) -> list[Asset]:
        """Direct parent first, root last."""
        g = self._g()
        ancestor_ids = nx.ancestors(g, asset_id)
        # Build path from node to root via in_degree traversal to get ordered list
        path: list[str] = []
        current = asset_id
        while True:
            preds = list(g.predecessors(current))
            if not preds:
                break
            current = preds[0]
            path.append(current)
        return [self._asset(aid) for aid in path]

    def get_root(self, asset_id: str) -> Asset:
        g = self._g()
        current = asset_id
        while True:
            preds = list(g.predecessors(current))
            if not preds:
                return self._asset(current)
            current = preds[0]

    def get_descendants(self, asset_id: str) -> list[Asset]:
        """BFS order."""
        g = self._g()
        visited: list[str] = []
        queue = list(g.successors(asset_id))
        seen: set[str] = set(queue)
        while queue:
            node = queue.pop(0)
            visited.append(node)
            for child in g.successors(node):
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return [self._asset(aid) for aid in visited]

    def get_subtree(self, asset_id: str) -> list[Asset]:
        return [self._asset(asset_id)] + self.get_descendants(asset_id)

    def get_children_by_type(self, asset_id: str, asset_type: AssetType) -> list[Asset]:
        return [a for a in self.get_children(asset_id) if a.asset_type == asset_type]

    def find_path(self, source_id: str, target_id: str) -> list[Asset]:
        try:
            path = nx.shortest_path(self._g(), source_id, target_id)
            return [self._asset(aid) for aid in path]
        except nx.NetworkXNoPath:
            return []
        except nx.NodeNotFound as exc:
            raise KeyError(str(exc)) from exc

    def get_depth(self, asset_id: str) -> int:
        root = self.get_root(asset_id)
        if root.id == asset_id:
            return 0
        path = nx.shortest_path(self._g(), root.id, asset_id)
        return len(path) - 1

    def get_subtree_size(self, asset_id: str) -> int:
        return len(self.get_subtree(asset_id))
