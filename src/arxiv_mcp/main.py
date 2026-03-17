
from fastmcp import FastMCP
from typing import List
from .tools.search import search_arxiv
from .tools.ingest import ingest_paper
from .tools.rag import ask_paper
from .resources.library import list_library

# Initialize FastMCP server
mcp = FastMCP("ArXiv Intelligence")

# Register Tools
mcp.tool()(search_arxiv)
mcp.tool()(ingest_paper)
mcp.tool()(ask_paper)

# Register Resources
# FastMCP resource decorator is slightly different, let's use the explicit add_resource or decorator if available
# The documentation for FastMCP suggests using decorators for resources too.
# Let's wrap list_library as a resource.

@mcp.resource("research://library")
async def library_resource() -> str:
    """List all papers in the local library."""
    return await list_library()

def main():
    mcp.run()

if __name__ == "__main__":
    main()
