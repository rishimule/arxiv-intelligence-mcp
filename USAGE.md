# User Guide: ArXiv Intelligence MCP

Welcome to **ArXiv Intelligence**, your local AI research assistant. This server empowers your LLM (like Claude) to search for scientific papers, read them in detail, and answer questions based on their content using a local vector database.

## 🚀 Getting Started

### 1. Prerequisites
-   **Python 3.11+** installed.
-   **uv** installed (Recommended modern Python package manager).
    -   *Install uv*: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `pip install uv`)

### 2. Installation
Navigate to the project directory and sync dependencies:
```bash
cd arxiv-intelligence-mcp
uv sync
```

### 3. Configuration
This project uses reliable defaults, but you can customize it.
-   **Embeddings**: By default, it uses a local `sentence-transformers` model (runs on CPU/Metal). No API key needed.
-   **Storage**: Data is stored in `data/` within the project folder.

## 🔌 Connecting to Claude Desktop

To use this with Claude Desktop, you need to add it to your `claude_desktop_config.json`.

1.  Open the config file:
    -   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    -   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2.  Add the following entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "arxiv-intelligence": {
      "command": "/absolute/path/to/arxiv-intelligence-mcp/.venv/bin/python",
      "args": [
        "-m",
        "arxiv_mcp.main"
      ],
      "cwd": "/absolute/path/to/arxiv-intelligence-mcp",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```
*Note: Replace `/absolute/path/to/...` with the actual full paths on your machine. You can find the path to `uv` by running `which uv`.*

3.  Restart Claude Desktop.

## 💡 How to Use

Once connected, you can ask Claude to perform research tasks naturally.

### 🔍 Tools (Commands)

| Tool | Description | Example Usage |
| :--- | :--- | :--- |
| **`search_arxiv`** | Searches ArXiv for papers. | *"Search for recent papers on 'chain of thought reasoning'."* |
| **`ingest_paper`** | Downloads a paper & saves it to memory. | *"Read and memorize the paper with ID 2201.11903."* |
| **`ask_paper`** | Asks questions about saved papers. | *"What does the 'chain of thought' paper say about few-shot prompting?"* |

### 📚 Resources (Data)

| Resource | Description | Example Usage |
| :--- | :--- | :--- |
| **`research://library`** | Lists all ingested papers. | *"Show me what papers are currently in my library."* |

## 🧠 Example Workflow

1.  **Discovery**: "Find me the top 3 papers about 'vision transformers'."
    *Claude uses `search_arxiv`.*
2.  **Selection**: "That second paper looks interesting. Please read it."
    *Claude uses `ingest_paper` (this downloads and processes the PDF).*
3.  **Analysis**: "Explain the main architecture diagram described in that paper."
    *Claude uses `ask_paper` to retrieve specific details from the text.*
4.  **Synthesis**: "Compare this approach to the standard transformer."
    *Claude combines its internal knowledge with the retrieved context.*

## ⚠️ Troubleshooting

-   **"Failed to initialize NumPy"**: Ensure you are using the installed virtual environment (`.venv`). This project pins `numpy<2` to avoid conflicts on macOS. Always run commands with `uv run`.
-   **Ingestion is slow**: Converting PDFs to Markdown (DocLing) is computationally intensive. It may take 30-60 seconds per paper depending on complexity.
-   **Search finds nothing**: Try broader keywords. ArXiv search is exact-match on some fields.

## 🏗️ Architecture

-   **Backend**: Python (FastMCP)
-   **PDF Engine**: DocLing (IBM) - Converts visual layout to text.
-   **Memory**: ChromaDB - Local vector storage.
