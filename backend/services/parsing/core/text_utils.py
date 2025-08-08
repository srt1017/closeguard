"""Text processing utilities for document parsing."""

import re
from typing import Optional, List, Dict, Any


class TextUtils:
    """Utility functions for text processing and extraction."""
    
    @staticmethod
    def extract_amount(text: str) -> Optional[float]:
        """Extract monetary amount from text."""
        if not text:
            return None
        
        # Remove common prefixes and clean text
        clean_text = text.replace('$', '').replace(',', '').strip()
        
        # Handle parentheses (negative amounts)
        is_negative = '(' in text and ')' in text
        clean_text = clean_text.replace('(', '').replace(')', '')
        
        # Try to extract number
        try:
            amount = float(clean_text)
            return -amount if is_negative else amount
        except (ValueError, TypeError):
            # Try regex extraction for more complex cases
            pattern = r'[\d,]+\.?\d*'
            match = re.search(pattern, clean_text)
            if match:
                try:
                    amount = float(match.group().replace(',', ''))
                    return -amount if is_negative else amount
                except ValueError:
                    pass
        
        return None
    
    @staticmethod
    def extract_percentage(text: str) -> Optional[float]:
        """Extract percentage from text."""
        if not text:
            return None
        
        # Look for percentage patterns
        patterns = [
            r'(\d+\.?\d*)\s*%',     # "6.625%"
            r'(\d+\.?\d*)\s*percent',  # "6.625 percent"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    @staticmethod
    def clean_description(text: str) -> str:
        """Clean and normalize description text."""
        if not text:
            return ""
        
        # Basic cleaning
        cleaned = text.strip()
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common artifacts
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)  # Remove leading numbers
        cleaned = re.sub(r'\s*to\s*$', '', cleaned, re.IGNORECASE)  # Remove trailing "to"
        
        return cleaned.strip()
    
    @staticmethod
    def extract_vendor(text: str) -> Optional[str]:
        """Extract vendor name from text."""
        if not text:
            return None
        
        # Look for "to VENDOR_NAME" pattern
        pattern = r'\bto\s+([A-Z][A-Z\s\.,&-]+)'
        match = re.search(pattern, text)
        if match:
            vendor = match.group(1).strip()
            # Clean up vendor name
            vendor = re.sub(r'[,.]$', '', vendor)  # Remove trailing punctuation
            return vendor if len(vendor) > 1 else None
        
        return None
    
    @staticmethod
    def parse_line_number(text: str) -> Optional[str]:
        """Parse line number from text (e.g., 'A.01', 'B.02')."""
        pattern = r'^([A-Z])\.?(\d{2})'
        match = re.search(pattern, text.strip())
        if match:
            letter, number = match.groups()
            return f"{letter}.{number}"
        return None
    
    @staticmethod
    def extract_date(text: str) -> Optional[str]:
        """Extract date from text in various formats."""
        if not text:
            return None
        
        # Common date patterns
        patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',        # MM/DD/YYYY
            r'(\d{1,2}/\d{1,2}/\d{2})',        # MM/DD/YY
            r'(\d{2}/\d{2}/\d{4})',            # MM/DD/YYYY
            r'(\d{4}-\d{2}-\d{2})',            # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def is_optional_item(text: str) -> bool:
        """Check if line item is optional based on text content."""
        if not text:
            return False
        
        optional_indicators = [
            'optional',
            '(optional)', 
            'OPTIONAL',
            '(OPTIONAL)'
        ]
        
        return any(indicator in text for indicator in optional_indicators)
    
    @staticmethod
    def normalize_section_name(text: str) -> str:
        """Normalize section names for consistent matching."""
        if not text:
            return ""
        
        normalized = text.lower().strip()
        
        # Common normalizations
        replacements = {
            'origination charges': 'origination_charges',
            'services borrower did not shop for': 'services_not_shopped',
            'services borrower did shop for': 'services_shopped',
            'taxes and other government fees': 'taxes_government_fees',
            'prepaids': 'prepaids',
            'initial escrow payment at closing': 'initial_escrow',
            'other': 'other'
        }
        
        for original, replacement in replacements.items():
            if original in normalized:
                return replacement
        
        return normalized.replace(' ', '_')
    
    @staticmethod
    def extract_table_data(page, table_settings: Dict[str, Any] = None) -> List[List[str]]:
        """Extract table data from a page with custom settings."""
        if table_settings is None:
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "join_tolerance": 3
            }
        
        try:
            tables = page.extract_tables(table_settings=table_settings)
            return tables[0] if tables else []
        except Exception:
            # Fallback to simple extraction
            try:
                return page.extract_tables() or []
            except Exception:
                return []