import os
from typing import Dict, Any, Optional, List
from pydantic import BaseSettings, Field, ConfigDict
from functools import lru_cache
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # App information
    APP_NAME: str = "OpenSearchEval"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A comprehensive search evaluation platform with agent architecture"
    
    # API settings
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    API_ROOT_PATH: str = Field("", env="API_ROOT_PATH")
    
    # UI settings
    UI_HOST: str = Field(default="0.0.0.0", env="UI_HOST")
    UI_PORT: int = Field(default=5000, env="UI_PORT")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")
    
    # Database
    DB_URL: Optional[str] = Field(default=None, env="DB_URL")
    DB_TYPE: str = Field(default="sqlite", env="DB_TYPE")
    DB_POOL_SIZE: int = Field(default=10, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=20, env="DB_MAX_OVERFLOW")
    
    # LLM settings
    LLM_MODEL: str = Field(default="gpt-4-turbo", env="LLM_MODEL")
    LLM_ENDPOINT: str = Field(
        default="https://api.openai.com/v1/chat/completions", 
        env="LLM_ENDPOINT"
    )
    LLM_API_KEY: str = Field(default="", env="LLM_API_KEY")
    LLM_TEMPERATURE: float = Field(default=0.1, env="LLM_TEMPERATURE")
    LLM_MAX_TOKENS: int = Field(default=1000, env="LLM_MAX_TOKENS")
    LLM_TIMEOUT: int = Field(default=30, env="LLM_TIMEOUT")
    
    # MLX settings
    USE_MLX: bool = Field(default=True, env="USE_MLX")
    MLX_MODEL_PATH: Optional[str] = Field(default=None, env="MLX_MODEL_PATH")
    MLX_BATCH_SIZE: int = Field(default=32, env="MLX_BATCH_SIZE")
    
    # Embedding settings
    EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002", env="EMBEDDING_MODEL")
    EMBEDDING_DIMENSION: int = Field(default=1536, env="EMBEDDING_DIMENSION")
    EMBEDDING_CACHE_SIZE: int = Field(default=10000, env="EMBEDDING_CACHE_SIZE")
    
    # Storage paths
    EXPERIMENTS_PATH: str = Field(default="./experiments", env="EXPERIMENTS_PATH")
    DATA_PATH: str = Field(default="./data", env="DATA_PATH")
    MODEL_PATH: str = Field(default="./models", env="MODEL_PATH")
    LOG_PATH: str = Field(default="./logs", env="LOG_PATH")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    CORS_METHODS: List[str] = Field(default=["*"], env="CORS_METHODS")
    CORS_HEADERS: List[str] = Field(default=["*"], env="CORS_HEADERS")
    
    # Redis settings (for caching)
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # Experiment settings
    DEFAULT_EXPERIMENT_CONFIDENCE_LEVEL: float = Field(default=0.95, env="DEFAULT_EXPERIMENT_CONFIDENCE_LEVEL")
    MAX_EXPERIMENT_DURATION_DAYS: int = Field(default=30, env="MAX_EXPERIMENT_DURATION_DAYS")
    MIN_SAMPLE_SIZE: int = Field(default=100, env="MIN_SAMPLE_SIZE")
    
    # Agent settings
    AGENT_POOL_SIZE: int = Field(default=5, env="AGENT_POOL_SIZE")
    AGENT_TIMEOUT: int = Field(default=300, env="AGENT_TIMEOUT")
    AGENT_MAX_RETRIES: int = Field(default=3, env="AGENT_MAX_RETRIES")
    
    # Metrics settings
    METRICS_RETENTION_DAYS: int = Field(default=90, env="METRICS_RETENTION_DAYS")
    METRICS_AGGREGATION_INTERVAL: int = Field(default=3600, env="METRICS_AGGREGATION_INTERVAL")  # seconds
    
    # Performance settings
    ENABLE_CACHING: bool = Field(default=True, env="ENABLE_CACHING")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # seconds
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    
    # Monitoring settings
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    HEALTH_CHECK_INTERVAL: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    # Data processing settings
    BATCH_SIZE: int = Field(default=1000, env="BATCH_SIZE")
    MAX_WORKERS: int = Field(default=4, env="MAX_WORKERS")
    CHUNK_SIZE: int = Field(default=10000, env="CHUNK_SIZE")
    
    # Search settings
    DEFAULT_SEARCH_LIMIT: int = Field(default=50, env="DEFAULT_SEARCH_LIMIT")
    MAX_SEARCH_RESULTS: int = Field(default=1000, env="MAX_SEARCH_RESULTS")
    SEARCH_TIMEOUT: int = Field(default=30, env="SEARCH_TIMEOUT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
    def model_post_init(self, __context):
        """Create required directories after initialization"""
        for path in [self.DATA_PATH, self.MODEL_PATH, self.LOG_PATH, self.EXPERIMENTS_PATH]:
            os.makedirs(path, exist_ok=True)
            
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
        
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"
        
    @property
    def database_url(self) -> str:
        """Get database URL"""
        if self.DB_URL:
            return self.DB_URL
        elif self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.DATA_PATH}/opensearcheval.db"
        else:
            return f"{self.DB_TYPE}://localhost/opensearcheval"
            
    @property
    def redis_url(self) -> str:
        """Get Redis URL"""
        if self.REDIS_URL:
            return self.REDIS_URL
        else:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached)
    
    Returns:
        Settings instance
    """
    return Settings()

# Create default environment file if it doesn't exist
def create_default_env_file():
    """Create a default .env file with example values"""
    env_file_path = ".env"
    
    if not os.path.exists(env_file_path):
        default_env = """# OpenSearchEval Configuration

# Application
APP_NAME=OpenSearchEval
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

# API
API_HOST=0.0.0.0
API_PORT=8000

# UI
UI_HOST=0.0.0.0
UI_PORT=5000

# Logging
LOG_LEVEL=INFO

# Database
DB_TYPE=sqlite
DB_URL=

# LLM
LLM_MODEL=gpt-4-turbo
LLM_API_KEY=your-openai-api-key
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000

# MLX
USE_MLX=true
MLX_MODEL_PATH=

# Embedding
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSION=1536

# Storage
DATA_PATH=./data
MODEL_PATH=./models
LOG_PATH=./logs
EXPERIMENTS_PATH=./experiments

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Experiments
DEFAULT_EXPERIMENT_CONFIDENCE_LEVEL=0.95
MIN_SAMPLE_SIZE=100

# Performance
ENABLE_CACHING=true
CACHE_TTL=3600
MAX_CONCURRENT_REQUESTS=100
"""
        
        with open(env_file_path, 'w') as f:
            f.write(default_env)
            
        logging.info(f"Created default .env file at {env_file_path}")

# Create default directories and environment file
if __name__ == "__main__":
    create_default_env_file()
    settings = get_settings()
    logging.info("Configuration loaded successfully")