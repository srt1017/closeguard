"""Rule engine service using modular rule handlers."""

from typing import List, Optional, Dict, Any
from collections import defaultdict

from models.rule import Rule
from models.flag import Flag
from models.user_context import UserContext
from config.rules_loader import RulesLoader

# Import rule handlers
from rules.numeric_rules import NumericThresholdHandler
from rules.regex_rules import RegexPresenceHandler, RegexAbsenceHandler, RegexAmountHandler
from rules.compound_rules import CompoundRuleHandler, CrossReferencePatternHandler
from rules.context_rules import ContextComparisonHandler


class RuleEngineService:
    """Service for processing rules against document text."""
    
    def __init__(self, config_path: str = "rules-config.yaml"):
        self.rules_loader = RulesLoader(config_path)
        self.handlers = [
            NumericThresholdHandler(),
            RegexPresenceHandler(),
            RegexAbsenceHandler(),
            RegexAmountHandler(),
            CompoundRuleHandler(),
            CrossReferencePatternHandler(),
            ContextComparisonHandler()
        ]
    
    def analyze_text(self, text: str, user_context: Optional[UserContext] = None) -> List[Flag]:
        """
        Analyze text using all enabled rules.
        
        Args:
            text: The document text to analyze
            user_context: Optional user context for enhanced analysis
            
        Returns:
            List of flags detected by the rules
        """
        flags = []
        flagged_rules = set()  # Track which rules have already been flagged to prevent duplicates
        
        # Load enabled rules
        rules = self.rules_loader.get_enabled_rules()
        
        for rule in rules:
            # Skip if this rule has already been flagged
            if rule.name in flagged_rules:
                continue
            
            try:
                # Find appropriate handler for this rule
                handler = self._get_handler_for_rule(rule)
                if handler:
                    rule_flags = handler.process_rule(rule, text, user_context)
                    
                    # If this rule found any flags, add the first one and mark rule as flagged
                    if rule_flags:
                        flags.append(rule_flags[0])  # Only take the first match to avoid duplicates
                        flagged_rules.add(rule.name)
                else:
                    print(f"Warning: No handler found for rule type '{rule.rule_type.value}' in rule '{rule.name}'")
                    
            except Exception as e:
                print(f"Error processing rule '{rule.name}': {e}")
                continue
        
        return flags
    
    def analyze_with_context(self, text: str, user_context: UserContext) -> List[Flag]:
        """
        Analyze text with enhanced context-aware rules.
        
        Args:
            text: The document text to analyze
            user_context: User context for enhanced analysis
            
        Returns:
            List of flags with enhanced context-aware detection
        """
        return self.analyze_text(text, user_context)
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """Get summary of loaded rules."""
        rules = self.rules_loader.load_rules()
        
        summary = {
            'total_rules': len(rules),
            'enabled_rules': len([r for r in rules if r.enabled]),
            'disabled_rules': len([r for r in rules if not r.enabled]),
            'rules_by_type': defaultdict(int)
        }
        
        for rule in rules:
            summary['rules_by_type'][rule.rule_type.value] += 1
        
        return summary
    
    def validate_rules_config(self) -> Dict[str, Any]:
        """Validate the rules configuration."""
        try:
            rules = self.rules_loader.load_rules()
            
            validation_results = {
                'valid': True,
                'errors': [],
                'warnings': [],
                'rules_count': len(rules)
            }
            
            for rule in rules:
                # Check if we have a handler for this rule type
                handler = self._get_handler_for_rule(rule)
                if not handler:
                    validation_results['errors'].append(
                        f"No handler available for rule type '{rule.rule_type.value}' in rule '{rule.name}'"
                    )
                    validation_results['valid'] = False
                
                # Check for required fields based on rule type
                if not rule.name:
                    validation_results['errors'].append("Rule missing name")
                    validation_results['valid'] = False
                
                if not rule.message:
                    validation_results['warnings'].append(f"Rule '{rule.name}' has no message")
            
            return validation_results
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Failed to load rules configuration: {e}"],
                'warnings': [],
                'rules_count': 0
            }
    
    def _get_handler_for_rule(self, rule: Rule):
        """Find the appropriate handler for a rule."""
        for handler in self.handlers:
            if handler.can_handle(rule):
                return handler
        return None
    
    def reload_rules(self):
        """Reload rules configuration."""
        # Rules are loaded fresh each time from the loader
        # This method exists for future caching implementations
        pass