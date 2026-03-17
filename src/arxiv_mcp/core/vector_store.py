
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
from ..utils.config import settings
from ..utils.logger import logger
import uuid

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.VECTOR_DB_DIR),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Use default sentence-transformers model
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        
        self.collection = self.client.get_or_create_collection(
            name="arxiv_papers",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_document(self, content: str, metadata: Dict[str, Any], chunk_size: int = 1000, overlap: int = 100):
        """
        Add a document to the vector store with chunking.
        """
        # Simple chunking strategy for now
        # Ideally we'd use a smarter splitter like LangChain's RecursiveCharacterTextSplitter
        # But keeping dependencies minimal for this core implementation
        
        chunks = self._chunk_text(content, chunk_size, overlap)
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [metadata] * len(chunks)
        
        try:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(chunks)} chunks for document {metadata.get('id', 'unknown')}")
        except Exception as e:
            logger.error(f"Error adding document to vector store: {e}")
            raise

    def search(self, query: str, n_results: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar documents.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_dict
            )
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
            
    def list_papers(self) -> List[str]:
        """List all unique paper IDs in the store."""
        try:
            # This is inefficient for large datasets but fine for a local tool
            # A better way would be to maintain a separate 'papers' collection or metadata table
            # For now, we'll just get all metadata and extract unique IDs
            result = self.collection.get(include=["metadatas"])
            if not result or not result['metadatas']:
                return []
            
            paper_ids = set()
            for meta in result['metadatas']:
                if 'id' in meta:
                    paper_ids.add(meta['id'])
            return list(paper_ids)
        except Exception as e:
            logger.error(f"Error listing papers: {e}")
            return []

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Simple text chunker."""
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
            
        return chunks
