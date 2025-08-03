"""Application settings and configuration."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application configuration settings."""
    
    # API Configuration
    api_title: str = "CloseGuard API"
    api_description: str = "Backend for analyzing home-closing PDFs"
    api_version: str = "1.0.0"
    
    # CORS Settings
    allow_origins: list = None
    allow_credentials: bool = True
    allow_methods: list = None
    allow_headers: list = None
    
    # File Processing
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: list = None
    temp_dir: str = "/tmp"
    
    # Rules Configuration
    rules_config_path: str = "rules-config.yaml"
    
    # Scoring Configuration
    max_forensic_score: int = 100
    severity_weights: dict = None
    
    def __post_init__(self):
        """Set default values for list/dict fields."""
        if self.allow_origins is None:
            self.allow_origins = ["*"]  # TODO: Restrict in production
        
        if self.allow_methods is None:
            self.allow_methods = ["*"]
        
        if self.allow_headers is None:
            self.allow_headers = ["*"]
        
        if self.allowed_file_types is None:
            self.allowed_file_types = [".pdf"]
        
        if self.severity_weights is None:
            self.severity_weights = {
                'high': 20,
                'medium': 10,
                'low': 5
            }
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables."""
        return cls(
            api_title=os.getenv('API_TITLE', cls.api_title),
            api_description=os.getenv('API_DESCRIPTION', cls.api_description),
            api_version=os.getenv('API_VERSION', cls.api_version),
            max_file_size=int(os.getenv('MAX_FILE_SIZE', cls.max_file_size)),
            temp_dir=os.getenv('TEMP_DIR', cls.temp_dir),
            rules_config_path=os.getenv('RULES_CONFIG_PATH', cls.rules_config_path)
        )