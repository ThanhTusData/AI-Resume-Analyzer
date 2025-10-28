"""
Application Configuration
Centralizes all configuration settings
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class AppConfig(BaseSettings):
    """Main application configuration"""
    
    # ==================== Application Settings ====================
    APP_NAME: str = Field(default="AI Resume Analyzer", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # ==================== API Keys ====================
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # ==================== LinkedIn Credentials ====================
    LINKEDIN_EMAIL: Optional[str] = Field(default=None, env="LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD: Optional[str] = Field(default=None, env="LINKEDIN_PASSWORD")
    LINKEDIN_SESSION_COOKIE: Optional[str] = Field(default=None, env="LINKEDIN_SESSION_COOKIE")
    
    # ==================== Database ====================
    DATABASE_URL: str = Field(
        default="sqlite:///./data/resume_analyzer.db",
        env="DATABASE_URL"
    )
    
    # ==================== Redis ====================
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_ENABLED: bool = Field(default=False, env="REDIS_ENABLED")
    
    # ==================== Security ====================
    SECRET_KEY: str = Field(default="change-this-secret-key", env="SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION_MINUTES: int = Field(default=60, env="JWT_EXPIRATION_MINUTES")
    
    # ==================== Scraper Settings ====================
    SCRAPER_HEADLESS: bool = Field(default=True, env="SCRAPER_HEADLESS")
    SCRAPER_TIMEOUT: int = Field(default=30, env="SCRAPER_TIMEOUT")
    SCRAPER_MAX_RETRIES: int = Field(default=3, env="SCRAPER_MAX_RETRIES")
    SCRAPER_DELAY_MIN: int = Field(default=2, env="SCRAPER_DELAY_MIN")
    SCRAPER_DELAY_MAX: int = Field(default=5, env="SCRAPER_DELAY_MAX")
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="USER_AGENT"
    )
    
    # ==================== File Upload ====================
    MAX_UPLOAD_SIZE_MB: int = Field(default=10, env="MAX_UPLOAD_SIZE_MB")
    ALLOWED_EXTENSIONS: str = Field(
        default="pdf,docx,doc,txt,png,jpg,jpeg",
        env="ALLOWED_EXTENSIONS"
    )
    UPLOAD_FOLDER: str = Field(default="./data/uploads", env="UPLOAD_FOLDER")
    
    # ==================== AI Settings ====================
    AI_PROVIDER: str = Field(default="openai", env="AI_PROVIDER")
    AI_TEMPERATURE: float = Field(default=0.7, env="AI_TEMPERATURE")
    AI_MAX_TOKENS: int = Field(default=2000, env="AI_MAX_TOKENS")
    EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-small",
        env="EMBEDDING_MODEL"
    )
    EMBEDDING_DIMENSION: int = Field(default=1536, env="EMBEDDING_DIMENSION")
    
    # ==================== Vector Store ====================
    VECTOR_STORE_TYPE: str = Field(default="faiss", env="VECTOR_STORE_TYPE")
    VECTOR_STORE_PATH: str = Field(
        default="./data/vector_stores",
        env="VECTOR_STORE_PATH"
    )
    SIMILARITY_THRESHOLD: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")
    
    # ==================== Email Configuration ====================
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(
        default="noreply@resumeanalyzer.com",
        env="SMTP_FROM_EMAIL"
    )
    
    # ==================== Rate Limiting ====================
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # ==================== Cache ====================
    CACHE_TTL_SECONDS: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    CACHE_MAX_SIZE: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # ==================== Feature Flags ====================
    ENABLE_JOB_SCRAPING: bool = Field(default=True, env="ENABLE_JOB_SCRAPING")
    ENABLE_RESUME_ANALYSIS: bool = Field(default=True, env="ENABLE_RESUME_ANALYSIS")
    ENABLE_JOB_MATCHING: bool = Field(default=True, env="ENABLE_JOB_MATCHING")
    ENABLE_EMAIL_NOTIFICATIONS: bool = Field(default=False, env="ENABLE_EMAIL_NOTIFICATIONS")
    ENABLE_API: bool = Field(default=True, env="ENABLE_API")
    
    # ==================== Paths ====================
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    @validator('ALLOWED_EXTENSIONS')
    def parse_extensions(cls, v):
        """Parse comma-separated extensions into a list"""
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(',')]
        return v
    
    @validator('DATA_DIR', 'LOGS_DIR', always=True)
    def create_directories(cls, v):
        """Ensure directories exist"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    def get_upload_path(self, filename: str) -> Path:
        """Get full path for uploaded file"""
        upload_dir = Path(self.UPLOAD_FOLDER)
        upload_dir.mkdir(parents=True, exist_ok=True)
        return upload_dir / filename
    
    def is_allowed_extension(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return ext in self.ALLOWED_EXTENSIONS
    
    def get_vector_store_path(self, name: str) -> Path:
        """Get path for vector store"""
        vector_dir = Path(self.VECTOR_STORE_PATH)
        vector_dir.mkdir(parents=True, exist_ok=True)
        return vector_dir / name
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create configuration singleton"""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


# Export for easy import
config = get_config()