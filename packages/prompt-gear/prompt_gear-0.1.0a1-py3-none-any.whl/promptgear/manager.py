"""
Main prompt manager for Prompt Gear.
"""
from typing import List, Optional, Dict, Any
from .core import BackendBase, PromptNotFoundError, PromptAlreadyExistsError
from .schema import PromptTemplate
from .config import get_config


class PromptManager:
    """Main prompt manager class."""
    
    def __init__(self, backend: Optional[BackendBase] = None, config_file: Optional[str] = None):
        """Initialize prompt manager."""
        self.config = get_config(config_file)
        
        if backend:
            self.backend = backend
        else:
            self.backend = self._create_backend()
    
    def _create_backend(self) -> BackendBase:
        """Create backend based on configuration."""
        backend_type = self.config.backend
        backend_config = self.config.get_backend_config()
        
        if backend_type == 'filesystem':
            from .filesystem_backend import FilesystemBackend
            return FilesystemBackend(backend_config['prompt_dir'])
        elif backend_type == 'sqlite':
            from .sqlite_backend import SQLiteBackend
            return SQLiteBackend(backend_config['db_url'])
        elif backend_type == 'postgres':
            from .postgres_backend import PostgresBackend
            return PostgresBackend(
                backend_config['db_url'],
                pool_size=backend_config['pool_size'],
                max_connections=backend_config['max_connections']
            )
        else:
            raise ValueError(f"Unsupported backend: {backend_type}")
    
    def create_prompt(self, name: str, version: str, system_prompt: str, 
                     user_prompt: str, config: Optional[Dict[str, Any]] = None,
                     overwrite: bool = False) -> PromptTemplate:
        """Create a new prompt template.
        
        Args:
            name: Prompt name
            version: Prompt version
            system_prompt: System prompt text
            user_prompt: User prompt text
            config: Optional configuration dictionary
            overwrite: Whether to overwrite existing prompt
        """
        if not overwrite and self.backend.prompt_exists(name, version):
            raise PromptAlreadyExistsError(f"Prompt {name}:{version} already exists")
        
        # Get sequence number for this prompt
        sequence_number = self.backend.get_next_sequence_number(name)
        
        prompt = PromptTemplate(
            name=name,
            version=version,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            config=config or {},
            sequence_number=sequence_number,
            is_latest=True  # New prompts are always latest
        )
        
        self.backend.save_prompt(prompt)
        
        # Return the saved prompt with all metadata populated
        return self.backend.get_prompt(name, version)
    
    def get_prompt(self, name: str, version: str = None) -> PromptTemplate:
        """Get a prompt template by name and version.
        
        Args:
            name: Prompt name
            version: Prompt version. If None, returns the latest version.
        """
        if version is None:
            return self.get_latest_prompt(name)
        
        prompt = self.backend.get_prompt(name, version)
        if not prompt:
            raise PromptNotFoundError(f"Prompt {name}:{version} not found")
        return prompt
    
    def get_latest_prompt(self, name: str) -> PromptTemplate:
        """Get the latest version of a prompt by creation time."""
        if hasattr(self.backend, 'get_latest_prompt'):
            # Use backend-specific implementation if available
            prompt = self.backend.get_latest_prompt(name)
            if not prompt:
                raise PromptNotFoundError(f"No versions found for prompt {name}")
            return prompt
        else:
            # Fallback: get all versions and find latest
            versions = self.list_versions(name)
            if not versions:
                raise PromptNotFoundError(f"No versions found for prompt {name}")
            
            # Try to get latest by sorting versions (basic heuristic)
            latest_version = self._get_latest_version_heuristic(versions)
            return self.get_prompt(name, latest_version)
    
    def _get_latest_version_heuristic(self, versions: List[str]) -> str:
        """Simple heuristic to determine latest version."""
        # Sort versions: v1.0.0 > v1.0 > v1 > latest
        def version_key(v):
            if v == 'latest':
                return (999, 999, 999)  # latest always wins
            
            # Try to parse semantic version
            import re
            match = re.match(r'v?(\d+)(?:\.(\d+))?(?:\.(\d+))?', v)
            if match:
                major = int(match.group(1) or 0)
                minor = int(match.group(2) or 0)
                patch = int(match.group(3) or 0)
                return (major, minor, patch)
            
            # Fallback: lexicographic sort
            return (0, 0, 0, v)
        
        return max(versions, key=version_key)
    
    def update_prompt(self, name: str, version: str, system_prompt: Optional[str] = None,
                     user_prompt: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> PromptTemplate:
        """Update an existing prompt template."""
        existing = self.get_prompt(name, version)
        
        # Update fields if provided
        if system_prompt is not None:
            existing.system_prompt = system_prompt
        if user_prompt is not None:
            existing.user_prompt = user_prompt
        if config is not None:
            existing.config = config
        
        self.backend.save_prompt(existing)
        return existing
    
    def delete_prompt(self, name: str, version: str) -> bool:
        """Delete a prompt template."""
        if not self.backend.prompt_exists(name, version):
            raise PromptNotFoundError(f"Prompt {name}:{version} not found")
        
        return self.backend.delete_prompt(name, version)
    
    def list_prompts(self, name: Optional[str] = None) -> List[PromptTemplate]:
        """List all prompts, optionally filtered by name."""
        return self.backend.list_prompts(name)
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt."""
        return self.backend.list_versions(name)
    
    def prompt_exists(self, name: str, version: str) -> bool:
        """Check if a prompt exists."""
        return self.backend.prompt_exists(name, version)
    
    def close(self) -> None:
        """Close the backend connection."""
        self.backend.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
