<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/ArXiv_Intelligence-MCP_Server-6366f1?style=for-the-badge&labelColor=0a0a0f">
  <img alt="ArXiv Intelligence MCP" src="https://img.shields.io/badge/ArXiv_Intelligence-MCP_Server-6366f1?style=for-the-badge&labelColor=0a0a0f">
</picture>

<br><br>

**Search, read, and reason over scientific papers with AI.**

An intelligent research assistant powered by [Model Context Protocol](https://modelcontextprotocol.io/), ArXiv, DocLing, and ChromaDB.<br>
Connect it to Claude Desktop or Cursor and start exploring the literature with natural language.

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22d3ee?style=flat-square)](LICENSE)
[![MCP](https://img.shields.io/badge/Protocol-MCP-6366f1?style=flat-square)](https://modelcontextprotocol.io/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-f7b731?style=flat-square)](https://docs.astral.sh/uv/)

[Website](https://rishimule.github.io/arxiv-intelligence-mcp) &nbsp;&middot;&nbsp; [Quick Start](#-quick-start) &nbsp;&middot;&nbsp; [Usage Guide](USAGE.md) &nbsp;&middot;&nbsp; [Architecture](#-architecture)

</div>

<br>

---

<br>

## Highlights

| | Feature | Description |
|:---|:---|:---|
| **Search** | Smart Discovery | Query ArXiv for papers ranked by relevance with full metadata |
| **Read** | Deep Ingestion | Download PDFs and convert them to clean Markdown via IBM DocLing |
| **Remember** | Semantic Memory | Chunk and embed papers locally with sentence-transformers &mdash; no API keys needed |
| **Reason** | RAG Q&A | Ask questions and get context-grounded answers with cited sources |

<br>

## Architecture

```
┌─────────────────────────────────┐
│   Claude Desktop  /  Cursor     │
└──────────────┬──────────────────┘
               │  MCP Protocol
               ▼
┌─────────────────────────────────┐
│   ArXiv Intelligence Server     │
│   (FastMCP)                     │
└──┬──────────┬───────────────┬───┘
   │          │               │
   ▼          ▼               ▼
┌────────┐ ┌────────────┐ ┌──────────┐
│ ArXiv  │ │  DocLing   │ │ ChromaDB │
│  API   │ │ (PDF→MD)   │ │(Vectors) │
└────────┘ └────────────┘ └──────────┘
```

1. **MCP Host** (Claude Desktop / Cursor) communicates with the server over the Model Context Protocol.
2. **ArXiv Client** searches and downloads papers from the ArXiv API.
3. **DocLing Processor** converts PDFs to structured Markdown.
4. **Vector Store** (ChromaDB) indexes chunked content with sentence-transformer embeddings.
5. **RAG Tool** retrieves relevant context to ground LLM responses.

<br>

## MCP Interface

| Type | Name | Description |
|:---|:---|:---|
| `Tool` | `search_arxiv` | Search ArXiv papers by query |
| `Tool` | `ingest_paper` | Download, process, and embed a paper |
| `Tool` | `ask_paper` | RAG query across ingested papers |
| `Resource` | `research://library` | List all ingested paper IDs |

<br>

## Quick Start

### Prerequisites

- **Python 3.11+**
- [**uv**](https://docs.astral.sh/uv/) (recommended) or pip

### Install

```bash
git clone https://github.com/rishimule/arxiv-intelligence-mcp.git
cd arxiv-intelligence-mcp
uv sync
```

### Configure (optional)

Defaults work out of the box. To customize, copy the example env:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|:---|:---|:---|
| `PAPERS_DIR` | `data/papers/` | PDF download cache |
| `VECTOR_DB_DIR` | `data/vector_db/` | ChromaDB persistence directory |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model name |
| `MAX_SEARCH_RESULTS` | `5` | Default search result count |

### Run

```bash
uv run arxiv-intelligence-mcp
```

<br>

## Connect to Claude Desktop

Add the server to your `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "arxiv-intelligence": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["-m", "arxiv_mcp.main"],
      "cwd": "/absolute/path/to/arxiv-intelligence-mcp",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

> Replace `/absolute/path/to/...` with the actual paths on your machine. Then restart Claude Desktop.

<br>

## Example Workflow

```
You:    "Find the top 3 papers on vision transformers"
Claude: → uses search_arxiv → returns ranked results

You:    "Read the second paper"
Claude: → uses ingest_paper → downloads, processes, embeds

You:    "Explain the architecture from that paper"
Claude: → uses ask_paper → retrieves relevant chunks → answers

You:    "Compare this approach to standard transformers"
Claude: → combines retrieved context with internal knowledge
```

See [**USAGE.md**](USAGE.md) for the full user guide, advanced configuration, and troubleshooting.

<br>

## Development

```bash
# Run all tests
uv run pytest

# Unit tests only
uv run pytest tests/test_basic.py -v

# Integration tests (requires network)
uv run pytest tests/integration_test.py -v
```

<br>

## Tech Stack

| Component | Technology |
|:---|:---|
| MCP Framework | [FastMCP](https://github.com/jlowin/fastmcp) |
| PDF Conversion | [DocLing](https://github.com/DS4SD/docling) (IBM) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| Embeddings | [sentence-transformers](https://www.sbert.net/) &mdash; local, no API key |
| ArXiv Client | [arxiv.py](https://github.com/lukasschwab/arxiv.py) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |
| Build System | [hatchling](https://hatch.pypa.io/) |

<br>

## License

[MIT](LICENSE)

<br>

<div align="center">
<sub>Built by <a href="https://github.com/rishimule">Rishi Mule</a></sub>
</div>
