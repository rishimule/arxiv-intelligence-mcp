
from pathlib import Path
from docling.document_converter import DocumentConverter
from ..utils.logger import logger

class PaperProcessor:
    def __init__(self):
        self.converter = DocumentConverter()

    def process_pdf(self, pdf_path: str) -> str:
        """
        Convert a PDF file to Markdown using DocLing.
        
        Args:
            pdf_path: Absolute path to the PDF file.
            
        Returns:
            The markdown content of the PDF.
        """
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            result = self.converter.convert(pdf_path)
            markdown_content = result.document.export_to_markdown()
            logger.info(f"Successfully processed PDF: {pdf_path}")
            return markdown_content
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
