# Python SDK

Complete guide to using Prompt Gear in your Python applications.

## 🚀 Quick Start

```python
from promptgear import PromptManager

# Initialize
pm = PromptManager()

# Create a prompt
prompt = pm.create_prompt(
    name="my_prompt",
    version="v1",
    system_prompt="You are helpful",
    user_prompt="Hello {{name}}",
    config={"temperature": 0.7}
)

# Use the prompt
retrieved = pm.get_prompt("my_prompt", "v1")
print(retrieved.system_prompt)
```

## 📚 Core Classes

### PromptManager

The main class for managing prompts.

```python
from promptgear import PromptManager

# Initialize with default backend
pm = PromptManager()

# Initialize with custom backend
from promptgear.sqlite_backend import SQLiteBackend
backend = SQLiteBackend("custom.db")
pm = PromptManager(backend=backend)

# Initialize with custom config file
pm = PromptManager(config_file="custom_config.env")
```

### PromptTemplate

Represents a prompt template with all its components.

```python
from promptgear.schema import PromptTemplate

# Create manually
prompt = PromptTemplate(
    name="example",
    version="v1",
    system_prompt="You are helpful",
    user_prompt="Hello {{user}}",
    config={"temperature": 0.7}
)

# Access properties
print(prompt.name)           # "example"
print(prompt.version)        # "v1"
print(prompt.system_prompt)  # "You are helpful"
print(prompt.user_prompt)    # "Hello {{user}}"
print(prompt.config)         # {"temperature": 0.7}
```

## 🔧 Core Methods

### Creating Prompts

```python
# Basic creation
prompt = pm.create_prompt(
    name="chatbot",
    version="v1",
    system_prompt="You are a helpful chatbot",
    user_prompt="User: {{message}}\nAssistant:",
    config={"temperature": 0.8, "max_tokens": 500}
)

# With overwrite
prompt = pm.create_prompt(
    name="chatbot",
    version="v1",
    system_prompt="Updated system prompt",
    user_prompt="Updated user prompt",
    overwrite=True
)

# Minimal creation
prompt = pm.create_prompt(
    name="simple",
    version="v1",
    system_prompt="You are helpful",
    user_prompt="{{input}}"
)
```

### Getting Prompts

```python
# Get specific prompt version
prompt = pm.get_prompt("chatbot", "v1")

# Get latest version (omit version parameter)
prompt = pm.get_prompt("chatbot")  # Returns the version marked as latest

# Handle missing prompts
try:
    prompt = pm.get_prompt("nonexistent", "v1")
except PromptNotFoundError:
    print("Prompt not found!")
```

**Version resolution:**
- If version is specified: Returns that exact version
- If version is omitted: Returns the version marked as `is_latest=True`
- The latest version is automatically managed by the system when creating/deleting prompts

### Updating Prompts

```python
# Update system prompt only
updated = pm.update_prompt(
    name="chatbot",
    version="v1",
    system_prompt="New system prompt"
)

# Update user prompt only
updated = pm.update_prompt(
    name="chatbot",
    version="v1",
    user_prompt="New user prompt"
)

# Update configuration only
updated = pm.update_prompt(
    name="chatbot",
    version="v1",
    config={"temperature": 0.9}
)

# Update multiple fields
updated = pm.update_prompt(
    name="chatbot",
    version="v1",
    system_prompt="New system",
    user_prompt="New user",
    config={"temperature": 0.5}
)
```

### Listing Prompts

```python
# List all prompts
all_prompts = pm.list_prompts()
for prompt in all_prompts:
    print(f"{prompt.name}:{prompt.version}")

# List prompts by name
chatbot_prompts = pm.list_prompts("chatbot")

# List versions of a prompt
versions = pm.list_versions("chatbot")
print(versions)  # ["v1", "v2", "v3"]
```

### Deleting Prompts

```python
# Delete a prompt
success = pm.delete_prompt("old_prompt", "v1")
if success:
    print("Deleted successfully")

# Handle missing prompts
try:
    pm.delete_prompt("nonexistent", "v1")
except PromptNotFoundError:
    print("Prompt not found!")
```

### Checking Existence

```python
# Check if prompt exists
exists = pm.prompt_exists("chatbot", "v1")
if exists:
    print("Prompt exists")
else:
    print("Prompt does not exist")
```

## 🗄️ Working with Backends

### Filesystem Backend

```python
from promptgear.filesystem_backend import FilesystemBackend

# Initialize
backend = FilesystemBackend("./my_prompts")
pm = PromptManager(backend=backend)

# Use normally
prompt = pm.create_prompt(
    name="test",
    version="v1",
    system_prompt="Test",
    user_prompt="{{input}}"
)
```

### SQLite Backend

```python
from promptgear.sqlite_backend import SQLiteBackend

# Initialize
backend = SQLiteBackend("prompts.db")
pm = PromptManager(backend=backend)

# Use normally
prompt = pm.create_prompt(
    name="test",
    version="v1",
    system_prompt="Test",
    user_prompt="{{input}}"
)
```

### PostgreSQL Backend

```python
from promptgear.postgres_backend import PostgresBackend

# Initialize
backend = PostgresBackend(
    connection_string="postgresql://user:pass@localhost/prompts",
    pool_size=5,
    max_connections=20
)
pm = PromptManager(backend=backend)

# Use normally
prompt = pm.create_prompt(
    name="test",
    version="v1",
    system_prompt="Test",
    user_prompt="{{input}}"
)
```

## 🔧 Configuration

### Environment Variables

```python
import os

# Set environment variables
os.environ['PROMPT_GEAR_BACKEND'] = 'postgres'
os.environ['PROMPT_GEAR_DB_URL'] = 'postgresql://user:pass@localhost/prompts'

# Initialize with environment config
pm = PromptManager()
```

### Configuration File

```python
# Create custom config file
config_content = """
PROMPT_GEAR_BACKEND=postgres
PROMPT_GEAR_DB_URL=postgresql://user:pass@localhost/prompts
PROMPT_GEAR_POOL_SIZE=10
"""

with open("custom.env", "w") as f:
    f.write(config_content)

# Use custom config
pm = PromptManager(config_file="custom.env")
```

## 🛠️ Advanced Usage

### Template Rendering

```python
# Get prompt with placeholders
prompt = pm.get_prompt("chatbot", "v1")
print(prompt.user_prompt)  # "Hello {{name}}, how are you?"

# Replace placeholders manually
user_input = prompt.user_prompt.replace("{{name}}", "Alice")
print(user_input)  # "Hello Alice, how are you?"

# Or use string formatting
user_input = prompt.user_prompt.format(name="Bob")
print(user_input)  # "Hello Bob, how are you?"
```

### Batch Operations

```python
# Create multiple prompts
prompts_to_create = [
    ("chatbot", "v1", "System 1", "User 1"),
    ("chatbot", "v2", "System 2", "User 2"),
    ("assistant", "v1", "System A", "User A"),
]

for name, version, system, user in prompts_to_create:
    pm.create_prompt(
        name=name,
        version=version,
        system_prompt=system,
        user_prompt=user
    )

# List all created prompts
all_prompts = pm.list_prompts()
print(f"Created {len(all_prompts)} prompts")
```

### Error Handling

```python
from promptgear import PromptNotFoundError, PromptAlreadyExistsError

try:
    # Try to create existing prompt
    pm.create_prompt("existing", "v1", "System", "User")
except PromptAlreadyExistsError:
    print("Prompt already exists, updating instead")
    pm.update_prompt("existing", "v1", system_prompt="Updated")

try:
    # Try to get non-existent prompt
    prompt = pm.get_prompt("nonexistent", "v1")
except PromptNotFoundError:
    print("Prompt not found, creating new one")
    pm.create_prompt("nonexistent", "v1", "System", "User")
```

### Connection Management

```python
# For database backends, connections are managed automatically
# But you can access backend methods if needed

# Get backend statistics (PostgreSQL only)
if hasattr(pm.backend, 'get_statistics'):
    stats = pm.backend.get_statistics()
    print(f"Total prompts: {stats['total_prompts']}")
    print(f"Total versions: {stats['total_versions']}")

# Check backend health
if hasattr(pm.backend, 'health_check'):
    is_healthy = pm.backend.health_check()
    print(f"Backend healthy: {is_healthy}")
```

## 🧪 Testing

### Unit Testing

```python
import unittest
from promptgear import PromptManager
from promptgear.sqlite_backend import SQLiteBackend

class TestPromptManager(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite for testing
        self.backend = SQLiteBackend(":memory:")
        self.pm = PromptManager(backend=self.backend)
    
    def test_create_prompt(self):
        prompt = self.pm.create_prompt(
            name="test",
            version="v1",
            system_prompt="Test system",
            user_prompt="Test user"
        )
        self.assertEqual(prompt.name, "test")
        self.assertEqual(prompt.version, "v1")
    
    def test_get_prompt(self):
        # Create first
        self.pm.create_prompt(
            name="test",
            version="v1",
            system_prompt="Test system",
            user_prompt="Test user"
        )
        
        # Then get
        retrieved = self.pm.get_prompt("test", "v1")
        self.assertEqual(retrieved.system_prompt, "Test system")
```

### Integration Testing

```python
import tempfile
import os
from promptgear import PromptManager

def test_with_filesystem():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set environment
        os.environ['PROMPT_GEAR_BACKEND'] = 'filesystem'
        os.environ['PROMPT_GEAR_PROMPT_DIR'] = tmpdir
        
        # Test
        pm = PromptManager()
        pm.create_prompt("test", "v1", "System", "User")
        
        # Verify file exists
        assert os.path.exists(os.path.join(tmpdir, "test", "v1.yaml"))
```

## 🔌 Integration Examples

### With LangChain

```python
from promptgear import PromptManager
from langchain.prompts import PromptTemplate as LCPromptTemplate

# Get prompt from Prompt Gear
pm = PromptManager()
prompt = pm.get_prompt("chatbot", "v1")

# Convert to LangChain prompt
lc_prompt = LCPromptTemplate(
    template=prompt.user_prompt,
    input_variables=["user_input"]
)

# Use with LangChain
formatted = lc_prompt.format(user_input="Hello world")
```

### With FastAPI

```python
from fastapi import FastAPI, HTTPException
from promptgear import PromptManager, PromptNotFoundError

app = FastAPI()
pm = PromptManager()

@app.get("/prompt/{name}/{version}")
async def get_prompt(name: str, version: str):
    try:
        prompt = pm.get_prompt(name, version)
        return {
            "name": prompt.name,
            "version": prompt.version,
            "system_prompt": prompt.system_prompt,
            "user_prompt": prompt.user_prompt,
            "config": prompt.config
        }
    except PromptNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt not found")

@app.post("/prompt/{name}/{version}")
async def create_prompt(
    name: str, 
    version: str, 
    system_prompt: str, 
    user_prompt: str, 
    config: dict = None
):
    prompt = pm.create_prompt(
        name=name,
        version=version,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        config=config or {}
    )
    return {"message": "Prompt created successfully"}
```

### With OpenAI

```python
import openai
from promptgear import PromptManager

# Get prompt
pm = PromptManager()
prompt = pm.get_prompt("chatbot", "v1")

# Use with OpenAI
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": prompt.user_prompt.format(user_input="Hello")}
    ],
    temperature=prompt.config.get("temperature", 0.7),
    max_tokens=prompt.config.get("max_tokens", 500)
)

print(response.choices[0].message.content)
```

## 🔍 Best Practices

### 1. Version Management

```python
# Create base version (sequence_number=1, is_latest=True)
pm.create_prompt("assistant", "v1", "Basic system", "Basic user")

# Create improved version (sequence_number=2, is_latest=True)
# v1 automatically becomes is_latest=False
pm.create_prompt("assistant", "v2", "Improved system", "Improved user")

# Always specify version in production code for consistency
prompt = pm.get_prompt("assistant", "v2")  # Explicit version

# Or use latest version for development/testing
prompt = pm.get_prompt("assistant")  # Gets latest version

# Check version metadata
print(f"Version: {prompt.version}")
print(f"Sequence: {prompt.sequence_number}")
print(f"Is Latest: {prompt.is_latest}")
print(f"Created: {prompt.created_at}")
```

### 2. Error Handling

```python
def safe_get_prompt(name: str, version: str, fallback_version: str = "v1"):
    try:
        return pm.get_prompt(name, version)
    except PromptNotFoundError:
        try:
            return pm.get_prompt(name, fallback_version)
        except PromptNotFoundError:
            raise ValueError(f"No version of {name} found")
```

### 3. Configuration Management

```python
# Store complex configs
complex_config = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
    "stop": ["Human:", "Assistant:"]
}

pm.create_prompt(
    name="complex",
    version="v1",
    system_prompt="Complex system",
    user_prompt="Complex user",
    config=complex_config
)
```

### 4. Resource Management

```python
# For database backends, connections are managed automatically
# But be mindful of connection limits

# Good: reuse manager instance
pm = PromptManager()
for i in range(100):
    prompt = pm.get_prompt("test", "v1")

# Avoid: creating new manager each time
for i in range(100):
    pm = PromptManager()  # Creates new connections
    prompt = pm.get_prompt("test", "v1")
```

## 📚 Next Steps

- Read [Best Practices](best-practices.md)
- Check out [Examples](examples.md)
- Learn about [Configuration](configuration.md)
- Explore [Backends](backends.md)
