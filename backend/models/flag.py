"""Flag data model for representing detected issues."""

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class FlagSeverity(Enum):
    """Severity levels for flags."""
    HIGH = "high"
    MEDIUM = "medium" 
    LOW = "low"


@dataclass
class Flag:
    """Represents a detected issue in a document."""
    
    rule: str
    message: str
    snippet: str
    severity: Optional[FlagSeverity] = None
    confidence: Optional[float] = None
    
    def __post_init__(self):
        """Determine severity if not explicitly set."""
        if self.severity is None:
            self.severity = self._determine_severity()
    
    def _determine_severity(self) -> FlagSeverity:
        """Determine severity based on message content."""
        message_lower = self.message.lower()
        
        # High severity keywords
        if any(keyword in message_lower for keyword in ['🚨', 'critical', 'error', 'fraud']):
            return FlagSeverity.HIGH
        
        # Medium severity keywords
        elif any(keyword in message_lower for keyword in ['⚠️', 'warning', 'dangerous', 'excessive']):
            return FlagSeverity.MEDIUM
        
        # Default to low severity
        else:
            return FlagSeverity.LOW
    
    def to_dict(self) -> dict:
        """Convert flag to dictionary format for API responses."""
        return {
            'rule': self.rule,
            'message': self.message,
            'snippet': self.snippet,
            'severity': self.severity.value if self.severity else None,
            'confidence': self.confidence
        }