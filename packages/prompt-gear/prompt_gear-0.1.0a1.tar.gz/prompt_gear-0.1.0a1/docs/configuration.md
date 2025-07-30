# Configuration

Complete guide to configuring Prompt Gear for different environments and use cases.

## 🔧 Configuration Methods

Prompt Gear supports multiple configuration methods, in order of precedence:

1. **Environment variables** (highest priority)
2. **Configuration file** (`.env` file)
3. **Default values** (lowest priority)

## 🌍 Environment Variables

### Core Configuration

```bash
# Backend selection
PROMPT_GEAR_BACKEND=filesystem|sqlite|postgres

# Debug mode
PROMPT_GEAR_DEBUG=0|1

# Custom configuration file path
PROMPT_GEAR_CONFIG_FILE=/path/to/custom.env
```

### Filesystem Backend

```bash
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./prompts
```

### SQLite Backend

```bash
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
```

### PostgreSQL Backend

```bash
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
```

## 📄 Configuration File

Create a `.env` file in your project root:

```env
# .env
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://promptgear:password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=10
PROMPT_GEAR_MAX_CONNECTIONS=50
PROMPT_GEAR_DEBUG=0
```

### Custom Configuration File

```python
from promptgear import PromptManager

# Use custom config file
pm = PromptManager(config_file="production.env")
```

## 🏗️ Backend-Specific Configuration

### Filesystem Backend

**Configuration:**
```env
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./prompts
```

**Directory Structure:**
```
prompts/
├── chatbot/
│   ├── v1.yaml
│   ├── v2.yaml
│   └── v3.yaml
├── assistant/
│   ├── v1.yaml
│   └── v2.yaml
└── translator/
    └── v1.yaml
```

**Advanced Options:**
```python
from promptgear.filesystem_backend import FilesystemBackend

# Custom directory and file extension
backend = FilesystemBackend(
    prompt_dir="./custom_prompts",
    file_extension=".yml"  # Default is .yaml
)
```

### SQLite Backend

**Configuration:**
```env
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
```

**Database URL Formats:**
```bash
# Relative path
PROMPT_GEAR_DB_URL=sqlite:///./data/prompts.db

# Absolute path
PROMPT_GEAR_DB_URL=sqlite:////absolute/path/to/prompts.db

# In-memory (for testing)
PROMPT_GEAR_DB_URL=sqlite:///:memory:
```

**Advanced Options:**
```python
from promptgear.sqlite_backend import SQLiteBackend

# Custom database with additional options
backend = SQLiteBackend(
    db_url="sqlite:///prompts.db",
    timeout=30,  # Connection timeout
    check_same_thread=False  # For multi-threading
)
```

### PostgreSQL Backend

**Configuration:**
```env
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
```

**Database URL Formats:**
```bash
# Basic format
postgresql://user:password@host:port/database

# With additional parameters
postgresql://user:password@host:port/database?sslmode=require

# With connection pooling info
postgresql://user:password@host:port/database?pool_size=10&max_connections=50
```

**Advanced Options:**
```python
from promptgear.postgres_backend import PostgresBackend

# Custom configuration
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost/prompts",
    pool_size=10,
    max_connections=50,
    timeout=30,
    retry_attempts=3
)
```

## 🐳 Docker Configuration

### Development with Docker Compose

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

  app:
    build: .
    environment:
      PROMPT_GEAR_BACKEND: postgres
      PROMPT_GEAR_DB_URL: postgresql://promptgear:password@postgres:5432/prompts
      PROMPT_GEAR_POOL_SIZE: 5
      PROMPT_GEAR_MAX_CONNECTIONS: 20
    depends_on:
      - postgres
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: myapp:latest
    environment:
      PROMPT_GEAR_BACKEND: postgres
      PROMPT_GEAR_DB_URL: postgresql://user:${DB_PASSWORD}@db.example.com:5432/prompts
      PROMPT_GEAR_POOL_SIZE: 20
      PROMPT_GEAR_MAX_CONNECTIONS: 100
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

## 🔒 Security Configuration

### Database Security

```bash
# Use environment variables for sensitive data
export DB_PASSWORD="your_secure_password"
export PROMPT_GEAR_DB_URL="postgresql://user:${DB_PASSWORD}@localhost/prompts"

# Or use a secrets management system
PROMPT_GEAR_DB_URL="postgresql://user:$(cat /run/secrets/db_password)@localhost/prompts"
```

### SSL Configuration

```bash
# PostgreSQL with SSL
PROMPT_GEAR_DB_URL="postgresql://user:pass@localhost/prompts?sslmode=require"

# With custom SSL certificate
PROMPT_GEAR_DB_URL="postgresql://user:pass@localhost/prompts?sslmode=require&sslcert=/path/to/cert.pem"
```

## 🌐 Environment-Specific Configurations

### Development

```env
# development.env
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///dev_prompts.db
PROMPT_GEAR_DEBUG=1
```

### Testing

```env
# testing.env
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///:memory:
PROMPT_GEAR_DEBUG=1
```

### Staging

```env
# staging.env
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:pass@staging-db:5432/prompts
PROMPT_GEAR_POOL_SIZE=3
PROMPT_GEAR_MAX_CONNECTIONS=10
PROMPT_GEAR_DEBUG=0
```

### Production

```env
# production.env
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:pass@prod-db:5432/prompts
PROMPT_GEAR_POOL_SIZE=20
PROMPT_GEAR_MAX_CONNECTIONS=100
PROMPT_GEAR_DEBUG=0
```

## 📝 Configuration File Examples

### Multi-Environment Setup

```python
import os
from promptgear import PromptManager

# Determine environment
env = os.getenv("ENVIRONMENT", "development")

# Load appropriate config
config_files = {
    "development": "dev.env",
    "testing": "test.env",
    "staging": "staging.env",
    "production": "prod.env"
}

pm = PromptManager(config_file=config_files[env])
```

### Custom Configuration Class

```python
from promptgear.config import Config

class CustomConfig(Config):
    def __init__(self):
        super().__init__()
        # Custom configuration logic
        if self.backend == "postgres":
            self.pool_size = 20
            self.max_connections = 100
```

## 🔍 Configuration Validation

### Check Current Configuration

```python
from promptgear import PromptManager

pm = PromptManager()

# Check backend configuration
print(f"Backend: {pm.config.backend}")
print(f"Database URL: {pm.config.get_backend_config()}")

# Validate configuration
if pm.config.backend == "postgres":
    backend_config = pm.config.get_backend_config()
    print(f"Pool size: {backend_config['pool_size']}")
    print(f"Max connections: {backend_config['max_connections']}")
```

### Configuration Testing

```python
import os
import tempfile
from promptgear import PromptManager

def test_filesystem_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['PROMPT_GEAR_BACKEND'] = 'filesystem'
        os.environ['PROMPT_GEAR_PROMPT_DIR'] = tmpdir
        
        pm = PromptManager()
        assert pm.config.backend == 'filesystem'
        assert pm.config.get_backend_config()['prompt_dir'] == tmpdir

def test_sqlite_config():
    os.environ['PROMPT_GEAR_BACKEND'] = 'sqlite'
    os.environ['PROMPT_GEAR_DB_URL'] = 'sqlite:///test.db'
    
    pm = PromptManager()
    assert pm.config.backend == 'sqlite'
    assert pm.config.get_backend_config()['db_url'] == 'sqlite:///test.db'
```

## 🚀 Performance Configuration

### Connection Pooling

```bash
# PostgreSQL connection pooling
PROMPT_GEAR_POOL_SIZE=10        # Initial pool size
PROMPT_GEAR_MAX_CONNECTIONS=50  # Maximum connections
```

### Memory Management

```python
# For large datasets, consider:
from promptgear.postgres_backend import PostgresBackend

backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost/prompts",
    pool_size=20,              # Higher for concurrent access
    max_connections=100,       # Limit total connections
    timeout=30                 # Connection timeout
)
```

## 🔧 Configuration Troubleshooting

### Common Issues

1. **Backend not found**
   ```bash
   # Check backend spelling
   PROMPT_GEAR_BACKEND=postgres  # Not "postgresql"
   ```

2. **Database connection errors**
   ```bash
   # Check connection string format
   PROMPT_GEAR_DB_URL=postgresql://user:pass@localhost:5432/prompts
   ```

3. **Permission errors**
   ```bash
   # Check file permissions for filesystem backend
   chmod 755 ./prompts
   ```

### Debug Configuration

```bash
# Enable debug mode
PROMPT_GEAR_DEBUG=1

# Check configuration
promptgear status --verbose
```

### Configuration Validation Script

```python
#!/usr/bin/env python3
"""Configuration validation script."""

import os
import sys
from promptgear import PromptManager

def validate_config():
    try:
        pm = PromptManager()
        print(f"✓ Backend: {pm.config.backend}")
        
        # Test basic operations
        pm.create_prompt("test", "v1", "Test", "Test", overwrite=True)
        prompt = pm.get_prompt("test", "v1")
        pm.delete_prompt("test", "v1")
        
        print("✓ Configuration valid")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)
```

## 📚 Next Steps

- Learn about [Backends](backends.md)
- Read [Best Practices](best-practices.md)
- Check out [Examples](examples.md)
- Explore [Python SDK](python-sdk.md)
