"""Loan summary model for page 1 of closing disclosure."""

from dataclasses import dataclass
from typing import Optional, Dict, Any

from .coordinates import CoordinatePosition


@dataclass
class LoanSummary:
    """Summary information from page 1 of closing disclosure."""
    
    # Basic loan info
    loan_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    monthly_payment: Optional[float] = None
    loan_term_years: Optional[int] = None
    
    # Property info
    property_address: Optional[str] = None
    sale_price: Optional[float] = None
    
    # Closing info
    closing_date: Optional[str] = None
    lender_name: Optional[str] = None
    
    # Cost summary
    total_closing_costs: Optional[float] = None
    cash_to_close: Optional[float] = None
    
    # Loan features
    loan_type: Optional[str] = None
    loan_purpose: Optional[str] = None
    
    # Coordinates for highlighting key fields
    coordinates: Optional[Dict[str, CoordinatePosition]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "loanAmount": self.loan_amount,
            "interestRate": self.interest_rate,
            "monthlyPayment": self.monthly_payment,
            "loanTermYears": self.loan_term_years,
            "propertyAddress": self.property_address,
            "salePrice": self.sale_price,
            "closingDate": self.closing_date,
            "lenderName": self.lender_name,
            "totalClosingCosts": self.total_closing_costs,
            "cashToClose": self.cash_to_close,
            "loanType": self.loan_type,
            "loanPurpose": self.loan_purpose,
            "coordinates": {k: v.to_dict() for k, v in self.coordinates.items()} if self.coordinates else None
        }
    
    def get_loan_to_value_ratio(self) -> Optional[float]:
        """Calculate loan-to-value ratio if data available."""
        if self.loan_amount and self.sale_price and self.sale_price > 0:
            return self.loan_amount / self.sale_price
        return None
    
    def has_basic_info(self) -> bool:
        """Check if essential loan info is present."""
        return all([
            self.loan_amount,
            self.interest_rate,
            self.monthly_payment
        ])