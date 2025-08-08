"""Validation service for input data."""

from typing import Optional, Dict, Any

from models.core import UserContext


class ValidationService:
    """Service for validating input data."""
    
    def validate_file_upload(self, filename: str, file_size: int, max_size: int = 50 * 1024 * 1024) -> Dict[str, Any]:
        """Validate uploaded file."""
        errors = []
        
        # Check file size
        if file_size > max_size:
            errors.append(f"File size ({file_size} bytes) exceeds maximum allowed size ({max_size} bytes)")
        
        # Check file extension
        if not filename.lower().endswith('.pdf'):
            errors.append("Only PDF files are allowed")
        
        # Check filename
        if not filename or len(filename.strip()) == 0:
            errors.append("Filename cannot be empty")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def validate_user_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user context data."""
        errors = []
        
        try:
            # Try to create UserContext object to validate structure
            context = UserContext.from_dict(context_data)
            
            # Additional business logic validation
            if context.expected_purchase_price and context.expected_purchase_price <= 0:
                errors.append("Expected purchase price must be positive")
            
            if context.expected_loan_amount and context.expected_loan_amount <= 0:
                errors.append("Expected loan amount must be positive")
            
            if context.expected_interest_rate and (context.expected_interest_rate < 0 or context.expected_interest_rate > 50):
                errors.append("Expected interest rate must be between 0% and 50%")
            
            if (context.expected_loan_amount and context.expected_purchase_price and 
                context.expected_loan_amount > context.expected_purchase_price):
                errors.append("Loan amount cannot exceed purchase price")
            
        except Exception as e:
            errors.append(f"Invalid user context data: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def validate_report_id(self, report_id: str) -> Dict[str, Any]:
        """Validate report ID format."""
        errors = []
        
        if not report_id or len(report_id.strip()) == 0:
            errors.append("Report ID cannot be empty")
        
        # Basic UUID format check (could be more strict)
        if len(report_id) < 10:
            errors.append("Report ID appears to be invalid")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def sanitize_text_input(self, text: str, max_length: int = 10000) -> str:
        """Sanitize text input by removing potentially harmful content."""
        if not text:
            return ""
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remove null bytes and other potentially problematic characters
        text = text.replace('\x00', '')
        
        return text.strip()