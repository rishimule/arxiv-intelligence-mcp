# Contributing to ArXiv Intelligence MCP

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Reporting Issues](#reporting-issues)
- [Security](#security)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Be kind, constructive, and professional in all interactions.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/arxiv-intelligence-mcp.git
   cd arxiv-intelligence-mcp
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/rishimule/arxiv-intelligence-mcp.git
   ```

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Install Dependencies

```bash
uv sync
```

### Environment Configuration

Copy the example environment file (defaults work out of the box):

```bash
cp .env.example .env
```

### Verify Your Setup

```bash
uv run pytest
```

## Making Changes

### Branch Naming

Always create a feature branch from `main` -- never commit directly to `main`.

```bash
git checkout main
git pull upstream main
git checkout -b <type>/<short-description>
```

Branch type prefixes:

| Prefix | Use |
| :--- | :--- |
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `refactor/` | Code restructuring (no behavior change) |
| `docs/` | Documentation only |
| `test/` | Adding or updating tests |
| `chore/` | Dependencies, CI, tooling |

**Examples**: `feature/batch-ingest`, `fix/pdf-parsing-timeout`, `docs/api-examples`

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(scope): <imperative message>
```

| Type | When to Use |
| :--- | :--- |
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `chore` | Build process, dependency updates, tooling |
| `perf` | Performance improvements |

**Rules:**
- Use imperative mood: "add feature" not "added feature"
- Keep commits atomic -- one logical change per commit
- No WIP commits on branches intended for merge

**Examples:**
```
feat(tools): add batch paper ingestion
fix(vector-store): handle empty embedding response
test(rag): add integration test for multi-paper queries
docs(readme): update Claude Desktop config example
chore(deps): bump chromadb to 0.5.x
```

## Pull Request Process

1. **Sync** your branch with the latest `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push** your branch:
   ```bash
   git push origin <your-branch>
   ```

3. **Open a PR** against `main` with a descriptive title matching the commit convention.

4. **PR description** must include:
   - **What** changed
   - **Why** it changed
   - **How to test** the changes

5. All PRs are merged via **squash-and-merge** to keep `main` history clean.

6. The feature branch is **deleted** after merge.

### PR Checklist

Before submitting your PR, make sure:

- [ ] Code follows the existing style and patterns
- [ ] All tests pass (`uv run pytest`)
- [ ] New features include tests
- [ ] No secrets, API keys, or `.env` files are committed
- [ ] Commit messages follow the conventional commits format
- [ ] PR description explains what, why, and how to test

## Project Structure

```
src/arxiv_mcp/
├── main.py              # FastMCP server init, tool/resource registration
├── core/
│   ├── arxiv_client.py  # ArXiv API wrapper
│   ├── processor.py     # PDF-to-Markdown conversion (DocLing)
│   └── vector_store.py  # ChromaDB storage, chunking, semantic search
├── tools/
│   ├── search.py        # search_arxiv tool
│   ├── ingest.py        # ingest_paper tool
│   └── rag.py           # ask_paper tool
├── resources/
│   └── library.py       # research://library resource
└── utils/
    ├── config.py        # Settings (pydantic-settings)
    └── logger.py        # Logger singleton
tests/
├── test_basic.py        # Unit / smoke tests
└── integration_test.py  # End-to-end workflow tests
```

### Where to Add New Features

| What You're Adding | Where It Goes |
| :--- | :--- |
| New MCP tool | `src/arxiv_mcp/tools/` (new file) + register in `main.py` |
| New MCP resource | `src/arxiv_mcp/resources/` (new file) + register in `main.py` |
| Core functionality | `src/arxiv_mcp/core/` |
| Configuration options | `src/arxiv_mcp/utils/config.py` |
| Unit tests | `tests/test_*.py` |
| Integration tests | `tests/integration_test.py` |

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Unit Tests Only

```bash
uv run pytest tests/test_basic.py -v
```

### Run Integration Tests

Integration tests require network access (ArXiv API calls):

```bash
uv run pytest tests/integration_test.py -v
```

### Writing Tests

- Unit tests go in `tests/test_basic.py` or a new `tests/test_<module>.py` file
- Integration tests go in `tests/integration_test.py`
- Use `pytest-asyncio` for async test functions
- Test new tools end-to-end: input -> expected output

## Reporting Issues

### Bug Reports

When filing a bug, include:

- **Python version** (`python --version`)
- **OS** and version
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Error logs** or tracebacks (if applicable)

### Feature Requests

When suggesting a feature, include:

- **Use case** -- what problem does it solve?
- **Proposed solution** -- how should it work?
- **Alternatives considered** -- any other approaches?

## Security

- **Never** commit API keys, secrets, or `.env` files
- Use environment variables for all sensitive configuration
- If you discover a security vulnerability, please report it privately rather than opening a public issue

## Questions?

Open a [GitHub Discussion](https://github.com/rishimule/arxiv-intelligence-mcp/discussions) or file an issue. We're happy to help!
