<div align="center">

<a href="https://yifanfeng97.github.io/Hyper-Extract/latest/">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo/logo-horizontal-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo/logo-horizontal.svg">
  <img alt="Hyper-Extract Logo" src="docs/assets/logo/logo-horizontal.svg" width="600">
</picture>
</a>

<br/>
<br/>

**Smart Knowledge Extraction CLI**

**Transform documents into structured knowledge with one command.**

[📖 English Version](./README.md) · [中文版](./README_ZH.md)

<!-- Status ribbon -->
<p align="center">
  <a href="https://trendshift.io/repositories/25420" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/25420" alt="Trendshift" width="250" height="55">
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/hyperextract/">
    <img src="https://img.shields.io/pypi/v/hyperextract?style=for-the-badge&logo=pypi&logoColor=white&labelColor=1a1a2e&color=3776ab" alt="PyPI Version">
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/python-3.11%2B-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e" alt="Python Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-06b6d4?style=for-the-badge&labelColor=1a1a2e" alt="License">
  </a>
  <a href="https://yifanfeng97.github.io/Hyper-Extract/latest/">
    <img src="https://img.shields.io/badge/docs-online-3b82f6?style=for-the-badge&logo=readthedocs&logoColor=white&labelColor=1a1a2e" alt="Docs">
  </a>
  <a href="https://github.com/yifanfeng97/hyper-extract/stargazers">
    <img src="https://img.shields.io/github/stars/yifanfeng97/hyper-extract?style=for-the-badge&logo=github&labelColor=1a1a2e&color=facc15" alt="GitHub Stars">
  </a>
</p>

<br/>

> **"Stop reading. Start understanding."**  
> *"告别文档焦虑，让信息一目了然"*

<br/>

<img src="docs/assets/hero.jpg" alt="Hero & Workflow" width="800" style="max-width: 100%;">

<br/>
</div>

## 📰 What's New

<!-- News snippets are derived from the latest merged PRs. Update as new releases land. -->

### v0.8.1 / v0.8.2

- **🏷️ Source Tags & Scoped Search** — `he tag ./ka/ --source doc-1 --add legal`, then `he search ./ka/ "query" --tag legal` to retrieve only within tagged documents. Works for graph, hypergraph, and set KAs. *(#89, #84)*
- **🛡️ Input Validation** — `he parse` / `he feed` now reject unsupported file types (PDF/Office) with a conversion hint instead of silently ingesting garbage. *(#88)*
- **📦 Document Archive Fix** — re-feeding the same source from a differently-named file no longer accumulates stale copies. *(#89)*

### v0.8.0

- **🔄 Document Upsert** — re-feed an attributed document and its previous version is rolled back automatically: removed facts disappear, shared keys re-merge from surviving sources. *(#84)*
- **📁 Per-File Source Attribution** — `he parse ./docs/` attributes each file by its name automatically; roll back or audit any single file later. An explicit `--source` still overrides.
- **⏱️ Spatiotemporal Provenance** — temporal/spatial/spatio-temporal graphs fully support source attribution and rollback, with deterministic (MERGE_FIELD) replay tests.

<details>
<summary><b>v0.5.0 – v0.7.0</b> — provenance, deletion, incremental index, template validator, GraphML/CSV export</summary>

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

</details>

### Archived

See the full changelog in the [GitHub releases](https://github.com/yifanfeng97/hyper-extract/releases).

Hyper-Extract is an intelligent, LLM-powered knowledge extraction and evolution framework. It radically simplifies transforming highly unstructured texts into persistent, predictable, and strongly-typed **Knowledge Abstracts**. It effortlessly extracts information into a wide spectrum of formats—ranging from simple **Collections** (Lists/Sets) and **Pydantic Models**, to complex **Knowledge Graphs**, **Hypergraphs**, and even **Spatio-Temporal Graphs**.

## ✨ Core Features

| | |
|:---|:---|
| 🔷 **8 Knowledge Structures** | From simple Lists to advanced Graphs, Hypergraphs, and Spatio-Temporal Graphs |
| 🧠 **10+ Extraction Engines** | GraphRAG, LightRAG, Hyper-RAG, KG-Gen, and more — ready to use |
| 📝 **80+ YAML Templates** | Zero-code extraction across Finance, Legal, Medical, TCM, Industry, and General domains |
| 🔄 **Incremental Evolution & Provenance** | Feed new documents anytime — every source is attributed and the index updates incrementally; audit (`he info --sources`), roll back (`he remove --document`), or upsert updated versions as your sources change |
| 📤 **Obsidian Export** | Turn any extracted graph into an Obsidian vault — Markdown notes linked by `[[wikilinks]]` |

## 🎯 What Can You Do With It?

<details>
<summary><b>📄 Researcher — Turn papers into knowledge graphs</b></summary>
<br>

Feed a 20-page academic paper, get an interactive graph of key concepts, authors, and citations.

```bash
he parse paper.pdf -t general/academic_graph -o ./paper_kb/
he show ./paper_kb/
```

</details>

<details>
<summary><b>🏦 Financial Analyst — Extract entities from earnings reports</b></summary>
<br>

Automatically identify companies, executives, financial metrics, and their relationships from unstructured reports.

```bash
he parse earnings.md -t finance/earnings_graph -o ./finance_kb/
he search ./finance_kb/ "What are the key risk factors?"
```

</details>

<details>
<summary><b>🔒 Local Deployment — Keep data on-premise with vLLM</b></summary>
<br>

Run Qwen3.5-9B + bge-m3 locally via vLLM. No data leaves your machine.

```python
from hyperextract import create_client
llm, emb = create_client(
    llm="vllm:Qwen3.5-9B@http://localhost:8000/v1",
    embedder="vllm:bge-m3@http://localhost:8001/v1",
    api_key="dummy",
)
```

</details>

## 🚀 Supported Platforms & Models

Hyper-Extract uses LangChain structured output with **function calling**. The model must support tool/function calling.

| Platform | Verified Models |
|----------|-----------------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-5 |
| **Anthropic** | claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5 |
| **DeepSeek** | deepseek-v4-flash, deepseek-v4-pro |
| **阿里云百炼** | qwen-plus, qwen-turbo, deepseek-r1 |
| **Local vLLM** | Qwen3.5-9B (GPTQ-Marlin) |

**Embedding models** (semantic search) work with any OpenAI-compatible endpoint: `text-embedding-3-small`, `text-embedding-v4` (Bailian), `bge-m3` (local vLLM).

> **DeepSeek note:** DeepSeek V4 models default to "thinking" mode, which Hyper-Extract auto-disables so structured extraction works. Set `DEEPSEEK_API_KEY`. DeepSeek has no embeddings API — pair it with an OpenAI-compatible embedder:
> ```python
> from hyperextract import create_client
> llm, emb = create_client(llm="deepseek", embedder="openai:text-embedding-3-small")
> ```

> **Anthropic note:** Claude is used for the **LLM** (set `ANTHROPIC_API_KEY`). Anthropic has no embeddings API, so pair it with an OpenAI-compatible embedder:
> ```python
> from hyperextract import create_client
> llm, emb = create_client(llm="anthropic", embedder="openai:text-embedding-3-small")
> ```
> Requires the extra: `pip install 'hyperextract[anthropic]'`.

> 📖 Full guide: [Provider System & Local Model Support](https://yifanfeng97.github.io/Hyper-Extract/latest/concepts/provider-system/)

## ⚡ 30-Second Quick Start

**1. Install:**

```bash
# Install uv first (if you haven't)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Hyper-Extract CLI
uv tool install hyperextract
# or: pipx install hyperextract
```

**2. Configure your provider** (pick one):

**OpenAI:**
```bash
he config init -p openai -k YOUR_OPENAI_API_KEY
```

**Anthropic (Claude):**
```bash
he config llm -p anthropic -k YOUR_ANTHROPIC_API_KEY
he config embedder -p openai -k YOUR_OPENAI_API_KEY
```

**DeepSeek:**
```bash
he config llm -p deepseek -k YOUR_DEEPSEEK_API_KEY
he config embedder -p openai -k YOUR_OPENAI_API_KEY
```

**Bailian (Alibaba Cloud):**
```bash
he config init -p bailian -k YOUR_BAILIAN_API_KEY
```

**Local vLLM:**
```bash
he config llm -p vllm -u http://localhost:8000/v1 -k dummy -m Qwen/Qwen3.5-9B
he config embedder -p vllm -u http://localhost:8001/v1 -k dummy -m BAAI/bge-m3
```

**3. Extract, query & visualize:**

```bash
# Extract knowledge from a document
he parse examples/en/tesla.md -t general/biography_graph -o ./output/ -l en

# Query it
he search ./output/ "What are Tesla's major achievements?"

# Visualize
he show ./output/

# Export to an Obsidian vault (Markdown notes + [[wikilinks]])
he export obsidian ./output/ -o ./vault/
```

> **Which provider should I use?** OpenAI and Bailian provide both LLM and embedding models in one API. Anthropic and DeepSeek are LLM-only (pair them with an OpenAI embedder for search/chat). Local vLLM is free but requires a GPU. DeepSeek is the most cost-effective option (~$0.001-0.005/page vs ~$0.01-0.05/page for OpenAI gpt-4o-mini).

<details>
<summary><b>🐍 Python API</b> (click to expand)</summary>
<br>

```bash
uv pip install hyperextract
```

```python
from hyperextract import Template

ka = Template.create("general/biography_graph")

with open("examples/en/tesla.md") as f:
    result = ka.parse(f.read())

result.show()
```

> 🔗 More examples: [examples/en](./examples/en/)

</details>

## 📈 Why Hyper-Extract?

| Feature | GraphRAG | LightRAG | KG-Gen | ATOM | **Hyper-Extract** |
| :------ | :------: | :------: | :----: | :--: | :---------------: |
| Knowledge Graph | ✅ | ✅ | ✅ | ✅ | ✅ |
| Temporal Graph | ✅ | ❌ | ❌ | ✅ | ✅ |
| Spatial Graph | ❌ | ❌ | ❌ | ❌ | ✅ |
| Hypergraph | ❌ | ❌ | ❌ | ❌ | ✅ |
| Domain Templates | ❌ | ❌ | ❌ | ❌ | ✅ |
| Interactive CLI | ✅ | ❌ | ❌ | ❌ | ✅ |
| Multi-language | ✅ | ❌ | ❌ | ❌ | ✅ |

## 🧩 Supported Knowledge Structures

From simple to complex — pick the right structure for your data:

<img src="docs/assets/autotypes.jpg" alt="Knowledge Structures Matrix" width="750" style="max-width: 100%;">

**Example — AutoGraph visualization:**

<img src="docs/assets/en_show.jpg" alt="AutoGraph Visualization" width="750" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">

<details>
<summary><b>📋 What's under the hood? (Architecture & Templates)</b></summary>
<br>

Hyper-Extract follows a **three-layer architecture**:

- **Auto-Types** — 8 strongly-typed data structures (Model, List, Set, Graph, Hypergraph, Temporal Graph, Spatial Graph, Spatio-Temporal Graph)
- **Methods** — Extraction algorithms: KG-Gen, GraphRAG, LightRAG, Hyper-RAG, Cog-RAG, and more
- **Templates** — 80+ presets across 6 domains. Zero-code setup.

<img src="docs/assets/arch.jpg" alt="Architecture" width="750" style="max-width: 100%;">

**Template example (Graph type):**

```yaml
language: en
name: Knowledge Graph
type: graph
tags: [general]
description: 'Extract entities and their relationships.'
output:
  entities:
    fields:
    - name: name
      type: str
    - name: type
      type: str
    - name: description
      type: str
  relations:
    fields:
    - name: source
      type: str
    - name: target
      type: str
    - name: type
      type: str
identifiers:
  entity_id: name
  relation_id: '{source}|{type}|{target}'
```

- [Browse all 80+ templates](./hyperextract/templates/presets/)
- [Create custom templates](./hyperextract/templates/DESIGN_GUIDE.md)

</details>

## 📚 Documentation & Resources

| Resource | Link |
| :------- | :--- |
| Full Documentation | [yifanfeng97.github.io/Hyper-Extract](https://yifanfeng97.github.io/Hyper-Extract/latest/) |
| CLI Guide | [Command-line interface](https://yifanfeng97.github.io/Hyper-Extract/latest/cli/) |
| Provider System | [Model compatibility & local deployment](https://yifanfeng97.github.io/Hyper-Extract/latest/concepts/provider-system/) |
| Template Gallery | [80+ presets](./hyperextract/templates/presets/) |
| Examples | [Working code](./examples/) |

## 🔌 MCP Server

Expose your knowledge abstracts to MCP-capable assistants (Claude Desktop, IDE agents) via the [Model Context Protocol](https://modelcontextprotocol.io) — read + export only.

```bash
pip install 'hyperextract[mcp]'
he-mcp        # stdio MCP server
```

Tools: `list_templates`, `info`, `search`, `ask` (RAG), `export_obsidian`. Full guide: [MCP Server docs](https://yifanfeng97.github.io/Hyper-Extract/latest/mcp/).

## 🤝 Contributing & License

Contributions are welcome! Please submit [Issues](https://github.com/yifanfeng97/hyper-extract/issues) and [PRs](https://github.com/yifanfeng97/hyper-extract/pulls).  
Licensed under **Apache-2.0**.

## 🔒 Security

This project has been security assessed by [MseeP.ai](https://mseep.ai/app/yifanfeng97-hyper-extract).

## AtomGit Mirror

AtomGit mirror - a synchronized AtomGit mirror of Agent Reach for easier access and cloning in China. Hosted on AtomGit: https://atomgit.com/yifanfeng97/Hyper-Extract
