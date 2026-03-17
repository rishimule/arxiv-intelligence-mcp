# ArXiv Intelligence MCP

An intelligent research assistant powered by [MCP](https://modelcontextprotocol.io/), ArXiv, DocLing, and ChromaDB. Connect it to Claude Desktop or Cursor and let your AI search, read, and reason over scientific papers.

## Features

- **Smart Search** -- Query ArXiv for papers sorted by relevance
- **Deep Ingestion** -- Download PDFs and convert them to clean Markdown via IBM DocLing
- **Semantic Memory** -- Store paper embeddings in a local ChromaDB vector store
- **RAG Q&A** -- Ask questions about your library and get context-grounded answers

## Architecture

```
Claude Desktop / Cursor
        |
        v  (MCP protocol)
ArXiv Intelligence Server
   |         |          |
   v         v          v
ArXiv API   DocLing   ChromaDB
(search)   (PDF->MD)  (vectors)
```

1. **MCP Host** (Claude Desktop / Cursor) communicates with the ArXiv Intelligence Server.
2. **ArXiv Client** fetches papers from the ArXiv API.
3. **DocLing Processor** converts PDFs to Markdown.
4. **Vector Store** (ChromaDB) indexes chunked content with sentence-transformer embeddings.
5. **RAG Tool** retrieves relevant context for LLM queries.

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install

```bash
git clone https://github.com/<your-username>/arxiv-intelligence-mcp.git
cd arxiv-intelligence-mcp
uv sync
```

### Configure

Copy the example environment file (optional -- defaults work out of the box):

```bash
cp .env.example .env
```

### Run

```bash
uv run arxiv-intelligence-mcp
```

## Connecting to Claude Desktop

Add the server to your `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "arxiv-intelligence": {
      "command": "/absolute/path/to/arxiv-intelligence-mcp/.venv/bin/python",
      "args": ["-m", "arxiv_mcp.main"],
      "cwd": "/absolute/path/to/arxiv-intelligence-mcp",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

> Replace `/absolute/path/to/...` with the actual path on your machine.

Then restart Claude Desktop.

## Usage

Once connected, ask Claude to perform research tasks naturally:

| Tool | Description | Example |
| :--- | :--- | :--- |
| `search_arxiv` | Search ArXiv for papers | *"Find papers on chain-of-thought reasoning"* |
| `ingest_paper` | Download & memorize a paper | *"Read paper 2201.11903"* |
| `ask_paper` | Ask questions about saved papers | *"What does the CoT paper say about few-shot prompting?"* |

| Resource | Description | Example |
| :--- | :--- | :--- |
| `research://library` | List all ingested papers | *"Show me my paper library"* |

### Example Workflow

1. **Discover** -- *"Find the top 3 papers on vision transformers"*
2. **Ingest** -- *"Read the second paper"*
3. **Query** -- *"Explain the architecture from that paper"*
4. **Synthesize** -- *"Compare this approach to standard transformers"*

See [USAGE.md](USAGE.md) for a detailed user guide, configuration options, and troubleshooting.

## Development

```bash
# Run tests
uv run pytest

# Run integration tests
uv run pytest tests/integration_test.py -v
```

## Tech Stack

| Component | Technology |
| :--- | :--- |
| MCP Framework | [FastMCP](https://github.com/jlowin/fastmcp) |
| PDF Conversion | [DocLing](https://github.com/DS4SD/docling) (IBM) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| Embeddings | [sentence-transformers](https://www.sbert.net/) (local, no API key needed) |
| ArXiv API | [arxiv.py](https://github.com/lukasschwab/arxiv.py) |

## License

[MIT](LICENSE)
