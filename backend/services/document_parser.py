"""Document parsing service for extracting text from PDFs."""

import tempfile
from typing import Optional
from pathlib import Path

# Import the existing parser functionality
from parser import extract_text


class DocumentParserService:
    """Service for parsing documents and extracting text."""
    
    def __init__(self, temp_dir: str = "/tmp"):
        self.temp_dir = temp_dir
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from a file path."""
        try:
            return extract_text(file_path)
        except Exception as e:
            raise Exception(f"Failed to extract text from file: {e}")
    
    def extract_text_from_upload(self, file_content: bytes, filename: str) -> str:
        """Extract text from uploaded file content."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Extract text using existing parser
                text = self.extract_text_from_file(temp_file_path)
                return text
            finally:
                # Clean up temporary file
                try:
                    Path(temp_file_path).unlink()
                except OSError:
                    pass  # File might already be deleted
                    
        except Exception as e:
            raise Exception(f"Failed to process uploaded file: {e}")
    
    def validate_file_type(self, filename: str, allowed_types: list = None) -> bool:
        """Validate file type based on extension."""
        if allowed_types is None:
            allowed_types = ['.pdf']
        
        file_extension = Path(filename).suffix.lower()
        return file_extension in allowed_types
    
    def get_text_stats(self, text: str) -> dict:
        """Get basic statistics about extracted text."""
        return {
            'length': len(text),
            'word_count': len(text.split()),
            'line_count': len(text.splitlines()),
            'character_count': len(text.replace(' ', '').replace('\n', ''))
        }