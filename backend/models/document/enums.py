"""Enums for document parsing and classification."""

from enum import Enum


class PaymentResponsibility(Enum):
    """Who is responsible for paying a specific cost."""
    BORROWER = "borrower"
    SELLER = "seller"
    OTHERS = "others"


class CostCategory(Enum):
    """Categories of costs in closing disclosure."""
    LOAN_COSTS = "loan_costs"
    OTHER_COSTS = "other_costs" 
    ADJUSTMENT = "adjustment"


class DocumentSection(Enum):
    """Standard TRID closing disclosure sections."""
    # Page 1
    LOAN_SUMMARY = "loan_summary"
    
    # Page 2 - Loan Costs
    ORIGINATION_CHARGES = "origination_charges"  # A
    SERVICES_NOT_SHOPPED = "services_not_shopped"  # B
    SERVICES_SHOPPED = "services_shopped"  # C
    
    # Page 2 - Other Costs
    TAXES_GOVERNMENT_FEES = "taxes_government_fees"  # E
    PREPAIDS = "prepaids"  # F
    INITIAL_ESCROW = "initial_escrow"  # G
    OTHER = "other"  # H
    
    # Page 3 - Transactions
    BORROWER_TRANSACTION = "borrower_transaction"  # K
    SELLER_TRANSACTION = "seller_transaction"  # L
    
    @classmethod
    def get_section_letter(cls, section: 'DocumentSection') -> str:
        """Get the letter identifier for a section (A, B, C, etc.)."""
        section_map = {
            cls.ORIGINATION_CHARGES: "A",
            cls.SERVICES_NOT_SHOPPED: "B", 
            cls.SERVICES_SHOPPED: "C",
            cls.TAXES_GOVERNMENT_FEES: "E",
            cls.PREPAIDS: "F",
            cls.INITIAL_ESCROW: "G",
            cls.OTHER: "H",
            cls.BORROWER_TRANSACTION: "K",
            cls.SELLER_TRANSACTION: "L"
        }
        return section_map.get(section, "")