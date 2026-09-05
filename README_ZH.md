<div align="center">

<a href="https://yifanfeng97.github.io/Hyper-Extract/latest/zh/">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo/logo-horizontal-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo/logo-horizontal.svg">
  <img alt="Hyper-Extract Logo" src="docs/assets/logo/logo-horizontal.svg" width="600">
</picture>
</a>

<br/>
<br/>

**智能知识提取 CLI**

**一行命令，将文档转化为结构化知识。**

[📖 English Version](./README.md) · [中文版](./README_ZH.md)

<!-- 状态徽章带 -->
<p align="center">
  <a href="https://trendshift.io/repositories/25420" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/25420" alt="Trendshift" width="250" height="55">
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/hyperextract/">
    <img src="https://img.shields.io/pypi/v/hyperextract?style=for-the-badge&logo=pypi&logoColor=white&labelColor=1a1a2e&color=3776ab" alt="PyPI版本">
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/python-3.11%2B-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e" alt="Python版本">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-06b6d4?style=for-the-badge&labelColor=1a1a2e" alt="开源协议">
  </a>
  <a href="https://yifanfeng97.github.io/Hyper-Extract/latest/zh/">
    <img src="https://img.shields.io/badge/docs-online-3b82f6?style=for-the-badge&logo=readthedocs&logoColor=white&labelColor=1a1a2e" alt="文档">
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

## ⚡ 30 秒快速上手

**1. 安装：**

```bash
# 先安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Hyper-Extract CLI
uv tool install hyperextract
# 或：pipx install hyperextract
```

**2. 配置你的 provider**（任选其一）：

**OpenAI：**
```bash
he config init -p openai -k YOUR_OPENAI_API_KEY
```

**Anthropic (Claude)：**
```bash
he config llm -p anthropic -k YOUR_ANTHROPIC_API_KEY
he config embedder -p openai -k YOUR_OPENAI_API_KEY
```

**DeepSeek：**
```bash
he config llm -p deepseek -k YOUR_DEEPSEEK_API_KEY
he config embedder -p openai -k YOUR_OPENAI_API_KEY
```

**百炼（阿里云）：**
```bash
he config init -p bailian -k YOUR_BAILIAN_API_KEY
```

**本地 vLLM：**
```bash
he config llm -p vllm -u http://localhost:8000/v1 -k dummy -m Qwen/Qwen3.5-9B
he config embedder -p vllm -u http://localhost:8001/v1 -k dummy -m BAAI/bge-m3
```

**3. 提取、查询与可视化：**

```bash
# 从文档提取知识
he parse examples/zh/sushi.md -t general/biography_graph -o ./output/ -l zh

# 查询
he search ./output/ "苏轼有哪些重要的作品？"

# 可视化
he show ./output/

# 导出为 Obsidian 知识库（Markdown 笔记 + [[双向链接]]）
he export obsidian ./output/ -o ./vault/
```

> **该用哪个 provider？** OpenAI 和百炼同时提供 LLM 和 embedding 模型。Anthropic 和 DeepSeek 仅提供 LLM（搜索/聊天功能需搭配 OpenAI 的 embedder）。本地 vLLM 免费但需要 GPU。DeepSeek 最经济（约 $0.001-0.005/页，而 OpenAI gpt-4o-mini 约 $0.01-0.05/页）。

<details>
<summary><b>🐍 Python API</b>（点击展开）</summary>
<br>

```bash
uv pip install hyperextract
```

```python
from hyperextract import Template

ka = Template.create("general/biography_graph")

with open("examples/zh/sushi.md") as f:
    result = ka.parse(f.read())

result.show()
```

> 🔗 更多示例：[examples/zh](./examples/zh/)

</details>

## ✨ 核心亮点

| | |
|:---|:---|
| 🔷 **8 种知识结构** | 从简单的列表到复杂的图谱、超图、时空图谱 |
| 🧠 **10+ 提取引擎** | GraphRAG、LightRAG、Hyper-RAG、KG-Gen 等开箱即用 |
| 📝 **80+ YAML 模板** | 零代码提取，覆盖金融、法律、医疗、中医、工业、通用 6 大领域 |
| 🔄 **增量演进与溯源** | 随时喂入新文档——每个来源自动标注、索引增量更新；可审计（`he info --sources`）、回滚（`he remove --document`）或以 upsert 方式更新文档 |
| 📤 **Obsidian 导出** | 将提取的图谱导出为 Obsidian 知识库——以 `[[双向链接]]` 关联的 Markdown 笔记 |

## 🎯 它能做什么？

<details>
<summary><b>📄 科研人员 — 将论文转为知识图谱</b></summary>
<br>

丢进去一篇 20 页的学术论文，一键生成关键概念、作者、引用的交互式图谱。

```bash
he parse paper.pdf -t general/academic_graph -o ./paper_kb/
he show ./paper_kb/
```

</details>

<details>
<summary><b>🏦 金融分析师 — 从财报中提取实体关系</b></summary>
<br>

自动识别非结构化报告中的公司、高管、财务指标及其关系。

```bash
he parse earnings.md -t finance/earnings_graph -o ./finance_kb/
he search ./finance_kb/ "关键风险因素有哪些？"
```

</details>

<details>
<summary><b>🔒 本地部署 — vLLM 数据不出境</b></summary>
<br>

通过 vLLM 本地运行 Qwen3.5-9B + bge-m3，数据绝不离开本机。

```python
from hyperextract import create_client
llm, emb = create_client(
    llm="vllm:Qwen3.5-9B@http://localhost:8000/v1",
    embedder="vllm:bge-m3@http://localhost:8001/v1",
    api_key="dummy",
)
```

</details>

## 🚀 支持的平台与模型

Hyper-Extract 通过 LangChain 结构化输出的 **function calling** 方法工作。模型需支持 tool/function calling。

| 平台 | 已验证模型 |
|----------|-----------------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-5 |
| **Anthropic** | claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5 |
| **DeepSeek** | deepseek-v4-flash, deepseek-v4-pro |
| **阿里云百炼** | qwen-plus, qwen-turbo, deepseek-r1 |
| **本地 vLLM** | Qwen3.5-9B (GPTQ-Marlin) |

**嵌入模型**（语义搜索）支持任意 OpenAI 兼容端点：`text-embedding-3-small`、`text-embedding-v4`（百炼）、`bge-m3`（本地 vLLM）。

> **DeepSeek 说明：** V4 模型默认开启 "thinking" 模式，Hyper-Extract 会自动关闭以保证结构化抽取可用。设置 `DEEPSEEK_API_KEY`。DeepSeek 没有嵌入接口，请搭配 OpenAI 兼容的嵌入模型使用：
> ```python
> from hyperextract import create_client
> llm, emb = create_client(llm="deepseek", embedder="openai:text-embedding-3-small")
> ```

> **Anthropic 说明：** Claude 仅用于 **LLM**（设置 `ANTHROPIC_API_KEY`）。Anthropic 没有嵌入接口，请搭配 OpenAI 兼容的嵌入模型使用：
> ```python
> from hyperextract import create_client
> llm, emb = create_client(llm="anthropic", embedder="openai:text-embedding-3-small")
> ```
> 需安装额外依赖：`pip install 'hyperextract[anthropic]'`。

> 📖 完整指南：[Provider 系统与本地模型支持](https://yifanfeng97.github.io/Hyper-Extract/latest/zh/concepts/provider-system/)

## 📈 为什么选择 Hyper-Extract？

| 特性 | GraphRAG | LightRAG | KG-Gen | ATOM | **Hyper-Extract** |
| :------ | :------: | :------: | :----: | :--: | :---------------: |
| 知识图谱 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 时序图谱 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 空间图谱 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 超图 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 领域模板 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 交互式 CLI | ✅ | ❌ | ❌ | ❌ | ✅ |
| 多语言 | ✅ | ❌ | ❌ | ❌ | ✅ |

## 🧩 支持的知识结构

从简单到复杂 —— 为你的数据选择最合适的结构：

<img src="docs/assets/autotypes.jpg" alt="知识结构矩阵" width="750" style="max-width: 100%;">

**示例 — AutoGraph 可视化效果：**

<img src="docs/assets/zh_show.jpg" alt="AutoGraph 可视化" width="750" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">

<details>
<summary><b>📋 底层架构与模板（点击展开）</b></summary>
<br>

Hyper-Extract 采用**三层架构**：

- **Auto-Types** — 8 种强类型数据结构（模型、列表、集合、图谱、超图、时序图、空间图、时空图）
- **Methods** — 提取算法：KG-Gen、GraphRAG、LightRAG、Hyper-RAG、Cog-RAG 等
- **Templates** — 覆盖 6 大领域的 80+ 预设模板，零代码配置

<img src="docs/assets/arch.jpg" alt="系统架构" width="750" style="max-width: 100%;">

**模板示例（Graph 类型）：**

```yaml
language: zh
name: 知识图谱
type: graph
tags: [general]
description: '从文本中提取实体及其关系。'
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

- [浏览全部 80+ 模板](./hyperextract/templates/presets/)
- [创建自定义模板](./hyperextract/templates/DESIGN_GUIDE_ZH.md)

</details>

## 📰 最新动态

<!-- 以下摘要来自最近合并的 PR，随版本更新而更新。 -->

### v0.8.1 / v0.8.2

- **🏷️ 来源标签与范围检索** — `he tag ./ka/ --source doc-1 --add legal`，然后 `he search ./ka/ "query" --tag legal` 即可只在已标注文档范围内检索。适用于 graph、hypergraph 和 set。*(#89, #84)*
- **🛡️ 输入类型校验** — `he parse` / `he feed` 现在会拒绝不支持的文件类型（PDF/Office）并给出转换提示，而不是静默摄入乱码。*(#88)*
- **📦 文档存档修复** — 同一来源换文件名重喂不再积累陈旧副本。*(#89)*

### v0.8.0

- **🔄 文档级 Upsert** — 重新喂入已标注的文档时自动回滚其旧版本：更新后删掉的事实不再残留，共享 key 从幸存来源重新合并。*(#84)*
- **📁 逐文件来源标注** — `he parse ./docs/` 自动按文件名标注每个文件；之后可单独回滚或审计任意文件。显式 `--source` 仍可覆盖。*(#84)*
- **⏱️ 时空图谱溯源** — 时序/空间/时空图谱完整支持来源标注与回滚，MERGE_FIELD 重放测试保证确定性。*(#84)*

<details>
<summary><b>v0.5.0 – v0.7.0</b> — 溯源、删除、增量索引、模板校验、GraphML/CSV 导出</summary>

- **🗑️ 两级知识删除** — 按 key 硬删除（`he remove --node/--edge`，孤儿边自动清理），或借助大模型移除单条错误事实（`he remove --edit-node --fact`），支持 dry-run、key 不变性校验与自动备份。*(#84)*
- **📜 来源标注与溯源** — `he feed --source` / `he parse --source` 记录每份文档的原始贡献；`he remove --document` 精确回滚单份文档的贡献；`he info --sources` 查看来源账本。*(#84)*
- **📈 全链路增量** — feed/parse/删除/编辑均原地修补向量索引（只重嵌受影响向量）；`he feed` 对内容哈希未变的文档自动跳过（`--refeed` 强制重喂）。*(#84)*
- **🧪 `he template validate`** — 在调用大模型前发现模板语义错误：9 条诊断规则、`--json` 接入 CI、`--all` 批量校验。*(#77)*
- **📊 GraphML 与 CSV 导出** — 对接桌面图分析工具与表格软件；超图附带超边表。*(#85)*
- **🌐 OrcaRouter 提供商** — 一个 key 调用 150+ 模型：`create_client("orcarouter")`。*(#71)*
- **🔐 配置文件权限** — `~/.he/config.toml` 以 `0600` 保存。*(#86)*
- **🔗 Obsidian 链接修复** — wikilink 别名不再因 `[ ] | # ^` 断链。*(#87)*
- **🛡️ Chunk 级故障隔离** — 单个 chunk 失败不再丢弃多 chunk 抽取的其余结果。*(#78)*
- **⚡ MCP Python SDK 2.x** — `he-mcp` 同时兼容 mcp 1.x / 2.x。*(#72, #82)*
- **🔀 有向边修复** — 保留 `(source, target)` 方向；支持自定义端点字段名。*(#74)*
- **🔑 DeepSeek API Key 修复** — OpenAI 兼容路径正确读取 `DEEPSEEK_API_KEY`。*(#76)*
- **🎓 教育领域模板** — `course_concept_graph` 与 `curriculum_structure`。*(#80)*
- **🧭 其他修复** — Graph_RAG.search 3-tuple；`he talk -i` 支持 `--top-k`；入门/开发安装/结构化输出文档更新。*(#70, #73, #57)*

</details>

### 更早版本

完整更新日志请参阅 [GitHub releases](https://github.com/yifanfeng97/hyper-extract/releases)。

## 📚 文档与资源

| 资源 | 链接 |
| :------- | :--- |
| 完整文档 | [yifanfeng97.github.io/Hyper-Extract](https://yifanfeng97.github.io/Hyper-Extract/latest/zh/) |
| CLI 指南 | [命令行界面](https://yifanfeng97.github.io/Hyper-Extract/latest/zh/cli/) |
| Provider 系统 | [模型兼容性与本地部署](https://yifanfeng97.github.io/Hyper-Extract/latest/zh/concepts/provider-system/) |
| 模板画廊 | [80+ 预设模板](./hyperextract/templates/presets/) |
| 示例代码 | [可运行示例](./examples/) |

## 🔌 MCP 服务器

通过 [Model Context Protocol](https://modelcontextprotocol.io) 将知识摘要暴露给支持 MCP 的助手（Claude Desktop、IDE 智能体）——只读 + 导出。

```bash
pip install 'hyperextract[mcp]'
he-mcp        # stdio MCP 服务器
```

工具：`list_templates`、`info`、`search`、`ask`（RAG）、`export_obsidian`。完整指南：[MCP 服务器文档](https://yifanfeng97.github.io/Hyper-Extract/latest/zh/mcp/)。

## 🤝 参与贡献与协议

热烈欢迎社区提交 [Issues](https://github.com/yifanfeng97/hyper-extract/issues) 和 [PRs](https://github.com/yifanfeng97/hyper-extract/pulls)。  
项目基于 **Apache-2.0** 协议开源。

## 🔒 安全认证

本项目已通过 [MseeP.ai](https://mseep.ai/app/yifanfeng97-hyper-extract) 安全审计。

## AtomGit 镜像

AtomGit镜像一Agent Reach的AtomGit同步镜像，便于国内访问与克隆。国内 AtomGit 托管：https://atomgit.com/yifanfeng97/Hyper-Extract
