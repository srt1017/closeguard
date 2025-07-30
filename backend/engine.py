import yaml
import re
from typing import List, Dict, Any, Optional
from pathlib import Path


class RuleEngine:
    def __init__(self, config_path: str = "rules-config.yaml"):
        """
        Initialize the rule engine with configuration from YAML file.
        
        Args:
            config_path: Path to the rules configuration YAML file
        """
        self.config_path = config_path
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict[str, Any]]:
        """Load rules from YAML configuration file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Rules configuration file not found: {self.config_path}")
            
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('rules', [])
        except Exception as e:
            raise Exception(f"Failed to load rules configuration: {e}")
    
    def check_text(self, text: str) -> List[Dict[str, str]]:
        """
        Run all rules against the provided text and return any flags.
        
        Args:
            text: The text content to analyze
            
        Returns:
            List of flags, each containing rule name, message, and snippet
        """
        flags = []
        
        for rule in self.rules:
            try:
                rule_flags = self._apply_rule(rule, text)
                flags.extend(rule_flags)
            except Exception as e:
                # Log error but continue with other rules
                print(f"Error applying rule '{rule.get('name', 'unknown')}': {e}")
        
        return flags
    
    def _apply_rule(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Apply a single rule to the text and return any flags."""
        rule_type = rule.get('type')
        rule_name = rule.get('name', 'unknown')
        
        if rule_type == 'numeric_threshold':
            return self._check_numeric_threshold(rule, text)
        elif rule_type == 'regex_absence':
            return self._check_regex_absence(rule, text)
        elif rule_type == 'regex_amount':
            return self._check_regex_amount(rule, text)
        else:
            print(f"Unknown rule type: {rule_type}")
            return []
    
    def _check_numeric_threshold(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Check if numeric values in text exceed/fall below threshold."""
        flags = []
        pattern = rule.get('pattern', '')
        threshold = rule.get('threshold', 0)
        operator = rule.get('operator', '>')
        message = rule.get('message', 'Threshold check failed')
        rule_name = rule.get('name', 'unknown')
        
        # Find all matches in the text
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            try:
                # Extract numeric value (remove commas and convert to float)
                value_str = match.group(1).replace(',', '')
                value = float(value_str)
                
                # Check threshold condition
                condition_met = False
                if operator == '>':
                    condition_met = value > threshold
                elif operator == '<':
                    condition_met = value < threshold
                elif operator == '>=':
                    condition_met = value >= threshold
                elif operator == '<=':
                    condition_met = value <= threshold
                elif operator == '==':
                    condition_met = value == threshold
                
                if condition_met:
                    # Get surrounding context for snippet
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    snippet = text[start:end].strip()
                    
                    formatted_message = message.replace('${value}', f'${value_str}').replace('{value}', str(value))
                    
                    flags.append({
                        'rule': rule_name,
                        'message': formatted_message,
                        'snippet': snippet
                    })
            except (ValueError, IndexError) as e:
                print(f"Error processing numeric value in rule '{rule_name}': {e}")
                continue
        
        return flags
    
    def _check_regex_absence(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Check if a required pattern is absent from the text."""
        pattern = rule.get('pattern', '')
        message = rule.get('message', 'Required pattern not found')
        rule_name = rule.get('name', 'unknown')
        
        # Check if pattern is NOT found in text
        if not re.search(pattern, text, re.IGNORECASE):
            return [{
                'rule': rule_name,
                'message': message,
                'snippet': 'Pattern not found in document'
            }]
        
        return []
    
    def _check_regex_amount(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Check for specific amounts that match a pattern and exceed threshold."""
        flags = []
        pattern = rule.get('pattern', '')
        threshold = rule.get('threshold', 0)
        operator = rule.get('operator', '>')
        message = rule.get('message', 'Amount check failed')
        rule_name = rule.get('name', 'unknown')
        
        # Find all matches in the text
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            try:
                # Extract numeric value (remove commas and convert to float)
                value_str = match.group(1).replace(',', '')
                value = float(value_str)
                
                # Check threshold condition
                condition_met = False
                if operator == '>':
                    condition_met = value > threshold
                elif operator == '<':
                    condition_met = value < threshold
                elif operator == '>=':
                    condition_met = value >= threshold
                elif operator == '<=':
                    condition_met = value <= threshold
                
                if condition_met:
                    # Get surrounding context for snippet
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    snippet = text[start:end].strip()
                    
                    formatted_message = message.replace('${value}', f'${value_str}')
                    
                    flags.append({
                        'rule': rule_name,
                        'message': formatted_message,
                        'snippet': snippet
                    })
            except (ValueError, IndexError) as e:
                print(f"Error processing amount in rule '{rule_name}': {e}")
                continue
        
        return flags