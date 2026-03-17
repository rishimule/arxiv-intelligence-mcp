
from typing import List, Dict
from ..core.arxiv_client import ArxivClient
from ..utils.logger import logger

async def search_arxiv(query: str, max_results: int = 5) -> str:
    """
    Search for papers on ArXiv.
    
    Args:
        query: The search query.
        max_results: Maximum number of results to return.
        
    Returns:
        A formulated string containing the search results.
    """
    client = ArxivClient()
    try:
        results = client.search(query, max_results)
        if not results:
            return "No papers found."
            
        formatted_results = []
        for paper in results:
            formatted_results.append(
                f"ID: {paper.id}\n"
                f"Title: {paper.title}\n"
                f"Authors: {', '.join(paper.authors)}\n"
                f"Published: {paper.published}\n"
                f"Summary: {paper.summary}\n"
                f"PDF URL: {paper.pdf_url}\n"
                "---"
            )
            
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Error in search_arxiv tool: {e}")
        return f"Error searching ArXiv: {e}"
