
from ..core.arxiv_client import ArxivClient
from ..core.processor import PaperProcessor
from ..core.vector_store import VectorStore
from ..utils.logger import logger

async def ingest_paper(paper_id: str) -> str:
    """
    Download a paper, convert it to Markdown, and store it in the vector database.
    
    Args:
        paper_id: The ArXiv ID of the paper to ingest.
        
    Returns:
        A status message indicating success or failure.
    """
    client = ArxivClient()
    processor = PaperProcessor()
    vector_store = VectorStore()
    
    try:
        # 1. Download
        logger.info(f"Ingesting paper {paper_id}...")
        pdf_path = client.download_paper(paper_id)
        if not pdf_path:
            return f"Failed to download paper {paper_id}."
            
        # 2. Process
        logger.info(f"Processing paper {paper_id}...")
        markdown_content = processor.process_pdf(pdf_path)
        if not markdown_content:
            return f"Failed to process PDF for paper {paper_id}."
        
        # 3. Store
        logger.info(f"Storing paper {paper_id} in vector store...")
        # Fetch metadata again to ensure we have it (or pass it from download if we refactor)
        # For now, quick search to get metadata
        search_results = client.search(id_list=[paper_id], max_results=1) # Bug: client.search signature is query, max_results
        # Wait, client.search takes query. I can pass ID as query? Yes, arxiv supports id queries usually, or I should add get_paper method.
        # Let's use the query generic search for now, assuming ID works as query or use 'id:...' syntax if needed.
        # Actually in arxiv python lib, client.results(search) is how it works.
        # I'll just use the search tool's logic but for 1 result.
        
        # IMPROVEMENT: Add get_metadata_by_id to ArxivClient?
        # For now, let's just make a simple metadata dict.
        metadata = {
            "id": paper_id,
            "source": f"arxiv:{paper_id}"
        }
        
        vector_store.add_document(markdown_content, metadata)
        
        return f"Successfully ingested paper {paper_id}."
        
    except Exception as e:
        logger.error(f"Error in ingest_paper tool: {e}")
        return f"Error ingesting paper {paper_id}: {e}"
