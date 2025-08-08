"""Forensic scoring service for analysis results."""

from typing import List

from models.core import Flag, FlagSeverity, ReportAnalytics


class ScoringService:
    """Service for calculating forensic scores and analytics."""
    
    def __init__(self, max_score: int = 100, severity_weights: dict = None):
        self.max_score = max_score
        self.severity_weights = severity_weights or {
            'high': 20,
            'medium': 10,
            'low': 5
        }
    
    def calculate_forensic_score(self, flags: List[Flag]) -> int:
        """Calculate forensic score (0-100) based on detected flags."""
        if not flags:
            return self.max_score  # Perfect score if no issues
        
        total_deductions = 0
        for flag in flags:
            if flag.severity:
                weight = self.severity_weights.get(flag.severity.value, 5)
                total_deductions += weight
        
        forensic_score = max(0, self.max_score - total_deductions)
        return forensic_score
    
    def categorize_flags_by_severity(self, flags: List[Flag]) -> dict:
        """Categorize flags by severity level."""
        severity_counts = {
            FlagSeverity.HIGH: 0,
            FlagSeverity.MEDIUM: 0,
            FlagSeverity.LOW: 0
        }
        
        for flag in flags:
            if flag.severity:
                severity_counts[flag.severity] += 1
        
        return {
            'high': severity_counts[FlagSeverity.HIGH],
            'medium': severity_counts[FlagSeverity.MEDIUM],
            'low': severity_counts[FlagSeverity.LOW]
        }
    
    def create_analytics(self, flags: List[Flag]) -> ReportAnalytics:
        """Create complete analytics from flags."""
        severity_counts = self.categorize_flags_by_severity(flags)
        forensic_score = self.calculate_forensic_score(flags)
        
        return ReportAnalytics(
            forensic_score=forensic_score,
            total_flags=len(flags),
            high_severity=severity_counts['high'],
            medium_severity=severity_counts['medium'],
            low_severity=severity_counts['low']
        )
    
    def get_risk_level(self, forensic_score: int) -> str:
        """Get risk level based on forensic score."""
        if forensic_score >= 70:
            return "LOW"
        elif forensic_score >= 30:
            return "MODERATE"
        else:
            return "HIGH"