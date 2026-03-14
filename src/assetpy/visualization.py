from __future__ import annotations

import os
import webbrowser
from typing import Any

import networkx as nx
import plotly.graph_objects as go

from .graph import AssetGraph
from .models import AssetType, Criticality


# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

TYPE_COLORS: dict[AssetType, str] = {
    AssetType.ENTERPRISE: "#0a1628",   # dark navy
    AssetType.SITE: "#1a3a6b",         # navy
    AssetType.FACILITY: "#1e5fa8",     # deep blue
    AssetType.SYSTEM: "#6b3fa0",       # purple
    AssetType.EQUIPMENT: "#c0392b",    # coral red
    AssetType.COMPONENT: "#e67e22",    # amber
}

CRITICALITY_COLORS: dict[Criticality, str] = {
    Criticality.CRITICAL: "#c0392b",
    Criticality.HIGH: "#e67e22",
    Criticality.MEDIUM: "#f1c40f",
    Criticality.LOW: "#27ae60",
}

NODE_SIZES: dict[AssetType, int] = {
    AssetType.ENTERPRISE: 30,
    AssetType.SITE: 24,
    AssetType.FACILITY: 20,
    AssetType.SYSTEM: 16,
    AssetType.EQUIPMENT: 12,
    AssetType.COMPONENT: 9,
}


class PlotlyVisualizer:
    def __init__(self, asset_graph: AssetGraph) -> None:
        self._ag = asset_graph

    def render(
        self,
        color_by: str = "asset_type",
        output_path: str = "asset_graph.html",
        title: str = "EAM Asset Hierarchy",
        open_browser: bool = True,
    ) -> str:
        g = self._ag.graph
        pos = self._compute_layout(g)
        fig = self._build_figure(g, pos, color_by, title)
        fig.write_html(output_path)
        if open_browser:
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
        return output_path

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _compute_layout(self, g: nx.DiGraph) -> dict[str, tuple[float, float]]:
        # 1. Try graphviz dot layout
        try:
            pos = nx.drawing.nx_agraph.graphviz_layout(g, prog="dot")
            return pos
        except Exception:
            pass

        # 2. Multipartite layout (requires depth attribute on each node)
        try:
            depths = nx.single_source_shortest_path_length(
                g, next(n for n, d in g.in_degree() if d == 0)
            )
            nx.set_node_attributes(g, depths, name="depth")
            pos = nx.multipartite_layout(g, subset_key="depth")
            return pos
        except Exception:
            pass

        # 3. Spring layout fallback
        return nx.spring_layout(g, seed=42)

    # ------------------------------------------------------------------
    # Figure construction
    # ------------------------------------------------------------------

    def _build_figure(
        self,
        g: nx.DiGraph,
        pos: dict[str, tuple[float, float]],
        color_by: str,
        title: str,
    ) -> go.Figure:
        traces: list[Any] = []

        # Edge traces (one per edge for simplicity, batched into single trace)
        edge_x: list[float | None] = []
        edge_y: list[float | None] = []
        for src, dst in g.edges():
            x0, y0 = pos[src]
            x1, y1 = pos[dst]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        traces.append(go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=0.8, color="#cccccc"),
            hoverinfo="none",
            showlegend=False,
        ))

        # Node traces — grouped by color scheme
        if color_by == "asset_type":
            groups = {t: [] for t in AssetType}
            for node_id in g.nodes():
                asset = self._ag.get_asset(node_id)
                groups[asset.asset_type].append(node_id)
            for asset_type, node_ids in groups.items():
                if not node_ids:
                    continue
                traces.append(self._node_trace(
                    g, pos, node_ids,
                    color=TYPE_COLORS[asset_type],
                    name=asset_type.value.title(),
                ))
        else:  # criticality
            groups_crit = {c: [] for c in Criticality}
            for node_id in g.nodes():
                asset = self._ag.get_asset(node_id)
                groups_crit[asset.criticality].append(node_id)
            for criticality, node_ids in groups_crit.items():
                if not node_ids:
                    continue
                traces.append(self._node_trace(
                    g, pos, node_ids,
                    color=CRITICALITY_COLORS[criticality],
                    name=criticality.value.title(),
                ))

        fig = go.Figure(
            data=traces,
            layout=go.Layout(
                title=dict(text=title, font=dict(size=18)),
                showlegend=True,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=50),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor="#f8f9fa",
                paper_bgcolor="#ffffff",
                legend=dict(
                    title=dict(text=color_by.replace("_", " ").title()),
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#cccccc",
                    borderwidth=1,
                ),
            ),
        )
        return fig

    def _node_trace(
        self,
        g: nx.DiGraph,
        pos: dict[str, tuple[float, float]],
        node_ids: list[str],
        color: str,
        name: str,
    ) -> go.Scatter:
        x_vals: list[float] = []
        y_vals: list[float] = []
        hover_texts: list[str] = []
        sizes: list[int] = []
        labels: list[str] = []

        for node_id in node_ids:
            asset = self._ag.get_asset(node_id)
            x, y = pos[node_id]
            x_vals.append(x)
            y_vals.append(y)
            sizes.append(NODE_SIZES[asset.asset_type])
            labels.append(asset.name)

            meta_lines = "<br>".join(
                f"  {k}: {v}" for k, v in asset.metadata.items()
            )
            hover = (
                f"<b>{asset.name}</b><br>"
                f"ID: {asset.id}<br>"
                f"Type: {asset.asset_type.value}<br>"
                f"Status: {asset.status.value}<br>"
                f"Criticality: {asset.criticality.value}<br>"
                f"Parent: {asset.parent_id or '—'}<br>"
            )
            if meta_lines:
                hover += f"<br><b>Metadata:</b><br>{meta_lines}"
            hover_texts.append(hover)

        return go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers+text",
            marker=dict(
                size=sizes,
                color=color,
                line=dict(width=1, color="#ffffff"),
            ),
            text=labels,
            textposition="top center",
            textfont=dict(size=8),
            hovertext=hover_texts,
            hoverinfo="text",
            name=name,
        )
