"""
Configuration module for Echo Sync Protocol.
"""
from typing import Optional, Dict, Any, List
from pydantic import Field
from pydantic_settings import BaseSettings
import os
from pathlib import Path

class DatabaseSettings(BaseSettings):
    """Database connection settings."""
    host: str = Field(default="localhost", env="ECHO_DB_HOST")
    port: int = Field(default=5432, env="ECHO_DB_PORT")
    database: str = Field(default="echo_sync", env="ECHO_DB_NAME")
    user: str = Field(default="postgres", env="ECHO_DB_USER")
    password: str = Field(default="", env="ECHO_DB_PASSWORD")
    pool_size: int = Field(default=5, env="ECHO_DB_POOL_SIZE")
    max_overflow: int = Field(default=10, env="ECHO_DB_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="ECHO_DB_ECHO")

    @property
    def connection_string(self) -> str:
        """Get database connection string."""
        url = os.getenv("ECHO_DB_URL")
        if url:
            return url
        return f"sqlite:///echo_sync.db"

class SyncSettings(BaseSettings):
    """Echo Sync Protocol settings."""
    # Node settings
    node_id: str = Field(default="", env="ECHO_NODE_ID")
    node_name: str = Field(default="", env="ECHO_NODE_NAME")
    
    # Sync settings
    sync_interval: int = Field(default=60, env="ECHO_SYNC_INTERVAL")
    max_retries: int = Field(default=3, env="ECHO_MAX_RETRIES")
    retry_delay: int = Field(default=5, env="ECHO_RETRY_DELAY")
    
    # Conflict resolution
    default_resolution_strategy: str = Field(
        default="merge",
        env="ECHO_DEFAULT_RESOLUTION_STRATEGY"
    )
    
    # State management
    state_retention_days: int = Field(default=30, env="ECHO_STATE_RETENTION_DAYS")
    max_state_size_mb: int = Field(default=10, env="ECHO_MAX_STATE_SIZE_MB")
    
    # Security
    jwt_secret: str = Field(default="", env="ECHO_JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="ECHO_JWT_ALGORITHM")
    jwt_expiry_minutes: int = Field(default=60, env="ECHO_JWT_EXPIRY_MINUTES")
    
    # Monitoring
    enable_metrics: bool = Field(default=False, env="ECHO_ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="ECHO_METRICS_PORT")
    
    # Logging
    log_level: str = Field(default="INFO", env="ECHO_LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="ECHO_LOG_FILE")

    # Replay/Visualization tool
    enable_replay_tool: bool = Field(default=False, env="ECHO_ENABLE_REPLAY_TOOL")
    replay_tool_port: int = Field(default=8080, env="ECHO_REPLAY_TOOL_PORT")

class APISettings(BaseSettings):
    """API server settings."""
    host: str = Field(default="0.0.0.0", env="ECHO_API_HOST")
    port: int = Field(default=8000, env="ECHO_API_PORT")
    workers: int = Field(default=4, env="ECHO_API_WORKERS")
    timeout: int = Field(default=30, env="ECHO_API_TIMEOUT")
    cors_origins: List[str] = Field(default=["*"], env="ECHO_CORS_ORIGINS")
    rate_limit: int = Field(default=100, env="ECHO_RATE_LIMIT")

class Settings(BaseSettings):
    """Main settings class combining all settings."""
    database: DatabaseSettings = DatabaseSettings()
    sync: SyncSettings = SyncSettings()
    api: APISettings = APISettings()
    
    # Environment
    environment: str = Field(default="development", env="ECHO_ENVIRONMENT")
    debug: bool = Field(default=False, env="ECHO_DEBUG")
    
    # Paths
    base_dir: Path = Field(default=Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default=Path(__file__).parent.parent.parent / "data")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        """Initialize settings with environment variables."""
        super().__init__(**kwargs)
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        if self.sync.log_file:
            log_path = self.data_dir / self.sync.log_file
            log_path.parent.mkdir(parents=True, exist_ok=True)

# Create global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get settings instance."""
    return settings 
