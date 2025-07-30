"""
PostgreSQL backend for Prompt Gear.
Stores prompts in PostgreSQL database with structured fields and advanced features.
"""
import json
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
import logging

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import ThreadedConnectionPool
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    ThreadedConnectionPool = None

from .core import BackendBase, PromptNotFoundError, PromptAlreadyExistsError
from .schema import PromptTemplate


class PostgresBackend(BackendBase):
    """PostgreSQL-based storage backend with connection pooling."""
    
    def __init__(self, db_url: str, pool_size: int = 5, max_connections: int = 20):
        """Initialize PostgreSQL backend."""
        if psycopg2 is None:
            raise ImportError("psycopg2 is required for PostgreSQL backend. Install with: pip install prompt-gear[postgres]")
        
        self.db_url = db_url
        self.pool_size = pool_size
        self.max_connections = max_connections
        self.logger = logging.getLogger(__name__)
        
        # Parse database URL
        parsed = urlparse(db_url)
        if parsed.scheme not in ("postgresql", "postgres"):
            raise ValueError(f"Invalid PostgreSQL URL: {db_url}")
        
        # Create connection pool
        try:
            self.connection_pool = ThreadedConnectionPool(
                pool_size, max_connections, db_url
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create connection pool: {e}")
        
        self.initialize()
    
    def get_connection(self):
        """Get a connection from the pool."""
        try:
            return self.connection_pool.getconn()
        except Exception as e:
            raise RuntimeError(f"Failed to get database connection: {e}")
    
    def put_connection(self, conn):
        """Return a connection to the pool."""
        try:
            self.connection_pool.putconn(conn)
        except Exception as e:
            self.logger.error(f"Failed to return connection to pool: {e}")
    
    def initialize(self) -> None:
        """Create database tables if they don't exist."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Create prompts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS prompts (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        version VARCHAR(100) NOT NULL,
                        system_prompt TEXT NOT NULL,
                        user_prompt TEXT NOT NULL,
                        config JSONB NOT NULL DEFAULT '{}',
                        sequence_number INTEGER NOT NULL DEFAULT 1,
                        is_latest BOOLEAN NOT NULL DEFAULT FALSE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(name, version),
                        UNIQUE(name, sequence_number)
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_name_version 
                    ON prompts(name, version)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_name 
                    ON prompts(name)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_created_at 
                    ON prompts(created_at)
                """)
                
                # Create indexes for version management
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_sequence 
                    ON prompts(name, sequence_number)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_latest 
                    ON prompts(name, is_latest)
                """)
                
                # Create index on JSONB config for advanced queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_prompts_config 
                    ON prompts USING GIN(config)
                """)
                
                # Create function to update updated_at timestamp
                cursor.execute("""
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql'
                """)
                
                # Create trigger to automatically update updated_at
                cursor.execute("""
                    DROP TRIGGER IF EXISTS update_prompts_updated_at ON prompts
                """)
                
                cursor.execute("""
                    CREATE TRIGGER update_prompts_updated_at
                    BEFORE UPDATE ON prompts
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column()
                """)
                
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to initialize database: {e}")
        finally:
            self.put_connection(conn)
    
    def close(self) -> None:
        """Close all connections in the pool."""
        try:
            self.connection_pool.closeall()
        except Exception as e:
            self.logger.error(f"Failed to close connection pool: {e}")
    
    def get_next_sequence_number(self, name: str) -> int:
        """Get the next sequence number for a prompt."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COALESCE(MAX(sequence_number), 0) + 1 
                    FROM prompts 
                    WHERE name = %s
                """, (name,))
                return cursor.fetchone()[0]
        except Exception as e:
            raise RuntimeError(f"Failed to get next sequence number: {e}")
        finally:
            self.put_connection(conn)
    
    def save_prompt(self, prompt: PromptTemplate) -> None:
        """Save a prompt template to PostgreSQL database."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Get sequence number if not provided
                sequence_number = prompt.sequence_number
                if sequence_number is None:
                    sequence_number = self.get_next_sequence_number(prompt.name)
                
                # Start transaction
                cursor.execute("BEGIN")
                
                # Update existing latest version to false
                cursor.execute("""
                    UPDATE prompts SET is_latest = FALSE 
                    WHERE name = %s AND is_latest = TRUE
                """, (prompt.name,))
                
                # Insert or update the prompt
                cursor.execute("""
                    INSERT INTO prompts (name, version, system_prompt, user_prompt, config, 
                                       sequence_number, is_latest)
                    VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                    ON CONFLICT (name, version) 
                    DO UPDATE SET
                        system_prompt = EXCLUDED.system_prompt,
                        user_prompt = EXCLUDED.user_prompt,
                        config = EXCLUDED.config,
                        sequence_number = EXCLUDED.sequence_number,
                        is_latest = TRUE,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    prompt.name,
                    prompt.version,
                    prompt.system_prompt,
                    prompt.user_prompt,
                    json.dumps(prompt.config or {}),
                    sequence_number
                ))
                
                cursor.execute("COMMIT")
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to save prompt: {e}")
        finally:
            self.put_connection(conn)
    
    def get_prompt(self, name: str, version: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name and version."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT name, version, system_prompt, user_prompt, config,
                           sequence_number, is_latest, created_at, updated_at
                    FROM prompts 
                    WHERE name = %s AND version = %s
                """, (name, version))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return PromptTemplate(
                    name=row['name'],
                    version=row['version'],
                    system_prompt=row['system_prompt'],
                    user_prompt=row['user_prompt'],
                    config=row['config'] or {},
                    sequence_number=row['sequence_number'],
                    is_latest=row['is_latest'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        except Exception as e:
            raise PromptNotFoundError(f"Error loading prompt {name}:{version}: {e}")
        finally:
            self.put_connection(conn)
    
    def list_prompts(self, name: Optional[str] = None) -> List[PromptTemplate]:
        """List all prompts, optionally filtered by name."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if name:
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config,
                               sequence_number, is_latest, created_at, updated_at
                        FROM prompts 
                        WHERE name = %s
                        ORDER BY sequence_number
                    """, (name,))
                else:
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config,
                               sequence_number, is_latest, created_at, updated_at
                        FROM prompts 
                        ORDER BY name, sequence_number
                    """)
                
                prompts = []
                for row in cursor.fetchall():
                    prompts.append(PromptTemplate(
                        name=row['name'],
                        version=row['version'],
                        system_prompt=row['system_prompt'],
                        user_prompt=row['user_prompt'],
                        config=row['config'] or {},
                        sequence_number=row['sequence_number'],
                        is_latest=row['is_latest'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                
                return prompts
        except Exception as e:
            raise RuntimeError(f"Failed to list prompts: {e}")
        finally:
            self.put_connection(conn)
    
    def delete_prompt(self, name: str, version: str) -> bool:
        """Delete a prompt template."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("BEGIN")
                
                # Check if the version to delete is the latest
                cursor.execute("""
                    SELECT is_latest FROM prompts 
                    WHERE name = %s AND version = %s
                """, (name, version))
                
                result = cursor.fetchone()
                if not result:
                    cursor.execute("ROLLBACK")
                    return False
                
                was_latest = result[0]
                
                # Delete the prompt
                cursor.execute("""
                    DELETE FROM prompts 
                    WHERE name = %s AND version = %s
                """, (name, version))
                
                deleted = cursor.rowcount > 0
                
                # If we deleted the latest version, update the next highest sequence number to be latest
                if deleted and was_latest:
                    cursor.execute("""
                        UPDATE prompts SET is_latest = TRUE 
                        WHERE name = %s AND sequence_number = (
                            SELECT MAX(sequence_number) FROM prompts WHERE name = %s
                        )
                    """, (name, name))
                
                cursor.execute("COMMIT")
                return deleted
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to delete prompt: {e}")
        finally:
            self.put_connection(conn)
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT version FROM prompts 
                    WHERE name = %s 
                    ORDER BY version
                """, (name,))
                
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            raise RuntimeError(f"Failed to list versions: {e}")
        finally:
            self.put_connection(conn)
    
    def prompt_exists(self, name: str, version: str) -> bool:
        """Check if a prompt exists."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 1 FROM prompts 
                    WHERE name = %s AND version = %s
                """, (name, version))
                
                return cursor.fetchone() is not None
        except Exception as e:
            raise RuntimeError(f"Failed to check prompt existence: {e}")
        finally:
            self.put_connection(conn)
    
    def search_prompts(self, query: str, field: str = "all") -> List[PromptTemplate]:
        """Search prompts by text query."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if field == "all":
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config 
                        FROM prompts 
                        WHERE name ILIKE %s OR system_prompt ILIKE %s OR user_prompt ILIKE %s
                        ORDER BY name, version
                    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
                elif field == "name":
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config 
                        FROM prompts 
                        WHERE name ILIKE %s
                        ORDER BY name, version
                    """, (f"%{query}%",))
                elif field == "system_prompt":
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config 
                        FROM prompts 
                        WHERE system_prompt ILIKE %s
                        ORDER BY name, version
                    """, (f"%{query}%",))
                elif field == "user_prompt":
                    cursor.execute("""
                        SELECT name, version, system_prompt, user_prompt, config 
                        FROM prompts 
                        WHERE user_prompt ILIKE %s
                        ORDER BY name, version
                    """, (f"%{query}%",))
                else:
                    raise ValueError(f"Invalid search field: {field}")
                
                prompts = []
                for row in cursor.fetchall():
                    prompts.append(PromptTemplate(
                        name=row['name'],
                        version=row['version'],
                        system_prompt=row['system_prompt'],
                        user_prompt=row['user_prompt'],
                        config=row['config'] or {}
                    ))
                
                return prompts
        except Exception as e:
            raise RuntimeError(f"Failed to search prompts: {e}")
        finally:
            self.put_connection(conn)
    
    def get_prompts_by_config(self, config_query: Dict[str, Any]) -> List[PromptTemplate]:
        """Get prompts by config parameters using JSONB queries."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT name, version, system_prompt, user_prompt, config 
                    FROM prompts 
                    WHERE config @> %s
                    ORDER BY name, version
                """, (json.dumps(config_query),))
                
                prompts = []
                for row in cursor.fetchall():
                    prompts.append(PromptTemplate(
                        name=row['name'],
                        version=row['version'],
                        system_prompt=row['system_prompt'],
                        user_prompt=row['user_prompt'],
                        config=row['config'] or {}
                    ))
                
                return prompts
        except Exception as e:
            raise RuntimeError(f"Failed to query prompts by config: {e}")
        finally:
            self.put_connection(conn)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Basic counts
                cursor.execute("SELECT COUNT(*) as total_prompts FROM prompts")
                total_prompts = cursor.fetchone()['total_prompts']
                
                cursor.execute("SELECT COUNT(DISTINCT name) as unique_names FROM prompts")
                unique_names = cursor.fetchone()['unique_names']
                
                # Most recent prompts
                cursor.execute("""
                    SELECT name, version, created_at 
                    FROM prompts 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """)
                recent_prompts = cursor.fetchall()
                
                # Config statistics
                cursor.execute("""
                    SELECT COUNT(*) as count, 
                           jsonb_object_keys(config) as config_key
                    FROM prompts, jsonb_object_keys(config)
                    GROUP BY config_key
                    ORDER BY count DESC
                    LIMIT 10
                """)
                config_stats = cursor.fetchall()
                
                # Database info
                cursor.execute("SELECT version() as db_version")
                db_info = cursor.fetchone()
                
                return {
                    "total_prompts": total_prompts,
                    "unique_names": unique_names,
                    "recent_prompts": [
                        {
                            "name": r['name'],
                            "version": r['version'],
                            "created_at": r['created_at'].isoformat()
                        } for r in recent_prompts
                    ],
                    "config_stats": [
                        {
                            "key": r['config_key'],
                            "count": r['count']
                        } for r in config_stats
                    ],
                    "database_url": self.db_url,
                    "database_version": db_info['db_version'],
                    "pool_size": self.pool_size,
                    "max_connections": self.max_connections
                }
        except Exception as e:
            raise RuntimeError(f"Failed to get database stats: {e}")
        finally:
            self.put_connection(conn)
    
    def get_latest_prompt(self, name: str) -> Optional[PromptTemplate]:
        """Get the latest version of a prompt."""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT name, version, system_prompt, user_prompt, config,
                           sequence_number, is_latest, created_at, updated_at
                    FROM prompts 
                    WHERE name = %s AND is_latest = TRUE
                """, (name,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return PromptTemplate(
                    name=row['name'],
                    version=row['version'],
                    system_prompt=row['system_prompt'],
                    user_prompt=row['user_prompt'],
                    config=row['config'] or {},
                    sequence_number=row['sequence_number'],
                    is_latest=row['is_latest'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        except Exception as e:
            raise PromptNotFoundError(f"Error loading latest prompt {name}: {e}")
        finally:
            self.put_connection(conn)
