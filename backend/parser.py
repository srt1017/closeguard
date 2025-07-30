import pdfplumber
import PyPDF2
from typing import Optional


def extract_text(path: str) -> str:
    """
    Extract text from PDF using pdfplumber as primary method,
    with PyPDF2 as fallback.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        Extracted text content as string
        
    Raises:
        Exception: If PDF cannot be processed
    """
    try:
        # Primary method: pdfplumber (better for tables and complex layouts)
        with pdfplumber.open(path) as pdf:
            text_content = []
            
            for page in pdf.pages:
                # Extract text
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                
                # Extract tables and convert to text
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        for row in table:
                            if row:
                                row_text = " | ".join([cell or "" for cell in row])
                                text_content.append(row_text)
            
            return "\n".join(text_content)
            
    except Exception as e:
        # Fallback method: PyPDF2
        try:
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                
                return "\n".join(text_content)
                
        except Exception as fallback_error:
            raise Exception(f"Failed to extract text from PDF. Primary error: {e}, Fallback error: {fallback_error}")


def extract_tables(path: str) -> list:
    """
    Extract tables from PDF using pdfplumber.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        List of tables, where each table is a list of rows
    """
    try:
        with pdfplumber.open(path) as pdf:
            all_tables = []
            
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
            
            return all_tables
            
    except Exception as e:
        raise Exception(f"Failed to extract tables from PDF: {e}")