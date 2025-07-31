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
        flagged_rules = set()  # Track which rules have already been flagged
        
        for rule in self.rules:
            try:
                rule_name = rule.get('name', 'unknown')
                
                # Skip if this rule has already been flagged
                if rule_name in flagged_rules:
                    continue
                    
                rule_flags = self._apply_rule(rule, text)
                
                # If this rule found any flags, add the first one and mark rule as flagged
                if rule_flags:
                    flags.append(rule_flags[0])  # Only take the first match
                    flagged_rules.add(rule_name)
                    
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
        elif rule_type == 'calculated_percentage':
            return self._check_calculated_percentage(rule, text)
        elif rule_type == 'compound_rule':
            return self._check_compound_rule(rule, text)
        elif rule_type == 'cross_reference_pattern':
            return self._check_cross_reference_pattern(rule, text)
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
    
    def _check_calculated_percentage(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Calculate percentage from two extracted values and check against threshold."""
        flags = []
        numerator_pattern = rule.get('numerator_pattern', '')
        denominator_pattern = rule.get('denominator_pattern', '')
        threshold = rule.get('threshold', 0)
        operator = rule.get('operator', '>')
        message = rule.get('message', 'Percentage check failed')
        rule_name = rule.get('name', 'unknown')
        
        try:
            # Extract numerator (e.g., origination fee amount)
            numerator_match = re.search(numerator_pattern, text, re.IGNORECASE)
            if not numerator_match:
                return []
            
            numerator_str = numerator_match.group(1).replace(',', '')
            numerator = float(numerator_str)
            
            # Extract denominator (e.g., loan amount)
            denominator_match = re.search(denominator_pattern, text, re.IGNORECASE)
            if not denominator_match:
                return []
            
            denominator_str = denominator_match.group(1).replace(',', '')
            denominator = float(denominator_str)
            
            # Avoid division by zero
            if denominator == 0:
                print(f"Division by zero in rule '{rule_name}': denominator is 0")
                return []
            
            # Calculate percentage
            percentage = (numerator / denominator) * 100
            
            # Check threshold condition
            condition_met = False
            if operator == '>':
                condition_met = percentage > threshold
            elif operator == '<':
                condition_met = percentage < threshold
            elif operator == '>=':
                condition_met = percentage >= threshold
            elif operator == '<=':
                condition_met = percentage <= threshold
            elif operator == '==':
                condition_met = percentage == threshold
            
            if condition_met:
                # Get context around both matches
                start1 = max(0, numerator_match.start() - 30)
                end1 = min(len(text), numerator_match.end() + 30)
                snippet1 = text[start1:end1].strip()
                
                start2 = max(0, denominator_match.start() - 30)
                end2 = min(len(text), denominator_match.end() + 30)
                snippet2 = text[start2:end2].strip()
                
                snippet = f"Numerator: {snippet1} | Denominator: {snippet2}"
                
                formatted_message = message.replace('{percentage}', f'{percentage:.2f}').replace('{numerator}', f'${numerator_str}').replace('{denominator}', f'${denominator_str}')
                
                flags.append({
                    'rule': rule_name,
                    'message': formatted_message,
                    'snippet': snippet
                })
        
        except (ValueError, IndexError) as e:
            print(f"Error calculating percentage in rule '{rule_name}': {e}")
        
        return flags
    
    def _check_compound_rule(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Check multiple conditions that must all be met."""
        conditions = rule.get('conditions', [])
        message = rule.get('message', 'Compound condition met')
        rule_name = rule.get('name', 'unknown')
        
        if not conditions:
            return []
        
        condition_results = []
        extracted_values = {}
        
        # Check each condition
        for i, condition in enumerate(conditions):
            pattern = condition.get('pattern', '')
            threshold = condition.get('threshold', 0)
            operator = condition.get('operator', '>')
            value_name = condition.get('value_name', f'value{i+1}')
            
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                return []  # All conditions must have matches
            
            try:
                value_str = match.group(1).replace(',', '')
                value = float(value_str)
                extracted_values[value_name] = value
                
                # Check condition
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
                
                condition_results.append(condition_met)
                
            except (ValueError, IndexError) as e:
                print(f"Error processing condition {i+1} in compound rule '{rule_name}': {e}")
                return []
        
        # All conditions must be met
        if all(condition_results):
            # Format message with extracted values
            formatted_message = message
            for value_name, value in extracted_values.items():
                formatted_message = formatted_message.replace(f'{{{value_name}}}', str(value))
            
            return [{
                'rule': rule_name,
                'message': formatted_message,
                'snippet': f"Multiple conditions met: {', '.join([f'{k}={v}' for k, v in extracted_values.items()])}"
            }]
        
        return []
    
    def _check_cross_reference_pattern(self, rule: Dict[str, Any], text: str) -> List[Dict[str, str]]:
        """Check if related fields contain similar company names."""
        primary_pattern = rule.get('primary_pattern', '')
        secondary_patterns = rule.get('secondary_patterns', [])
        message = rule.get('message', 'Cross-reference match found')
        rule_name = rule.get('name', 'unknown')
        fuzzy_match = rule.get('fuzzy_match', True)
        
        # Extract primary value (e.g., seller name)
        primary_match = re.search(primary_pattern, text, re.IGNORECASE)
        if not primary_match:
            return []
        
        primary_value = primary_match.group(1).strip().upper()
        
        # Extract key words from primary value for fuzzy matching
        if fuzzy_match:
            primary_keywords = set(re.findall(r'\b[A-Z]{2,}\b', primary_value))
            if not primary_keywords:
                # Fallback to all words if no all-caps words found
                primary_keywords = set(word.upper() for word in primary_value.split() if len(word) > 2)
        
        matched_services = []
        
        # Check each secondary pattern (e.g., lender, insurance company)
        for secondary_info in secondary_patterns:
            pattern = secondary_info.get('pattern', '')
            service_name = secondary_info.get('service', 'service')
            
            secondary_match = re.search(pattern, text, re.IGNORECASE)
            if secondary_match:
                secondary_value = secondary_match.group(1).strip().upper()
                
                # Check for match
                match_found = False
                if fuzzy_match:
                    # Check if any primary keywords appear in secondary value
                    for keyword in primary_keywords:
                        if keyword in secondary_value:
                            match_found = True
                            break
                else:
                    # Exact match
                    match_found = primary_value == secondary_value
                
                if match_found:
                    matched_services.append(service_name)
        
        if matched_services:
            services_text = ', '.join(matched_services)
            formatted_message = message.replace('{primary}', primary_value).replace('{services}', services_text)
            
            return [{
                'rule': rule_name,
                'message': formatted_message,
                'snippet': f"Primary: {primary_value} | Matched services: {services_text}"
            }]
        
        return []