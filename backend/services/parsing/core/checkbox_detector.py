"""Checkbox detection utilities for PDF forms."""

from typing import Dict, List, Optional, Tuple


class CheckboxDetector:
    """Detects filled/selected checkboxes in PDF documents."""
    
    def __init__(self, page):
        """Initialize with pdfplumber page object."""
        self.page = page
        self.chars = page.chars
        self.rectangles = page.rects
        self.curves = getattr(page, 'curves', [])
        self.lines = getattr(page, 'lines', [])
    
    def find_checkboxes(self, min_size: float = 5, max_size: float = 20) -> List[Dict]:
        """Find all potential checkbox rectangles on the page."""
        checkboxes = []
        
        for i, rect in enumerate(self.rectangles):
            x0, y0, x1, y1 = rect['x0'], rect['y0'], rect['x1'], rect['y1']
            width = x1 - x0
            height = y1 - y0
            
            # Filter for checkbox-sized rectangles
            if min_size <= width <= max_size and min_size <= height <= max_size:
                center_x = (x0 + x1) / 2
                center_y = (y0 + y1) / 2
                
                # Check if checkbox is filled by looking for overlaid elements
                is_filled = self._detect_checkbox_filled(center_x, center_y, width, height)
                
                checkboxes.append({
                    'id': i,
                    'center_x': center_x,
                    'center_y': center_y,
                    'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                    'width': width,
                    'height': height,
                    'filled': is_filled,
                    'rect': rect
                })
        
        return checkboxes
    
    def _detect_checkbox_filled(self, center_x: float, center_y: float, 
                               width: float, height: float) -> bool:
        """Detect if a checkbox is filled by looking for overlaid marks."""
        search_radius = max(width, height) / 2 + 2  # Slightly larger than checkbox
        
        # Method 1: Look for diagonal lines (X marks)
        diagonal_lines = self._find_diagonal_lines_in_area(center_x, center_y, search_radius)
        if diagonal_lines:
            return True
        
        # Method 2: Look for filled curves/paths
        filled_curves = self._find_filled_curves_in_area(center_x, center_y, search_radius)
        if filled_curves:
            return True
        
        # Method 3: Look for checkmark characters
        checkmark_chars = self._find_checkmark_chars_in_area(center_x, center_y, search_radius)
        if checkmark_chars:
            return True
        
        # Method 4: Look for multiple intersecting lines (could be checkmark)
        intersecting_lines = self._find_intersecting_lines_in_area(center_x, center_y, search_radius)
        if len(intersecting_lines) >= 2:  # Multiple lines might form a checkmark
            return True
        
        return False
    
    def _find_diagonal_lines_in_area(self, center_x: float, center_y: float, 
                                   radius: float) -> List[Dict]:
        """Find diagonal lines that could be X marks."""
        diagonal_lines = []
        
        for line in self.lines:
            line_center_x = (line['x0'] + line['x1']) / 2
            line_center_y = (line['y0'] + line['y1']) / 2
            
            # Check if line is within search area
            distance = ((line_center_x - center_x)**2 + (line_center_y - center_y)**2)**0.5
            if distance <= radius:
                # Check if line is diagonal (not horizontal or vertical)
                dx = abs(line['x1'] - line['x0'])
                dy = abs(line['y1'] - line['y0'])
                
                # Diagonal if both dx and dy are significant
                if dx > 2 and dy > 2:  # Minimum diagonal length
                    diagonal_lines.append(line)
        
        return diagonal_lines
    
    def _find_filled_curves_in_area(self, center_x: float, center_y: float, 
                                  radius: float) -> List[Dict]:
        """Find filled curves that could indicate selection."""
        filled_curves = []
        
        for curve in self.curves:
            curve_center_x = (curve['x0'] + curve['x1']) / 2
            curve_center_y = (curve['y0'] + curve['y1']) / 2
            
            distance = ((curve_center_x - center_x)**2 + (curve_center_y - center_y)**2)**0.5
            if distance <= radius:
                # Check if curve is filled
                if curve.get('fill', False) or curve.get('non_stroking_color', 0) > 0:
                    filled_curves.append(curve)
        
        return filled_curves
    
    def _find_checkmark_chars_in_area(self, center_x: float, center_y: float, 
                                    radius: float) -> List[str]:
        """Find checkmark characters near the checkbox."""
        checkmark_symbols = ['✓', '✗', '✘', '×', '☑', '☒', '▪', '■', '●', 'X']
        found_chars = []
        
        for char in self.chars:
            char_x = char.get('x0', 0)
            char_y = char.get('y0', 0)
            char_text = char.get('text', '')
            
            distance = ((char_x - center_x)**2 + (char_y - center_y)**2)**0.5
            if distance <= radius and char_text in checkmark_symbols:
                found_chars.append(char_text)
        
        return found_chars
    
    def _find_intersecting_lines_in_area(self, center_x: float, center_y: float, 
                                       radius: float) -> List[Dict]:
        """Find lines that could form checkmarks or X marks."""
        nearby_lines = []
        
        for line in self.lines:
            line_center_x = (line['x0'] + line['x1']) / 2
            line_center_y = (line['y0'] + line['y1']) / 2
            
            distance = ((line_center_x - center_x)**2 + (line_center_y - center_y)**2)**0.5
            if distance <= radius:
                nearby_lines.append(line)
        
        return nearby_lines
    
    def map_checkboxes_to_text(self, text_options: List[str], 
                              max_distance: float = 50) -> Dict[str, Optional[bool]]:
        """Map checkboxes to nearby text options and determine selection."""
        checkboxes = self.find_checkboxes()
        results = {}
        
        # Find positions of text options
        text_positions = self._find_text_positions(text_options)
        
        # Match each text option to its nearest checkbox
        for text_option in text_options:
            if text_option.lower() not in text_positions:
                results[text_option] = None
                continue
            
            pos = text_positions[text_option.lower()]
            closest_checkbox = None
            closest_distance = float('inf')
            
            for checkbox in checkboxes:
                # Calculate distance (prioritize Y alignment for horizontal layouts)
                x_diff = abs(checkbox['center_x'] - pos['x'])
                y_diff = abs(checkbox['center_y'] - pos['y'])
                distance = (x_diff**2 + (y_diff * 1.5)**2)**0.5  # Weight Y difference slightly more
                
                if distance < max_distance and distance < closest_distance:
                    closest_distance = distance
                    closest_checkbox = checkbox
            
            results[text_option] = closest_checkbox['filled'] if closest_checkbox else None
        
        return results
    
    def _find_text_positions(self, text_options: List[str]) -> Dict[str, Dict]:
        """Find positions of text options by combining characters into words."""
        positions = {}
        current_word = ''
        word_start_x = None
        word_y = None
        
        for char in self.chars:
            char_text = char.get('text', '')
            char_x = char.get('x0', 0)
            char_y = char.get('y0', 0)
            
            if char_text.isalpha():  # Letter
                if current_word == '':
                    word_start_x = char_x
                    word_y = char_y
                current_word += char_text
            else:  # Space or punctuation - end of word
                if current_word.lower() in [opt.lower() for opt in text_options]:
                    positions[current_word.lower()] = {
                        'x': word_start_x,
                        'y': word_y,
                        'word': current_word
                    }
                current_word = ''
        
        # Check final word
        if current_word.lower() in [opt.lower() for opt in text_options]:
            positions[current_word.lower()] = {
                'x': word_start_x,
                'y': word_y,
                'word': current_word
            }
        
        return positions