"""Rules configuration loader."""

import yaml
from typing import List
from pathlib import Path

from models.core import Rule


class RulesLoader:
    """Loads and manages rule configurations."""
    
    def __init__(self, config_path: str = "rules-config.yaml"):
        self.config_path = config_path
    
    def load_rules(self) -> List[Rule]:
        """Load rules from YAML configuration file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Rules configuration file not found: {self.config_path}")
            
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                rules_data = config.get('rules', [])
                
                rules = []
                for rule_data in rules_data:
                    try:
                        rule = Rule.from_dict(rule_data)
                        rules.append(rule)
                    except Exception as e:
                        print(f"Warning: Failed to load rule '{rule_data.get('name', 'unknown')}': {e}")
                        continue
                
                return rules
                
        except Exception as e:
            raise Exception(f"Failed to load rules configuration: {e}")
    
    def get_enabled_rules(self) -> List[Rule]:
        """Get only enabled rules."""
        all_rules = self.load_rules()
        return [rule for rule in all_rules if rule.enabled]
    
    def get_rules_by_type(self, rule_type: str) -> List[Rule]:
        """Get rules filtered by type."""
        all_rules = self.load_rules()
        return [rule for rule in all_rules if rule.rule_type.value == rule_type]