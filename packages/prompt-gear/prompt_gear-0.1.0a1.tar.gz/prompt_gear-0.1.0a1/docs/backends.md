# Storage Backends

Detailed guide to Prompt Gear's storage backends and their characteristics.

## 🏗️ Backend Overview

Prompt Gear supports three storage backends:

| Backend | Use Case | Pros | Cons |
|---------|----------|------|------|
| **Filesystem** | Development, Small teams | Simple, Version control friendly | No querying, Limited scalability |
| **SQLite** | Single-user apps, Prototyping | No server needed, ACID transactions | No concurrent writes, Single file |
| **PostgreSQL** | Production, Multi-user | High performance, Concurrent access | Requires server, More complex |

## 📁 Filesystem Backend

### Overview

Stores prompts as YAML files in a directory structure. Each prompt name gets its own directory, with versions stored as separate files.

### Configuration

```bash
# Environment variables
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./prompts
```

### Directory Structure

```
prompts/
├── chatbot/
│   ├── .metadata.json         # Version management metadata
│   ├── latest.yaml            # Symlink to latest version
│   ├── v1.yaml
│   ├── v2.yaml
│   └── v3.yaml
├── assistant/
│   ├── .metadata.json
│   ├── latest.yaml
│   ├── v1.yaml
│   └── v2.yaml
├── email_writer/
│   ├── .metadata.json
│   ├── latest.yaml
│   └── v1.yaml
└── translator/
    ├── .metadata.json
    ├── latest.yaml
    ├── v1.yaml
    └── v2.yaml
```

### Metadata Management

Each prompt directory contains a `.metadata.json` file that tracks version information:

```json
{
  "name": "chatbot",
  "next_sequence": 4,
  "versions": {
    "v1": {
      "sequence_number": 1,
      "is_latest": false,
      "created_at": "2025-01-15T10:30:00.000000",
      "updated_at": "2025-01-15T10:30:00.000000"
    },
    "v2": {
      "sequence_number": 2,
      "is_latest": false,
      "created_at": "2025-01-15T11:00:00.000000",
      "updated_at": "2025-01-15T11:00:00.000000"
    },
    "v3": {
      "sequence_number": 3,
      "is_latest": true,
      "created_at": "2025-01-15T11:30:00.000000",
      "updated_at": "2025-01-15T11:30:00.000000"
    }
  }
}
```

### Example Files

```yaml
# prompts/chatbot/v1.yaml
name: chatbot
version: v1
system_prompt: |
  You are a helpful customer support assistant.
  Always be polite and professional.
user_prompt: |
  Customer: {{customer_message}}
  
  Please provide a helpful response.
config:
  temperature: 0.7
  max_tokens: 500
  model: gpt-3.5-turbo
```

### Advantages

- **Simple setup**: No database server required
- **Version control**: Easy to track changes with git
- **Human readable**: YAML format is easy to read and edit
- **Backup**: Simple file copying for backup
- **Debugging**: Easy to inspect and modify files directly
- **Robust versioning**: Metadata-based version tracking with sequence numbers
- **Latest version access**: Symlink provides quick access to latest version

### Disadvantages

- **No querying**: Can't search or filter prompts efficiently
- **No transactions**: No ACID guarantees (though metadata updates are atomic)
- **Concurrent access**: Limited protection against simultaneous modifications
- **Scalability**: Performance degrades with many prompts
- **Metadata overhead**: Each prompt requires additional .metadata.json file

### Best Practices

```python
# Use for development and small teams
from promptgear.filesystem_backend import FilesystemBackend

# Custom directory structure
backend = FilesystemBackend(
    prompt_dir="./my_prompts",
    file_extension=".yml"  # Use .yml instead of .yaml
)

# Version control integration
# Add to .gitignore if needed:
# prompts/temp/
# prompts/**/*.tmp
```

### Performance Characteristics

- **Read**: O(1) for specific prompt, O(n) for listing
- **Write**: O(1) for single prompt
- **Search**: O(n) - requires scanning all files
- **Concurrent reads**: Safe
- **Concurrent writes**: Unsafe

## 🗄️ SQLite Backend

### Overview

Uses SQLite database for structured storage. Provides ACID transactions and basic querying capabilities while maintaining simplicity.

### Configuration

```bash
# Environment variables
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
```

### Database Schema

```sql
-- Main prompts table
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    config TEXT NOT NULL,  -- JSON string
    sequence_number INTEGER NOT NULL DEFAULT 1,
    is_latest BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version),
    UNIQUE(name, sequence_number)
);

-- Metadata table for sequence tracking
CREATE TABLE prompt_metadata (
    name TEXT PRIMARY KEY,
    next_sequence INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_prompts_name ON prompts(name);
CREATE INDEX idx_prompts_name_version ON prompts(name, version);
CREATE INDEX idx_prompts_created_at ON prompts(created_at);
CREATE INDEX idx_prompts_sequence ON prompts(name, sequence_number);
CREATE INDEX idx_prompts_latest ON prompts(name, is_latest);
```

### Connection Options

```python
from promptgear.sqlite_backend import SQLiteBackend

# Basic connection
backend = SQLiteBackend("sqlite:///prompts.db")

# With custom timeout
backend = SQLiteBackend(
    db_url="sqlite:///prompts.db",
    timeout=30
)

# In-memory database (for testing)
backend = SQLiteBackend("sqlite:///:memory:")
```

### Advantages

- **ACID transactions**: Data integrity guarantees
- **No server**: Self-contained database file
- **SQL querying**: Basic search and filter capabilities
- **Concurrent reads**: Multiple readers supported
- **Backup**: Simple file copying

### Disadvantages

- **Single writer**: Only one write operation at a time
- **File locking**: Can cause issues in some environments
- **Scalability**: Limited for large datasets or high concurrency
- **Features**: Fewer advanced features than PostgreSQL

### Best Practices

```python
# Use for single-user applications
from promptgear.sqlite_backend import SQLiteBackend

# Production configuration
backend = SQLiteBackend(
    db_url="sqlite:///prod_prompts.db",
    timeout=30,
    check_same_thread=False  # For web applications
)

# Enable WAL mode for better concurrency
import sqlite3
conn = sqlite3.connect("prompts.db")
conn.execute("PRAGMA journal_mode=WAL")
conn.close()
```

### Performance Characteristics

- **Read**: O(log n) with indexes
- **Write**: O(log n) with indexes
- **Search**: O(log n) with proper indexes
- **Concurrent reads**: Excellent
- **Concurrent writes**: Sequential only

## 🐘 PostgreSQL Backend

### Overview

Full-featured PostgreSQL backend with connection pooling, advanced querying, and high concurrency support. Designed for production use.

### Configuration

```bash
# Environment variables
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
```

### Database Schema

```sql
CREATE TABLE prompts (
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
);

-- Indexes for performance
CREATE INDEX idx_prompts_name ON prompts(name);
CREATE INDEX idx_prompts_name_version ON prompts(name, version);
CREATE INDEX idx_prompts_created_at ON prompts(created_at);
CREATE INDEX idx_prompts_sequence ON prompts(name, sequence_number);
CREATE INDEX idx_prompts_latest ON prompts(name, is_latest);
CREATE INDEX idx_prompts_config ON prompts USING GIN(config);

-- Full-text search
CREATE INDEX idx_prompts_search ON prompts USING GIN(
    to_tsvector('english', name || ' ' || system_prompt || ' ' || user_prompt)
);

-- Automatic updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_prompts_updated_at
    BEFORE UPDATE ON prompts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Connection Pool Configuration

```python
from promptgear.postgres_backend import PostgresBackend

# Production configuration
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost:5432/prompts",
    pool_size=20,           # Initial connections
    max_connections=100,    # Maximum connections
    timeout=30,            # Connection timeout
    retry_attempts=3       # Retry failed connections
)
```

### Advanced Features

#### 1. JSONB Configuration Storage

```python
# Complex configuration with JSONB
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "tools": [
        {"name": "search", "enabled": True},
        {"name": "calculator", "enabled": False}
    ],
    "metadata": {
        "created_by": "user123",
        "team": "ai-team"
    }
}

pm.create_prompt("complex", "v1", "system", "user", config=config)
```

#### 2. Full-Text Search

```python
# Search across all prompt content
from promptgear.postgres_backend import PostgresBackend

backend = PostgresBackend(connection_string)
# Search implemented in backend
results = backend.search_prompts("customer support chatbot")
```

#### 3. Statistics and Analytics

```python
# Get usage statistics
if hasattr(pm.backend, 'get_statistics'):
    stats = pm.backend.get_statistics()
    print(f"Total prompts: {stats['total_prompts']}")
    print(f"Total versions: {stats['total_versions']}")
    print(f"Most recent: {stats['most_recent']}")
```

### Advantages

- **High concurrency**: Handles many simultaneous users
- **ACID transactions**: Full data integrity
- **Advanced querying**: Complex searches and filters
- **JSONB support**: Flexible configuration storage
- **Full-text search**: Built-in search capabilities
- **Connection pooling**: Efficient resource management
- **Scalability**: Handles large datasets efficiently

### Disadvantages

- **Server required**: Must run PostgreSQL server
- **Complexity**: More complex setup and configuration
- **Resources**: Higher memory and CPU usage
- **Dependencies**: Requires psycopg2 driver

### Best Practices

```python
# Production deployment
from promptgear.postgres_backend import PostgresBackend

# Configure for your workload
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost:5432/prompts",
    pool_size=min(cpu_count() * 2, 20),  # Based on CPU cores
    max_connections=100,                  # Based on expected load
    timeout=30
)

# Use connection pooling wisely
# Don't create new managers frequently
pm = PromptManager(backend=backend)  # Reuse this instance
```

### Performance Characteristics

- **Read**: O(log n) with excellent indexing
- **Write**: O(log n) with excellent performance
- **Search**: O(log n) with full-text search
- **Concurrent reads**: Excellent
- **Concurrent writes**: Excellent

## 🔄 Backend Comparison

### Performance Comparison

| Operation | Filesystem | SQLite | PostgreSQL |
|-----------|------------|---------|------------|
| Single read | Fast | Fast | Fast |
| Bulk read | Slow | Medium | Fast |
| Single write | Fast | Fast | Fast |
| Bulk write | Medium | Fast | Fast |
| Search | Very slow | Medium | Fast |
| Concurrent read | Good | Good | Excellent |
| Concurrent write | Poor | Poor | Excellent |

### Storage Comparison

| Feature | Filesystem | SQLite | PostgreSQL |
|---------|------------|---------|------------|
| File size | Multiple files | Single file | Database |
| Backup | Copy directory | Copy file | Dump/restore |
| Transactions | None | ACID | ACID |
| Integrity | Manual | Automatic | Automatic |
| Compression | None | None | Available |

### Scalability Comparison

| Metric | Filesystem | SQLite | PostgreSQL |
|---------|------------|---------|------------|
| Max prompts | ~10,000 | ~100,000 | Unlimited |
| Concurrent users | 1-5 | 1-10 | 100+ |
| Read throughput | Low | Medium | High |
| Write throughput | Low | Medium | High |
| Query complexity | None | Basic | Advanced |

## 🚀 Choosing the Right Backend

### Development Environment

```python
# For development - use filesystem
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./dev_prompts
```

**Why**: Easy to edit files directly, version control friendly

### Testing Environment

```python
# For testing - use SQLite in memory
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///:memory:
```

**Why**: Fast, isolated, no cleanup needed

### Small Applications

```python
# For small apps - use SQLite
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
```

**Why**: No server needed, good performance for small scale

### Production Applications

```python
# For production - use PostgreSQL
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:pass@prod-db:5432/prompts
PROMPT_GEAR_POOL_SIZE=20
PROMPT_GEAR_MAX_CONNECTIONS=100
```

**Why**: High performance, concurrent access, advanced features

## 🐳 Docker Setup

### PostgreSQL Development Environment

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: prompts
      POSTGRES_USER: promptgear
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U promptgear"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Multi-Backend Testing

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  postgres-test:
    image: postgres:15
    environment:
      POSTGRES_DB: test_prompts
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data
    ports:
      - "5433:5432"
```

## 🔧 Backend Migration

### Filesystem to SQLite

```python
def migrate_filesystem_to_sqlite():
    # Source: filesystem
    fs_backend = FilesystemBackend("./prompts")
    fs_pm = PromptManager(backend=fs_backend)
    
    # Destination: SQLite
    sqlite_backend = SQLiteBackend("sqlite:///prompts.db")
    sqlite_pm = PromptManager(backend=sqlite_backend)
    
    # Migrate all prompts
    prompts = fs_pm.list_prompts()
    for prompt in prompts:
        sqlite_pm.create_prompt(
            name=prompt.name,
            version=prompt.version,
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            config=prompt.config,
            overwrite=True
        )
```

### SQLite to PostgreSQL

```python
def migrate_sqlite_to_postgres():
    # Source: SQLite
    sqlite_backend = SQLiteBackend("sqlite:///prompts.db")
    sqlite_pm = PromptManager(backend=sqlite_backend)
    
    # Destination: PostgreSQL
    postgres_backend = PostgresBackend(
        "postgresql://user:pass@localhost:5432/prompts"
    )
    postgres_pm = PromptManager(backend=postgres_backend)
    
    # Migrate all prompts
    prompts = sqlite_pm.list_prompts()
    for prompt in prompts:
        postgres_pm.create_prompt(
            name=prompt.name,
            version=prompt.version,
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            config=prompt.config,
            overwrite=True
        )
```

## 🔄 Version Management Across Backends

All backends implement the same version management system with sequence-based versioning and explicit latest tracking.

### Core Features

#### 1. Sequence Number Assignment
- Each prompt gets auto-incrementing sequence numbers (1, 2, 3...)
- Sequence numbers are maintained per prompt name
- Deleted versions don't affect sequence numbering

#### 2. Latest Version Tracking
- Exactly one version per prompt is marked as "latest"
- Creating a new version automatically updates the latest flag
- Deleting the latest version promotes the highest sequence number

#### 3. Automatic Metadata Management
- Creation and update timestamps are automatically maintained
- Backend-specific optimizations for metadata storage
- Consistent behavior across all backends

### Implementation Details

| Backend | Sequence Storage | Latest Tracking | Metadata |
|---------|------------------|-----------------|----------|
| **Filesystem** | `.metadata.json` | Symlink + JSON | JSON file |
| **SQLite** | `prompt_metadata` table | `is_latest` column | Database columns |
| **PostgreSQL** | Database constraints | `is_latest` column | Database columns |

### Example Usage

```python
# Works identically across all backends
pm = PromptManager()  # Auto-detects backend

# Create versions with auto-sequence numbering
v1 = pm.create_prompt("example", "v1", "System v1", "User v1")
print(f"Created: {v1.sequence_number}, Latest: {v1.is_latest}")  # 1, True

v2 = pm.create_prompt("example", "v2", "System v2", "User v2")
print(f"Created: {v2.sequence_number}, Latest: {v2.is_latest}")  # 2, True

# v1 is automatically marked as not latest
v1_updated = pm.get_prompt("example", "v1")
print(f"v1 Latest: {v1_updated.is_latest}")  # False

# Get latest version (no version specified)
latest = pm.get_prompt("example")
print(f"Latest version: {latest.version}")  # v2

# Delete latest version - auto-promotes previous
pm.delete_prompt("example", "v2")
new_latest = pm.get_prompt("example")
print(f"New latest: {new_latest.version}")  # v1
print(f"Is latest: {new_latest.is_latest}")  # True
```

### Version Integrity

All backends ensure:
- **Uniqueness**: No duplicate sequence numbers per prompt
- **Consistency**: Exactly one latest version per prompt
- **Atomicity**: Version operations are transactional
- **Durability**: Metadata survives backend restarts

### Migration Between Backends

Version management is compatible across backends:

```python
# Export from filesystem
fs_pm = PromptManager(backend=FilesystemBackend("./prompts"))
prompts = fs_pm.list_prompts()

# Import to PostgreSQL
pg_pm = PromptManager(backend=PostgresBackend(connection_string))
for prompt in prompts:
    pg_pm.create_prompt(
        prompt.name, prompt.version,
        prompt.system_prompt, prompt.user_prompt,
        config=prompt.config
    )
```

## 🔍 Backend Monitoring

### Health Checks

```python
def check_backend_health():
    try:
        pm = PromptManager()
        
        # Test basic operations
        pm.create_prompt("health", "v1", "test", "test", overwrite=True)
        pm.get_prompt("health", "v1")
        pm.delete_prompt("health", "v1")
        
        return {"status": "healthy", "backend": pm.config.backend}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Performance Monitoring

```python
import time
from contextlib import contextmanager

@contextmanager
def monitor_operation(operation_name):
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        print(f"{operation_name}: {duration:.3f}s")

# Usage
with monitor_operation("create_prompt"):
    pm.create_prompt("test", "v1", "system", "user")
```

## 📚 Next Steps

- Learn about [Configuration](configuration.md) for backend setup
- Check [Best Practices](best-practices.md) for production usage
- Explore [Examples](examples.md) for real-world implementations
- Read [Troubleshooting](troubleshooting.md) for common issues
