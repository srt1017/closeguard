"""Line item model for TRID closing disclosure entries."""

from dataclasses import dataclass
from typing import Optional, Dict, Any

from .enums import PaymentResponsibility, CostCategory, DocumentSection
from .coordinates import CoordinatePosition


@dataclass 
class ClosingDisclosureLineItem:
    """Represents a single line item from TRID closing disclosure."""
    
    # Core identification
    line_number: str  # e.g., "B.01", "A.02"
    page_number: int
    section: DocumentSection
    
    # Item details
    description: str
    vendor: Optional[str] = None
    amount: Optional[float] = None
    paid_by: PaymentResponsibility = PaymentResponsibility.BORROWER
    category: CostCategory = CostCategory.LOAN_COSTS
    is_optional: bool = False
    
    # For highlighting in UI
    coordinates: Optional[CoordinatePosition] = None
    
    # Raw text for debugging
    raw_text: Optional[str] = None
    
    # Payment clarity notes
    payment_notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "lineNumber": self.line_number,
            "pageNumber": self.page_number,
            "section": self.section.value,
            "description": self.description,
            "vendor": self.vendor,
            "amount": self.amount,
            "paidBy": self.paid_by.value,
            "category": self.category.value,
            "isOptional": self.is_optional,
            "coordinates": self.coordinates.to_dict() if self.coordinates else None,
            "rawText": self.raw_text,
            "paymentNotes": self.payment_notes
        }
    
    def is_borrower_paid(self) -> bool:
        """Check if this item is paid by borrower."""
        return self.paid_by == PaymentResponsibility.BORROWER
    
    def is_seller_paid(self) -> bool:
        """Check if this item is paid by seller."""
        return self.paid_by == PaymentResponsibility.SELLER
    
    def has_amount(self) -> bool:
        """Check if this item has a valid amount."""
        return self.amount is not None and self.amount > 0