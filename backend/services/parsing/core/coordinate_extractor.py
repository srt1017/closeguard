"""Coordinate extraction utilities for PDF text highlighting."""

import re
from typing import List, Optional, Dict, Tuple
from models.document import CoordinatePosition


class CoordinateExtractor:
    """Utility class for extracting text coordinates from PDF pages."""
    
    def __init__(self, page):
        """Initialize with a pdfplumber page object."""
        self.page = page
        
    def find_text_coordinates(self, search_text: str, case_sensitive: bool = False) -> List[CoordinatePosition]:
        """Find coordinates for specific text on the page."""
        try:
            chars = self.page.chars
            if not chars:
                return []
            
            # Prepare search text
            if not case_sensitive:
                search_text = search_text.lower()
            
            coordinates = []
            search_len = len(search_text)
            
            # Build text string with character positions
            page_text = ""
            char_positions = []
            
            for char in chars:
                char_text = char.get('text', '')
                if not case_sensitive:
                    char_text = char_text.lower()
                page_text += char_text
                char_positions.append({
                    'x0': char.get('x0', 0),
                    'y0': char.get('y0', 0), 
                    'x1': char.get('x1', 0),
                    'y1': char.get('y1', 0)
                })
            
            # Find all occurrences of search text
            start_index = 0
            while True:
                index = page_text.find(search_text, start_index)
                if index == -1:
                    break
                
                # Get bounding box for the text span
                if index + search_len <= len(char_positions):
                    start_char = char_positions[index]
                    end_char = char_positions[index + search_len - 1]
                    
                    coord = CoordinatePosition(
                        x=start_char['x0'],
                        y=start_char['y0'],
                        width=end_char['x1'] - start_char['x0'],
                        height=end_char['y1'] - start_char['y0']
                    )
                    coordinates.append(coord)
                
                start_index = index + 1
            
            return coordinates
            
        except Exception:
            return []
    
    def find_amount_coordinates(self, amount: float, formats: List[str] = None) -> List[CoordinatePosition]:
        """Find coordinates for monetary amounts in various formats."""
        if formats is None:
            formats = [
                f"${amount:,.2f}",      # $1,234.56
                f"${amount:.2f}",       # $1234.56  
                f"{amount:,.2f}",       # 1,234.56
                f"{amount:.2f}",        # 1234.56
                f"${amount:,.0f}",      # $1,234 (if whole number)
                f"{amount:,.0f}"        # 1,234 (if whole number)
            ]
        
        coordinates = []
        for format_str in formats:
            coords = self.find_text_coordinates(format_str)
            coordinates.extend(coords)
        
        return coordinates
    
    def find_pattern_coordinates(self, pattern: str) -> List[CoordinatePosition]:
        """Find coordinates for text matching a regex pattern."""
        try:
            page_text = self.page.extract_text() or ""
            compiled_pattern = re.compile(pattern)
            
            coordinates = []
            for match in compiled_pattern.finditer(page_text):
                match_text = match.group()
                coords = self.find_text_coordinates(match_text)
                coordinates.extend(coords)
            
            return coordinates
            
        except Exception:
            return []
    
    def find_table_cell_coordinates(self, row_index: int, col_index: int) -> Optional[CoordinatePosition]:
        """Find coordinates for a specific table cell."""
        try:
            tables = self.page.extract_tables()
            if not tables or row_index >= len(tables):
                return None
            
            table = tables[0]  # Assume first table for now
            if row_index >= len(table) or col_index >= len(table[row_index]):
                return None
            
            cell_text = table[row_index][col_index]
            if cell_text:
                coords = self.find_text_coordinates(cell_text.strip())
                return coords[0] if coords else None
            
            return None
            
        except Exception:
            return None
    
    def get_page_dimensions(self) -> Tuple[float, float]:
        """Get page width and height."""
        bbox = self.page.bbox
        return bbox[2] - bbox[0], bbox[3] - bbox[1]  # width, height
    
    def find_section_header_coordinates(self, section_letter: str) -> Optional[CoordinatePosition]:
        """Find coordinates for section headers like 'A. Origination Charges'."""
        patterns = [
            f"{section_letter}\\.",              # "A."
            f"{section_letter}\\s+",            # "A "  
            f"^{section_letter}\\.",            # Line starting with "A."
        ]
        
        for pattern in patterns:
            coords = self.find_pattern_coordinates(pattern)
            if coords:
                return coords[0]
        
        return None