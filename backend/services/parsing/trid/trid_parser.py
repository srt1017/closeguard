"""Main TRID Closing Disclosure parser orchestrator."""

from typing import Optional
from pathlib import Path

from ..core import BaseParser
from models.document import ParsedDocument, LoanSummary


class TridParser(BaseParser):
    """Main parser for TRID Closing Disclosure documents."""
    
    def __init__(self, file_path: str):
        """Initialize TRID parser."""
        super().__init__(file_path)
        self.document_type = "TRID Closing Disclosure"
        
        # Page parsers (to be imported when implemented)
        self._page1_parser = None
        self._page2_parser = None  
        self._page3_parser = None
    
    def parse(self) -> ParsedDocument:
        """Parse complete TRID document."""
        # Initialize result document
        result = ParsedDocument(
            filename=self.file_path.name,
            page_count=self.get_page_count(),
            parsing_errors=self.errors.copy()
        )
        
        # Add raw text as fallback
        result.raw_text = self.extract_raw_text()
        
        try:
            # Validate document structure
            if not self._validate_trid_structure():
                result.parsing_success = False
                result.add_parsing_error("Document does not appear to be a valid TRID Closing Disclosure")
                return result
            
            # Parse each page
            loan_summary = self._parse_page1()
            if loan_summary:
                result.loan_summary = loan_summary
            
            page2_items = self._parse_page2()
            if page2_items:
                result.line_items.extend(page2_items)
            
            page3_items = self._parse_page3()
            if page3_items:
                result.line_items.extend(page3_items)
            
            page4_items = self._parse_page4()
            if page4_items:
                result.line_items.extend(page4_items)
            
            # Set success status
            result.parsing_success = not self.has_errors()
            result.parsing_errors = self.errors.copy()
            
        except Exception as e:
            result.parsing_success = False
            result.add_parsing_error(f"Unexpected parsing error: {e}")
        
        return result
    
    def _validate_trid_structure(self) -> bool:
        """Validate that this is a TRID Closing Disclosure."""
        try:
            # Check minimum page count
            if self.get_page_count() < 3:
                self.add_error("TRID documents require at least 3 pages")
                return False
            
            # Check for key identifiers on page 1
            page1 = self.get_page(1)
            if not page1:
                return False
            
            page1_text = page1.extract_text() or ""
            
            # Look for TRID-specific text
            trid_indicators = [
                "Closing Disclosure",
                "Loan Terms",
                "Closing Costs", 
                "Cash to Close"
            ]
            
            found_indicators = sum(1 for indicator in trid_indicators if indicator in page1_text)
            
            if found_indicators < 2:
                self.add_error("Document does not contain expected TRID indicators")
                return False
            
            return True
            
        except Exception as e:
            self.add_error(f"Error validating TRID structure: {e}")
            return False
    
    def _parse_page1(self) -> Optional[LoanSummary]:
        """Parse page 1 - loan summary information."""
        try:
            page1 = self.get_page(1)
            if not page1:
                return None
            
            # Use dedicated Page1Parser
            from .page1_parser import Page1Parser
            parser = Page1Parser(page1)
            return parser.parse()
            
        except Exception as e:
            self.add_error(f"Error parsing page 1: {e}")
            return None
    
    def _parse_page2(self) -> list:
        """Parse page 2 - closing costs sections."""
        try:
            page2 = self.get_page(2)
            if not page2:
                return []
            
            # Use dedicated Page2Parser
            from .page2_parser import Page2Parser
            parser = Page2Parser(page2)
            return parser.parse()
            
        except Exception as e:
            self.add_error(f"Error parsing page 2: {e}")
            return []
    
    def _parse_page3(self) -> list:
        """Parse page 3 - transaction sections.""" 
        try:
            page3 = self.get_page(3)
            if not page3:
                return []
            
            # Use dedicated Page3Parser
            from .page3_parser import Page3Parser
            parser = Page3Parser(page3)
            return parser.parse()
            
        except Exception as e:
            self.add_error(f"Error parsing page 3: {e}")
            return []
    
    def _parse_page4(self) -> list:
        """Parse page 4 - loan disclosures and escrow information."""
        try:
            page4 = self.get_page(4)
            if not page4:
                return []
            
            # Use dedicated Page4Parser
            from .page4_parser import Page4Parser
            parser = Page4Parser(page4)
            return parser.parse()
            
        except Exception as e:
            self.add_error(f"Error parsing page 4: {e}")
            return []
    
    def get_document_metadata(self) -> dict:
        """Get metadata about the parsed document."""
        return {
            'document_type': self.document_type,
            'page_count': self.get_page_count(),
            'has_errors': self.has_errors(),
            'error_count': len(self.errors)
        }