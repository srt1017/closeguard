import pdfplumber
import PyPDF2
from typing import Optional
import os

# OCR imports (optional - only used if needed)
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


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
            # Final fallback: OCR for scanned PDFs
            if OCR_AVAILABLE:
                try:
                    return extract_text_ocr(path)
                except Exception as ocr_error:
                    raise Exception(f"Failed to extract text from PDF. Primary error: {e}, PyPDF2 error: {fallback_error}, OCR error: {ocr_error}")
            else:
                raise Exception(f"Failed to extract text from PDF. Primary error: {e}, Fallback error: {fallback_error}. For scanned PDFs, install OCR dependencies: pip install pytesseract pdf2image")


def extract_text_ocr(path: str) -> str:
    """
    Extract text from scanned PDF using OCR (Tesseract).
    
    Args:
        path: Path to the PDF file
        
    Returns:
        Extracted text content as string
        
    Raises:
        Exception: If OCR processing fails
    """
    if not OCR_AVAILABLE:
        raise Exception("OCR dependencies not available. Install with: pip install pytesseract pdf2image")
    
    try:
        # Convert PDF pages to images with lower DPI for faster processing
        print(f"Converting PDF to images for OCR: {path}")
        images = convert_from_path(path, dpi=150, first_page=1, last_page=10)  # Limit pages and lower DPI
        
        text_content = []
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)} with OCR...")
            
            # Extract text from image using Tesseract with faster config
            page_text = pytesseract.image_to_string(image, config='--psm 6 -c tessedit_do_invert=0')
            if page_text.strip():
                text_content.append(page_text)
            
            # Limit total processing time
            if i >= 4:  # Process max 5 pages to avoid timeout
                print(f"Limiting OCR to first 5 pages for performance")
                break
        
        result = "\n".join(text_content)
        print(f"OCR completed. Extracted {len(result)} characters.")
        return result
        
    except Exception as e:
        raise Exception(f"OCR processing failed: {e}")


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