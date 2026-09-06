# News

Release notes and highlights. For a complete changelog, see the [GitHub releases](https://github.com/yifanfeng97/hyper-extract/releases).

---

## v0.9.0 — Rich Document Ingestion & chunk_rag Baseline

- **📄 Rich Document Ingestion** — `he parse` / `he feed` now accept PDF, Word, PowerPoint, Excel, HTML, CSV/JSON/XML, EPUB and more via the optional ingest extra (`pip install "hyperextract[ingest]"`, powered by [MarkItDown](https://github.com/microsoft/markitdown)). Non-UTF-8 text (GBK, etc.) is auto-detected; text-less (scanned) PDFs fail with a clear OCR hint instead of silently ingesting garbage.
- **🧱 `chunk_rag` Baseline Method** — a new zero-extraction method: documents are chunked and embedded as-is, and search returns raw text chunks. Zero LLM cost at ingestion, with full provenance (tags, scoped search, per-document rollback). The chunk-retrieval baseline for corpus Q&A and method benchmarking.
- **🐛 Fixes** — `he tag` crashed on every knowledge abstract (`tag_source` was never exposed on any type); `he search`/`he talk`/`he feed`/`he remove --document` crashed on method-built KAs (`method/*` templates were not resolvable from KA metadata).

---

## v0.8.1 / v0.8.2

- **🏷️ Source Tags & Scoped Search** — `he tag ./ka/ --source doc-1 --add legal`, then `he search ./ka/ "query" --tag legal` to retrieve only within tagged documents. Works for graph, hypergraph, and set KAs. *(#89, #84)*
- **🛡️ Input Validation** — `he parse` / `he feed` now reject unsupported file types with a conversion hint instead of silently ingesting garbage. *(#88)*
- **📦 Document Archive Fix** — re-feeding the same source from a differently-named file no longer accumulates stale copies. *(#89)*

---

## v0.8.0

- **🔄 Document Upsert** — re-feed an attributed document and its previous version is rolled back automatically: removed facts disappear, shared keys re-merge from surviving sources. *(#84)*
- **📁 Per-File Source Attribution** — `he parse ./docs/` attributes each file by its name automatically; roll back or audit any single file later. An explicit `--source` still overrides.
- **⏱️ Spatiotemporal Provenance** — temporal/spatial/spatio-temporal graphs fully support source attribution and rollback, with deterministic (MERGE_FIELD) replay tests.

---

## v0.5.0 – v0.7.0

- **🗑️ Two-Tier Knowledge Deletion** — hard-delete by key (`he remove --node/--edge`, orphan edges pruned) or remove a single wrong fact via LLM-assisted editing (`he remove --edit-node --fact`), with dry-run, key-invariance checks, and automatic backups. *(#84)*
- **📜 Source Attribution & Provenance** — `he feed --source` / `he parse --source` record each document's raw contributions; `he remove --document` rolls back exactly what one document contributed; `he info --sources` shows the ledger. *(#84)*
- **📈 Incremental Everything** — feed/parse/removal/edit patch the vector index in place (only affected vectors re-embedded); `he feed` skips documents whose content hash is unchanged (`--refeed` to force). *(#84)*
- **🧪 `he template validate`** — catch semantic template errors before paying for LLM calls: 9 diagnostic rules, `--json` for CI, `--all` for directories. *(#77)*
- **📊 GraphML & CSV Export** — desktop graph tools and spreadsheets; hypergraphs get a hyperedges table. *(#85)*
- **🌐 OrcaRouter Provider** — one key for 150+ models via `create_client("orcarouter")`. *(#71)*
- **🔐 Config File Permissions** — `~/.he/config.toml` saved `0600`. *(#86)*
- **🔗 Obsidian wikilink fix** — aliases no longer break on `[ ] | # ^`. *(#87)*
- **🛡️ Chunk-Level Fault Isolation** — one failed chunk no longer discards the rest of a multi-chunk extraction. *(#78)*
- **⚡ MCP Python SDK 2.x** — `he-mcp` works on mcp 1.x and 2.x. *(#72, #82)*
- **🔀 Directed-Edge Fix** — `(source, target)` order preserved; custom endpoint field names. *(#74)*
- **🔑 DeepSeek API Key Fix** — `DEEPSEEK_API_KEY` honored on the OpenAI-compatible path. *(#76)*
- **🎓 Education Templates** — `course_concept_graph` + `curriculum_structure`. *(#80)*
- **🧭 Smaller Fixes** — Graph_RAG.search 3-tuple; `he talk -i --top-k`; onboarding/docs overhaul. *(#70, #73, #57)*
