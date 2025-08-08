"""Core parsing infrastructure and utilities."""

from .base_parser import BaseParser
from .coordinate_extractor import CoordinateExtractor
from .text_utils import TextUtils
from .checkbox_detector import CheckboxDetector

__all__ = [
    'BaseParser',
    'CoordinateExtractor', 
    'TextUtils',
    'CheckboxDetector'
]