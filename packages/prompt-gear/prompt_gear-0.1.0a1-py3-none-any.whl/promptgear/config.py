"""
Configuration management for Prompt Gear.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path


class Config:
    """Configuration class for Prompt Gear."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration."""
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load .env from current directory or parent directories
            current_dir = Path.cwd()
            env_path = current_dir / '.env'
            if env_path.exists():
                load_dotenv(env_path)
            else:
                # Check parent directories
                for parent in current_dir.parents:
                    env_path = parent / '.env'
                    if env_path.exists():
                        load_dotenv(env_path)
                        break
    
    @property
    def backend(self) -> str:
        """Get backend type."""
        return os.getenv('PROMPT_GEAR_BACKEND', 'filesystem')
    
    @property
    def prompt_dir(self) -> str:
        """Get prompts directory."""
        return os.getenv('PROMPT_GEAR_PROMPT_DIR', './prompts')
    
    @property
    def db_url(self) -> str:
        """Get database URL."""
        return os.getenv('PROMPT_GEAR_DB_URL', 'sqlite:///prompts.db')
    
    @property
    def debug(self) -> bool:
        """Get debug mode."""
        return os.getenv('PROMPT_GEAR_DEBUG', 'false').lower() == 'true'
    
    @property
    def postgres_pool_size(self) -> int:
        """Get PostgreSQL connection pool size."""
        return int(os.getenv('PROMPT_GEAR_POSTGRES_POOL_SIZE', '5'))
    
    @property
    def postgres_max_connections(self) -> int:
        """Get PostgreSQL max connections."""
        return int(os.getenv('PROMPT_GEAR_POSTGRES_MAX_CONNECTIONS', '20'))
    
    def get_backend_config(self) -> dict:
        """Get backend-specific configuration."""
        if self.backend == 'filesystem':
            return {
                'prompt_dir': self.prompt_dir
            }
        elif self.backend == 'sqlite':
            return {
                'db_url': self.db_url
            }
        elif self.backend == 'postgres':
            return {
                'db_url': self.db_url,
                'pool_size': self.postgres_pool_size,
                'max_connections': self.postgres_max_connections
            }
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")


# Global configuration instance
_config = None


def get_config(env_file: Optional[str] = None) -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config(env_file)
    return _config


def reload_config(env_file: Optional[str] = None) -> Config:
    """Reload configuration."""
    global _config
    _config = Config(env_file)
    return _config
