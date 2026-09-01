"""Tests for the interactive `he talk` chat loop."""

import hyperextract.cli.cli as climod


def test_chat_loop_passes_top_k(monkeypatch):
    """Interactive chat must forward top_k to ka.chat, not use the default."""
    recorded = {}

    class _StubKA:
        def chat(self, query, top_k=3):
            recorded["top_k"] = top_k
            return type("_Resp", (), {"content": "ok"})()

    queries = iter(["hello", "exit"])
    monkeypatch.setattr(climod.console, "input", lambda *a, **k: next(queries))

    climod.chat_loop(_StubKA(), "some/ka", top_k=10)

    assert recorded["top_k"] == 10
