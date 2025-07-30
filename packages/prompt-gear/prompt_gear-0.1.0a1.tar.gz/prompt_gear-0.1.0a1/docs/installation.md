# Installation & Setup

This guide covers installing and setting up Prompt Gear in your environment.

## 📦 Installation

### Using pip

```bash
pip install prompt-gear
```

### Development Installation

If you want to contribute or run the latest development version:

```bash
git clone https://github.com/miniGears/prompt-gear.git
cd prompt-gear
pip install -e .
```

### Using uv (Recommended for Development)

```bash
git clone https://github.com/miniGears/prompt-gear.git
cd prompt-gear
uv sync
```

## 🚀 Initial Setup

### 1. Initialize Prompt Gear

Choose your storage backend and initialize:

```bash
# Filesystem backend (default, no database required)
promptgear init --backend filesystem

# SQLite backend (local database file)
promptgear init --backend sqlite

# PostgreSQL backend (requires PostgreSQL server)
promptgear init --backend postgres
```

### 2. Configuration

Prompt Gear uses environment variables for configuration. Create a `.env` file in your project root:

```env
# Filesystem backend
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./prompts

# SQLite backend
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db

# PostgreSQL backend
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
```

### 3. Verify Installation

Test that everything is working:

```bash
# Check status
promptgear status

# Create a test prompt
promptgear create test_prompt --version v1 \
  --system "You are helpful" \
  --user "Hello world"

# List prompts
promptgear list

# Get the prompt
promptgear get test_prompt v1
```

## 🔧 Backend-Specific Setup

### Filesystem Backend

**Requirements**: None (uses local YAML files)

**Setup**:
```bash
promptgear init --backend filesystem
```

**Configuration**:
```env
PROMPT_GEAR_BACKEND=filesystem
PROMPT_GEAR_PROMPT_DIR=./prompts  # Directory for YAML files
```

**Pros**:
- No database required
- Human-readable YAML files
- Version control friendly
- Fast for small to medium datasets

**Cons**:
- No advanced querying
- No concurrent access protection
- Limited scalability

### SQLite Backend

**Requirements**: None (SQLite is built into Python)

**Setup**:
```bash
promptgear init --backend sqlite
```

**Configuration**:
```env
PROMPT_GEAR_BACKEND=sqlite
PROMPT_GEAR_DB_URL=sqlite:///prompts.db
```

**Pros**:
- No server required
- ACID transactions
- Good for single-user applications
- Full-text search support

**Cons**:
- No concurrent writers
- Limited scalability
- Single file database

### PostgreSQL Backend

**Requirements**: PostgreSQL server, psycopg2-binary

**Setup**:

1. Install PostgreSQL server
2. Create database and user:
   ```sql
   CREATE DATABASE prompts;
   CREATE USER promptgear WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE prompts TO promptgear;
   ```

3. Initialize backend:
   ```bash
   promptgear init --backend postgres
   ```

**Configuration**:
```env
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://promptgear:your_password@localhost:5432/prompts
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
```

**Docker Setup** (Recommended for development):
```bash
# Use the provided docker-compose.yml
docker-compose up -d postgres
```

**Pros**:
- High performance and scalability
- Concurrent access support
- Advanced querying capabilities
- Connection pooling
- Full-text search with PostgreSQL features

**Cons**:
- Requires PostgreSQL server
- More complex setup
- Higher resource usage

## 🐳 Docker Development

For easy development and testing, use Docker:

```bash
# Start PostgreSQL for testing
docker-compose up -d postgres

# Run tests
make test-postgres

# Stop services
docker-compose down
```

## 🧪 Testing Your Setup

### Basic Functionality Test

```bash
# Create test prompt
promptgear create hello_world --version v1 \
  --system "You are a helpful assistant" \
  --user "Say hello to {{name}}"

# Verify it works
promptgear get hello_world v1
```

### Python SDK Test

```python
from promptgear import PromptManager

# Initialize
pm = PromptManager()

# Create prompt
prompt = pm.create_prompt(
    name="test_sdk",
    version="v1",
    system_prompt="You are helpful",
    user_prompt="Hello {{user}}"
)

# Get prompt
retrieved = pm.get_prompt("test_sdk", "v1")
print(f"System: {retrieved.system_prompt}")
print(f"User: {retrieved.user_prompt}")
```

## 🔍 Troubleshooting

### Common Issues

1. **"promptgear command not found"**
   - Ensure Prompt Gear is installed: `pip install prompt-gear`
   - Check your PATH includes pip install directory

2. **Database connection errors**
   - Verify your database server is running
   - Check connection string in `.env` file
   - Ensure database user has proper permissions

3. **Permission errors with filesystem backend**
   - Check write permissions in the prompts directory
   - Ensure the directory exists and is writable

4. **Module import errors**
   - Verify installation: `pip show prompt-gear`
   - Try reinstalling: `pip uninstall prompt-gear && pip install prompt-gear`

### Getting Help

- Check the [Troubleshooting](troubleshooting.md) guide
- Run `promptgear status` to check backend status
- Enable debug logging by setting `PROMPT_GEAR_DEBUG=1`

## ✅ Next Steps

- Learn the [CLI commands](cli-reference.md)
- Explore the [Python SDK](python-sdk.md)
- Read [Best Practices](best-practices.md)
- Check out [Examples](examples.md)
