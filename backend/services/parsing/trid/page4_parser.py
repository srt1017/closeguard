"""Page 4 parser for TRID loan disclosures and escrow account information."""

import re
from typing import List, Optional, Dict, Any
from ..core import CoordinateExtractor, TextUtils, CheckboxDetector
from models.document import (
    ClosingDisclosureLineItem, 
    DocumentSection, 
    PaymentResponsibility, 
    CostCategory,
    CoordinatePosition
)


class Page4Parser:
    """Parser for TRID Closing Disclosure Page 4 - Loan Disclosures & Escrow."""
    
    def __init__(self, page):
        """Initialize with pdfplumber page object."""
        self.page = page
        self.coordinate_extractor = CoordinateExtractor(page)
        self.checkbox_detector = CheckboxDetector(page)
        self.page_text = page.extract_text() or ""
    
    def parse(self) -> List[ClosingDisclosureLineItem]:
        """Parse page 4 and extract loan disclosures and escrow information."""
        try:
            line_items = []
            
            # Parse loan disclosures with checkboxes
            disclosure_items = self._parse_loan_disclosures()
            line_items.extend(disclosure_items)
            
            # Parse escrow account information
            escrow_items = self._parse_escrow_information()
            line_items.extend(escrow_items)
            
            # Parse other loan features
            feature_items = self._parse_loan_features()
            line_items.extend(feature_items)
            
            return line_items
            
        except Exception as e:
            return []
    
    def _parse_loan_disclosures(self) -> List[ClosingDisclosureLineItem]:
        """Parse loan disclosure checkboxes and features."""
        items = []
        
        try:
            lines = self.page_text.split('\n')
            
            # Assumption disclosure
            assumption_status = self._detect_assumption_feature(lines)
            if assumption_status:
                item = ClosingDisclosureLineItem(
                    line_number="DISC.01",
                    page_number=4,
                    section=DocumentSection.LOAN_SUMMARY,
                    description=f"Loan Assumption: {assumption_status['status']}",
                    amount=None,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.LOAN_COSTS,
                    is_optional=False,
                    raw_text=assumption_status['raw_text'],
                    payment_notes=assumption_status['explanation']
                )
                items.append(item)
            
            # Demand feature disclosure
            demand_status = self._detect_demand_feature(lines)
            if demand_status:
                item = ClosingDisclosureLineItem(
                    line_number="DISC.02",
                    page_number=4,
                    section=DocumentSection.LOAN_SUMMARY,
                    description=f"Demand Feature: {demand_status['status']}",
                    amount=None,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.LOAN_COSTS,
                    is_optional=False,
                    raw_text=demand_status['raw_text'],
                    payment_notes=demand_status['explanation']
                )
                items.append(item)
            
            # Late payment terms
            late_payment = self._parse_late_payment_terms(lines)
            if late_payment:
                item = ClosingDisclosureLineItem(
                    line_number="DISC.03",
                    page_number=4,
                    section=DocumentSection.LOAN_SUMMARY,
                    description="Late Payment Fee",
                    amount=None,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.LOAN_COSTS,
                    is_optional=False,
                    raw_text=late_payment['raw_text'],
                    payment_notes=late_payment['terms']
                )
                items.append(item)
            
            return items
            
        except Exception:
            return []
    
    def _parse_escrow_information(self) -> List[ClosingDisclosureLineItem]:
        """Parse escrow account details - crucial for first-time homebuyers."""
        items = []
        
        try:
            # Parse escrowed property costs
            escrowed_costs = self._extract_escrowed_costs()
            if escrowed_costs:
                item = ClosingDisclosureLineItem(
                    line_number="ESC.01",
                    page_number=4,
                    section=DocumentSection.INITIAL_ESCROW,
                    description="Escrowed Property Costs (Annual)",
                    amount=escrowed_costs['amount'],
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.OTHER_COSTS,
                    is_optional=False,
                    raw_text=escrowed_costs['raw_text'],
                    payment_notes=f"Includes: {escrowed_costs['includes']}. Paid monthly through escrow account."
                )
                items.append(item)
            
            # Parse non-escrowed costs
            non_escrowed_costs = self._extract_non_escrowed_costs()
            if non_escrowed_costs:
                item = ClosingDisclosureLineItem(
                    line_number="ESC.02",
                    page_number=4,
                    section=DocumentSection.OTHER,
                    description="Non-Escrowed Property Costs (Annual)",
                    amount=non_escrowed_costs['amount'],
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.OTHER_COSTS,
                    is_optional=False,
                    raw_text=non_escrowed_costs['raw_text'],
                    payment_notes=f"Includes: {non_escrowed_costs['includes']}. You pay directly (not through lender)."
                )
                items.append(item)
            
            # Parse initial escrow payment
            initial_escrow = self._extract_initial_escrow_payment()
            if initial_escrow:
                item = ClosingDisclosureLineItem(
                    line_number="ESC.03",
                    page_number=4,
                    section=DocumentSection.INITIAL_ESCROW,
                    description="Initial Escrow Payment (Cushion)",
                    amount=initial_escrow['amount'],
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.OTHER_COSTS,
                    is_optional=False,
                    raw_text=initial_escrow['raw_text'],
                    payment_notes="Paid at closing to start your escrow account. See Section G on Page 2."
                )
                items.append(item)
            
            # Parse monthly escrow payment
            monthly_escrow = self._extract_monthly_escrow_payment()
            if monthly_escrow:
                item = ClosingDisclosureLineItem(
                    line_number="ESC.04",
                    page_number=4,
                    section=DocumentSection.INITIAL_ESCROW,
                    description="Monthly Escrow Payment",
                    amount=monthly_escrow['amount'],
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.OTHER_COSTS,
                    is_optional=False,
                    raw_text=monthly_escrow['raw_text'],
                    payment_notes="Included in your total monthly mortgage payment to cover property taxes and insurance."
                )
                items.append(item)
            
            return items
            
        except Exception:
            return []
    
    def _parse_loan_features(self) -> List[ClosingDisclosureLineItem]:
        """Parse other important loan features."""
        items = []
        
        try:
            # Negative amortization check
            neg_am = self._detect_negative_amortization()
            if neg_am:
                item = ClosingDisclosureLineItem(
                    line_number="FEAT.01",
                    page_number=4,
                    section=DocumentSection.LOAN_SUMMARY,
                    description=f"Negative Amortization: {neg_am['status']}",
                    amount=None,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.LOAN_COSTS,
                    is_optional=False,
                    raw_text=neg_am['raw_text'],
                    payment_notes=neg_am['explanation']
                )
                items.append(item)
            
            # Partial payments policy
            partial_payments = self._detect_partial_payments_policy()
            if partial_payments:
                item = ClosingDisclosureLineItem(
                    line_number="FEAT.02",
                    page_number=4,
                    section=DocumentSection.LOAN_SUMMARY,
                    description=f"Partial Payments: {partial_payments['status']}",
                    amount=None,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.LOAN_COSTS,
                    is_optional=False,
                    raw_text=partial_payments['raw_text'],
                    payment_notes=partial_payments['explanation']
                )
                items.append(item)
            
            return items
            
        except Exception:
            return []
    
    def _detect_assumption_feature(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Detect loan assumption checkbox status."""
        for line in lines:
            if 'assumption' in line.lower() and ('will allow' in line or 'will not allow' in line):
                if 'will allow' in line:
                    status = "Allowed under certain conditions"
                    explanation = "Your loan can be assumed by a buyer under certain conditions."
                else:
                    status = "Not allowed"
                    explanation = "Your loan cannot be assumed by a buyer on the original terms."
                
                return {
                    'status': status,
                    'explanation': explanation,
                    'raw_text': line.strip()
                }
        return None
    
    def _detect_demand_feature(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Detect demand feature checkbox status."""
        for line in lines:
            if 'demand feature' in line.lower():
                if 'has a demand feature' in line:
                    status = "Yes"
                    explanation = "Lender can require early repayment of the loan. Review your note for details."
                else:
                    status = "No"
                    explanation = "Lender cannot require early repayment."
                
                return {
                    'status': status,
                    'explanation': explanation,
                    'raw_text': line.strip()
                }
        return None
    
    def _parse_late_payment_terms(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Parse late payment fee terms."""
        for line in lines:
            if 'late' in line.lower() and ('fee' in line.lower() or 'charge' in line.lower()):
                # Look for percentage and days
                percentage_match = re.search(r'(\d+)%', line)
                days_match = re.search(r'(\d+)\s+days?', line)
                
                if percentage_match and days_match:
                    percentage = percentage_match.group(1)
                    days = days_match.group(1)
                    terms = f"{percentage}% of overdue payment if more than {days} days late"
                    
                    return {
                        'terms': terms,
                        'raw_text': line.strip()
                    }
        return None
    
    def _extract_escrowed_costs(self) -> Optional[Dict[str, Any]]:
        """Extract escrowed property costs amount and details."""
        pattern = r'Escrowed\s+\$([0-9,]+\.?\d*)\s+.*?year\s+1.*?escrowed.*?costs'
        match = re.search(pattern, self.page_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            amount = TextUtils.extract_amount(match.group(1))
            
            # Look for what's included (Hazard Insurance, Property Taxes, etc.)
            includes = []
            if 'hazard insurance' in self.page_text.lower():
                includes.append('Hazard Insurance')
            if 'property tax' in self.page_text.lower():
                includes.append('Property Taxes')
            if 'mortgage insurance' in self.page_text.lower():
                includes.append('Mortgage Insurance')
            
            return {
                'amount': amount,
                'includes': ', '.join(includes) if includes else 'Property taxes and insurance',
                'raw_text': match.group(0)
            }
        return None
    
    def _extract_non_escrowed_costs(self) -> Optional[Dict[str, Any]]:
        """Extract non-escrowed property costs."""
        pattern = r'Non-Escrowed\s+\$([0-9,]+\.?\d*)\s+.*?year\s+1.*?non-escrowed.*?costs'
        match = re.search(pattern, self.page_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            amount = TextUtils.extract_amount(match.group(1))
            
            # Look for what's included
            includes = []
            if 'homeowner association' in self.page_text.lower() or 'hoa' in self.page_text.lower():
                includes.append('HOA Dues')
            if 'association dues' in self.page_text.lower():
                includes.append('Association Dues')
            
            return {
                'amount': amount,
                'includes': ', '.join(includes) if includes else 'Other property costs',
                'raw_text': match.group(0)
            }
        return None
    
    def _extract_initial_escrow_payment(self) -> Optional[Dict[str, Any]]:
        """Extract initial escrow payment amount."""
        pattern = r'Initial Escrow\s+\$([0-9,]+\.?\d*)'
        match = re.search(pattern, self.page_text, re.IGNORECASE)
        
        if match:
            amount = TextUtils.extract_amount(match.group(1))
            # Find the full context
            for line in self.page_text.split('\n'):
                if 'Initial Escrow' in line and str(amount).replace(',', '') in line:
                    return {
                        'amount': amount,
                        'raw_text': line.strip()
                    }
        return None
    
    def _extract_monthly_escrow_payment(self) -> Optional[Dict[str, Any]]:
        """Extract monthly escrow payment amount."""
        pattern = r'Monthly Escrow\s+\$([0-9,]+\.?\d*)'
        match = re.search(pattern, self.page_text, re.IGNORECASE)
        
        if match:
            amount = TextUtils.extract_amount(match.group(1))
            # Find the full context
            for line in self.page_text.split('\n'):
                if 'Monthly Escrow' in line and str(amount).replace(',', '') in line:
                    return {
                        'amount': amount,
                        'raw_text': line.strip()
                    }
        return None
    
    def _detect_negative_amortization(self) -> Optional[Dict[str, Any]]:
        """Detect negative amortization feature."""
        for line in self.page_text.split('\n'):
            if 'negative amortization' in line.lower():
                if 'do not have' in line.lower():
                    status = "No"
                    explanation = "Your payments will reduce the loan balance each month."
                else:
                    status = "Yes" 
                    explanation = "Your loan balance may increase if payments don't cover all interest due."
                
                return {
                    'status': status,
                    'explanation': explanation,
                    'raw_text': line.strip()
                }
        return None
    
    def _detect_partial_payments_policy(self) -> Optional[Dict[str, Any]]:
        """Detect partial payments policy."""
        for line in self.page_text.split('\n'):
            if 'partial payment' in line.lower():
                if 'does not accept' in line.lower():
                    status = "Not accepted"
                    explanation = "Lender does not accept payments less than the full amount due."
                elif 'may accept' in line.lower():
                    status = "May be accepted"
                    explanation = "Lender may accept partial payments under certain conditions."
                elif 'may hold' in line.lower():
                    status = "Held until complete"
                    explanation = "Lender may hold partial payments until full payment is received."
                else:
                    continue
                
                return {
                    'status': status,
                    'explanation': explanation,
                    'raw_text': line.strip()
                }
        return None