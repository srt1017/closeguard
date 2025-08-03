"""Context-aware rule handlers that use user-provided context."""

import re
from typing import List, Optional

from models.rule import Rule, RuleType
from models.flag import Flag
from models.user_context import UserContext
from .base_rule import BaseRuleHandler


class ContextComparisonHandler(BaseRuleHandler):
    """Handler for context comparison rules that compare document content with user expectations."""
    
    def can_handle(self, rule: Rule) -> bool:
        """Check if this handler can process the given rule."""
        return rule.rule_type == RuleType.CONTEXT_COMPARISON
    
    def process_rule(self, rule: Rule, text: str, context: Optional[UserContext] = None) -> List[Flag]:
        """Process context comparison rule."""
        if not context:
            return []  # Cannot process without user context
        
        comparison_type = rule.config.get('comparison_type', '')
        
        if comparison_type == 'price_mismatch':
            return self._check_price_mismatch(rule, text, context)
        elif comparison_type == 'loan_amount_mismatch':
            return self._check_loan_amount_mismatch(rule, text, context)
        elif comparison_type == 'broken_promise':
            return self._check_broken_promise(rule, text, context)
        elif comparison_type == 'unexpected_charge':
            return self._check_unexpected_charge(rule, text, context)
        else:
            return []
    
    def _check_price_mismatch(self, rule: Rule, text: str, context: UserContext) -> List[Flag]:
        """Check for purchase price mismatches."""
        if not context.expected_purchase_price:
            return []
        
        pattern = rule.config.get('pattern', r'(?:Sale Price|Purchase Price).*?\$([0-9,]+(?:\.[0-9]{2})?)')
        tolerance_percent = rule.config.get('tolerance_percent', 5.0)
        
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                document_price = float(match.group(1).replace(',', ''))
                expected_price = context.expected_purchase_price
                
                # Calculate percentage difference
                diff_percent = abs(document_price - expected_price) / expected_price * 100
                
                if diff_percent > tolerance_percent:
                    snippet = self.extract_snippet(text, match.start(), match.end())
                    formatted_message = self.format_message(
                        rule.message,
                        document_price=document_price,
                        expected_price=expected_price,
                        difference=abs(document_price - expected_price)
                    )
                    
                    return [Flag(
                        rule=rule.name,
                        message=formatted_message,
                        snippet=snippet
                    )]
            except (ValueError, IndexError):
                pass
        
        return []
    
    def _check_loan_amount_mismatch(self, rule: Rule, text: str, context: UserContext) -> List[Flag]:
        """Check for loan amount mismatches."""
        if not context.expected_loan_amount:
            return []
        
        pattern = rule.config.get('pattern', r'Loan Amount.*?\$([0-9,]+(?:\.[0-9]{2})?)')
        tolerance_percent = rule.config.get('tolerance_percent', 5.0)
        
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                document_amount = float(match.group(1).replace(',', ''))
                expected_amount = context.expected_loan_amount
                
                # Calculate percentage difference
                diff_percent = abs(document_amount - expected_amount) / expected_amount * 100
                
                if diff_percent > tolerance_percent:
                    snippet = self.extract_snippet(text, match.start(), match.end())
                    formatted_message = self.format_message(
                        rule.message,
                        document_amount=document_amount,
                        expected_amount=expected_amount,
                        difference=abs(document_amount - expected_amount)
                    )
                    
                    return [Flag(
                        rule=rule.name,
                        message=formatted_message,
                        snippet=snippet
                    )]
            except (ValueError, IndexError):
                pass
        
        return []
    
    def _check_broken_promise(self, rule: Rule, text: str, context: UserContext) -> List[Flag]:
        """Check for broken promises based on user context."""
        promise_type = rule.config.get('promise_type', '')
        
        if promise_type == 'zero_closing_costs' and context.promised_zero_closing_costs:
            return self._check_zero_closing_costs_promise(rule, text)
        elif promise_type == 'title_fees' and context.builder_promised_to_cover_title_fees:
            return self._check_title_fees_promise(rule, text)
        elif promise_type == 'escrow_fees' and context.builder_promised_to_cover_escrow_fees:
            return self._check_escrow_fees_promise(rule, text)
        
        return []
    
    def _check_zero_closing_costs_promise(self, rule: Rule, text: str) -> List[Flag]:
        """Check if zero closing costs promise was broken."""
        # Look for closing costs charges
        pattern = r'(?:Total Closing Costs|closing costs?).*?\$([0-9,]+(?:\.[0-9]{2})?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            try:
                amount = float(match.group(1).replace(',', ''))
                if amount > 100:  # Allow small fees but not significant costs
                    snippet = self.extract_snippet(text, match.start(), match.end())
                    formatted_message = self.format_message(rule.message, amount=amount)
                    
                    return [Flag(
                        rule=rule.name,
                        message=formatted_message,
                        snippet=snippet
                    )]
            except (ValueError, IndexError):
                pass
        
        return []
    
    def _check_title_fees_promise(self, rule: Rule, text: str) -> List[Flag]:
        """Check if title fees promise was broken."""
        pattern = r'(?:Owner.*?Title Insurance|Title.*?Policy).*?\$([0-9,]+(?:\.[0-9]{2})?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            snippet = self.extract_snippet(text, match.start(), match.end())
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet=snippet
            )]
        
        return []
    
    def _check_escrow_fees_promise(self, rule: Rule, text: str) -> List[Flag]:
        """Check if escrow fees promise was broken."""
        pattern = r'(?:Escrow|Settlement).*?Fee.*?\$([0-9,]+(?:\.[0-9]{2})?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            snippet = self.extract_snippet(text, match.start(), match.end())
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet=snippet
            )]
        
        return []
    
    def _check_unexpected_charge(self, rule: Rule, text: str, context: UserContext) -> List[Flag]:
        """Check for unexpected charges based on Texas market norms."""
        charge_type = rule.config.get('charge_type', '')
        pattern = rule.config.get('pattern', '')
        
        if not pattern:
            return []
        
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            snippet = self.extract_snippet(text, match.start(), match.end())
            return [Flag(
                rule=rule.name,
                message=rule.message,
                snippet=snippet
            )]
        
        return []