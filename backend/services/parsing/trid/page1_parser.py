"""Page 1 parser for TRID loan summary information."""

import re
from typing import Optional, Dict
from ..core import CoordinateExtractor, TextUtils
from models.document import LoanSummary, CoordinatePosition


class Page1Parser:
    """Parser for TRID Closing Disclosure Page 1 - Loan Summary."""
    
    def __init__(self, page):
        """Initialize with pdfplumber page object."""
        self.page = page
        self.coordinate_extractor = CoordinateExtractor(page)
        self.page_text = page.extract_text() or ""
    
    def parse(self) -> Optional[LoanSummary]:
        """Parse page 1 and extract loan summary information."""
        try:
            loan_summary = LoanSummary()
            coordinates = {}
            
            # Extract loan terms
            loan_summary.loan_amount = self._extract_loan_amount(coordinates)
            loan_summary.interest_rate = self._extract_interest_rate(coordinates)
            loan_summary.monthly_payment = self._extract_monthly_payment(coordinates)
            loan_summary.loan_term_years = self._extract_loan_term(coordinates)
            
            # Extract property info
            loan_summary.property_address = self._extract_property_address(coordinates)
            loan_summary.sale_price = self._extract_sale_price(coordinates)
            
            # Extract closing info
            loan_summary.closing_date = self._extract_closing_date(coordinates)
            loan_summary.lender_name = self._extract_lender_name(coordinates)
            
            # Extract cost summary
            loan_summary.total_closing_costs = self._extract_closing_costs(coordinates)
            loan_summary.cash_to_close = self._extract_cash_to_close(coordinates)
            
            # Extract loan features
            loan_summary.loan_type = self._extract_loan_type(coordinates)
            loan_summary.loan_purpose = self._extract_loan_purpose(coordinates)
            
            # Store coordinates for highlighting
            loan_summary.coordinates = coordinates if coordinates else None
            
            return loan_summary
            
        except Exception as e:
            # Return None if parsing fails completely
            return None
    
    def _extract_loan_amount(self, coordinates: Dict) -> Optional[float]:
        """Extract loan amount from page."""
        patterns = [
            r'Loan Amount\s*\$?([0-9,]+\.?\d*)',
            r'Loan Amount\s*([0-9,]+\.?\d*)',
            r'Principal Amount\s*\$?([0-9,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount:
                    # Find coordinates for highlighting
                    coords = self.coordinate_extractor.find_amount_coordinates(amount)
                    if coords:
                        coordinates['loan_amount'] = coords[0]
                    return amount
        
        return None
    
    def _extract_interest_rate(self, coordinates: Dict) -> Optional[float]:
        """Extract interest rate from page."""
        patterns = [
            r'Interest Rate\s*([0-9.]+)\s*%',
            r'Rate\s*([0-9.]+)\s*%',
            r'Interest\s*([0-9.]+)\s*%'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                rate = float(match.group(1))
                # Find coordinates
                coords = self.coordinate_extractor.find_text_coordinates(f"{rate}%")
                if coords:
                    coordinates['interest_rate'] = coords[0]
                return rate
        
        return None
    
    def _extract_monthly_payment(self, coordinates: Dict) -> Optional[float]:
        """Extract monthly principal & interest payment."""
        patterns = [
            r'Monthly Principal & Interest\s*\$?([0-9,]+\.?\d*)',
            r'Monthly Payment\s*\$?([0-9,]+\.?\d*)',
            r'Principal & Interest\s*\$?([0-9,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount:
                    coords = self.coordinate_extractor.find_amount_coordinates(amount)
                    if coords:
                        coordinates['monthly_payment'] = coords[0]
                    return amount
        
        return None
    
    def _extract_loan_term(self, coordinates: Dict) -> Optional[int]:
        """Extract loan term in years."""
        patterns = [
            r'Loan Term\s*(\d+)\s*years?',
            r'Term\s*(\d+)\s*years?',
            r'(\d+)\s*year[s]?\s*term'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                term = int(match.group(1))
                coords = self.coordinate_extractor.find_text_coordinates(f"{term} year")
                if coords:
                    coordinates['loan_term'] = coords[0]
                return term
        
        return None
    
    def _extract_property_address(self, coordinates: Dict) -> Optional[str]:
        """Extract property address."""
        patterns = [
            r'Property\s+([^\n]+?)(?:\n|Lender|$)',
            r'Property Address\s+([^\n]+?)(?:\n|Lender|$)',
            r'Subject Property\s+([^\n]+?)(?:\n|Lender|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE | re.MULTILINE)
            if match:
                address = match.group(1).strip()
                
                # Clean up common artifacts and stop at common following fields
                address = re.sub(r'^[:\-\s]+', '', address)
                address = re.sub(r'[,\s]+$', '', address)
                
                # Stop at known following fields
                stop_words = ['Lender', 'LENDER', 'Loan ID', 'MIC #', 'Settlement Agent']
                for stop_word in stop_words:
                    if stop_word in address:
                        address = address.split(stop_word)[0].strip()
                
                # Additional cleanup - remove trailing state/zip pattern if needed
                # Only apply this if the address seems to have extra trailing content
                # This pattern is too aggressive, so let's be more careful
                if any(word in address.upper() for word in ['SETTLEMENT', 'AGENT', 'FILE']):
                    # Only clean if we detect trailing non-address content
                    address_match = re.match(r'^(.+?)\s+(?:SETTLEMENT|AGENT|FILE)', address, re.IGNORECASE)
                    if address_match:
                        address = address_match.group(1).strip()
                
                if len(address) > 10:  # Basic validation
                    coords = self.coordinate_extractor.find_text_coordinates(address[:20])
                    if coords:
                        coordinates['property_address'] = coords[0]
                    return address
        
        return None
    
    def _extract_sale_price(self, coordinates: Dict) -> Optional[float]:
        """Extract sale price."""
        patterns = [
            r'Sale Price\s*\$?([0-9,]+\.?\d*)',
            r'Purchase Price\s*\$?([0-9,]+\.?\d*)',
            r'Sales Price\s*\$?([0-9,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount:
                    coords = self.coordinate_extractor.find_amount_coordinates(amount)
                    if coords:
                        coordinates['sale_price'] = coords[0]
                    return amount
        
        return None
    
    def _extract_closing_date(self, coordinates: Dict) -> Optional[str]:
        """Extract closing date."""
        patterns = [
            r'Closing Date\s*([0-9/\-]+)',
            r'Settlement Date\s*([0-9/\-]+)',
            r'Closing\s*([0-9/\-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                date = TextUtils.extract_date(match.group(1))
                if date:
                    coords = self.coordinate_extractor.find_text_coordinates(date)
                    if coords:
                        coordinates['closing_date'] = coords[0]
                    return date
        
        return None
    
    def _extract_lender_name(self, coordinates: Dict) -> Optional[str]:
        """Extract lender name."""
        patterns = [
            r'Lender\s+([^\n]+?)(?:\n|Loan ID|$)',
            r'Lender Name\s+([^\n]+?)(?:\n|Loan ID|$)',
            r'Loan Officer\s+([^\n]+?)(?:\n|Loan ID|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE | re.MULTILINE)
            if match:
                lender = match.group(1).strip()
                lender = re.sub(r'^[:\-\s]+', '', lender)
                
                # Stop at known following fields
                stop_patterns = [
                    r'\s+Loan\s+ID\s*#',
                    r'\s+MIC\s*#',
                    r'\s+NMLS\s*#',
                    r'\s+License\s*#'
                ]
                
                for stop_pattern in stop_patterns:
                    if re.search(stop_pattern, lender, re.IGNORECASE):
                        lender = re.split(stop_pattern, lender, flags=re.IGNORECASE)[0].strip()
                
                # Additional cleanup for common lender name patterns
                # Remove trailing punctuation and extra spaces
                lender = re.sub(r'[,\.\s]+$', '', lender)
                
                if len(lender) > 3:
                    coords = self.coordinate_extractor.find_text_coordinates(lender[:15])
                    if coords:
                        coordinates['lender_name'] = coords[0]
                    return lender
        
        return None
    
    def _extract_closing_costs(self, coordinates: Dict) -> Optional[float]:
        """Extract total closing costs."""
        patterns = [
            r'Closing Costs\s*\$?([0-9,]+\.?\d*)',
            r'Total Closing Costs\s*\$?([0-9,]+\.?\d*)',
            r'Total Costs\s*\$?([0-9,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount:
                    coords = self.coordinate_extractor.find_amount_coordinates(amount)
                    if coords:
                        coordinates['closing_costs'] = coords[0]
                    return amount
        
        return None
    
    def _extract_cash_to_close(self, coordinates: Dict) -> Optional[float]:
        """Extract cash to close amount."""
        patterns = [
            r'Cash to Close\s*\$?([0-9,]+\.?\d*)',
            r'Cash Required\s*\$?([0-9,]+\.?\d*)',
            r'Funds Required\s*\$?([0-9,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount:
                    coords = self.coordinate_extractor.find_amount_coordinates(amount)
                    if coords:
                        coordinates['cash_to_close'] = coords[0]
                    return amount
        
        return None
    
    def _extract_loan_type(self, coordinates: Dict) -> Optional[str]:
        """Extract loan type using checkbox detection."""
        try:
            from ..core.checkbox_detector import CheckboxDetector
            
            # Use checkbox detection for loan type
            detector = CheckboxDetector(self.page)
            loan_type_options = ['Conventional', 'FHA', 'VA', 'USDA']
            
            checkbox_results = detector.map_checkboxes_to_text(loan_type_options)
            
            # Find which loan type is selected (checkbox is filled)
            for loan_type, is_selected in checkbox_results.items():
                if is_selected is True:
                    # Get coordinates for the selected loan type
                    coords = self.coordinate_extractor.find_text_coordinates(loan_type, case_sensitive=False)
                    if coords:
                        coordinates['loan_type'] = coords[0]
                    return loan_type
            
            # Fallback to old method if checkbox detection fails
            loan_types = ['Conventional', 'FHA', 'VA', 'USDA', 'Jumbo']
            for loan_type in loan_types:
                if loan_type.lower() in self.page_text.lower():
                    coords = self.coordinate_extractor.find_text_coordinates(loan_type, case_sensitive=False)
                    if coords:
                        coordinates['loan_type'] = coords[0]
                    return loan_type
            
            return None
            
        except Exception as e:
            # Fallback to text-based detection if checkbox detection fails
            loan_types = ['Conventional', 'FHA', 'VA', 'USDA', 'Jumbo']
            for loan_type in loan_types:
                if loan_type.lower() in self.page_text.lower():
                    coords = self.coordinate_extractor.find_text_coordinates(loan_type, case_sensitive=False)
                    if coords:
                        coordinates['loan_type'] = coords[0]
                    return loan_type
            return None
    
    def _extract_loan_purpose(self, coordinates: Dict) -> Optional[str]:
        """Extract loan purpose (Purchase, Refinance, etc.)."""
        patterns = [
            r'Purpose\s+([A-Za-z]+)',
            r'Loan Purpose\s+([A-Za-z]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.page_text, re.IGNORECASE)
            if match:
                purpose = match.group(1).strip()
                coords = self.coordinate_extractor.find_text_coordinates(purpose)
                if coords:
                    coordinates['loan_purpose'] = coords[0]
                return purpose
        
        # Look for common purposes in text
        purposes = ['Purchase', 'Refinance', 'Cash-out', 'Construction']
        for purpose in purposes:
            if purpose.lower() in self.page_text.lower():
                coords = self.coordinate_extractor.find_text_coordinates(purpose, case_sensitive=False)
                if coords:
                    coordinates['loan_purpose'] = coords[0]
                return purpose
        
        return None