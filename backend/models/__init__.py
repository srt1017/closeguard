"""Data models for CloseGuard application."""

# Core business models
from .core import (
    Flag, FlagSeverity,
    Report, ReportAnalytics, ReportMetadata,
    UserContext,
    Rule, RuleType
)

# Document parsing models
from .document import (
    CoordinatePosition,
    PaymentResponsibility, CostCategory, DocumentSection,
    ClosingDisclosureLineItem,
    LoanSummary,
    ParsedDocument
)

# Analysis models (future)
from .analysis import *

__all__ = [
    # Core models
    'Flag',
    'FlagSeverity', 
    'Report',
    'ReportAnalytics',
    'ReportMetadata',
    'UserContext',
    'Rule',
    'RuleType',
    
    # Document parsing models
    'CoordinatePosition',
    'PaymentResponsibility',
    'CostCategory', 
    'DocumentSection',
    'ClosingDisclosureLineItem',
    'LoanSummary',
    'ParsedDocument'
]