
import asyncio
import sys
from arxiv_mcp.tools.search import search_arxiv
from arxiv_mcp.tools.ingest import ingest_paper
from arxiv_mcp.tools.rag import ask_paper
from arxiv_mcp.resources.library import list_library

async def main():
    print(">>> 1. deeply_test_search: Searching for 'attention is all you need'...")
    search_results = await search_arxiv("attention is all you need", max_results=1)
    print(search_results)
    
    if "ID:" not in search_results:
        print("!!! Search failed or found nothing.")
        return

    # Extract ID (rudimentary parsing for test)
    # Expected format: "ID: 1706.03762v5..."
    try:
        paper_id = search_results.split("ID: ")[1].split("\n")[0].strip()
        print(f">>> Found Paper ID: {paper_id}")
    except IndexError:
        print("!!! Could not extract paper ID.")
        return

    print(f"\n>>> 2. deeply_test_ingest: Ingesting paper {paper_id} (this may take a while)...")
    ingest_result = await ingest_paper(paper_id)
    print(ingest_result)

    print(f"\n>>> 3. deeply_test_library: Listing library...")
    library_list = await list_library()
    print(library_list)
    
    if "Library is empty" in library_list:
        print("!!! Ingestion seemed to fail silently or library is empty.")
    
    print("\n>>> 4. deeply_test_rag: Asking 'What is the Transformer architecture?'...")
    rag_result = await ask_paper("What is the Transformer architecture?")
    print(rag_result)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
