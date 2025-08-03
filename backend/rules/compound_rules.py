"""Compound rule handlers for complex logic."""

import re
from typing import List, Optional, Dict, Any

from models.rule import Rule, RuleType
from models.flag import Flag
from models.user_context import UserContext
from .base_rule import BaseRuleHandler


class CompoundRuleHandler(BaseRuleHandler):
    """Handler for compound rules that combine multiple conditions."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.COMPOUND_RULE
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process compound rule with multiple conditions."""
        conditions = rule.config.get('conditions', [])
        logic = rule.config.get('logic', 'AND')  # AND or OR
        
        if not conditions:
            return []
        
        condition_results = []
        match_info = None
        
        # Evaluate each condition
        for condition in conditions:
            result, info = self._evaluate_condition(condition, text)
            condition_results.append(result)
            
            # Store match info from the first successful condition for snippet
            if result and match_info is None:
                match_info = info
        
        # Apply logic
        if logic.upper() == 'AND':
            conditions_met = all(condition_results)
        else:  # OR
            conditions_met = any(condition_results)
        
        if conditions_met:
            snippet = 'Multiple conditions met'
            if match_info:
                snippet = self.extract_snippet(text, match_info['start'], match_info['end'])
            
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet=snippet
            )]
        
        return []
    
    def _evaluate_condition(self, condition: Dict[str, Any], text: str) -> tuple:
        """Evaluate a single condition."""
        condition_type = condition.get('type', '')
        
        if condition_type == 'regex_presence':
            return self._check_regex_presence(condition, text)
        elif condition_type == 'regex_absence':
            return self._check_regex_absence(condition, text)
        elif condition_type == 'numeric_threshold':
            return self._check_numeric_threshold(condition, text)
        else:
            return False, None
    
    def _check_regex_presence(self, condition: Dict[str, Any], text: str) -> tuple:
        """Check if regex pattern is present."""
        pattern = condition.get('pattern', '')
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return True, {'start': match.start(), 'end': match.end()}
        return False, None
    
    def _check_regex_absence(self, condition: Dict[str, Any], text: str) -> tuple:
        """Check if regex pattern is absent."""
        pattern = condition.get('pattern', '')
        match = re.search(pattern, text, re.IGNORECASE)
        
        # Return True if pattern is NOT found
        return not bool(match), None
    
    def _check_numeric_threshold(self, condition: Dict[str, Any], text: str) -> tuple:
        """Check numeric threshold condition."""
        pattern = condition.get('pattern', '')
        threshold = condition.get('threshold', 0)
        operator = condition.get('operator', '>')
        
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value_str = match.group(1).replace(',', '')
                value = float(value_str)
                
                condition_met = self._evaluate_numeric_condition(value, threshold, operator)
                if condition_met:
                    return True, {'start': match.start(), 'end': match.end()}
            except (ValueError, IndexError):
                pass
        
        return False, None
    
    def _evaluate_numeric_condition(self, value: float, threshold: float, operator: str) -> bool:
        """Evaluate numeric condition."""
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
            return value > threshold


class CrossReferencePatternHandler(BaseRuleHandler):
    """Handler for cross-reference pattern rules."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.CROSS_REFERENCE_PATTERN
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process cross-reference pattern rule."""
        primary_pattern = rule.config.get('primary_pattern', '')
        reference_pattern = rule.config.get('reference_pattern', '')
        
        if not primary_pattern or not reference_pattern:
            return []
        
        # Find primary match
        primary_match = re.search(primary_pattern, text, re.IGNORECASE)
        if not primary_match:
            return []
        
        # Find reference match
        reference_match = re.search(reference_pattern, text, re.IGNORECASE)
        if not reference_match:
            return []
        
        # Both patterns found - this indicates a potential issue
        snippet = self.extract_snippet(text, primary_match.start(), primary_match.end())
        
        return [Flag(
            rule=rule.name,
            message=rule.message,
            snippet=snippet
        )]