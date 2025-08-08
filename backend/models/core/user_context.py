"""User context data model for enhanced analysis."""

from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class UserContext:
    """User-provided context for enhanced document analysis."""
    
    # Basic loan expectations
    expected_loan_type: Optional[Literal['FHA', 'Conventional', 'VA', 'USDA', 'Not sure']] = None
    expected_interest_rate: Optional[float] = None
    expected_closing_costs: Optional[float] = None
    
    # Purchase details
    expected_purchase_price: Optional[float] = None
    expected_loan_amount: Optional[float] = None
    
    # Promises made by builder/lender
    promised_zero_closing_costs: bool = False
    promised_lender_credit: Optional[float] = None
    promised_seller_credit: Optional[float] = None
    promised_rebate: Optional[float] = None
    
    # Builder/lender relationships
    used_builders_preferred_lender: bool = False
    builder_name: Optional[str] = None
    
    # Specific promises about fees
    builder_promised_to_cover_title_fees: bool = False
    builder_promised_to_cover_escrow_fees: bool = False
    builder_promised_to_cover_inspection: bool = False
    
    # Representation and services
    has_buyer_agent_representation: bool = True
    buyer_agent_name: Optional[str] = None
    title_company_chosen_by: Optional[Literal['buyer', 'seller', 'builder', 'lender']] = None
    
    # Additional context
    first_time_home_buyer: bool = False
    cash_purchase: bool = False
    investment_property: bool = False
    
    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            'expected_loan_type': self.expected_loan_type,
            'expected_interest_rate': self.expected_interest_rate,
            'expected_closing_costs': self.expected_closing_costs,
            'expected_purchase_price': self.expected_purchase_price,
            'expected_loan_amount': self.expected_loan_amount,
            'promised_zero_closing_costs': self.promised_zero_closing_costs,
            'promised_lender_credit': self.promised_lender_credit,
            'promised_seller_credit': self.promised_seller_credit,
            'promised_rebate': self.promised_rebate,
            'used_builders_preferred_lender': self.used_builders_preferred_lender,
            'builder_name': self.builder_name,
            'builder_promised_to_cover_title_fees': self.builder_promised_to_cover_title_fees,
            'builder_promised_to_cover_escrow_fees': self.builder_promised_to_cover_escrow_fees,
            'builder_promised_to_cover_inspection': self.builder_promised_to_cover_inspection,
            'has_buyer_agent_representation': self.has_buyer_agent_representation,
            'buyer_agent_name': self.buyer_agent_name,
            'title_company_chosen_by': self.title_company_chosen_by,
            'first_time_home_buyer': self.first_time_home_buyer,
            'cash_purchase': self.cash_purchase,
            'investment_property': self.investment_property
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserContext':
        """Create UserContext from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})