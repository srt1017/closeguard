"""Parsed document model representing complete TRID analysis."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from .line_item import ClosingDisclosureLineItem
from .loan_summary import LoanSummary
from .enums import DocumentSection, CostCategory, PaymentResponsibility


@dataclass 
class ParsedDocument:
    """Complete parsed closing disclosure document."""
    
    # Document metadata
    filename: str
    page_count: int
    
    # Parsed content
    loan_summary: Optional[LoanSummary] = None
    line_items: List[ClosingDisclosureLineItem] = None
    
    # Raw text for fallback/debugging
    raw_text: Optional[str] = None
    
    # Parsing metadata
    parsing_success: bool = True
    parsing_errors: List[str] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.line_items is None:
            self.line_items = []
        if self.parsing_errors is None:
            self.parsing_errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "filename": self.filename,
            "pageCount": self.page_count,
            "loanSummary": self.loan_summary.to_dict() if self.loan_summary else None,
            "lineItems": [item.to_dict() for item in self.line_items],
            "rawText": self.raw_text,
            "parsingSuccess": self.parsing_success,
            "parsingErrors": self.parsing_errors
        }
    
    def get_items_by_section(self, section: DocumentSection) -> List[ClosingDisclosureLineItem]:
        """Get all line items from a specific section."""
        return [item for item in self.line_items if item.section == section]
    
    def get_items_by_category(self, category: CostCategory) -> List[ClosingDisclosureLineItem]:
        """Get all line items of a specific category.""" 
        return [item for item in self.line_items if item.category == category]
    
    def get_total_by_payer(self, paid_by: PaymentResponsibility) -> float:
        """Get total amount paid by specific party."""
        return sum(
            item.amount or 0 
            for item in self.line_items 
            if item.paid_by == paid_by and item.amount is not None
        )
    
    def get_borrower_costs(self) -> List[ClosingDisclosureLineItem]:
        """Get all costs paid by borrower."""
        return [item for item in self.line_items if item.is_borrower_paid()]
    
    def get_seller_costs(self) -> List[ClosingDisclosureLineItem]:
        """Get all costs paid by seller.""" 
        return [item for item in self.line_items if item.is_seller_paid()]
    
    def get_total_borrower_costs(self) -> float:
        """Calculate total costs paid by borrower."""
        return self.get_total_by_payer(PaymentResponsibility.BORROWER)
    
    def get_total_seller_costs(self) -> float:
        """Calculate total costs paid by seller."""
        return self.get_total_by_payer(PaymentResponsibility.SELLER)
    
    def has_parsing_errors(self) -> bool:
        """Check if document had parsing errors."""
        return not self.parsing_success or bool(self.parsing_errors)
    
    def add_parsing_error(self, error: str) -> None:
        """Add a parsing error to the document."""
        self.parsing_errors.append(error)
        self.parsing_success = False