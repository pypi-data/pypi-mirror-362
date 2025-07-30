"""
Filesystem backend for Prompt Gear.
Stores prompts as YAML files in a directory structure with metadata management.
"""
import os
import yaml
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .core import BackendBase, PromptNotFoundError, PromptAlreadyExistsError
from .schema import PromptTemplate


class PromptMetadata:
    """Manages metadata for prompts in filesystem backend."""
    
    def __init__(self, name: str):
        self.name = name
        self.versions: Dict[str, Dict[str, Any]] = {}
        self.next_sequence = 1
    
    def add_version(self, version: str, sequence_number: int = None, is_latest: bool = False):
        """Add a new version to metadata."""
        # If setting as latest, unmark all other versions
        if is_latest:
            for v in self.versions.values():
                v['is_latest'] = False
        
        # Use provided sequence number or get next one
        if sequence_number is None:
            sequence_number = self.next_sequence
        
        self.versions[version] = {
            'sequence_number': sequence_number,
            'is_latest': is_latest,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Update next_sequence to be higher than current max
        self.next_sequence = max(self.next_sequence, sequence_number + 1)
    
    def update_version(self, version: str, is_latest: bool = None):
        """Update existing version metadata."""
        if version not in self.versions:
            raise ValueError(f"Version {version} not found")
        
        if is_latest is not None:
            # If setting as latest, unmark all other versions
            if is_latest:
                for v in self.versions.values():
                    v['is_latest'] = False
            
            self.versions[version]['is_latest'] = is_latest
        
        self.versions[version]['updated_at'] = datetime.now().isoformat()
    
    def remove_version(self, version: str):
        """Remove a version from metadata."""
        if version in self.versions:
            del self.versions[version]
    
    def get_latest_version(self) -> Optional[str]:
        """Get the version marked as latest."""
        for version, metadata in self.versions.items():
            if metadata.get('is_latest', False):
                return version
        return None
    
    def get_highest_sequence_version(self) -> Optional[str]:
        """Get the version with highest sequence number."""
        if not self.versions:
            return None
        
        highest_seq = max(v['sequence_number'] for v in self.versions.values())
        for version, metadata in self.versions.items():
            if metadata['sequence_number'] == highest_seq:
                return version
        return None
    
    def get_next_sequence_number(self) -> int:
        """Get the next sequence number."""
        return self.next_sequence
    
    def reset_sequence(self):
        """Reset the sequence number counter to 1."""
        self.next_sequence = 1
    
    def is_latest(self, version: str) -> bool:
        """Check if a version is marked as latest."""
        return self.versions.get(version, {}).get('is_latest', False)
    
    def get_version_info(self, version: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific version."""
        return self.versions.get(version)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'next_sequence': self.next_sequence,
            'versions': self.versions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptMetadata':
        """Create metadata from dictionary."""
        metadata = cls(data['name'])
        metadata.next_sequence = data.get('next_sequence', 1)
        metadata.versions = data.get('versions', {})
        return metadata


class FilesystemBackend(BackendBase):
    """Filesystem-based storage backend."""
    
    def __init__(self, prompt_dir: str = "./prompts"):
        """Initialize filesystem backend."""
        self.prompt_dir = Path(prompt_dir)
        self.initialize()
    
    def initialize(self) -> None:
        """Create prompts directory if it doesn't exist."""
        self.prompt_dir.mkdir(parents=True, exist_ok=True)
    
    def close(self) -> None:
        """Close the backend (no-op for filesystem)."""
        pass
    
    def _get_prompt_path(self, name: str, version: str) -> Path:
        """Get the file path for a prompt."""
        return self.prompt_dir / name / f"{version}.yaml"
    
    def _get_prompt_dir(self, name: str) -> Path:
        """Get the directory path for a prompt."""
        return self.prompt_dir / name
    
    def _get_metadata_path(self, name: str) -> Path:
        """Get the metadata file path for a prompt."""
        return self.prompt_dir / name / ".metadata.json"
    
    def _get_latest_link_path(self, name: str) -> Path:
        """Get the latest symlink path for a prompt."""
        return self.prompt_dir / name / "latest.yaml"
    
    def _load_metadata(self, name: str) -> PromptMetadata:
        """Load metadata for a prompt."""
        metadata_path = self._get_metadata_path(name)
        
        if not metadata_path.exists():
            return PromptMetadata(name)
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return PromptMetadata.from_dict(data)
        except (json.JSONDecodeError, FileNotFoundError):
            return PromptMetadata(name)
    
    def _save_metadata(self, name: str, metadata: PromptMetadata) -> None:
        """Save metadata for a prompt."""
        metadata_path = self._get_metadata_path(name)
        
        # Create prompt directory if it doesn't exist
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
    
    def _update_latest_link(self, name: str, version: str) -> None:
        """Update the latest symlink to point to the specified version."""
        latest_link = self._get_latest_link_path(name)
        version_file = self._get_prompt_path(name, version)
        
        # Remove existing link if it exists
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        
        # Create new symlink
        try:
            latest_link.symlink_to(version_file.name)
        except OSError:
            # If symlinks are not supported, create a copy instead
            if version_file.exists():
                import shutil
                shutil.copy2(version_file, latest_link)
    
    def _remove_latest_link(self, name: str) -> None:
        """Remove the latest symlink."""
        latest_link = self._get_latest_link_path(name)
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
    
    def get_next_sequence_number(self, name: str) -> int:
        """Get the next sequence number for a prompt."""
        metadata = self._load_metadata(name)
        return metadata.get_next_sequence_number()
    
    def save_prompt(self, prompt: PromptTemplate) -> None:
        """Save a prompt template to filesystem."""
        prompt_path = self._get_prompt_path(prompt.name, prompt.version)
        
        # Create prompt directory if it doesn't exist
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        metadata = self._load_metadata(prompt.name)
        
        # Get sequence number if not provided
        sequence_number = prompt.sequence_number
        if sequence_number is None:
            sequence_number = metadata.get_next_sequence_number()
        
        # Update metadata with sequence number
        metadata.add_version(prompt.version, sequence_number=sequence_number, is_latest=True)
        self._save_metadata(prompt.name, metadata)
        
        # Convert to dict for YAML serialization
        prompt_data = {
            'name': prompt.name,
            'version': prompt.version,
            'system_prompt': prompt.system_prompt,
            'user_prompt': prompt.user_prompt,
            'config': prompt.config or {},
            # Include internal fields for completeness
            'sequence_number': sequence_number,
            'is_latest': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Write YAML file
        with open(prompt_path, 'w', encoding='utf-8') as f:
            yaml.dump(prompt_data, f, default_flow_style=False, 
                     allow_unicode=True, sort_keys=False)
        
        # Update latest symlink
        self._update_latest_link(prompt.name, prompt.version)
    
    def get_prompt(self, name: str, version: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name and version."""
        prompt_path = self._get_prompt_path(name, version)
        
        if not prompt_path.exists():
            return None
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_data = yaml.safe_load(f)
            
            # Get metadata to fill in internal fields
            metadata = self._load_metadata(name)
            version_info = metadata.get_version_info(version)
            
            # Create PromptTemplate with all fields
            return PromptTemplate(
                name=prompt_data['name'],
                version=prompt_data['version'],
                system_prompt=prompt_data['system_prompt'],
                user_prompt=prompt_data['user_prompt'],
                config=prompt_data.get('config', {}),
                sequence_number=version_info.get('sequence_number') if version_info else None,
                is_latest=version_info.get('is_latest', False) if version_info else False,
                created_at=self._parse_timestamp(version_info.get('created_at')) if version_info else None,
                updated_at=self._parse_timestamp(version_info.get('updated_at')) if version_info else None
            )
        except Exception as e:
            raise PromptNotFoundError(f"Error loading prompt {name}:{version}: {e}")
    
    def list_prompts(self, name: Optional[str] = None) -> List[PromptTemplate]:
        """List all prompts, optionally filtered by name."""
        prompts = []
        
        if name:
            # List specific prompt versions
            prompt_dir = self._get_prompt_dir(name)
            if prompt_dir.exists():
                for yaml_file in prompt_dir.glob("*.yaml"):
                    if yaml_file.name != "latest.yaml":  # Skip the latest symlink
                        version = yaml_file.stem
                        prompt = self.get_prompt(name, version)
                        if prompt:
                            prompts.append(prompt)
        else:
            # List all prompts
            for prompt_dir in self.prompt_dir.iterdir():
                if prompt_dir.is_dir():
                    for yaml_file in prompt_dir.glob("*.yaml"):
                        if yaml_file.name != "latest.yaml":  # Skip the latest symlink
                            version = yaml_file.stem
                            prompt = self.get_prompt(prompt_dir.name, version)
                            if prompt:
                                prompts.append(prompt)
        
        return prompts
    
    def delete_prompt(self, name: str, version: str) -> bool:
        """Delete a prompt template."""
        prompt_path = self._get_prompt_path(name, version)
        
        if not prompt_path.exists():
            return False
        
        try:
            # Load metadata to check if this is the latest version
            metadata = self._load_metadata(name)
            was_latest = metadata.is_latest(version)
            
            # Remove the file
            prompt_path.unlink()
            
            # Remove from metadata
            metadata.remove_version(version)
            
            # If this was the latest version, update latest to the highest sequence number
            if was_latest:
                new_latest = metadata.get_highest_sequence_version()
                if new_latest:
                    metadata.update_version(new_latest, is_latest=True)
                    self._update_latest_link(name, new_latest)
                else:
                    # No versions left, remove latest link and reset sequence
                    self._remove_latest_link(name)
                    metadata.reset_sequence()
            
            # Save updated metadata
            self._save_metadata(name, metadata)
            
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to delete prompt {name}:{version}: {e}")
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt."""
        prompt_dir = self._get_prompt_dir(name)
        
        if not prompt_dir.exists():
            return []
        
        versions = []
        for yaml_file in prompt_dir.glob("*.yaml"):
            if yaml_file.name != "latest.yaml":  # Skip the latest symlink
                versions.append(yaml_file.stem)
        
        return sorted(versions)
    
    def prompt_exists(self, name: str, version: str) -> bool:
        """Check if a prompt exists."""
        prompt_path = self._get_prompt_path(name, version)
        return prompt_path.exists()

    def get_latest_prompt(self, name: str) -> Optional[PromptTemplate]:
        """Get the latest version of a prompt."""
        metadata = self._load_metadata(name)
        latest_version = metadata.get_latest_version()
        
        if latest_version is None:
            return None
        
        return self.get_prompt(name, latest_version)
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """Parse timestamp string to datetime object."""
        if not timestamp_str:
            return None
        try:
            # Try to parse ISO format datetime
            return datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            return None
