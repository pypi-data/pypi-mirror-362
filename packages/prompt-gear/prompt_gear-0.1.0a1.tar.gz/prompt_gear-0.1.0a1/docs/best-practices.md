# Best Practices

This guide covers recommended practices for using Prompt Gear effectively in production environments.

## 🎯 General Best Practices

### 1. Version Management

**Use semantic versioning for prompts:**
```bash
# Good: Clear version progression
promptgear create chatbot --version v1.0.0 --system "Basic chatbot"
promptgear create chatbot --version v1.1.0 --system "Improved chatbot"
promptgear create chatbot --version v2.0.0 --system "Major chatbot update"

# Avoid: Unclear versions
promptgear create chatbot --version latest --system "Some chatbot"
```

**Create incremental versions:**
```python
# Good: Gradual improvements
pm.create_prompt("assistant", "v1", "Basic assistant", "Hello")
pm.create_prompt("assistant", "v2", "Polite assistant", "Hello, how may I help?")
pm.create_prompt("assistant", "v3", "Professional assistant", "Good day! How may I assist you?")
```

### 2. Naming Conventions

**Use descriptive, consistent names:**
```bash
# Good: Clear purpose
promptgear create customer_support_greeting --version v1
promptgear create email_summarizer --version v1
promptgear create code_reviewer --version v1

# Avoid: Vague names
promptgear create prompt1 --version v1
promptgear create thing --version v1
```

**Use underscores for multi-word names:**
```bash
# Good
promptgear create chatbot_greeting --version v1
promptgear create error_handler --version v1

# Avoid
promptgear create chatbotgreeting --version v1
promptgear create "error handler" --version v1  # Spaces cause issues
```

### 3. Environment Separation

**Use different backends for different environments:**
```bash
# Development
export PROMPT_GEAR_BACKEND=filesystem
export PROMPT_GEAR_PROMPT_DIR=./dev_prompts

# Production
export PROMPT_GEAR_BACKEND=postgres
export PROMPT_GEAR_DB_URL=postgresql://user:pass@prod-db:5432/prompts
```

**Environment-specific configurations:**
```python
# config.py
import os

ENVIRONMENTS = {
    "development": {
        "backend": "filesystem",
        "prompt_dir": "./dev_prompts"
    },
    "production": {
        "backend": "postgres",
        "db_url": "postgresql://user:pass@prod-db/prompts",
        "pool_size": 20
    }
}

env = os.getenv("ENVIRONMENT", "development")
config = ENVIRONMENTS[env]
```

## 🏗️ Architecture Best Practices

### 1. Backend Selection

**Choose backend based on needs:**

**Filesystem** - Good for:
- Small teams
- Version control integration
- Simple deployments
- Development environments

**SQLite** - Good for:
- Single-user applications
- Small to medium datasets
- Embedded applications
- Local development

**PostgreSQL** - Good for:
- Multi-user applications
- Large datasets
- Production environments
- Advanced querying needs

### 2. Connection Management

**Reuse PromptManager instances:**
```python
# Good: Single instance
class PromptService:
    def __init__(self):
        self.pm = PromptManager()
    
    def get_prompt(self, name, version):
        return self.pm.get_prompt(name, version)

# Avoid: Multiple instances
def get_prompt(name, version):
    pm = PromptManager()  # Creates new connections each time
    return pm.get_prompt(name, version)
```

**Use connection pooling for PostgreSQL:**
```python
from promptgear.postgres_backend import PostgresBackend

# Configure appropriate pool size
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost/prompts",
    pool_size=10,      # Based on expected concurrent users
    max_connections=50  # Database connection limit
)
```

### 3. Error Handling

**Always handle exceptions:**
```python
from promptgear import PromptNotFoundError, PromptAlreadyExistsError

def safe_get_prompt(name, version, fallback_version="v1"):
    try:
        return pm.get_prompt(name, version)
    except PromptNotFoundError:
        try:
            return pm.get_prompt(name, fallback_version)
        except PromptNotFoundError:
            return None  # or raise custom exception

def safe_create_prompt(name, version, system, user):
    try:
        return pm.create_prompt(name, version, system, user)
    except PromptAlreadyExistsError:
        # Decide: update, version bump, or error
        return pm.update_prompt(name, version, system_prompt=system, user_prompt=user)
```

## 📝 Prompt Design Best Practices

### 1. Template Structure

**Use clear, structured prompts:**
```python
# Good: Clear structure
system_prompt = """
You are a helpful customer support assistant.

Guidelines:
- Be polite and professional
- Provide accurate information
- Ask clarifying questions when needed
- Escalate complex issues appropriately
"""

user_prompt = """
Customer Query: {{query}}
Customer Name: {{customer_name}}
Priority: {{priority}}

Please provide a helpful response.
"""

# Avoid: Unclear prompts
system_prompt = "help customer"
user_prompt = "{{query}}"
```

### 2. Variable Naming

**Use descriptive variable names:**
```python
# Good: Clear variables
user_prompt = "Hello {{customer_name}}, regarding {{issue_type}}: {{description}}"

# Avoid: Unclear variables
user_prompt = "Hello {{x}}, regarding {{y}}: {{z}}"
```

### 3. Configuration Management

**Store model parameters in config:**
```python
# Good: Explicit configuration
config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.9,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
    "stop": ["Human:", "Assistant:"]
}

pm.create_prompt("chatbot", "v1", system, user, config=config)
```

## 🔒 Security Best Practices

### 1. Database Security

**Use environment variables for sensitive data:**
```bash
# Good: Environment variables
export DB_PASSWORD="secure_password"
export PROMPT_GEAR_DB_URL="postgresql://user:${DB_PASSWORD}@localhost/prompts"

# Avoid: Hardcoded credentials
export PROMPT_GEAR_DB_URL="postgresql://user:password123@localhost/prompts"
```

**Use connection encryption:**
```bash
# PostgreSQL with SSL
PROMPT_GEAR_DB_URL="postgresql://user:pass@localhost/prompts?sslmode=require"
```

### 2. Input Validation

**Validate prompt inputs:**
```python
import re

def validate_prompt_name(name):
    if not re.match(r'^[a-zA-Z0-9_]+$', name):
        raise ValueError("Prompt name must contain only letters, numbers, and underscores")
    if len(name) > 100:
        raise ValueError("Prompt name must be less than 100 characters")

def validate_version(version):
    if not re.match(r'^v\d+(\.\d+)*$', version):
        raise ValueError("Version must follow format: v1, v1.0, v1.0.0, etc.")
```

### 3. Access Control

**Implement access control in applications:**
```python
class SecurePromptManager:
    def __init__(self, user_id, permissions):
        self.pm = PromptManager()
        self.user_id = user_id
        self.permissions = permissions
    
    def get_prompt(self, name, version):
        if not self.can_read(name):
            raise PermissionError("Access denied")
        return self.pm.get_prompt(name, version)
    
    def create_prompt(self, name, version, system, user, config=None):
        if not self.can_write(name):
            raise PermissionError("Access denied")
        return self.pm.create_prompt(name, version, system, user, config)
```

## 🚀 Performance Best Practices

### 1. Caching

**Implement caching for frequently accessed prompts:**
```python
from functools import lru_cache

class CachedPromptManager:
    def __init__(self):
        self.pm = PromptManager()
    
    @lru_cache(maxsize=100)
    def get_prompt(self, name, version):
        return self.pm.get_prompt(name, version)
    
    def create_prompt(self, name, version, system, user, config=None):
        # Clear cache when creating new prompts
        self.get_prompt.cache_clear()
        return self.pm.create_prompt(name, version, system, user, config)
```

### 2. Batch Operations

**Process multiple prompts efficiently:**
```python
def batch_create_prompts(prompts_data):
    """Create multiple prompts in batch."""
    results = []
    for prompt_info in prompts_data:
        try:
            result = pm.create_prompt(**prompt_info)
            results.append(("success", result))
        except Exception as e:
            results.append(("error", str(e)))
    return results

# Usage
prompts = [
    {"name": "prompt1", "version": "v1", "system_prompt": "...", "user_prompt": "..."},
    {"name": "prompt2", "version": "v1", "system_prompt": "...", "user_prompt": "..."},
]
results = batch_create_prompts(prompts)
```

### 3. Connection Optimization

**Optimize database connections:**
```python
# For PostgreSQL
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost/prompts",
    pool_size=min(20, expected_concurrent_users),
    max_connections=100,
    timeout=30
)
```

## 🧪 Testing Best Practices

### 1. Unit Testing

**Test prompt operations:**
```python
import unittest
from promptgear import PromptManager
from promptgear.sqlite_backend import SQLiteBackend

class TestPromptOperations(unittest.TestCase):
    def setUp(self):
        self.pm = PromptManager(backend=SQLiteBackend(":memory:"))
    
    def test_create_and_get_prompt(self):
        # Create
        prompt = self.pm.create_prompt(
            "test", "v1", "system", "user", {"temp": 0.7}
        )
        self.assertEqual(prompt.name, "test")
        
        # Get
        retrieved = self.pm.get_prompt("test", "v1")
        self.assertEqual(retrieved.system_prompt, "system")
        self.assertEqual(retrieved.config["temp"], 0.7)
    
    def test_error_handling(self):
        with self.assertRaises(PromptNotFoundError):
            self.pm.get_prompt("nonexistent", "v1")
```

### 2. Integration Testing

**Test with real backends:**
```python
def test_postgres_integration():
    # Use test database
    backend = PostgresBackend("postgresql://test:test@localhost/test_prompts")
    pm = PromptManager(backend=backend)
    
    # Test operations
    pm.create_prompt("test", "v1", "system", "user")
    prompt = pm.get_prompt("test", "v1")
    assert prompt.name == "test"
    
    # Cleanup
    pm.delete_prompt("test", "v1")
```

### 3. Load Testing

**Test performance under load:**
```python
import concurrent.futures
import time

def load_test_prompts(num_operations=100):
    pm = PromptManager()
    
    def create_prompt(i):
        return pm.create_prompt(f"test_{i}", "v1", "system", "user")
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_prompt, i) for i in range(num_operations)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    print(f"Created {num_operations} prompts in {end_time - start_time:.2f} seconds")
    return results
```

## 📊 Monitoring Best Practices

### 1. Logging

**Implement comprehensive logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingPromptManager:
    def __init__(self):
        self.pm = PromptManager()
    
    def get_prompt(self, name, version):
        logger.info(f"Getting prompt: {name}:{version}")
        try:
            prompt = self.pm.get_prompt(name, version)
            logger.info(f"Successfully retrieved prompt: {name}:{version}")
            return prompt
        except Exception as e:
            logger.error(f"Failed to get prompt {name}:{version}: {e}")
            raise
```

### 2. Metrics

**Track usage metrics:**
```python
from collections import defaultdict
from datetime import datetime

class MetricsPromptManager:
    def __init__(self):
        self.pm = PromptManager()
        self.metrics = defaultdict(int)
        self.access_times = defaultdict(list)
    
    def get_prompt(self, name, version):
        key = f"{name}:{version}"
        self.metrics[key] += 1
        self.access_times[key].append(datetime.now())
        return self.pm.get_prompt(name, version)
    
    def get_usage_stats(self):
        return dict(self.metrics)
```

### 3. Health Checks

**Implement health checks:**
```python
def health_check():
    try:
        pm = PromptManager()
        # Test basic operations
        pm.create_prompt("health_check", "v1", "test", "test", overwrite=True)
        pm.get_prompt("health_check", "v1")
        pm.delete_prompt("health_check", "v1")
        return {"status": "healthy", "backend": pm.config.backend}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 🔄 Deployment Best Practices

### 1. Environment Management

**Use environment-specific configurations:**
```python
# deploy.py
import os
from promptgear import PromptManager

def deploy_prompts():
    env = os.getenv("ENVIRONMENT", "development")
    
    # Load environment-specific config
    config_file = f"{env}.env"
    pm = PromptManager(config_file=config_file)
    
    # Deploy prompts
    prompts_to_deploy = load_prompts_from_file("prompts.json")
    for prompt_data in prompts_to_deploy:
        pm.create_prompt(**prompt_data, overwrite=True)
```

### 2. Version Control Integration

**Track prompt changes:**
```bash
# Create deployment script
#!/bin/bash
set -e

# Deploy prompts from version control
python deploy_prompts.py

# Tag deployment
git tag "prompts-$(date +%Y%m%d-%H%M%S)"
```

### 3. Rollback Strategy

**Implement rollback capability:**
```python
def rollback_prompts(backup_version):
    """Rollback prompts to a previous version."""
    pm = PromptManager()
    
    # Load backup data
    backup_data = load_backup(backup_version)
    
    # Restore prompts
    for prompt_data in backup_data:
        pm.create_prompt(**prompt_data, overwrite=True)
        
    logger.info(f"Rolled back to version {backup_version}")
```

## 📚 Documentation Best Practices

### 1. Prompt Documentation

**Document prompt purpose and usage:**
```python
# prompts_documentation.py
PROMPT_DOCS = {
    "chatbot_greeting": {
        "purpose": "Initial greeting for customer support chatbot",
        "variables": {
            "customer_name": "Customer's full name",
            "issue_type": "Type of issue (billing, technical, etc.)"
        },
        "versions": {
            "v1": "Basic greeting",
            "v2": "Added personalization",
            "v3": "Added issue type handling"
        }
    }
}
```

### 2. API Documentation

**Document your prompt service API:**
```python
from fastapi import FastAPI
from promptgear import PromptManager

app = FastAPI(title="Prompt Service API")
pm = PromptManager()

@app.get("/prompt/{name}/{version}")
async def get_prompt(name: str, version: str):
    """
    Get a specific prompt by name and version.
    
    Args:
        name: Prompt name
        version: Prompt version (e.g., v1, v2.0)
    
    Returns:
        Prompt template with system/user prompts and configuration
    """
    return pm.get_prompt(name, version)
```

## 🎯 Summary

Following these best practices will help you:

- **Maintain** clean, organized prompt libraries
- **Scale** your applications effectively
- **Secure** your prompt management system
- **Monitor** usage and performance
- **Deploy** reliably across environments

Remember:
- Use clear naming conventions
- Implement proper error handling
- Choose appropriate backends
- Test thoroughly
- Monitor in production
- Document everything

## 📚 Next Steps

- Check out [Examples](examples.md) for real-world implementations
- Learn about [Backends](backends.md) for architecture decisions
- Explore [Troubleshooting](troubleshooting.md) for common issues
