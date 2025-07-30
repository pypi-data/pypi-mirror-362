"""
SQLite backend for Prompt Gear.
Stores prompts in SQLite database with structured fields.
"""
import sqlite3
import json
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
from datetime import datetime

from .core import BackendBase, PromptNotFoundError, PromptAlreadyExistsError
from .schema import PromptTemplate


class SQLiteBackend(BackendBase):
    """SQLite-based storage backend."""
    
    def __init__(self, db_url: str = "sqlite:///prompts.db"):
        """Initialize SQLite backend."""
        # Parse database URL
        parsed = urlparse(db_url)
        if parsed.scheme != "sqlite":
            raise ValueError(f"Invalid SQLite URL: {db_url}")
        
        # Extract database path
        self.db_path = parsed.path.lstrip("/") if parsed.path else "prompts.db"
        
        # Ensure parent directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.initialize()
    
    def initialize(self) -> None:
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    system_prompt TEXT NOT NULL,
                    user_prompt TEXT NOT NULL,
                    config TEXT NOT NULL DEFAULT '{}',
                    sequence_number INTEGER NOT NULL DEFAULT 1,
                    is_latest BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, version),
                    UNIQUE(name, sequence_number)
                )
            """)
            
            # Create index for better query performance
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_name_version 
                ON prompts(name, version)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_name 
                ON prompts(name)
            """)
            
            # Create indexes for version management
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_sequence 
                ON prompts(name, sequence_number)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_latest 
                ON prompts(name, is_latest)
            """)
            
            # Create metadata table for sequence tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompt_metadata (
                    name TEXT PRIMARY KEY,
                    next_sequence INTEGER DEFAULT 1
                )
            """)
    
    def close(self) -> None:
        """Close the backend connection (no-op for SQLite)."""
        pass
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """Parse timestamp string to datetime object."""
        if not timestamp_str:
            return None
        try:
            # Try to parse ISO format datetime
            return datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            return None
    
    def get_next_sequence_number(self, name: str) -> int:
        """Get the next sequence number for a prompt."""
        with sqlite3.connect(self.db_path) as conn:
            # Check if any versions exist for this prompt
            cursor = conn.execute("""
                SELECT COUNT(*) FROM prompts WHERE name = ?
            """, (name,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                # No versions exist, start from 1 and reset stored sequence
                conn.execute("""
                    INSERT OR REPLACE INTO prompt_metadata (name, next_sequence) 
                    VALUES (?, 1)
                """, (name,))
                return 1
            
            # Get the maximum sequence number ever used for this prompt
            cursor = conn.execute("""
                SELECT COALESCE(MAX(sequence_number), 0) + 1 
                FROM prompts 
                WHERE name = ?
            """, (name,))
            next_seq = cursor.fetchone()[0]
            
            # Also check if we have any record of higher sequence numbers
            # by looking at the database schema for any auto-increment info
            # For now, we'll maintain a simple counter per prompt name
            
            # Check if we have a metadata table for sequence tracking
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='prompt_metadata'
            """)
            
            if not cursor.fetchone():
                # Create metadata table if it doesn't exist
                conn.execute("""
                    CREATE TABLE prompt_metadata (
                        name TEXT PRIMARY KEY,
                        next_sequence INTEGER DEFAULT 1
                    )
                """)
            
            # Get or create the next sequence for this prompt
            cursor = conn.execute("""
                SELECT next_sequence FROM prompt_metadata WHERE name = ?
            """, (name,))
            result = cursor.fetchone()
            
            if result:
                stored_next = result[0]
                # Use the higher of the two values
                next_seq = max(next_seq, stored_next)
            
            # Update the stored next sequence
            conn.execute("""
                INSERT OR REPLACE INTO prompt_metadata (name, next_sequence) 
                VALUES (?, ?)
            """, (name, next_seq + 1))
            
            return next_seq
    
    def save_prompt(self, prompt: PromptTemplate) -> None:
        """Save a prompt template to SQLite database."""
        config_json = json.dumps(prompt.config or {})
        
        with sqlite3.connect(self.db_path) as conn:
            try:
                # Get sequence number if not provided
                sequence_number = prompt.sequence_number
                if sequence_number is None:
                    sequence_number = self.get_next_sequence_number(prompt.name)
                
                # Start transaction
                conn.execute("BEGIN")
                
                # Update existing latest version to false
                conn.execute("""
                    UPDATE prompts SET is_latest = 0 
                    WHERE name = ? AND is_latest = 1
                """, (prompt.name,))
                
                # Insert or replace the prompt
                now = datetime.now().isoformat()
                conn.execute("""
                    INSERT OR REPLACE INTO prompts 
                    (name, version, system_prompt, user_prompt, config, 
                     sequence_number, is_latest, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
                """, (
                    prompt.name,
                    prompt.version,
                    prompt.system_prompt,
                    prompt.user_prompt,
                    config_json,
                    sequence_number,
                    now,
                    now
                ))
                
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Failed to save prompt: {e}")
    
    def get_prompt(self, name: str, version: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name and version."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT name, version, system_prompt, user_prompt, config,
                       sequence_number, is_latest, created_at, updated_at
                FROM prompts 
                WHERE name = ? AND version = ?
            """, (name, version))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            try:
                config = json.loads(row['config']) if row['config'] else {}
                return PromptTemplate(
                    name=row['name'],
                    version=row['version'],
                    system_prompt=row['system_prompt'],
                    user_prompt=row['user_prompt'],
                    config=config,
                    sequence_number=row['sequence_number'],
                    is_latest=bool(row['is_latest']),
                    created_at=self._parse_timestamp(row['created_at']),
                    updated_at=self._parse_timestamp(row['updated_at'])
                )
            except (json.JSONDecodeError, ValueError) as e:
                raise PromptNotFoundError(f"Error loading prompt {name}:{version}: {e}")
    
    def list_prompts(self, name: Optional[str] = None) -> List[PromptTemplate]:
        """List all prompts, optionally filtered by name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if name:
                cursor = conn.execute("""
                    SELECT name, version, system_prompt, user_prompt, config 
                    FROM prompts 
                    WHERE name = ?
                    ORDER BY version
                """, (name,))
            else:
                cursor = conn.execute("""
                    SELECT name, version, system_prompt, user_prompt, config 
                    FROM prompts 
                    ORDER BY name, version
                """)
            
            prompts = []
            for row in cursor:
                try:
                    config = json.loads(row['config']) if row['config'] else {}
                    prompts.append(PromptTemplate(
                        name=row['name'],
                        version=row['version'],
                        system_prompt=row['system_prompt'],
                        user_prompt=row['user_prompt'],
                        config=config
                    ))
                except (json.JSONDecodeError, ValueError):
                    # Skip invalid entries
                    continue
            
            return prompts
    
    def delete_prompt(self, name: str, version: str) -> bool:
        """Delete a prompt template."""
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("BEGIN")
                
                # Check if the version to delete is the latest
                cursor = conn.execute("""
                    SELECT is_latest FROM prompts 
                    WHERE name = ? AND version = ?
                """, (name, version))
                
                result = cursor.fetchone()
                if not result:
                    conn.execute("ROLLBACK")
                    return False
                
                was_latest = bool(result[0])
                
                # Delete the prompt
                cursor = conn.execute("""
                    DELETE FROM prompts 
                    WHERE name = ? AND version = ?
                """, (name, version))
                
                deleted = cursor.rowcount > 0
                
                # If we deleted the latest version, update the next highest sequence number to be latest
                if deleted and was_latest:
                    conn.execute("""
                        UPDATE prompts SET is_latest = 1 
                        WHERE name = ? AND sequence_number = (
                            SELECT MAX(sequence_number) FROM prompts WHERE name = ?
                        )
                    """, (name, name))
                
                conn.commit()
                return deleted
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete prompt: {e}")
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT version FROM prompts 
                WHERE name = ? 
                ORDER BY version
            """, (name,))
            
            return [row[0] for row in cursor.fetchall()]
    
    def prompt_exists(self, name: str, version: str) -> bool:
        """Check if a prompt exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 1 FROM prompts 
                WHERE name = ? AND version = ?
            """, (name, version))
            
            return cursor.fetchone() is not None
    
    def get_stats(self) -> dict:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM prompts")
            total_prompts = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(DISTINCT name) FROM prompts")
            unique_names = cursor.fetchone()[0]
            
            return {
                "total_prompts": total_prompts,
                "unique_names": unique_names,
                "database_path": self.db_path
            }
    
    def get_latest_prompt(self, name: str) -> Optional[PromptTemplate]:
        """Get the latest version of a prompt."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT name, version, system_prompt, user_prompt, config,
                       sequence_number, is_latest, created_at, updated_at
                FROM prompts 
                WHERE name = ? AND is_latest = 1
            """, (name,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            try:
                config = json.loads(row['config']) if row['config'] else {}
                return PromptTemplate(
                    name=row['name'],
                    version=row['version'],
                    system_prompt=row['system_prompt'],
                    user_prompt=row['user_prompt'],
                    config=config,
                    sequence_number=row['sequence_number'],
                    is_latest=bool(row['is_latest']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            except (json.JSONDecodeError, ValueError) as e:
                raise PromptNotFoundError(f"Error loading prompt {name}: {e}")
