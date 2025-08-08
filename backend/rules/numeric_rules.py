"""Numeric rule handlers for threshold-based detection."""

import re
from typing import List, Optional

from models.core import Rule, RuleType, Flag, UserContext
from .base_rule import BaseRuleHandler


class NumericThresholdHandler(BaseRuleHandler):
    """Handler for numeric threshold rules."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type in [RuleType.NUMERIC_THRESHOLD, RuleType.CALCULATED_PERCENTAGE]
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process numeric threshold or calculated percentage rule."""
        if rule.rule_type == RuleType.NUMERIC_THRESHOLD:
            return self._check_numeric_threshold(rule, text)
        elif rule.rule_type == RuleType.CALCULATED_PERCENTAGE:
            return self._check_calculated_percentage(rule, text)
        return []
    
    def _check_numeric_threshold(self, rule: Rule, text: str) -> List[Flag]:
        """Check if numeric values exceed a threshold."""
        flags = []
        
        if not rule.pattern or rule.threshold is None:
            return flags
        
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
                    formatted_message = self.format_message(rule.message, value=value, value_str=value_str)
                    
                    flags.append(Flag(
                        rule=rule.name,
                        message=formatted_message,
                        snippet=snippet
                    ))
                    
            except (ValueError, IndexError) as e:
                print(f"Error processing numeric value in rule '{rule.name}': {e}")
                continue
        
        return flags
    
    def _check_calculated_percentage(self, rule: Rule, text: str) -> List[Flag]:
        """Check calculated percentage against threshold."""
        flags = []
        
        if not rule.numerator_pattern or not rule.denominator_pattern or rule.threshold is None:
            return flags
        
        try:
            # Find numerator value
            numerator_match = re.search(rule.numerator_pattern, text, re.IGNORECASE)
            if not numerator_match:
                return flags
            
            numerator_str = numerator_match.group(1).replace(',', '')
            numerator = float(numerator_str)
            
            # Find denominator value
            denominator_match = re.search(rule.denominator_pattern, text, re.IGNORECASE)
            if not denominator_match:
                return flags
            
            denominator_str = denominator_match.group(1).replace(',', '')
            denominator = float(denominator_str)
            
            if denominator == 0:
                return flags
            
            # Calculate percentage
            percentage = (numerator / denominator) * 100
            
            # Check threshold condition
            condition_met = self._evaluate_condition(percentage, rule.threshold, rule.operator or '>')
            
            if condition_met:
                # Use numerator match for snippet location
                snippet = self.extract_snippet(text, numerator_match.start(), numerator_match.end())
                formatted_message = self.format_message(
                    rule.message, 
                    percentage=round(percentage, 2),
                    numerator=numerator,
                    denominator=denominator
                )
                
                flags.append(Flag(
                    rule=rule.name,
                    message=formatted_message,
                    snippet=snippet
                ))
                
        except (ValueError, IndexError) as e:
            print(f"Error calculating percentage in rule '{rule.name}': {e}")
        
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