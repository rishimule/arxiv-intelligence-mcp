
import os
from typing import Optional

import httpx

from ..utils.logger import logger

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
S2_REC_BASE = "https://api.semanticscholar.org/recommendations/v1"
S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

S2_PAPER_FIELDS = (
    "paperId,externalIds,title,abstract,year,citationCount,"
    "influentialCitationCount,referenceCount,authors,url,"
    "venue,publicationDate,openAccessPdf,fieldsOfStudy,tldr"
)

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _s2_headers() -> dict:
    """Return Semantic Scholar request headers, with API key if available."""
    headers = {"Accept": "application/json"}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
    return headers


async def _s2_get(path: str, params: dict | None = None) -> dict:
    """Perform an async GET against the S2 Graph API."""
    url = f"{S2_API_BASE}{path}" if path.startswith("/") else path
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params=params, headers=_s2_headers())
        resp.raise_for_status()
        return resp.json()


def _format_authors(authors: list, max_shown: int = 3) -> str:
    """Format an author list, truncating with 'et al.' if needed."""
    names = [a.get("name", "?") for a in authors[:max_shown]]
    result = ", ".join(names)
    if len(authors) > max_shown:
        result += " et al."
    return result


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

async def get_paper_details(paper_id: str) -> str:
    """
    Get detailed metadata for a paper from Semantic Scholar.

    Args:
        paper_id: A paper identifier. Accepts Semantic Scholar ID,
                  ArXiv ID with prefix (e.g. "ArXiv:2301.12345"),
                  DOI with prefix (e.g. "DOI:10.1234/example"),
                  or CorpusID (e.g. "CorpusID:12345678").

    Returns:
        Formatted paper metadata including title, authors, citations,
        abstract, and TL;DR.
    """
    try:
        data = await _s2_get(f"/paper/{paper_id}", {"fields": S2_PAPER_FIELDS})

        authors_str = _format_authors(data.get("authors", []), max_shown=10)
        tldr = data.get("tldr")
        tldr_text = tldr.get("text", "") if tldr else "N/A"
        pdf_info = data.get("openAccessPdf")
        pdf_url = pdf_info.get("url", "N/A") if pdf_info else "N/A"
        ext_ids = data.get("externalIds", {})
        fields = data.get("fieldsOfStudy") or []

        return (
            f"**{data.get('title', 'Unknown')}**\n\n"
            f"Authors: {authors_str}\n"
            f"Year: {data.get('year', 'N/A')}\n"
            f"Venue: {data.get('venue', 'N/A')}\n"
            f"Citations: {data.get('citationCount', 0)} "
            f"(influential: {data.get('influentialCitationCount', 0)})\n"
            f"References: {data.get('referenceCount', 0)}\n"
            f"Fields: {', '.join(fields) if fields else 'N/A'}\n"
            f"ArXiv: {ext_ids.get('ArXiv', 'N/A')} | DOI: {ext_ids.get('DOI', 'N/A')}\n"
            f"Open Access PDF: {pdf_url}\n"
            f"S2 URL: {data.get('url', 'N/A')}\n\n"
            f"**TL;DR:** {tldr_text}\n\n"
            f"**Abstract:** {data.get('abstract', 'N/A')}"
        )
    except Exception as e:
        logger.error(f"Error fetching paper details for {paper_id}: {e}")
        return f"Error fetching paper details: {e}"


async def get_citations(
    paper_id: str,
    limit: int = 10,
    fields: Optional[str] = None,
) -> str:
    """
    Get papers that cite a given paper (forward citation traversal).

    Use this to discover who is building on a paper's results — essential
    for literature reviews and tracking research influence.

    Args:
        paper_id: Paper identifier (S2 ID, ArXiv:..., DOI:..., CorpusID:...).
        limit: Number of citing papers to return (1-100, default 10).
        fields: Comma-separated fields for each citing paper.
                Default: "title,year,citationCount,authors,url"

    Returns:
        Formatted list of papers that cite the given paper.
    """
    limit = max(1, min(100, limit))
    if not fields:
        fields = "title,year,citationCount,authors,url"

    try:
        data = await _s2_get(
            f"/paper/{paper_id}/citations",
            {"fields": fields, "limit": limit},
        )

        citations = data.get("data", [])
        if not citations:
            return "No citations found for this paper."

        results = []
        for item in citations:
            cp = item.get("citingPaper", {})
            authors = _format_authors(cp.get("authors", []))
            results.append(
                f"- **{cp.get('title', 'Unknown')}** ({cp.get('year', '?')})\n"
                f"  Authors: {authors}\n"
                f"  Citations: {cp.get('citationCount', 0)} | {cp.get('url', '')}"
            )

        return f"Showing {len(citations)} citing papers:\n\n" + "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error fetching citations for {paper_id}: {e}")
        return f"Error fetching citations: {e}"


async def get_references(
    paper_id: str,
    limit: int = 10,
    fields: Optional[str] = None,
) -> str:
    """
    Get papers referenced by a given paper (reverse citation traversal).

    Use this to understand what a paper builds on — the intellectual
    foundations and prior work.

    Args:
        paper_id: Paper identifier (S2 ID, ArXiv:..., DOI:..., CorpusID:...).
        limit: Number of referenced papers to return (1-100, default 10).
        fields: Comma-separated fields for each referenced paper.

    Returns:
        Formatted list of papers referenced by the given paper.
    """
    limit = max(1, min(100, limit))
    if not fields:
        fields = "title,year,citationCount,authors,url"

    try:
        data = await _s2_get(
            f"/paper/{paper_id}/references",
            {"fields": fields, "limit": limit},
        )

        references = data.get("data", [])
        if not references:
            return "No references found for this paper."

        results = []
        for item in references:
            rp = item.get("citedPaper", {})
            authors = _format_authors(rp.get("authors", []))
            results.append(
                f"- **{rp.get('title', 'Unknown')}** ({rp.get('year', '?')})\n"
                f"  Authors: {authors}\n"
                f"  Citations: {rp.get('citationCount', 0)} | {rp.get('url', '')}"
            )

        return f"Showing {len(references)} referenced papers:\n\n" + "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error fetching references for {paper_id}: {e}")
        return f"Error fetching references: {e}"


async def find_related(paper_id: str, limit: int = 10) -> str:
    """
    Find papers similar to a given paper using Semantic Scholar recommendations.

    Unlike citations/references which follow explicit links, this uses
    embedding-based similarity to find thematically related work that
    may not directly cite each other.

    Args:
        paper_id: Paper identifier (S2 ID, ArXiv:..., DOI:..., CorpusID:...).
        limit: Number of recommendations (1-50, default 10).

    Returns:
        Formatted list of related papers with abstracts.
    """
    limit = max(1, min(50, limit))

    try:
        url = f"{S2_REC_BASE}/papers/forpaper/{paper_id}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                url,
                params={
                    "fields": "title,year,citationCount,authors,url,abstract",
                    "limit": limit,
                },
                headers=_s2_headers(),
            )
            resp.raise_for_status()
            data = resp.json()

        papers = data.get("recommendedPapers", [])
        if not papers:
            return "No recommendations found."

        results = []
        for p in papers:
            authors = _format_authors(p.get("authors", []))
            abstract = (p.get("abstract") or "")[:200]
            results.append(
                f"- **{p.get('title', 'Unknown')}** ({p.get('year', '?')})\n"
                f"  Authors: {authors}\n"
                f"  Citations: {p.get('citationCount', 0)} | {p.get('url', '')}\n"
                f"  {abstract}..."
            )

        return f"Found {len(papers)} related papers:\n\n" + "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error finding related papers for {paper_id}: {e}")
        return f"Error finding related papers: {e}"


async def search_author(query: str, limit: int = 5) -> str:
    """
    Search for an author by name on Semantic Scholar.

    Args:
        query: Author name to search for.
        limit: Number of results (1-20, default 5).

    Returns:
        Formatted list of matching authors with their metrics.
    """
    limit = max(1, min(20, limit))

    try:
        data = await _s2_get(
            "/author/search",
            {
                "query": query,
                "limit": limit,
                "fields": "authorId,name,url,paperCount,citationCount,hIndex,affiliations",
            },
        )

        authors = data.get("data", [])
        if not authors:
            return f"No authors found matching '{query}'."

        results = []
        for a in authors:
            affiliations = a.get("affiliations", [])
            aff_str = ", ".join(affiliations) if affiliations else "N/A"
            results.append(
                f"- **{a.get('name', '?')}** (ID: {a.get('authorId', '?')})\n"
                f"  Affiliations: {aff_str}\n"
                f"  Papers: {a.get('paperCount', 0)} | "
                f"Citations: {a.get('citationCount', 0)} | "
                f"h-index: {a.get('hIndex', 'N/A')}"
            )

        return f"Found {len(authors)} authors:\n\n" + "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error searching for author '{query}': {e}")
        return f"Error searching for author: {e}"


async def get_author_papers(author_id: str, limit: int = 10) -> str:
    """
    Get an author's publications from Semantic Scholar.

    Args:
        author_id: Semantic Scholar author ID (numeric string).
        limit: Number of papers to return (1-100, default 10).

    Returns:
        Formatted list of the author's papers.
    """
    limit = max(1, min(100, limit))

    try:
        data = await _s2_get(
            f"/author/{author_id}/papers",
            {
                "fields": "title,year,citationCount,venue,url,openAccessPdf",
                "limit": limit,
            },
        )

        papers = data.get("data", [])
        if not papers:
            return "No papers found for this author."

        results = []
        for p in papers:
            pdf_info = p.get("openAccessPdf")
            pdf_url = pdf_info.get("url", "") if pdf_info else ""
            pdf_str = f" | PDF: {pdf_url}" if pdf_url else ""
            results.append(
                f"- **{p.get('title', 'Unknown')}** ({p.get('year', '?')})\n"
                f"  Venue: {p.get('venue', 'N/A')} | "
                f"Citations: {p.get('citationCount', 0)}{pdf_str}\n"
                f"  {p.get('url', '')}"
            )

        return f"Showing {len(papers)} papers:\n\n" + "\n\n".join(results)
    except Exception as e:
        logger.error(f"Error fetching papers for author {author_id}: {e}")
        return f"Error fetching author papers: {e}"
