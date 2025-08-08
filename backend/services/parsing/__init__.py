"""Document parsing services for TRID closing disclosures."""

# New structured parsers
from .trid import TridParser
from .core import CoordinateExtractor, BaseParser, TextUtils

# Legacy parsers (backup)
from .legacy.document_parser_legacy import DocumentParserService

__all__ = [
    # New parsing services
    'TridParser',
    'CoordinateExtractor',
    'BaseParser', 
    'TextUtils',
    
    # Legacy service
    'DocumentParserService'
]