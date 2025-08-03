#!/usr/bin/env python3
"""
Test script to verify API compatibility between old and new implementations.
"""

import sys
import os
sys.path.insert(0, '.')

def test_rule_loading():
    """Test that both engines load the same rules."""
    print("=== Testing Rule Loading ===")
    
    # Test old engine
    try:
        from engine import RuleEngine
        old_engine = RuleEngine("rules-config.yaml")
        old_rules_count = len(old_engine.rules)
        print(f"Old engine loaded {old_rules_count} rules")
    except Exception as e:
        print(f"Old engine failed: {e}")
        old_rules_count = 0
    
    # Test new engine
    try:
        from services.rule_engine import RuleEngineService
        new_engine = RuleEngineService("rules-config.yaml")
        summary = new_engine.get_rules_summary()
        new_rules_count = summary['enabled_rules']
        print(f"New engine loaded {new_rules_count} enabled rules")
        print(f"Rules by type: {dict(summary['rules_by_type'])}")
    except Exception as e:
        print(f"New engine failed: {e}")
        new_rules_count = 0
    
    print(f"Rules count match: {old_rules_count == new_rules_count}")
    return old_rules_count == new_rules_count


def test_text_analysis():
    """Test that both engines produce similar results on sample text."""
    print("\n=== Testing Text Analysis ===")
    
    # Sample text with known issues
    sample_text = """
    Closing Disclosure
    
    Loan Amount: $450,000.00
    Total Closing Costs: $25,000.00
    Origination Fee: $8,000.00
    
    Wire Transfer: $15,000.00
    Owner's Title Insurance: $2,500.00
    """
    
    # Test old engine
    old_flags = []
    try:
        from engine import RuleEngine
        old_engine = RuleEngine("rules-config.yaml")
        old_flags = old_engine.check_text(sample_text)
        print(f"Old engine found {len(old_flags)} flags")
        for flag in old_flags[:3]:  # Show first 3
            print(f"  - {flag.get('rule', 'unknown')}: {flag.get('message', 'no message')[:50]}...")
    except Exception as e:
        print(f"Old engine analysis failed: {e}")
    
    # Test new engine
    new_flags = []
    try:
        from services.rule_engine import RuleEngineService
        new_engine = RuleEngineService("rules-config.yaml")
        new_flags = new_engine.analyze_text(sample_text)
        print(f"New engine found {len(new_flags)} flags")
        for flag in new_flags[:3]:  # Show first 3
            print(f"  - {flag.rule}: {flag.message[:50]}...")
    except Exception as e:
        print(f"New engine analysis failed: {e}")
    
    # Compare results
    flags_match = len(old_flags) == len(new_flags)
    print(f"Flag count match: {flags_match}")
    
    # Compare specific rules triggered
    old_rules = set(flag.get('rule', 'unknown') for flag in old_flags)
    new_rules = set(flag.rule for flag in new_flags)
    rules_match = old_rules == new_rules
    print(f"Triggered rules match: {rules_match}")
    if not rules_match:
        print(f"  Old rules: {old_rules}")
        print(f"  New rules: {new_rules}")
    
    return flags_match and rules_match


def test_scoring():
    """Test that scoring produces similar results."""
    print("\n=== Testing Scoring ===")
    
    # Create sample flags
    sample_flags_old = [
        {'rule': 'high_closing_costs', 'message': '🚨 Critical issue', 'snippet': 'test'},
        {'rule': 'excessive_fee', 'message': '⚠️ Warning issue', 'snippet': 'test'},
        {'rule': 'minor_issue', 'message': 'General issue', 'snippet': 'test'}
    ]
    
    # Test old scoring
    try:
        from engine import RuleEngine
        old_engine = RuleEngine("rules-config.yaml")
        old_score = old_engine.calculate_forensic_score(sample_flags_old)
        print(f"Old engine forensic score: {old_score}")
    except Exception as e:
        print(f"Old engine scoring failed: {e}")
        old_score = None
    
    # Test new scoring
    try:
        from models.flag import Flag
        from services.scoring_service import ScoringService
        
        # Convert to new flag format
        new_flags = [
            Flag(rule='high_closing_costs', message='🚨 Critical issue', snippet='test'),
            Flag(rule='excessive_fee', message='⚠️ Warning issue', snippet='test'),
            Flag(rule='minor_issue', message='General issue', snippet='test')
        ]
        
        scoring_service = ScoringService()
        new_score = scoring_service.calculate_forensic_score(new_flags)
        print(f"New engine forensic score: {new_score}")
    except Exception as e:
        print(f"New engine scoring failed: {e}")
        new_score = None
    
    if old_score is not None and new_score is not None:
        score_match = old_score == new_score
        print(f"Scores match: {score_match}")
        return score_match
    
    return False


def main():
    """Run all compatibility tests."""
    print("CloseGuard API Compatibility Test")
    print("=" * 40)
    
    tests = [
        test_rule_loading,
        test_text_analysis,
        test_scoring
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)
    
    print("\n=== Summary ===")
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ All compatibility tests passed!")
        return True
    else:
        print("❌ Some compatibility tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)