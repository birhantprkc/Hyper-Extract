# he feed

Add documents to an existing knowledge abstract incrementally.

---

## Synopsis

```bash
he feed KA_PATH INPUT [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `KA_PATH` | Path to existing knowledge abstract directory |
| `INPUT` | Input file path (`.txt` or `.md`) or `-` for stdin |

Supported suffixes are `.txt` and `.md` (case-insensitive, including `.TXT` and `.MD`). This CLI does not parse PDF or Office files and does not perform OCR — convert those documents to `.txt` or `.md` first. Stdin (`-`) is not suffix-checked.

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--template` | `-t` | Override template (uses metadata if omitted) |
| `--lang` | `-l` | Override language (uses metadata if omitted) |
| `--source` | — | Source attribution (document id) — enables per-document rollback via `he remove --document` |

---

## Description

The `feed` command adds new documents to an existing knowledge abstract without losing existing data:

1. **Loads existing knowledge** — Reads current knowledge abstract state
2. **Extracts from new document** — Processes the new content
3. **Merges intelligently** — Combines new and existing data, handling duplicates
4. **Updates metadata** — Records the update timestamp

This is ideal for:
- Building knowledge abstracts over time
- Adding updates to existing documents
- Combining information from multiple sources

---

## Examples

### Basic Usage

```bash
# Initial extraction
he parse tesla_bio.md -t general/biography_graph -o ./tesla_kb/ -l en

# Add more content
he feed ./tesla_kb/ tesla_inventions.md
```

### Feed Multiple Documents

```bash
he feed ./ka/ doc1.md
he feed ./ka/ doc2.md
he feed ./ka/ doc3.md
```

Or use a loop:

```bash
for file in updates/*.md; do
    he feed ./ka/ "$file"
done
```

### From Stdin

```bash
cat new_content.md | he feed ./ka/ -
```

---

## Merge Behavior

The merge process handles:

| Scenario | Behavior |
|----------|----------|
| Same entity | Merged, descriptions combined |
| Same relation | Updated with latest information |
| New entities | Added to knowledge abstract |
| New relations | Added connecting existing/new entities |

---

## Workflow Example

### Building a Research Knowledge Abstract

```bash
# Day 1: Initial paper
he parse paper_v1.md -t general/concept_graph -o ./research_kb/ -l en
he show ./research_kb/

# Day 7: Updated version
he feed ./research_kb/ paper_v2.md
he show ./research_kb/

# Day 14: Related work
he feed ./research_kb/ related_work.md
he build-index ./research_kb/
he talk ./research_kb/ -q "What are the key concepts across all papers?"
```

### Incremental Biography

```bash
# Start with early life
he parse early_life.md -t general/biography_graph -o ./bio_kb/ -l en

# Add career period
he feed ./bio_kb/ career.md

# Add later years
he feed ./bio_kb/ later_years.md

# Final visualization
he show ./bio_kb/
```

---

## Verification

Check that the feed worked:

```bash
he info ./ka/
```

Look for:
- Increased node count
- Increased edge count  
- Updated timestamp

---

## Best Practices

1. **Use same template** — Feeding should use compatible templates
2. **Match language** — Use consistent language for best results
3. **Rebuild index after** — `he build-index ./ka/` for search/chat
4. **Visualize changes** — `he show ./ka/` to see updates

---

## Error Handling

### "Not a valid Knowledge Abstract directory"

The directory doesn't contain a valid knowledge abstract. Check:

```bash
ls ./ka/
# Should contain: data.json, metadata.json
```

### "Template mismatch"

Feeding works best with the same template type. Override if needed:

```bash
he feed ./ka/ doc.md -t general/biography_graph
```

---

## See Also

- [`he parse`](parse.md) — Create new knowledge abstract
- [`he info`](info.md) — View knowledge abstract statistics
- [`he build-index`](build-index.md) — Rebuild search index after feeding
