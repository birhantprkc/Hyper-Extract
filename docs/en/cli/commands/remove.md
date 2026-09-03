# he remove

Delete knowledge from an existing knowledge abstract: hard-delete nodes/edges by key, or soft-remove a single fact with LLM assistance.

---

## Synopsis

```bash
he remove KA_PATH [OPTIONS]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--node TEXT` | — | Node key(s) to **hard-delete**; edges anchored by a removed node are removed too |
| `--edge TEXT` | — | Edge key(s) to **hard-delete** |
| `--edit-node TEXT` | — | Node key to **soft-edit** (LLM rewrites it minus `--fact`) |
| `--edit-edge TEXT` | — | Edge key to **soft-edit** |
| `--fact TEXT` | — | The fact to remove from the `--edit-node` / `--edit-edge` item |
| `--instruction TEXT` | — | Free-form edit instruction (alternative to `--fact`) |
| `--dry-run` | off | Preview the change without persisting it |
| `--backup / --no-backup` | on | Back up `data.json` as `data.json.bak.<timestamp>` before writing |
| `--yes` | `-y` | Skip the confirmation prompt |

Hard delete (`--node` / `--edge`) and soft delete (`--edit-node` / `--edit-edge`) are mutually exclusive.

---

## Hard Delete: by Key

Remove whole items. Keys are the values produced by the template's `identifiers` (typically the entity name for nodes, `"{source}|{type}|{target}"`-style keys for edges). Use [`he show`](show.md) or read `data.json` to find them.

```bash
# Remove two nodes; any edge touching them is removed as well
he remove ./ka/ --node Apple --node Nokia

# Remove one edge by its exact key
he remove ./ka/ --edge "Apple-partner-Google"
```

The command prints a removal report (removed items, keys not found, orphaned edges pruned).

!!! warning
    Hard delete is **permanent** for the deleted items. A `data.json.bak.<timestamp>` backup is written next to the KA before writing unless `--no-backup` is passed.

---

## Soft Delete: remove a single fact (LLM-assisted)

Sometimes a node should stay, but one claim inside it is wrong or obsolete:

```bash
# Preview first (nothing is written)
he remove ./ka/ --edit-node Apple \
  --fact "founded by Steve Jobs" --dry-run

# Apply
he remove ./ka/ --edit-node Apple \
  --fact "founded by Steve Jobs" -y
```

The LLM rewrites the item under the **same schema**, removing the fact while keeping every other field unchanged. Guardrails:

- **Key invariance** — a rewrite that changes the item's key is rejected (renaming is not an edit; delete the old item and add the new one instead).
- **Dry run** — `--dry-run` prints the old and proposed items and writes nothing.
- **No-op detection** — if the fact was not found, the command reports `No change` and writes nothing.
- **Backup** — `data.json.bak.<timestamp>` is written before the edit unless `--no-backup`.

For edges, remember that fields used by the edge key (e.g. `relation_type`) cannot be changed by a soft edit — the rewrite would be rejected; hard-delete the edge instead.

```bash
he remove ./ka/ --edit-edge "Apple-acquired-Beats" \
  --instruction "Remove the price from the description"
```

---

## After removal

Removal invalidates the search index (the stale `index/` directory is deleted). Rebuild it before searching or chatting again:

```bash
he build-index ./ka/
```

---

## Python API

```python
ka.remove_nodes("Apple", "Nokia")   # -> {"removed_nodes": [...], "not_found_nodes": [...], "removed_orphan_edges": [...]}
ka.remove_edges("Apple-partner-Google")

report = ka.edit_node("Apple", remove_fact="founded by Steve Jobs", dry_run=True)
# report: {"changed": bool, "applied": bool, "old": <item>, "new": <item>}
ka.edit_node("Apple", remove_fact="founded by Steve Jobs")  # applies

ka.dump("./ka/")  # persist
```

Works for graph, hypergraph, and temporal/spatial graph knowledge abstracts.

---

## See Also

- [`he clean`](clean.md) — remove the search index or the whole KA
- [`he show`](show.md) — inspect keys before deleting
- [`he build-index`](build-index.md) — rebuild the search index after removal
