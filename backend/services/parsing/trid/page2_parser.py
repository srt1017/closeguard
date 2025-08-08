"""Page 2 parser for TRID closing costs sections A, B, C, E, F, G, H."""

import re
from typing import List, Optional, Dict, Tuple
from ..core import CoordinateExtractor, TextUtils
from models.document import (
    ClosingDisclosureLineItem, 
    DocumentSection, 
    PaymentResponsibility, 
    CostCategory,
    CoordinatePosition
)


class Page2Parser:
    """Parser for TRID Closing Disclosure Page 2 - Closing Costs."""
    
    def __init__(self, page):
        """Initialize with pdfplumber page object."""
        self.page = page
        self.coordinate_extractor = CoordinateExtractor(page)
        self.page_text = page.extract_text() or ""
        
        # Section mappings
        self.section_map = {
            'A': DocumentSection.ORIGINATION_CHARGES,
            'B': DocumentSection.SERVICES_NOT_SHOPPED,  
            'C': DocumentSection.SERVICES_SHOPPED,
            'D': DocumentSection.ORIGINATION_CHARGES,  # Total loan costs (summary)
            'E': DocumentSection.TAXES_GOVERNMENT_FEES,
            'F': DocumentSection.PREPAIDS,
            'G': DocumentSection.INITIAL_ESCROW,
            'H': DocumentSection.OTHER,
            'I': DocumentSection.OTHER,  # Total other costs (summary)
            'J': DocumentSection.OTHER   # Total closing costs (summary)
        }
    
    def parse(self) -> List[ClosingDisclosureLineItem]:
        """Parse page 2 and extract all closing cost line items."""
        try:
            # Parse from text (TRID format is text-based, not table-based)
            return self._parse_from_text()
            
        except Exception as e:
            # Return empty list if parsing fails
            return []
    
    def _extract_table_data(self) -> List[List[str]]:
        """Extract structured table data from page."""
        try:
            # Try multiple table extraction strategies
            strategies = [
                {"vertical_strategy": "lines", "horizontal_strategy": "lines"},
                {"vertical_strategy": "text", "horizontal_strategy": "text"},
                {"vertical_strategy": "explicit", "horizontal_strategy": "explicit"}
            ]
            
            for settings in strategies:
                tables = self.page.extract_tables(table_settings=settings)
                if tables and len(tables[0]) > 5:  # Reasonable table size
                    return tables[0]
            
            # Fallback to default
            tables = self.page.extract_tables()
            return tables[0] if tables else []
            
        except Exception:
            return []
    
    def _parse_section(self, section_letter: str, table_data: List[List[str]]) -> List[ClosingDisclosureLineItem]:
        """Parse a specific section (A, B, C, etc.) from table data."""
        items = []
        
        try:
            section_start_row = self._find_section_start(section_letter, table_data)
            if section_start_row == -1:
                return []
            
            section = self.section_map[section_letter]
            category = CostCategory.LOAN_COSTS if section_letter in ['A', 'B', 'C'] else CostCategory.OTHER_COSTS
            
            # Parse rows until next section or end
            row_index = section_start_row + 1
            line_number = 1
            
            while row_index < len(table_data):
                row = table_data[row_index]
                
                # Check if we've hit the next section
                if self._is_section_header(row):
                    break
                
                # Parse the row
                item = self._parse_table_row(
                    row, 
                    section, 
                    f"{section_letter}.{line_number:02d}",
                    category,
                    row_index
                )
                
                if item and item.description.strip():  # Only add non-empty items
                    items.append(item)
                    line_number += 1
                
                row_index += 1
            
            return items
            
        except Exception:
            return []
    
    def _find_section_start(self, section_letter: str, table_data: List[List[str]]) -> int:
        """Find the row index where a section starts."""
        section_patterns = {
            'A': r'A\.\s*Origination Charges',
            'B': r'B\.\s*Services Borrower Did Not Shop For',
            'C': r'C\.\s*Services Borrower Did Shop For',
            'E': r'E\.\s*Taxes and Other Government Fees',
            'F': r'F\.\s*Prepaids',
            'G': r'G\.\s*Initial Escrow Payment',
            'H': r'H\.\s*Other'
        }
        
        pattern = section_patterns.get(section_letter, f'{section_letter}\\.')
        
        for i, row in enumerate(table_data):
            row_text = ' '.join(cell or '' for cell in row)
            if re.search(pattern, row_text, re.IGNORECASE):
                return i
        
        return -1
    
    def _parse_section_header(self, line: str) -> Optional[Dict]:
        """Parse section header and extract section info."""
        # Pattern for section headers like "A. Origination Charges $3,846.86"
        pattern = r'^([A-H])\. (.+?)(?:\s+\$([\d,]+\.?\d*))?$'
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
    
    def _parse_table_row(self, row: List[str], section: DocumentSection, line_number: str, 
                         category: CostCategory, row_index: int) -> Optional[ClosingDisclosureLineItem]:
        """Parse a single table row into a line item."""
        try:
            if not row or len(row) < 2:
                return None
            
            # Clean row data
            clean_row = [cell.strip() if cell else '' for cell in row]
            
            # Extract description (usually first or second column)
            description = self._extract_description(clean_row)
            if not description:
                return None
            
            # Extract vendor
            vendor = TextUtils.extract_vendor(description)
            
            # Clean description (remove vendor part)
            clean_description = TextUtils.clean_description(description)
            
            # Extract amounts from different columns
            borrower_amount, seller_amount, others_amount = self._extract_amounts_from_row(clean_row)
            
            # Determine who pays and the amount
            amount, paid_by = self._determine_payment_responsibility(
                borrower_amount, seller_amount, others_amount
            )
            
            # Check if optional
            is_optional = TextUtils.is_optional_item(description)
            
            # Get coordinates for highlighting
            coordinates = self._find_row_coordinates(description, row_index)
            
            return ClosingDisclosureLineItem(
                line_number=line_number,
                page_number=2,
                section=section,
                description=clean_description,
                vendor=vendor,
                amount=amount,
                paid_by=paid_by,
                category=category,
                is_optional=is_optional,
                coordinates=coordinates,
                raw_text=' | '.join(clean_row)
            )
            
        except Exception:
            return None
    
    def _extract_description(self, row: List[str]) -> Optional[str]:
        """Extract description from row, handling various column layouts."""
        # Try different approaches to find description
        for i, cell in enumerate(row):
            if cell and len(cell.strip()) > 3:
                # Skip if it's just a number or amount
                if re.match(r'^\d+\.?\d*$', cell.strip()):
                    continue
                if re.match(r'^\$?[\d,]+\.?\d*$', cell.strip()):
                    continue
                
                # This looks like a description
                return cell.strip()
        
        return None
    
    def _parse_line_item(self, line: str, section_letter: str, section: DocumentSection, 
                        category: CostCategory, line_number: int, line_index: int) -> Optional[ClosingDisclosureLineItem]:
        """Parse individual line item from text line."""
        try:
            # Skip empty lines and lines that don't look like items
            if not line or len(line.strip()) < 3:
                return None
            
            # Pattern for line items like "01APPRAISAL FEE to DUSTIN BADE $650.00"
            # or "012.97% of Loan Amount (Points) $3,846.86 $7,931.66"
            item_pattern = r'^(\d{1,2})(.+?)\s+(\$[\d,]+\.?\d*)(?:\s+(\$[\d,]+\.?\d*))?(?:\s+(\$[\d,]+\.?\d*))?'
            match = re.match(item_pattern, line)
            
            if not match:
                return None
            
            item_num = match.group(1)
            description_part = match.group(2).strip()
            amount1_str = match.group(3)  # Borrower amount
            amount2_str = match.group(4)  # Usually seller or before closing
            amount3_str = match.group(5)  # Additional amount
            
            # Extract amounts
            borrower_amount = TextUtils.extract_amount(amount1_str) if amount1_str else None
            seller_amount = TextUtils.extract_amount(amount2_str) if amount2_str else None
            others_amount = TextUtils.extract_amount(amount3_str) if amount3_str else None
            
            # Determine payment responsibility and final amount with enhanced logic
            amount, paid_by, payment_clarity = self._determine_payment_responsibility_enhanced(
                borrower_amount, seller_amount, others_amount, line, description_part
            )
            
            # Extract vendor from description
            vendor = TextUtils.extract_vendor(description_part)
            
            # Clean description
            clean_description = TextUtils.clean_description(description_part)
            
            # Check if optional
            is_optional = TextUtils.is_optional_item(description_part)
            
            # Get coordinates
            coordinates = self._find_line_coordinates(line, line_index)
            
            return ClosingDisclosureLineItem(
                line_number=f"{section_letter}.{item_num.zfill(2)}",
                page_number=2,
                section=section,
                description=clean_description,
                vendor=vendor,
                amount=amount,
                paid_by=paid_by,
                category=category,
                is_optional=is_optional,
                coordinates=coordinates,
                raw_text=line,
                payment_notes=payment_clarity  # Add payment clarity notes
            )
            
        except Exception:
            return None
    
    def _find_line_coordinates(self, line: str, line_index: int) -> Optional[CoordinatePosition]:
        """Find coordinates for a text line."""
        try:
            # Try to find coordinates based on the first few words of the line
            search_text = line[:30]  # First 30 characters
            coords = self.coordinate_extractor.find_text_coordinates(search_text)
            return coords[0] if coords else None
        except Exception:
            return None
    
    def _extract_amounts_from_row(self, row: List[str]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Extract borrower, seller, and others amounts from row."""
        borrower_amount = None
        seller_amount = None  
        others_amount = None
        
        # Look for amounts in the row (typically rightmost columns)
        amounts = []
        for cell in row:
            if cell:
                amount = TextUtils.extract_amount(cell)
                if amount is not None:
                    amounts.append(amount)
        
        # Assign amounts based on typical TRID layout
        # Usually: Description | Borrower At Closing | Borrower Before | Seller At | Seller Before | Others
        if len(amounts) >= 1:
            borrower_amount = amounts[0]
        if len(amounts) >= 3:
            seller_amount = amounts[2]
        if len(amounts) >= 5:
            others_amount = amounts[4]
        
        return borrower_amount, seller_amount, others_amount
    
    def _determine_payment_responsibility(self, borrower_amount: Optional[float], 
                                        seller_amount: Optional[float], 
                                        others_amount: Optional[float]) -> Tuple[Optional[float], PaymentResponsibility]:
        """Determine who pays and the amount."""
        # Priority: borrower > seller > others
        if borrower_amount and borrower_amount > 0:
            return borrower_amount, PaymentResponsibility.BORROWER
        elif seller_amount and seller_amount > 0:
            return seller_amount, PaymentResponsibility.SELLER
        elif others_amount and others_amount > 0:
            return others_amount, PaymentResponsibility.OTHERS
        else:
            # Default to borrower even if amount is None/0
            return borrower_amount, PaymentResponsibility.BORROWER
    
    def _determine_payment_responsibility_enhanced(self, borrower_amount: Optional[float], 
                                                 seller_amount: Optional[float], 
                                                 others_amount: Optional[float],
                                                 raw_line: str,
                                                 description: str) -> Tuple[Optional[float], PaymentResponsibility, Optional[str]]:
        """Enhanced payment responsibility detection with clarity notes."""
        payment_notes = None
        
        # Count how many amounts we have
        amounts = [amt for amt in [borrower_amount, seller_amount, others_amount] if amt and amt > 0]
        
        # CASE 1: Multiple amounts detected - need to analyze TRID column structure
        if len(amounts) > 1:
            # Based on TRID format: Borrower At/Before | Seller At/Before | Others
            # The position of amounts indicates who pays
            
            # For lines with 2+ amounts, we need to determine based on context
            if borrower_amount and borrower_amount > 0:
                # First amount typically goes to borrower
                primary_amount = borrower_amount
                paid_by = PaymentResponsibility.BORROWER
                
                # Note other amounts for transparency
                other_amounts = []
                if seller_amount and seller_amount > 0:
                    other_amounts.append(f"seller: ${seller_amount:,.2f}")
                if others_amount and others_amount > 0:
                    other_amounts.append(f"others: ${others_amount:,.2f}")
                
                if other_amounts:
                    payment_notes = f"Multiple amounts detected - borrower: ${borrower_amount:,.2f}, " + ", ".join(other_amounts)
                    
            elif seller_amount and seller_amount > 0:
                primary_amount = seller_amount
                paid_by = PaymentResponsibility.SELLER
                payment_notes = f"Seller-paid amount: ${seller_amount:,.2f}"
                
            elif others_amount and others_amount > 0:
                primary_amount = others_amount
                paid_by = PaymentResponsibility.OTHERS
                payment_notes = f"Others-paid amount: ${others_amount:,.2f}"
                
            else:
                # Shouldn't happen but handle gracefully
                primary_amount = amounts[0] if amounts else None
                paid_by = PaymentResponsibility.BORROWER
                payment_notes = "Payment responsibility unclear - defaulted to borrower"
                
        # CASE 2: Single amount - determine based on position and context
        elif len(amounts) == 1:
            if borrower_amount and borrower_amount > 0:
                primary_amount = borrower_amount
                paid_by = PaymentResponsibility.BORROWER
            elif seller_amount and seller_amount > 0:
                primary_amount = seller_amount
                paid_by = PaymentResponsibility.SELLER
                payment_notes = f"Seller-paid: ${seller_amount:,.2f}"
            elif others_amount and others_amount > 0:
                primary_amount = others_amount
                paid_by = PaymentResponsibility.OTHERS
                payment_notes = f"Others-paid: ${others_amount:,.2f}"
            else:
                primary_amount = amounts[0]
                paid_by = PaymentResponsibility.BORROWER
                payment_notes = "Payment responsibility unclear - defaulted to borrower"
                
        # CASE 3: No clear amounts
        else:
            primary_amount = None
            paid_by = PaymentResponsibility.BORROWER
            payment_notes = "No amount detected or all amounts are zero"
        
        # Additional checks for specific TRID patterns
        if "(L)" in description.upper():
            payment_notes = f"{payment_notes or ''} - Lender-paid item".strip(" - ")
        
        if "OPTIONAL" in description.upper():
            payment_notes = f"{payment_notes or ''} - Optional item".strip(" - ")
        
        return primary_amount, paid_by, payment_notes
    
    def _find_row_coordinates(self, description: str, row_index: int) -> Optional[CoordinatePosition]:
        """Find coordinates for a table row."""
        try:
            # Try to find coordinates based on description text
            coords = self.coordinate_extractor.find_text_coordinates(description[:20])
            return coords[0] if coords else None
        except Exception:
            return None
    
    def _parse_from_text(self) -> List[ClosingDisclosureLineItem]:
        """Parse line items from text-based TRID format."""
        line_items = []
        
        # Split text into lines
        lines = [line.strip() for line in self.page_text.split('\n') if line.strip()]
        
        current_section = None
        current_section_enum = None
        current_category = None
        line_counter = 1
        
        for i, line in enumerate(lines):
            # Check if this is a section header (A. B. C. etc.)
            section_match = self._parse_section_header(line)
            if section_match:
                current_section = section_match['letter']
                current_section_enum = self.section_map.get(current_section)
                current_category = CostCategory.LOAN_COSTS if current_section in ['A', 'B', 'C'] else CostCategory.OTHER_COSTS
                line_counter = 1
                
                # If section header has amount, create item for it
                if section_match.get('amount'):
                    item = ClosingDisclosureLineItem(
                        line_number=f"{current_section}.00",
                        page_number=2,
                        section=current_section_enum,
                        description=section_match['description'],
                        vendor=None,
                        amount=section_match['amount'],
                        paid_by=PaymentResponsibility.BORROWER,
                        category=current_category,
                        is_optional=False,
                        coordinates=self._find_line_coordinates(line, i),
                        raw_text=line
                    )
                    line_items.append(item)
                continue
            
            # Check if this is a line item within a section
            if current_section and current_section_enum:
                item = self._parse_line_item(line, current_section, current_section_enum, 
                                            current_category, line_counter, i)
                if item:
                    line_items.append(item)
                    line_counter += 1
        
        return line_items