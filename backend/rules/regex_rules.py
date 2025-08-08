"""Regex-based rule handlers."""

import re
from typing import List, Optional

from models.core import Rule, RuleType, Flag, UserContext
from .base_rule import BaseRuleHandler


class RegexPresenceHandler(BaseRuleHandler):
    """Handler for regex presence rules."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.REGEX_PRESENCE
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process regex presence rule."""
        if not rule.pattern:
            return []
        
        # Check if pattern IS found in text
        match = re.search(rule.pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            snippet = self.extract_snippet(text, match.start(), match.end())
            
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet=snippet
            )]
        
        return []


class RegexAbsenceHandler(BaseRuleHandler):
    """Handler for regex absence rules."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.REGEX_ABSENCE
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process regex absence rule."""
        if not rule.pattern:
            return []
        
        # Check if pattern is NOT found in text
        if not re.search(rule.pattern, text, re.IGNORECASE):
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet='Pattern not found in document'
            )]
        
        return []


class RegexAmountHandler(BaseRuleHandler):
    """Handler for regex amount rules (amounts matching patterns with thresholds)."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.REGEX_AMOUNT
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process regex amount rule."""
        flags = []
        
        if not rule.pattern or rule.threshold is None:
            return flags
        
        # Find all matches in the text
        matches = re.finditer(rule.pattern, text, re.IGNORECASE)
        
        for match in matches:
            try:
                # Extract numeric value (remove commas and convert to float)
                value_str = match.group(1).replace(',', '')
                value = float(value_str)
                
                # Check threshold condition
                condition_met = self._evaluate_condition(value, rule.threshold, rule.operator or '>')
                
                if condition_met:
                    snippet = self.extract_snippet(text, match.start(), match.end())
                    formatted_message = self.format_message(rule.message, value=value)
                    
                    flags.append(Flag(
                        rule=rule.name,
                        message=formatted_message,
                        snippet=snippet
                    ))
                    
            except (ValueError, IndexError) as e:
                print(f"Error processing amount in rule '{rule.name}': {e}")
                continue
        
        return flags
    
    def _evaluate_condition(self, value: float, threshold: float, operator: str) -> bool:
        """Evaluate threshold condition."""
        if operator == '>':
            return value > threshold
        elif operator == '<':
            return value < threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '==':
            return value == threshold
        else:
            return value > threshold  # Default to greater than