"""GraphML exporter for pairwise (binary) graphs.

Produces a directed GraphML 1.0 document that Gephi, yEd, and other
desktop tools can open. N-ary hyperedges have no single GraphML encoding;
callers should use :func:`hyperextract.utils.exporters.export_to_csv`
with ``hypergraph=True`` instead.

Endpoint order is preserved: ``source`` is the first incident node and
``target`` is the second. Endpoints are never sorted.
"""

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hyperextract.utils.logging import get_logger

from .common import (
    graphml_attr_type,
    graphml_attr_value,
    incident_ids,
    merge_graphml_type,
    resolve_nodes,
    scalar_fields,
    xml_escape,
)

logger = get_logger(__name__)

GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"


class GraphMLHypergraphError(ValueError):
    """Raised when GraphML export is asked to encode an N-ary edge."""


def export_to_graphml(
    nodes: Sequence[BaseModel],
    edges: Sequence[BaseModel],
    *,
    node_id_extractor: Callable[[Any], str],
    incident_nodes_extractor: Callable[[Any], Sequence[str]],
    file_path: str | Path,
    edge_id_extractor: Callable[[Any], str] | None = None,
) -> Path:
    """Export a pairwise graph to a GraphML file.

    Args:
        nodes: Node/entity models to export.
        edges: Pairwise edge models to export.
        node_id_extractor: Maps a node to its unique key (matches edge endpoints).
        incident_nodes_extractor: Maps an edge to ``(source, target)`` node
            keys. Must return exactly two endpoints; N-ary edges raise
            :class:`GraphMLHypergraphError`.
        file_path: Destination ``.graphml`` file.
        edge_id_extractor: Optional edge -> GraphML edge id. Defaults to
            ``e0``, ``e1``, ...

    Returns:
        The written file :class:`~pathlib.Path`.

    Raises:
        GraphMLHypergraphError: If any edge has more than two incident nodes.
        IsADirectoryError: If ``file_path`` exists and is a directory.
    """
    dest = Path(file_path)
    if dest.exists() and dest.is_dir():
        raise IsADirectoryError(
            f"Destination '{dest}' is a directory; pass a GraphML file path."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)

    by_id = resolve_nodes(nodes, node_id_extractor)

    node_keys: dict[str, str] = {}
    node_rows: list[tuple[str, dict[str, str | int | float | bool]]] = []
    for node_id, node in by_id.items():
        fields = scalar_fields(node)
        for name, value in fields.items():
            node_keys[name] = merge_graphml_type(
                node_keys.get(name), graphml_attr_type(value)
            )
        node_rows.append((node_id, fields))

    pairwise: list[tuple[str, str, str, dict[str, str | int | float | bool]]] = []
    edge_keys: dict[str, str] = {}
    skipped = 0
    for index, edge in enumerate(edges):
        members = incident_ids(edge, incident_nodes_extractor)
        if members is None:
            skipped += 1
            continue
        if len(members) > 2:
            raise GraphMLHypergraphError(
                "GraphML export supports pairwise graphs only; this edge has "
                f"{len(members)} incident nodes. Use CSV export for hypergraphs "
                "(he export csv / export_to_csv(..., hypergraph=True))."
            )
        if len(members) != 2:
            skipped += 1
            logger.warning(
                "export.graphml: skipping non-pairwise edge members=%s",
                members,
            )
            continue
        source, target = members[0], members[1]
        if source not in by_id or target not in by_id:
            skipped += 1
            logger.warning(
                "export.graphml: skipping edge with missing endpoint "
                "source=%s target=%s",
                source,
                target,
            )
            continue

        edge_id = _edge_id(edge, index, edge_id_extractor)
        fields = scalar_fields(edge)
        for name, value in fields.items():
            edge_keys[name] = merge_graphml_type(
                edge_keys.get(name), graphml_attr_type(value)
            )
        pairwise.append((edge_id, source, target, fields))

    xml = _render_graphml(node_keys, edge_keys, node_rows, pairwise)
    dest.write_text(xml, encoding="utf-8")

    logger.info(
        "graphml: exported nodes=%d edges=%d skipped_edges=%d path=%s",
        len(node_rows),
        len(pairwise),
        skipped,
        dest,
    )
    return dest


def _edge_id(edge: Any, index: int, extractor: Callable[[Any], str] | None) -> str:
    if extractor is None:
        return f"e{index}"
    try:
        value = extractor(edge)
    except Exception as exc:
        logger.debug("export.graphml: edge_id_extractor raised %s", exc)
        return f"e{index}"
    if value in (None, ""):
        return f"e{index}"
    return str(value)


def _key_id(prefix: str, name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)
    if not safe or safe[0].isdigit():
        safe = f"_{safe}"
    return f"{prefix}_{safe}"


def _render_graphml(
    node_keys: dict[str, str],
    edge_keys: dict[str, str],
    node_rows: list[tuple[str, dict[str, str | int | float | bool]]],
    edges: list[tuple[str, str, str, dict[str, str | int | float | bool]]],
) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<graphml xmlns="{GRAPHML_NS}">',
    ]
    node_key_ids: dict[str, str] = {}
    for name, attr_type in node_keys.items():
        kid = _key_id("n", name)
        node_key_ids[name] = kid
        lines.append(
            f'  <key id="{xml_escape(kid)}" for="node" '
            f'attr.name="{xml_escape(name)}" attr.type="{attr_type}"/>'
        )
    edge_key_ids: dict[str, str] = {}
    for name, attr_type in edge_keys.items():
        kid = _key_id("e", name)
        edge_key_ids[name] = kid
        lines.append(
            f'  <key id="{xml_escape(kid)}" for="edge" '
            f'attr.name="{xml_escape(name)}" attr.type="{attr_type}"/>'
        )

    lines.append('  <graph id="G" edgedefault="directed">')
    for node_id, fields in node_rows:
        if fields:
            lines.append(f'    <node id="{xml_escape(node_id)}">')
            for name, value in fields.items():
                kid = node_key_ids[name]
                lines.append(
                    f'      <data key="{xml_escape(kid)}">'
                    f"{xml_escape(graphml_attr_value(value))}</data>"
                )
            lines.append("    </node>")
        else:
            lines.append(f'    <node id="{xml_escape(node_id)}"/>')

    for edge_id, source, target, fields in edges:
        attrs = (
            f'id="{xml_escape(edge_id)}" '
            f'source="{xml_escape(source)}" '
            f'target="{xml_escape(target)}"'
        )
        if fields:
            lines.append(f"    <edge {attrs}>")
            for name, value in fields.items():
                kid = edge_key_ids[name]
                lines.append(
                    f'      <data key="{xml_escape(kid)}">'
                    f"{xml_escape(graphml_attr_value(value))}</data>"
                )
            lines.append("    </edge>")
        else:
            lines.append(f"    <edge {attrs}/>")

    lines.append("  </graph>")
    lines.append("</graphml>")
    lines.append("")
    return "\n".join(lines)
