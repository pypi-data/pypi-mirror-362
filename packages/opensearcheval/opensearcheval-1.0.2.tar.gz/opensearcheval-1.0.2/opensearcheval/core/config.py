import os
from typing import Dict, Any, Optional, List
from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_ROOT_PATH: str = ""
    
    # UI settings
    UI_HOST: str = "0.0.0.0"
    UI_PORT: int = 5000
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Database
    DB_URL: Optional[str] = None
    DB_TYPE: str = "sqlite"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # LLM settings
    LLM_MODEL: str = "gpt-4-turbo"
    LLM_ENDPOINT: str = "https://api.openai.com/v1/chat/completions"
    LLM_API_KEY: str = ""
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 1000
    LLM_TIMEOUT: int = 30
    
    # MLX settings
    USE_MLX: bool = True
    MLX_MODEL_PATH: Optional[str] = None
    MLX_BATCH_SIZE: int = 32
    
    # Embedding settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSIONS: int = 1536
    EMBEDDING_BATCH_SIZE: int = 100
    
    # Caching
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600
    ENABLE_CACHING: bool = True
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    METRICS_PATH: str = "/metrics"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    CORS_ORIGINS: List[str] = ["*"]
    
    # File paths
    DATA_DIR: str = "./data"
    MODELS_DIR: str = "./models"
    LOGS_DIR: str = "./logs"
    
    # Experiment settings
    DEFAULT_EXPERIMENT_DURATION: int = 7  # days
    MIN_SAMPLE_SIZE: int = 1000
    SIGNIFICANCE_LEVEL: float = 0.05
    
    # Performance
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 100
    REQUEST_TIMEOUT: int = 30
    
    # Feature flags
    ENABLE_AB_TESTING: bool = True
    ENABLE_LLM_JUDGE: bool = True
    ENABLE_REAL_TIME_METRICS: bool = True
    ENABLE_ADVANCED_ANALYTICS: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
    @property
    def database_url(self) -> str:
        """Get database URL with fallback"""
        if self.DB_URL:
            return self.DB_URL
        
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.DATA_DIR}/opensearcheval.db"
        elif self.DB_TYPE == "postgresql":
            return "postgresql://user:password@localhost/opensearcheval"
        elif self.DB_TYPE == "mysql":
            return "mysql://user:password@localhost/opensearcheval"
        else:
            return f"sqlite:///{self.DATA_DIR}/opensearcheval.db"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT.lower() == "development"
    
    def get_log_level(self) -> int:
        """Get logging level as integer"""
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins"""
        return self.CORS_ORIGINS
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate settings and return validation results"""
        issues = []
        
        # Check required API key for LLM
        if self.ENABLE_LLM_JUDGE and not self.LLM_API_KEY:
            issues.append("LLM_API_KEY is required when ENABLE_LLM_JUDGE is True")
        
        # Check MLX settings
        if self.USE_MLX and not self.MLX_MODEL_PATH:
            issues.append("MLX_MODEL_PATH is required when USE_MLX is True")
        
        # Check database settings
        if self.DB_TYPE not in ["sqlite", "postgresql", "mysql"]:
            issues.append(f"Unsupported database type: {self.DB_TYPE}")
        
        # Check directories exist
        for dir_path in [self.DATA_DIR, self.MODELS_DIR, self.LOGS_DIR]:
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path, exist_ok=True)
                except Exception as e:
                    issues.append(f"Cannot create directory {dir_path}: {e}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.get_log_level(),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{settings.LOGS_DIR}/opensearcheval.log")
    ]
)

logger = logging.getLogger(__name__)

# Validate settings on import
validation_result = settings.validate_settings()
if not validation_result["valid"]:
    logger.warning(f"Settings validation issues: {validation_result['issues']}")