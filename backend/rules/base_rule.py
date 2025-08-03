"""Base rule handler for all rule types."""

from abc import ABC, abstractmethod
from typing import List, Optional

from models.rule import Rule
from models.flag import Flag
from models.user_context import UserContext


class BaseRuleHandler(ABC):
    """Abstract base class for all rule handlers."""
    
    def __init__(self):
        self.rule_type = None
    
    @abstractmethod
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        pass
    
    @abstractmethod
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process a rule against text and return any flags."""
        pass
    
    def extract_snippet(self, text: str, start_pos: int, end_pos: int, context_chars: int = 50) -> str:
        """Extract a snippet of text around a match."""
        start = max(0, start_pos - context_chars)
        end = min(len(text), end_pos + context_chars)
        return text[start:end].strip()
    
    def format_message(self, message: str, **kwargs) -> str:
        """Format message with provided values."""
        formatted = message
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            dollar_placeholder = f"${{{key}}}"
            
            # Handle both {value} and ${value} formats
            if isinstance(value, (int, float)):
                formatted = formatted.replace(placeholder, str(value))
                formatted = formatted.replace(dollar_placeholder, f"${value}")
            else:
                formatted = formatted.replace(placeholder, str(value))
        
        return formatted