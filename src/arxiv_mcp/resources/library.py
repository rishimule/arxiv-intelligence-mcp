
from ..core.vector_store import VectorStore
from ..utils.logger import logger

async def list_library() -> str:
    """
    List all papers currently in the local library.
    
    Returns:
        A list of paper IDs.
    """
    vector_store = VectorStore()
    try:
        papers = vector_store.list_papers()
        if not papers:
            return "Library is empty."
            
        return "Papers in Library:\n" + "\n".join(f"- {p}" for p in papers)
    except Exception as e:
        logger.error(f"Error listing library: {e}")
        return f"Error accessing library: {e}"
