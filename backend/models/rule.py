"""Rule data model for fraud detection rules."""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class RuleType(Enum):
    """Types of rules supported by the engine."""
    NUMERIC_THRESHOLD = "numeric_threshold"
    CALCULATED_PERCENTAGE = "calculated_percentage" 
    REGEX_PRESENCE = "regex_presence"
    REGEX_ABSENCE = "regex_absence"
    REGEX_AMOUNT = "regex_amount"
    COMPOUND_RULE = "compound_rule"
    CROSS_REFERENCE_PATTERN = "cross_reference_pattern"
    CONTEXT_COMPARISON = "context_comparison"


@dataclass
class Rule:
    """Represents a fraud detection rule."""
    
    name: str
    rule_type: RuleType
    message: str
    config: Dict[str, Any]
    enabled: bool = True
    priority: int = 1
    
    # Rule-specific configuration
    pattern: Optional[str] = None
    threshold: Optional[float] = None
    operator: Optional[str] = None
    numerator_pattern: Optional[str] = None
    denominator_pattern: Optional[str] = None
    
    def __post_init__(self):
        """Extract common config fields."""
        if self.config:
            self.pattern = self.config.get('pattern', self.pattern)
            self.threshold = self.config.get('threshold', self.threshold)
            self.operator = self.config.get('operator', self.operator)
            self.numerator_pattern = self.config.get('numerator_pattern', self.numerator_pattern)
            self.denominator_pattern = self.config.get('denominator_pattern', self.denominator_pattern)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        """Create Rule from dictionary (e.g., from YAML config)."""
        rule_type_str = data.get('type', '')
        
        # Map string types to enum
        type_mapping = {
            'numeric_threshold': RuleType.NUMERIC_THRESHOLD,
            'calculated_percentage': RuleType.CALCULATED_PERCENTAGE,
            'regex_presence': RuleType.REGEX_PRESENCE,
            'regex_absence': RuleType.REGEX_ABSENCE,
            'regex_amount': RuleType.REGEX_AMOUNT,
            'compound_rule': RuleType.COMPOUND_RULE,
            'cross_reference_pattern': RuleType.CROSS_REFERENCE_PATTERN,
            'context_comparison': RuleType.CONTEXT_COMPARISON
        }
        
        rule_type = type_mapping.get(rule_type_str)
        if not rule_type:
            raise ValueError(f"Unknown rule type: {rule_type_str}")
        
        return cls(
            name=data.get('name', ''),
            rule_type=rule_type,
            message=data.get('message', ''),
            config=data,
            enabled=data.get('enabled', True),
            priority=data.get('priority', 1),
            pattern=data.get('pattern'),
            threshold=data.get('threshold'),
            operator=data.get('operator'),
            numerator_pattern=data.get('numerator_pattern'),
            denominator_pattern=data.get('denominator_pattern')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule back to dictionary format."""
        return {
            'name': self.name,
            'type': self.rule_type.value,
            'message': self.message,
            'enabled': self.enabled,
            'priority': self.priority,
            **self.config
        }