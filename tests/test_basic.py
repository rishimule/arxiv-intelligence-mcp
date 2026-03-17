
import pytest
from arxiv_mcp.core.arxiv_client import ArxivClient
from arxiv_mcp.core.processor import PaperProcessor
from arxiv_mcp.core.vector_store import VectorStore
from arxiv_mcp.tools.search import search_arxiv

def test_imports():
    """Verify that core modules can be imported."""
    assert ArxivClient is not None
    assert PaperProcessor is not None
    assert VectorStore is not None

def test_arxiv_client_init():
    """Verify ArXivClient initialization."""
    client = ArxivClient()
    assert client is not None

def test_paper_processor_init():
    """Verify PaperProcessor initialization."""
    processor = PaperProcessor()
    assert processor is not None

def test_vector_store_init():
    """Verify VectorStore initialization."""
    # This might fail if the DB dir is not writable or logic is wrong, but it's a good smoke test
    try:
        store = VectorStore()
        assert store is not None
    except Exception as e:
        pytest.fail(f"VectorStore initialization failed: {e}")

@pytest.mark.asyncio
async def test_search_tool():
    """Verify search tool wrapper."""
    # We mock the actual search to avoid network calls in basic tests if possible,
    # but for a smoke test, we just check if it runs without crashing.
    # We won't actually call it to avoid network dependency in this basic test,
    # just import check.
    assert search_arxiv is not None
