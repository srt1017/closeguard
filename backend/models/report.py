"""Report data models for analysis results."""

from typing import List, Optional
from dataclasses import dataclass
from .flag import Flag, FlagSeverity


@dataclass
class ReportMetadata:
    """Metadata about the analyzed document."""
    
    filename: str
    text_length: int
    upload_timestamp: Optional[str] = None
    processing_time: Optional[float] = None


@dataclass 
class ReportAnalytics:
    """Analytics and scoring for a report."""
    
    forensic_score: int
    total_flags: int
    high_severity: int = 0
    medium_severity: int = 0
    low_severity: int = 0
    
    def __post_init__(self):
        """Validate analytics data."""
        if self.forensic_score < 0 or self.forensic_score > 100:
            raise ValueError("Forensic score must be between 0 and 100")
        
        if self.total_flags != (self.high_severity + self.medium_severity + self.low_severity):
            # Auto-calculate if not provided correctly
            pass


@dataclass
class Report:
    """Complete analysis report for a document."""
    
    id: str
    status: str
    flags: List[Flag]
    analytics: Optional[ReportAnalytics] = None
    metadata: Optional[ReportMetadata] = None
    
    def calculate_analytics(self) -> ReportAnalytics:
        """Calculate analytics from flags."""
        severity_counts = {
            FlagSeverity.HIGH: 0,
            FlagSeverity.MEDIUM: 0, 
            FlagSeverity.LOW: 0
        }
        
        for flag in self.flags:
            if flag.severity:
                severity_counts[flag.severity] += 1
        
        # Calculate forensic score
        severity_weights = {
            FlagSeverity.HIGH: 20,
            FlagSeverity.MEDIUM: 10,
            FlagSeverity.LOW: 5
        }
        
        total_deductions = sum(
            count * severity_weights[severity] 
            for severity, count in severity_counts.items()
        )
        
        forensic_score = max(0, 100 - total_deductions)
        
        analytics = ReportAnalytics(
            forensic_score=forensic_score,
            total_flags=len(self.flags),
            high_severity=severity_counts[FlagSeverity.HIGH],
            medium_severity=severity_counts[FlagSeverity.MEDIUM],
            low_severity=severity_counts[FlagSeverity.LOW]
        )
        
        self.analytics = analytics
        return analytics
    
    def to_dict(self) -> dict:
        """Convert report to dictionary format for API responses."""
        return {
            'id': self.id,
            'status': self.status,
            'flags': [flag.to_dict() for flag in self.flags],
            'analytics': {
                'forensic_score': self.analytics.forensic_score,
                'total_flags': self.analytics.total_flags,
                'high_severity': self.analytics.high_severity,
                'medium_severity': self.analytics.medium_severity,
                'low_severity': self.analytics.low_severity
            } if self.analytics else None,
            'metadata': {
                'filename': self.metadata.filename,
                'text_length': self.metadata.text_length,
                'upload_timestamp': self.metadata.upload_timestamp,
                'processing_time': self.metadata.processing_time
            } if self.metadata else None
        }