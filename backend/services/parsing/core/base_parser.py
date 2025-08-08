"""Base abstract parser for document processing."""

from abc import ABC, abstractmethod
from typing import Optional, List, Any
import pdfplumber
from pathlib import Path

from models.document import ParsedDocument


class BaseParser(ABC):
    """Abstract base class for all document parsers."""
    
    def __init__(self, file_path: str):
        """Initialize parser with file path."""
        self.file_path = Path(file_path)
        self.pdf_document = None
        self.errors: List[str] = []
    
    def __enter__(self):
        """Context manager entry - open PDF."""
        try:
            self.pdf_document = pdfplumber.open(self.file_path)
            return self
        except Exception as e:
            self.errors.append(f"Failed to open PDF: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close PDF."""
        if self.pdf_document:
            self.pdf_document.close()
    
    @abstractmethod
    def parse(self) -> ParsedDocument:
        """Parse the document and return structured data."""
        pass
    
    def get_page(self, page_num: int) -> Optional[Any]:
        """Get a specific page from the PDF (1-indexed)."""
        if not self.pdf_document:
            return None
        
        try:
            if 1 <= page_num <= len(self.pdf_document.pages):
                return self.pdf_document.pages[page_num - 1]  # Convert to 0-indexed
            else:
                self.errors.append(f"Page {page_num} out of range")
                return None
        except Exception as e:
            self.errors.append(f"Error accessing page {page_num}: {e}")
            return None
    
    def get_page_count(self) -> int:
        """Get total number of pages."""
        if not self.pdf_document:
            return 0
        return len(self.pdf_document.pages)
    
    def extract_raw_text(self) -> str:
        """Extract all text from document as fallback."""
        if not self.pdf_document:
            return ""
        
        try:
            text_content = []
            for page in self.pdf_document.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            return "\n".join(text_content)
        except Exception as e:
            self.errors.append(f"Error extracting raw text: {e}")
            return ""
    
    def add_error(self, error: str) -> None:
        """Add an error to the parser."""
        self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if parser encountered errors."""
        return bool(self.errors)