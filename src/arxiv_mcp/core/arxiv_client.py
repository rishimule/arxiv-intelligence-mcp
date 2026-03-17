
import arxiv
import os
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..utils.config import settings
from ..utils.logger import logger

class ArxivPaper(BaseModel):
    id: str
    title: str
    summary: str
    authors: List[str]
    published: datetime
    pdf_url: str
    local_path: Optional[str] = None

class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client(
            page_size=settings.MAX_SEARCH_RESULTS,
            delay_seconds=3.0,
            num_retries=3
        )

    def search(self, query: str = "", max_results: int = 5, id_list: List[str] = None) -> List[ArxivPaper]:
        """Search for papers on ArXiv."""
        if id_list is None:
            id_list = []
            
        search = arxiv.Search(
            query=query,
            id_list=id_list,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        try:
            for result in self.client.results(search):
                paper = ArxivPaper(
                    id=result.entry_id.split('/')[-1],
                    title=result.title,
                    summary=result.summary,
                    authors=[a.name for a in result.authors],
                    published=result.published,
                    pdf_url=result.pdf_url
                )
                results.append(paper)
        except Exception as e:
            logger.error(f"Error searching ArXiv with query '{query}': {e}")
            raise

        return results

    def download_paper(self, paper_id: str) -> Optional[str]:
        """Download a paper by ID and return its local path."""
        try:
            # Construct the PDF URL correctly if only ID is missing
            # arxiv library handles id lookups well
            search = arxiv.Search(id_list=[paper_id])
            paper = next(self.client.results(search))
            
            # Clean filename
            filename = f"{paper_id}.pdf"
            filepath = settings.PAPERS_DIR / filename
            
            if filepath.exists():
                logger.info(f"Paper {paper_id} already exists at {filepath}")
                return str(filepath)
            
            # Download
            logger.info(f"Downloading paper {paper_id}...")
            paper.download_pdf(dirpath=settings.PAPERS_DIR, filename=filename)
            logger.info(f"Downloaded paper {paper_id} to {filepath}")
            return str(filepath)
            
        except StopIteration:
            logger.error(f"Paper {paper_id} not found.")
            return None
        except Exception as e:
            logger.error(f"Error downloading paper {paper_id}: {e}")
            return None
