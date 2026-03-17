
from ..core.vector_store import VectorStore
from ..utils.logger import logger

async def ask_paper(question: str) -> str:
    """
    Ask a question about the papers stored in the library (RAG).
    
    Args:
        question: The question to ask.
        
    Returns:
        Relevant excerpts from the papers that answer the question.
    """
    vector_store = VectorStore()
    try:
        results = vector_store.search(question, n_results=5)
        
        if not results:
            return "No relevant information found in the library."
            
        formatted_response = "Here are some relevant excerpts from the library:\n\n"
        for i, res in enumerate(results, 1):
            content = res.get('content', '').strip()
            meta = res.get('metadata', {})
            source = meta.get('source', 'Unknown Source')
            
            formatted_response += f"--- Excerpt {i} (Source: {source}) ---\n{content}\n\n"
            
        return formatted_response
    except Exception as e:
        logger.error(f"Error in ask_paper tool: {e}")
        return f"Error querying the library: {e}"
