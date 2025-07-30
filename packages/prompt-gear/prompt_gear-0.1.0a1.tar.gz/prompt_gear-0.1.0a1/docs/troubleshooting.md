# Troubleshooting

Common issues and solutions for Prompt Gear.

## 🚨 Installation Issues

### 1. Package Not Found

**Error:**
```
ERROR: Could not find a version that satisfies the requirement prompt-gear
```

**Solutions:**

1. **Check package name:**
   ```bash
   pip install prompt-gear  # Correct
   # Not: pip install promptgear
   ```

2. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   pip install prompt-gear
   ```

3. **Use Python 3.8+ (required):**
   ```bash
   python --version  # Should be 3.8+
   ```

4. **Install from source (if package not available):**
   ```bash
   git clone https://github.com/miniGears/prompt-gear.git
   cd prompt-gear
   pip install -e .
   ```

### 2. Command Not Found

**Error:**
```
'promptgear' is not recognized as an internal or external command
```

**Solutions:**

1. **Check installation:**
   ```bash
   pip show prompt-gear
   ```

2. **Use Python module:**
   ```bash
   python -m promptgear --help
   ```

3. **Check PATH:**
   ```bash
   # Windows
   where promptgear
   
   # Linux/macOS
   which promptgear
   ```

4. **Reinstall:**
   ```bash
   pip uninstall prompt-gear
   pip install prompt-gear
   ```

### 3. Import Errors

**Error:**
```python
ModuleNotFoundError: No module named 'promptgear'
```

**Solutions:**

1. **Verify installation:**
   ```bash
   pip list | grep prompt-gear
   ```

2. **Check Python environment:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. **Use correct Python:**
   ```bash
   # If using virtual environment
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

## 🔧 Configuration Issues

### 1. Backend Configuration Errors

**Error:**
```
ValueError: Unsupported backend: postgres
```

**Solutions:**

1. **Check backend spelling:**
   ```bash
   PROMPT_GEAR_BACKEND=postgres  # Not "postgresql"
   ```

2. **Verify environment variables:**
   ```bash
   # Check current settings
   env | grep PROMPT_GEAR
   
   # Or in Python
   import os
   print(os.environ.get('PROMPT_GEAR_BACKEND'))
   ```

3. **Use correct backend names:**
   ```bash
   # Valid backends
   PROMPT_GEAR_BACKEND=filesystem
   PROMPT_GEAR_BACKEND=sqlite
   PROMPT_GEAR_BACKEND=postgres
   ```

### 2. Database Connection Issues

**Error:**
```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**Solutions:**

1. **Check PostgreSQL server:**
   ```bash
   # Check if running
   pg_isready -h localhost -p 5432
   
   # Start if needed
   brew services start postgresql  # macOS
   sudo systemctl start postgresql  # Linux
   ```

2. **Verify connection string:**
   ```bash
   PROMPT_GEAR_DB_URL=postgresql://user:password@localhost:5432/database
   ```

3. **Test connection manually:**
   ```bash
   psql -h localhost -p 5432 -U user -d database
   ```

4. **Check firewall/network:**
   ```bash
   telnet localhost 5432
   ```

### 3. Environment Variable Issues

**Error:**
```
Backend configuration not found
```

**Solutions:**

1. **Create .env file:**
   ```bash
   # In project root
   echo "PROMPT_GEAR_BACKEND=filesystem" > .env
   echo "PROMPT_GEAR_PROMPT_DIR=./prompts" >> .env
   ```

2. **Load environment variables:**
   ```python
   # In Python
   from dotenv import load_dotenv
   load_dotenv()
   
   from promptgear import PromptManager
   pm = PromptManager()
   ```

3. **Set system environment variables:**
   ```bash
   # Linux/macOS
   export PROMPT_GEAR_BACKEND=filesystem
   
   # Windows
   set PROMPT_GEAR_BACKEND=filesystem
   ```

## 🗄️ Database Issues

### 1. SQLite Lock Errors

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. **Check for zombie processes:**
   ```bash
   # Kill processes using the database
   lsof | grep prompts.db
   ```

2. **Use WAL mode:**
   ```python
   import sqlite3
   conn = sqlite3.connect("prompts.db")
   conn.execute("PRAGMA journal_mode=WAL")
   conn.close()
   ```

3. **Increase timeout:**
   ```python
   from promptgear.sqlite_backend import SQLiteBackend
   backend = SQLiteBackend("sqlite:///prompts.db", timeout=30)
   ```

### 2. PostgreSQL Permission Errors

**Error:**
```
psycopg2.ProgrammingError: permission denied for relation prompts
```

**Solutions:**

1. **Grant permissions:**
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE prompts TO your_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
   ```

2. **Use superuser for setup:**
   ```bash
   psql -U postgres -c "CREATE USER promptgear WITH SUPERUSER PASSWORD 'password';"
   ```

3. **Check database ownership:**
   ```sql
   \l  -- List databases and owners
   \dt -- List tables and owners
   ```

### 3. Connection Pool Issues

**Error:**
```
psycopg2.pool.PoolError: connection pool exhausted
```

**Solutions:**

1. **Increase pool size:**
   ```bash
   PROMPT_GEAR_POOL_SIZE=20
   PROMPT_GEAR_MAX_CONNECTIONS=100
   ```

2. **Reuse PromptManager instances:**
   ```python
   # Good: single instance
   pm = PromptManager()
   
   # Bad: creates new connections
   def get_prompt():
       pm = PromptManager()  # Don't do this
       return pm.get_prompt("test", "v1")
   ```

3. **Monitor connections:**
   ```sql
   SELECT count(*) FROM pg_stat_activity WHERE datname = 'prompts';
   ```

## 📁 File System Issues

### 1. Permission Errors

**Error:**
```
PermissionError: [Errno 13] Permission denied: './prompts'
```

**Solutions:**

1. **Check directory permissions:**
   ```bash
   ls -la ./prompts
   chmod 755 ./prompts
   ```

2. **Create directory first:**
   ```bash
   mkdir -p ./prompts
   chmod 755 ./prompts
   ```

3. **Use different directory:**
   ```bash
   PROMPT_GEAR_PROMPT_DIR=~/prompts
   ```

### 2. File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: './prompts/test/v1.yaml'
```

**Solutions:**

1. **Check directory structure:**
   ```bash
   ls -la ./prompts/
   ls -la ./prompts/test/
   ```

2. **Verify prompt exists:**
   ```bash
   promptgear list
   ```

3. **Create missing directories:**
   ```bash
   mkdir -p ./prompts/test
   ```

### 3. YAML Parsing Errors

**Error:**
```
yaml.scanner.ScannerError: while scanning a quoted scalar
```

**Solutions:**

1. **Check YAML syntax:**
   ```bash
   # Validate YAML file
   python -c "import yaml; yaml.safe_load(open('prompts/test/v1.yaml'))"
   ```

2. **Fix common YAML issues:**
   ```yaml
   # Bad: unescaped quotes
   user_prompt: "Say "hello" to user"
   
   # Good: escaped quotes
   user_prompt: "Say \"hello\" to user"
   
   # Or use single quotes
   user_prompt: 'Say "hello" to user'
   ```

3. **Use literal blocks for multi-line:**
   ```yaml
   system_prompt: |
     You are a helpful assistant.
     Always be polite and professional.
   ```

## 🔍 CLI Issues

### 1. Command Parsing Errors

**Error:**
```
Error: No such option: --backend
```

**Solutions:**

1. **Check command syntax:**
   ```bash
   promptgear --help
   promptgear init --help
   ```

2. **Use correct options:**
   ```bash
   # Correct
   promptgear init --backend postgres
   
   # Wrong
   promptgear --backend postgres init
   ```

3. **Quote complex arguments:**
   ```bash
   promptgear create test --config '{"temperature": 0.7}'
   ```

### 2. JSON Parsing Errors

**Error:**
```
json.JSONDecodeError: Expecting ',' delimiter
```

**Solutions:**

1. **Validate JSON:**
   ```bash
   echo '{"temperature": 0.7}' | python -m json.tool
   ```

2. **Use single quotes for shell:**
   ```bash
   promptgear create test --config '{"temperature": 0.7}'
   ```

3. **Escape in double quotes:**
   ```bash
   promptgear create test --config "{\"temperature\": 0.7}"
   ```

### 3. Interactive Mode Issues

**Error:**
```
KeyboardInterrupt during interactive input
```

**Solutions:**

1. **Use non-interactive mode:**
   ```bash
   promptgear create test --system "System" --user "User"
   ```

2. **Prepare input in advance:**
   ```bash
   echo -e "test\nv1\nSystem prompt\nUser prompt\n{}" | promptgear create --interactive
   ```

## 🐍 Python SDK Issues

### 1. Import Errors

**Error:**
```python
ImportError: cannot import name 'PromptManager' from 'promptgear'
```

**Solutions:**

1. **Check installation:**
   ```bash
   pip show prompt-gear
   ```

2. **Use correct import:**
   ```python
   from promptgear import PromptManager  # Correct
   # Not: from promptgear.manager import PromptManager
   ```

3. **Check for name conflicts:**
   ```python
   # Check if you have a file named promptgear.py
   import promptgear
   print(promptgear.__file__)
   ```

### 2. Type Errors

**Error:**
```python
TypeError: PromptManager.__init__() got an unexpected keyword argument 'backend_type'
```

**Solutions:**

1. **Use correct parameter names:**
   ```python
   # Correct
   pm = PromptManager(backend=backend)
   
   # Wrong
   pm = PromptManager(backend_type=backend)
   ```

2. **Check documentation:**
   ```python
   help(PromptManager.__init__)
   ```

### 3. Configuration Errors

**Error:**
```python
AttributeError: 'Config' object has no attribute 'get_backend_config'
```

**Solutions:**

1. **Update to latest version:**
   ```bash
   pip install --upgrade prompt-gear
   ```

2. **Check configuration method:**
   ```python
   from promptgear.config import get_config
   config = get_config()
   print(dir(config))
   ```

## 🔄 Runtime Issues

### 1. Memory Issues

**Error:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Limit batch operations:**
   ```python
   # Process in chunks
   prompts = pm.list_prompts()
   for chunk in chunks(prompts, 100):
       process_chunk(chunk)
   ```

2. **Use generators:**
   ```python
   def process_prompts():
       for prompt in pm.list_prompts():
           yield process_prompt(prompt)
   ```

3. **Clear cache regularly:**
   ```python
   # If using caching
   cache.clear()
   ```

### 2. Performance Issues

**Error:**
```
Operations are very slow
```

**Solutions:**

1. **Check backend performance:**
   ```bash
   # Test database performance
   promptgear status --verbose
   ```

2. **Use appropriate backend:**
   ```python
   # For many prompts, use PostgreSQL
   PROMPT_GEAR_BACKEND=postgres
   ```

3. **Add indexes (PostgreSQL):**
   ```sql
   CREATE INDEX idx_prompts_name ON prompts(name);
   ```

4. **Monitor resource usage:**
   ```bash
   # Check system resources
   top
   htop
   ```

### 3. Concurrency Issues

**Error:**
```
RuntimeError: Database is locked
```

**Solutions:**

1. **Use PostgreSQL for concurrent access:**
   ```python
   PROMPT_GEAR_BACKEND=postgres
   ```

2. **Implement retry logic:**
   ```python
   import time
   import random
   
   def retry_operation(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return func()
           except Exception as e:
               if attempt == max_retries - 1:
                   raise
               time.sleep(random.uniform(0.1, 0.5))
   ```

3. **Use connection pooling:**
   ```python
   backend = PostgresBackend(
       connection_string="postgresql://user:pass@localhost/prompts",
       pool_size=20
   )
   ```

## 🐳 Docker Issues

### 1. Container Connection Issues

**Error:**
```
psycopg2.OperationalError: could not connect to server: Connection refused
```

**Solutions:**

1. **Check container status:**
   ```bash
   docker ps
   docker logs postgres_container
   ```

2. **Wait for container to be ready:**
   ```bash
   # Wait for PostgreSQL to start
   docker exec postgres_container pg_isready
   ```

3. **Use correct hostname:**
   ```bash
   # In docker-compose
   PROMPT_GEAR_DB_URL=postgresql://user:pass@postgres:5432/prompts
   
   # Not localhost when in container
   ```

### 2. Volume Mount Issues

**Error:**
```
Permission denied: '/var/lib/postgresql/data'
```

**Solutions:**

1. **Check volume permissions:**
   ```bash
   docker exec postgres_container ls -la /var/lib/postgresql/data
   ```

2. **Use named volumes:**
   ```yaml
   # docker-compose.yml
   volumes:
     - postgres_data:/var/lib/postgresql/data
   ```

3. **Fix ownership:**
   ```bash
   docker exec postgres_container chown -R postgres:postgres /var/lib/postgresql/data
   ```

## 🔍 Debugging

### 1. Enable Debug Mode

```bash
export PROMPT_GEAR_DEBUG=1
promptgear status
```

### 2. Check Logs

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from promptgear import PromptManager
pm = PromptManager()
```

### 3. Test Components

```python
# Test configuration
from promptgear.config import get_config
config = get_config()
print(f"Backend: {config.backend}")
print(f"Config: {config.get_backend_config()}")

# Test backend directly
from promptgear.postgres_backend import PostgresBackend
backend = PostgresBackend("postgresql://user:pass@localhost/prompts")
print(f"Health check: {backend.health_check()}")
```

## 📞 Getting Help

### 1. Check Documentation

- [Installation](installation.md)
- [Configuration](configuration.md)
- [Python SDK](python-sdk.md)
- [CLI Reference](cli-reference.md)

### 2. Common Commands

```bash
# Check status
promptgear status --verbose

# Test configuration
promptgear list

# Create test prompt
promptgear create test_debug --version v1 --system "Test" --user "Test"

# Get test prompt
promptgear get test_debug v1
```

### 3. Report Issues

When reporting issues, include:

1. **Environment info:**
   ```bash
   python --version
   pip show prompt-gear
   echo $PROMPT_GEAR_BACKEND
   ```

2. **Error message:**
   ```bash
   promptgear status --verbose 2>&1
   ```

3. **Configuration:**
   ```bash
   env | grep PROMPT_GEAR
   ```

4. **Minimal reproduction:**
   ```python
   from promptgear import PromptManager
   pm = PromptManager()
   # Steps to reproduce the issue
   ```

## ✅ Prevention Tips

1. **Use version control** for filesystem backend
2. **Backup regularly** for database backends
3. **Monitor resource usage** in production
4. **Test configuration changes** in development first
5. **Use appropriate backend** for your use case
6. **Keep dependencies updated**

## 📚 Next Steps

- Review [Best Practices](best-practices.md)
- Check [Examples](examples.md) for working code
- Understand [Backends](backends.md) for architecture decisions
- Read [Configuration](configuration.md) for setup details
