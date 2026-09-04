"""Hard delete (remove_nodes / remove_edges) and soft delete (edit_*) for
graph-family AutoTypes (issue #84)."""

import pytest
from pydantic import BaseModel, Field

from hyperextract.types import AutoGraph, AutoHypergraph
from tests.mocks import MockChatModel, MockEmbeddings


class Entity(BaseModel):
    name: str
    type: str = "ENTITY"
    description: str = ""


class Relation(BaseModel):
    source: str
    target: str
    relation_type: str
    description: str = ""


class HyperRelation(BaseModel):
    participants: list[str] = Field(default_factory=list)
    relation_type: str = "related"


def _graph():
    return AutoGraph(
        node_schema=Entity,
        edge_schema=Relation,
        node_key_extractor=lambda x: x.name,
        edge_key_extractor=lambda x: f"{x.source}-{x.relation_type}-{x.target}",
        nodes_in_edge_extractor=lambda x: (x.source, x.target),
        llm_client=MockChatModel(),
        embedder=MockEmbeddings(),
    )


def _hypergraph():
    return AutoHypergraph(
        node_schema=Entity,
        edge_schema=HyperRelation,
        node_key_extractor=lambda x: x.name,
        edge_key_extractor=lambda x: f"{x.relation_type}_{sorted(x.participants)}",
        nodes_in_edge_extractor=lambda x: tuple(x.participants),
        llm_client=MockChatModel(),
        embedder=MockEmbeddings(),
    )


class TestHardDelete:
    """remove_nodes / remove_edges: key-level deletion with orphan pruning."""

    def test_remove_node_drops_orphan_edges(self):
        g = _graph()
        g._node_memory.add(
            [Entity(name="Apple"), Entity(name="Google"), Entity(name="Meta")]
        )
        g._edge_memory.add(
            [
                Relation(source="Apple", target="Google", relation_type="partner"),
                Relation(source="Meta", target="Google", relation_type="partner"),
            ]
        )

        report = g.remove_nodes("Apple")

        assert report["removed_nodes"] == ["Apple"]
        assert report["not_found_nodes"] == []
        # The Apple-Google edge dangles (Apple gone) and must be pruned;
        # the Meta-Google edge survives.
        assert report["removed_orphan_edges"] == ["Apple-partner-Google"]
        assert {n.name for n in g.nodes} == {"Google", "Meta"}
        assert {e.source for e in g.edges} == {"Meta"}

    def test_remove_missing_node_is_reported_not_raised(self):
        g = _graph()
        report = g.remove_nodes("Nope")
        assert report["removed_nodes"] == []
        assert report["not_found_nodes"] == ["Nope"]

    def test_remove_edges(self):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B"), Entity(name="C")])
        g._edge_memory.add(
            [
                Relation(source="A", target="B", relation_type="r1"),
                Relation(source="B", target="C", relation_type="r2"),
            ]
        )

        report = g.remove_edges("A-r1-B", "missing")

        assert report["removed_edges"] == ["A-r1-B"]
        assert report["not_found_edges"] == ["missing"]
        assert {e.relation_type for e in g.edges} == {"r2"}
        assert {n.name for n in g.nodes} == {"A", "B", "C"}  # nodes untouched

    def test_removal_survives_dump_load_roundtrip(self, tmp_path):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        g._edge_memory.add([Relation(source="A", target="B", relation_type="r")])
        g.remove_nodes("A")
        g.dump(tmp_path)

        reloaded = _graph()
        reloaded.load(tmp_path)

        assert [n.name for n in reloaded.nodes] == ["B"]
        assert reloaded.edges == []

    def test_hypergraph_remove_node_drops_touching_hyperedges(self):
        h = _hypergraph()
        h._node_memory.add([Entity(name="A"), Entity(name="B"), Entity(name="C")])
        h._edge_memory.add(
            [
                HyperRelation(participants=["A", "B"], relation_type="group"),
                HyperRelation(participants=["C"], relation_type="solo"),
            ]
        )

        report = h.remove_nodes("A")

        assert report["removed_nodes"] == ["A"]
        keys_removed = report["removed_orphan_edges"]
        assert len(keys_removed) == 1 and "group_" in keys_removed[0]
        assert {e.relation_type for e in h.edges} == {"solo"}

    def test_spatiotemporal_subclass_inherits_removal(self):
        from hyperextract.types import AutoTemporalGraph

        g = AutoTemporalGraph(
            node_schema=Entity,
            edge_schema=Relation,
            node_key_extractor=lambda x: x.name,
            edge_key_extractor=lambda x: f"{x.source}-{x.relation_type}-{x.target}",
            time_in_edge_extractor=lambda x: "",
            nodes_in_edge_extractor=lambda x: (x.source, x.target),
            llm_client=MockChatModel(),
            embedder=MockEmbeddings(),
        )
        g._node_memory.add([Entity(name="A"), Entity(name="B")])

        report = g.remove_nodes("A", "B", "C")
        assert report["removed_nodes"] == ["A", "B"]
        assert report["not_found_nodes"] == ["C"]


class FakeEditor:
    """Stub for the node_editor/edge_editor runnables."""

    def __init__(self, rewritten):
        self.rewritten = rewritten
        self.calls = []

    def invoke(self, inp):
        self.calls.append(inp)
        return self.rewritten


class TestIndexPatching:
    """Phase A (#84): removals/edits patch the FAISS index in place.

    Assertions inspect the FAISS docstore directly (keys + re-embedded
    page_content) — MockEmbeddings is hash-based, so semantic-search
    result ordering is not meaningful here.
    """

    @staticmethod
    def _docstore(memory):
        return memory._index.docstore._dict

    def test_remove_node_keeps_index_without_stale_vectors(self):
        g = _graph()
        g._node_memory.add(
            [Entity(name="Apple"), Entity(name="Google"), Entity(name="Meta")]
        )
        g._edge_memory.add(
            [Relation(source="Apple", target="Google", relation_type="partner")]
        )
        g.build_index()
        assert g._node_memory.has_index()

        report = g.remove_nodes("Apple")

        assert report["index_patched"] is True
        # Index must survive the removal (no full-rebuild fallback).
        assert g._node_memory.has_index()
        assert g._edge_memory.has_index()
        # The removed node's vector and its edge's vector are gone.
        node_keys = {d.metadata["key"] for d in self._docstore(g._node_memory).values()}
        edge_keys = {d.metadata["key"] for d in self._docstore(g._edge_memory).values()}
        assert node_keys == {"Google", "Meta"}
        assert edge_keys == set()

    def test_remove_node_docstore_shrinks(self):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        g.build_index()
        size_before = len(g._node_memory._index.docstore._dict)

        g.remove_nodes("A")

        size_after = len(g._node_memory._index.docstore._dict)
        assert size_after == size_before - 1

    def test_edit_node_refreshes_vector(self):
        g = _graph()
        g._node_memory.add(
            [Entity(name="A", description="A was founded by X. A is in Y.")]
        )
        g.build_index()
        g.node_editor = FakeEditor(Entity(name="A", description="A is in Y."))

        report = g.edit_node("A", remove_fact="founded by X")

        assert report["index_patched"] is True
        assert g._node_memory.has_index()
        # Exactly one vector for the key, re-embedded with the new text.
        docs = [
            d
            for d in self._docstore(g._node_memory).values()
            if d.metadata["key"] == "A"
        ]
        assert len(docs) == 1
        assert "founded by X" not in docs[0].page_content
        assert "A is in Y" in docs[0].page_content

    def test_no_index_built_falls_back_to_lazy_rebuild(self):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        # No build_index() call — nothing to patch.

        report = g.remove_nodes("A")

        assert report["index_patched"] is False
        assert not g._node_memory.has_index()
        # OMem's lazy rebuild still reflects the removal.
        assert "A" not in {n.name for n in g.nodes}

    def test_patched_index_survives_dump_load(self, tmp_path):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        g._edge_memory.add([Relation(source="A", target="B", relation_type="r")])
        g.build_index()
        g.remove_nodes("A")
        g.dump(tmp_path)

        reloaded = _graph()
        reloaded.load(tmp_path)
        assert reloaded._node_memory.has_index()

        node_keys = {
            d.metadata["key"] for d in self._docstore(reloaded._node_memory).values()
        }
        assert node_keys == {"B"}
        edge_keys = {
            d.metadata["key"] for d in self._docstore(reloaded._edge_memory).values()
        }
        assert edge_keys == set()

    def test_hypergraph_removal_patches_index(self):
        h = _hypergraph()
        h._node_memory.add([Entity(name="A"), Entity(name="B"), Entity(name="C")])
        h._edge_memory.add(
            [HyperRelation(participants=["A", "B"], relation_type="group")]
        )
        h.build_index()

        report = h.remove_nodes("A")

        assert report["index_patched"] is True
        assert h._node_memory.has_index()
        node_keys = {d.metadata["key"] for d in self._docstore(h._node_memory).values()}
        assert node_keys == {"B", "C"}
        # The hyperedge containing the removed node is gone from the index.
        edge_keys = {d.metadata["key"] for d in self._docstore(h._edge_memory).values()}
        assert edge_keys == set()


class TestSoftDelete:
    """edit_node / edit_edge: LLM-assisted fact removal with guardrails."""

    def test_edit_dry_run_does_not_apply(self):
        g = _graph()
        g._node_memory.add(
            [Entity(name="A", description="A was founded by X. A is in Y.")]
        )
        g.node_editor = FakeEditor(Entity(name="A", description="A is in Y."))

        report = g.edit_node("A", remove_fact="founded by X", dry_run=True)

        assert report["changed"] is True
        assert report["applied"] is False
        # stored item untouched
        assert "founded by X" in g._node_memory.get("A").description

    def test_edit_applies_rewrite(self):
        g = _graph()
        g._node_memory.add(
            [Entity(name="A", description="A was founded by X. A is in Y.")]
        )
        g.node_editor = FakeEditor(Entity(name="A", description="A is in Y."))

        report = g.edit_node("A", remove_fact="founded by X")

        assert report["changed"] is True
        assert report["applied"] is True
        assert g._node_memory.get("A").description == "A is in Y."

    def test_editor_receives_item_json_key_and_target(self):
        g = _graph()
        g._node_memory.add([Entity(name="A", description="hello")])
        editor = FakeEditor(Entity(name="A", description="hello"))
        g.node_editor = editor

        g.edit_node("A", instruction="drop everything about X")

        assert editor.calls[0]["key"] == "A"
        assert "hello" in editor.calls[0]["item_json"]
        assert editor.calls[0]["target"] == "drop everything about X"

    def test_key_change_is_rejected(self):
        g = _graph()
        g._node_memory.add([Entity(name="A")])
        g.node_editor = FakeEditor(Entity(name="Renamed"))  # identity break

        with pytest.raises(ValueError, match="key changed"):
            g.edit_node("A", remove_fact="whatever")
        # nothing was mutated
        assert g._node_memory.get("A").name == "A"

    def test_unchanged_rewrite_reports_no_change(self):
        g = _graph()
        g._node_memory.add([Entity(name="A", description="same")])
        g.node_editor = FakeEditor(Entity(name="A", description="same"))

        report = g.edit_node("A", remove_fact="not present anyway")

        assert report["changed"] is False
        assert g._node_memory.get("A").description == "same"

    def test_missing_key_raises(self):
        g = _graph()
        with pytest.raises(KeyError):
            g.edit_node("Nope", remove_fact="x")

    def test_remove_fact_and_instruction_are_exclusive(self):
        g = _graph()
        with pytest.raises(ValueError, match="exactly one"):
            g.edit_node("A", remove_fact="a", instruction="b")
        with pytest.raises(ValueError, match="exactly one"):
            g.edit_node("A")

    def test_edit_edge(self):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        g._edge_memory.add(
            [
                Relation(
                    source="A",
                    target="B",
                    relation_type="acquired",
                    description="Acquired by Apple in 2016, first announced in March.",
                )
            ]
        )
        # relation_type is part of the edge key, so the rewrite keeps it and
        # only changes the description — a key-changing rewrite is rejected.
        g.edge_editor = FakeEditor(
            Relation(
                source="A",
                target="B",
                relation_type="acquired",
                description="Acquired by Apple in 2016.",
            )
        )

        report = g.edit_edge("A-acquired-B", remove_fact="first announced in March")

        assert report["applied"] is True
        assert "announced in March" not in g.edges[0].description

    def test_edit_edge_key_change_is_rejected(self):
        g = _graph()
        g._node_memory.add([Entity(name="A"), Entity(name="B")])
        g._edge_memory.add([Relation(source="A", target="B", relation_type="r")])
        g.edge_editor = FakeEditor(
            Relation(source="A", target="B", relation_type="partner")
        )

        with pytest.raises(ValueError, match="key changed"):
            g.edit_edge("A-r-B", remove_fact="whatever")
