"""
Core backend interfaces for Prompt Gear.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .schema import PromptTemplate


class BackendBase(ABC):
    """Base class for all storage backends."""
    
    @abstractmethod
    def save_prompt(self, prompt: PromptTemplate) -> None:
        """Save a prompt template."""
        pass
    
    @abstractmethod
    def get_prompt(self, name: str, version: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name and version."""
        pass
    
    @abstractmethod
    def list_prompts(self, name: Optional[str] = None) -> List[PromptTemplate]:
        """List all prompts, optionally filtered by name."""
        pass
    
    @abstractmethod
    def delete_prompt(self, name: str, version: str) -> bool:
        """Delete a prompt template."""
        pass
    
    @abstractmethod
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt."""
        pass
    
    @abstractmethod
    def prompt_exists(self, name: str, version: str) -> bool:
        """Check if a prompt exists."""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the backend (create directories, tables, etc.)."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the backend connection."""
        pass
    
    # Version management methods
    def get_next_sequence_number(self, name: str) -> int:
        """Get the next sequence number for a prompt.
        
        Default implementation for backends that don't override this method.
        """
        versions = self.list_versions(name)
        return len(versions) + 1
    
    def get_latest_prompt(self, name: str) -> Optional[PromptTemplate]:
        """Get the latest version of a prompt.
        
        Default implementation for backends that don't override this method.
        """
        versions = self.list_versions(name)
        if not versions:
            return None
        
        # Simple fallback: get the last version alphabetically
        latest_version = max(versions)
        return self.get_prompt(name, latest_version)


class BackendError(Exception):
    """Base exception for backend errors."""
    pass


class PromptNotFoundError(BackendError):
    """Raised when a prompt is not found."""
    pass


class PromptAlreadyExistsError(BackendError):
    """Raised when trying to create a prompt that already exists."""
    pass
