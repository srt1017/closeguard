"""Coordinate positioning models for document highlighting."""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class CoordinatePosition:
    """Represents x,y coordinates for text highlighting in PDFs."""
    
    x: float
    y: float
    width: Optional[float] = None
    height: Optional[float] = None
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for API responses."""
        result = {"x": self.x, "y": self.y}
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        return result
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"CoordinatePosition(x={self.x}, y={self.y}, w={self.width}, h={self.height})"