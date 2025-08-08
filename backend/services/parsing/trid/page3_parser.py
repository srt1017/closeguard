"""Page 3 parser for TRID transaction sections K and L."""

import re
from typing import List, Optional, Dict
from ..core import CoordinateExtractor, TextUtils
from models.document import (
    ClosingDisclosureLineItem, 
    DocumentSection, 
    PaymentResponsibility, 
    CostCategory,
    CoordinatePosition
)


class Page3Parser:
    """Parser for TRID Closing Disclosure Page 3 - Transaction Summaries."""
    
    def __init__(self, page):
        """Initialize with pdfplumber page object."""
        self.page = page
        self.coordinate_extractor = CoordinateExtractor(page)
        self.page_text = page.extract_text() or ""
    
    def parse(self) -> List[ClosingDisclosureLineItem]:
        """Parse page 3 and extract transaction line items."""
        try:
            line_items = []
            
            # Parse "Calculating Cash to Close" section with checkboxes
            cash_to_close_items = self._parse_cash_to_close_section()
            line_items.extend(cash_to_close_items)
            
            # Parse transaction sections from text
            transaction_items = self._parse_transaction_sections_from_text()
            line_items.extend(transaction_items)
            
            return line_items
            
        except Exception as e:
            return []
    
    def _parse_cash_to_close_section(self) -> List[ClosingDisclosureLineItem]:
        """Parse the 'Calculating Cash to Close' section with YES/NO checkboxes."""
        items = []
        
        try:
            from ..core.checkbox_detector import CheckboxDetector
            
            # Look for lines with YES/NO indicators
            lines = self.page_text.split('\n')
            
            for i, line in enumerate(lines):
                if 'YES•' in line or 'NO' in line:
                    # Extract the main description and amounts
                    # Example: "Total Closing Costs (J) $28,088.00 $18,215.96 YES• See Total Loan Costs (D)"
                    
                    # Parse the line for description and amounts
                    match = re.match(r'^([^$]+?)\s*\$([0-9,]+\.?\d*)\s*\$([0-9,]+\.?\d*)\s*(YES•?|NO)', line.strip())
                    if match:
                        description = match.group(1).strip()
                        estimate_amount = TextUtils.extract_amount(match.group(2))
                        final_amount = TextUtils.extract_amount(match.group(3))
                        change_indicator = match.group(4)
                        
                        has_changed = 'YES' in change_indicator
                        
                        item = ClosingDisclosureLineItem(
                            line_number=f"CASH.{len(items)+1:02d}",
                            page_number=3,
                            section=DocumentSection.BORROWER_TRANSACTION,
                            description=f"{description} (Changed: {'Yes' if has_changed else 'No'})",
                            amount=final_amount,
                            paid_by=PaymentResponsibility.BORROWER,
                            category=CostCategory.ADJUSTMENT,
                            is_optional=False,
                            coordinates=self._find_line_coordinates(line, i),
                            raw_text=line.strip(),
                            payment_notes=f"Loan Estimate: ${estimate_amount:,.2f}, Final: ${final_amount:,.2f}, Changed: {'Yes' if has_changed else 'No'}"
                        )
                        items.append(item)
                        
            return items
            
        except Exception:
            return []
    
    def _parse_transaction_sections_from_text(self) -> List[ClosingDisclosureLineItem]:
        """Parse transaction sections K, L, M, N from text."""
        items = []
        
        try:
            lines = [line.strip() for line in self.page_text.split('\n') if line.strip()]
            
            current_section = None
            line_counter = 1
            
            for i, line in enumerate(lines):
                # Check if this is a section header
                section_match = self._parse_transaction_section_header(line)
                if section_match:
                    current_section = section_match['letter']
                    line_counter = 1
                    
                    # Add section header as an item if it has an amount
                    if section_match.get('amount'):
                        section_enum = self._get_transaction_section_enum(current_section)
                        payment_responsibility = self._get_section_payment_responsibility(current_section)
                        
                        item = ClosingDisclosureLineItem(
                            line_number=f"{current_section}.00",
                            page_number=3,
                            section=section_enum,
                            description=section_match['description'],
                            amount=section_match['amount'],
                            paid_by=payment_responsibility,
                            category=CostCategory.ADJUSTMENT,
                            coordinates=self._find_line_coordinates(line, i),
                            raw_text=line
                        )
                        items.append(item)
                    continue
                
                # Parse line items within current section
                if current_section:
                    item = self._parse_transaction_line_item(line, current_section, line_counter, i)
                    if item:
                        items.append(item)
                        line_counter += 1
            
            return items
            
        except Exception:
            return []
    
    def _parse_transaction_section_header(self, line: str) -> Optional[Dict]:
        """Parse transaction section headers (K, L, M, N)."""
        # Pattern for section headers like "K. Due from Borrower at Closing $422,115.96"
        pattern = r'^([KLMN])\.\s+(.+?)(?:\s+\$([0-9,]+\.?\d*))?$'
        match = re.match(pattern, line)
        
        if match:
            letter = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3)
            amount = TextUtils.extract_amount(amount_str) if amount_str else None
            
            return {
                'letter': letter,
                'description': description,
                'amount': amount
            }
        
        return None
    
    def _parse_transaction_line_item(self, line: str, section_letter: str, line_number: int, line_index: int) -> Optional[ClosingDisclosureLineItem]:
        """Parse individual transaction line item."""
        try:
            # Skip page footer/header lines
            if 'CLOSING DISCLOSURE' in line.upper() or 'LOAN ID #' in line.upper():
                return None
            
            # Pattern for line items like "01Sale Price of Property $403,900.00"
            # More refined to handle the dual-column format
            item_pattern = r'^(\d{2})([^$]+?)\s*\$([0-9,]+\.?\d*)(?:\s+\d{2}.*)?$'
            match = re.match(item_pattern, line)
            
            if not match:
                return None
            
            item_num = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3)
            
            # Clean up description - remove duplicated text
            # Handle cases like "Sale Price of Property $403,900.00 01Sale Price of Property"
            words = description.split()
            if len(words) > 3:
                # Look for repeated patterns and take the first occurrence
                mid_point = len(words) // 2
                first_half = ' '.join(words[:mid_point])
                second_half = ' '.join(words[mid_point:])
                
                # If similar, use first half
                if first_half.lower() in second_half.lower() or len(set(first_half.split()) & set(second_half.split())) > 2:
                    description = first_half
            
            # Skip empty or meaningless descriptions
            if not description or len(description) < 3 or description.isdigit():
                return None
            
            # Skip very large amounts that are likely parsing errors
            amount = TextUtils.extract_amount(amount_str)
            if not amount or amount > 500000000:  # Skip amounts > $500M (parsing errors)
                return None
            
            # Get section and payment responsibility
            section_enum = self._get_transaction_section_enum(section_letter)
            payment_responsibility = self._get_section_payment_responsibility(section_letter)
            
            # Clean description further
            clean_description = TextUtils.clean_description(description)
            vendor = TextUtils.extract_vendor(description)
            
            return ClosingDisclosureLineItem(
                line_number=f"{section_letter}.{item_num}",
                page_number=3,
                section=section_enum,
                description=clean_description,
                vendor=vendor,
                amount=amount,
                paid_by=payment_responsibility,
                category=CostCategory.ADJUSTMENT,
                coordinates=self._find_line_coordinates(line, line_index),
                raw_text=line
            )
            
        except Exception:
            return None
    
    def _get_transaction_section_enum(self, section_letter: str) -> DocumentSection:
        """Get DocumentSection enum for transaction section letter."""
        section_map = {
            'K': DocumentSection.BORROWER_TRANSACTION,
            'L': DocumentSection.BORROWER_TRANSACTION,  # Paid by borrower
            'M': DocumentSection.SELLER_TRANSACTION,
            'N': DocumentSection.SELLER_TRANSACTION
        }
        return section_map.get(section_letter, DocumentSection.BORROWER_TRANSACTION)
    
    def _get_section_payment_responsibility(self, section_letter: str) -> PaymentResponsibility:
        """Get payment responsibility based on section."""
        responsibility_map = {
            'K': PaymentResponsibility.BORROWER,  # Due from borrower
            'L': PaymentResponsibility.BORROWER,  # Paid by borrower
            'M': PaymentResponsibility.SELLER,    # Due to seller
            'N': PaymentResponsibility.SELLER     # Due from seller
        }
        return responsibility_map.get(section_letter, PaymentResponsibility.BORROWER)
    
    def _find_line_coordinates(self, line: str, line_index: int) -> Optional[CoordinatePosition]:
        """Find coordinates for a text line."""
        try:
            search_text = line[:30]  # First 30 characters
            coords = self.coordinate_extractor.find_text_coordinates(search_text)
            return coords[0] if coords else None
        except Exception:
            return None
    
    def _parse_borrower_transaction(self) -> List[ClosingDisclosureLineItem]:
        """Parse Section K - Due from Borrower at Closing."""
        items = []
        
        try:
            # Find Section K in text
            section_pattern = r'K\.\s*Due from Borrower at Closing'
            section_match = re.search(section_pattern, self.page_text, re.IGNORECASE)
            
            if not section_match:
                return []
            
            # Extract the section text
            section_text = self._extract_section_text('K', section_match.start())
            if not section_text:
                return []
            
            # Parse common borrower transaction items
            line_number = 1
            
            # Sale Price of Property
            sale_price = self._extract_transaction_amount(section_text, [
                r'Sale Price of Property\s*\$?([0-9,]+\.?\d*)',
                r'01\s*Sale Price.*?\$?([0-9,]+\.?\d*)'
            ])
            if sale_price:
                item = ClosingDisclosureLineItem(
                    line_number=f"K.{line_number:02d}",
                    page_number=3,
                    section=DocumentSection.BORROWER_TRANSACTION,
                    description="Sale Price of Property",
                    amount=sale_price,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(sale_price),
                    raw_text=f"Sale Price: ${sale_price:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            # Closing Costs Paid at Closing
            closing_costs = self._extract_transaction_amount(section_text, [
                r'Closing Costs Paid at Closing.*?\$?([0-9,]+\.?\d*)',
                r'03\s*Closing Costs.*?\$?([0-9,]+\.?\d*)'
            ])
            if closing_costs:
                item = ClosingDisclosureLineItem(
                    line_number=f"K.{line_number:02d}",
                    page_number=3,
                    section=DocumentSection.BORROWER_TRANSACTION,
                    description="Closing Costs Paid at Closing",
                    amount=closing_costs,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(closing_costs),
                    raw_text=f"Closing Costs: ${closing_costs:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            # Parse other borrower transaction items
            other_items = self._parse_transaction_items(section_text, 'K', line_number, PaymentResponsibility.BORROWER)
            items.extend(other_items)
            
            return items
            
        except Exception:
            return []
    
    def _parse_seller_transaction(self) -> List[ClosingDisclosureLineItem]:
        """Parse Section L - Due to/from Seller at Closing.""" 
        items = []
        
        try:
            # Find Section L in text
            section_pattern = r'L\.\s*Paid Already by.*?Borrower'
            section_match = re.search(section_pattern, self.page_text, re.IGNORECASE)
            
            if not section_match:
                # Try alternative pattern
                section_pattern = r'L\.\s*'
                section_match = re.search(section_pattern, self.page_text, re.IGNORECASE)
            
            if not section_match:
                return []
            
            # Extract the section text
            section_text = self._extract_section_text('L', section_match.start())
            if not section_text:
                return []
            
            line_number = 1
            
            # Parse common seller transaction items
            # Deposit
            deposit = self._extract_transaction_amount(section_text, [
                r'Deposit\s*\$?([0-9,]+\.?\d*)',
                r'01\s*Deposit.*?\$?([0-9,]+\.?\d*)'
            ])
            if deposit:
                item = ClosingDisclosureLineItem(
                    line_number=f"L.{line_number:02d}",
                    page_number=3,
                    section=DocumentSection.SELLER_TRANSACTION,
                    description="Deposit",
                    amount=deposit,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(deposit),
                    raw_text=f"Deposit: ${deposit:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            # Loan Amount
            loan_amount = self._extract_transaction_amount(section_text, [
                r'Loan Amount\s*\$?([0-9,]+\.?\d*)',
                r'02\s*Loan Amount.*?\$?([0-9,]+\.?\d*)'
            ])
            if loan_amount:
                item = ClosingDisclosureLineItem(
                    line_number=f"L.{line_number:02d}",
                    page_number=3,
                    section=DocumentSection.SELLER_TRANSACTION,
                    description="Loan Amount",
                    amount=loan_amount,
                    paid_by=PaymentResponsibility.BORROWER,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(loan_amount),
                    raw_text=f"Loan Amount: ${loan_amount:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            # Seller Credit
            seller_credit = self._extract_transaction_amount(section_text, [
                r'Seller Credit\s*\$?([0-9,]+\.?\d*)',
                r'05\s*Seller Credit.*?\$?([0-9,]+\.?\d*)'
            ])
            if seller_credit:
                item = ClosingDisclosureLineItem(
                    line_number=f"L.{line_number:02d}",
                    page_number=3,
                    section=DocumentSection.SELLER_TRANSACTION,
                    description="Seller Credit",
                    amount=seller_credit,
                    paid_by=PaymentResponsibility.SELLER,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(seller_credit),
                    raw_text=f"Seller Credit: ${seller_credit:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            return items
            
        except Exception:
            return []
    
    def _extract_section_text(self, section_letter: str, start_pos: int) -> Optional[str]:
        """Extract text for a specific section."""
        try:
            # Get text from section start to next section or end
            section_text = self.page_text[start_pos:]
            
            # Find next section or end of meaningful content
            next_section_patterns = [
                r'\n[A-Z]\.',  # Next section
                r'CALCULATION',  # Calculation section
                r'Cash to Close'  # End marker
            ]
            
            end_pos = len(section_text)
            for pattern in next_section_patterns:
                match = re.search(pattern, section_text)
                if match:
                    end_pos = min(end_pos, match.start())
            
            return section_text[:end_pos]
            
        except Exception:
            return None
    
    def _extract_transaction_amount(self, text: str, patterns: List[str]) -> Optional[float]:
        """Extract amount using multiple patterns."""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                amount = TextUtils.extract_amount(match.group(1))
                if amount and amount > 0:
                    return amount
        return None
    
    def _parse_transaction_items(self, section_text: str, section_letter: str, 
                                start_line_number: int, default_payer: PaymentResponsibility) -> List[ClosingDisclosureLineItem]:
        """Parse additional transaction items from section text."""
        items = []
        line_number = start_line_number
        
        try:
            # Look for numbered items (01, 02, 03, etc.)
            item_pattern = r'(\d{2})\s+([^$\n]+?)\s*\$?([0-9,]+\.?\d*)'
            matches = re.finditer(item_pattern, section_text, re.MULTILINE)
            
            for match in matches:
                item_num, description, amount_str = match.groups()
                
                # Skip if already processed
                if int(item_num) <= 3:
                    continue
                
                amount = TextUtils.extract_amount(amount_str)
                if not amount:
                    continue
                
                clean_description = TextUtils.clean_description(description)
                if not clean_description:
                    continue
                
                # Determine section based on letter
                section = DocumentSection.BORROWER_TRANSACTION if section_letter == 'K' else DocumentSection.SELLER_TRANSACTION
                
                item = ClosingDisclosureLineItem(
                    line_number=f"{section_letter}.{line_number:02d}",
                    page_number=3,
                    section=section,
                    description=clean_description,
                    amount=amount,
                    paid_by=default_payer,
                    category=CostCategory.ADJUSTMENT,
                    coordinates=self._find_amount_coordinates(amount),
                    raw_text=f"{item_num} {description} ${amount:,.2f}"
                )
                items.append(item)
                line_number += 1
            
            return items
            
        except Exception:
            return []
    
    def _find_amount_coordinates(self, amount: float) -> Optional[CoordinatePosition]:
        """Find coordinates for an amount on the page."""
        try:
            coords = self.coordinate_extractor.find_amount_coordinates(amount)
            return coords[0] if coords else None
        except Exception:
            return None