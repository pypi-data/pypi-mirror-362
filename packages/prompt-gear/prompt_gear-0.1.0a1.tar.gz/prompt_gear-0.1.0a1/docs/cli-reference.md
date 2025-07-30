# CLI Reference

Complete reference for the Prompt Gear command-line interface.

## 🚀 Quick Reference

```bash
promptgear init [--backend BACKEND]           # Initialize Prompt Gear
promptgear create NAME [OPTIONS]              # Create a new prompt
promptgear get NAME VERSION                   # Get a specific prompt
promptgear list [NAME]                        # List prompts
promptgear delete NAME VERSION                # Delete a prompt
promptgear versions NAME                      # List versions of a prompt
promptgear status                             # Show backend status
```

## 📋 Command Details

### `promptgear init`

Initialize Prompt Gear in your project with a specific backend.

```bash
promptgear init [OPTIONS]
```

**Options:**
- `--backend BACKEND`: Storage backend (`filesystem`, `sqlite`, `postgres`)
- `--help`: Show help message

**Examples:**
```bash
# Initialize with filesystem backend (default)
promptgear init

# Initialize with SQLite backend
promptgear init --backend sqlite

# Initialize with PostgreSQL backend
promptgear init --backend postgres
```

**What it does:**
- Creates configuration files
- Sets up database schema (for database backends)
- Creates initial directory structure
- Generates sample `.env` file

---

### `promptgear create`

Create a new prompt template with automatic version management.

```bash
promptgear create NAME [OPTIONS]
```

**Arguments:**
- `NAME`: Prompt name (required)

**Options:**
- `--version, -v VERSION`: Prompt version (default: `v1`)
- `--system, -s TEXT`: System prompt
- `--user, -u TEXT`: User prompt
- `--config, -c JSON`: Configuration as JSON string
- `--interactive, -i`: Interactive mode
- `--overwrite`: Overwrite existing prompt
- `--help`: Show help message

**Examples:**

**Basic creation:**
```bash
promptgear create chatbot_greeting --version v1 \
  --system "You are a helpful assistant" \
  --user "Hello! How can I help you?"
```

**With configuration:**
```bash
promptgear create code_reviewer --version v1 \
  --system "You are a code review expert" \
  --user "Review this code: {{code}}" \
  --config '{"temperature": 0.3, "max_tokens": 1000}'
```

**Interactive mode:**
```bash
promptgear create my_prompt --interactive
```

**Overwrite existing:**
```bash
promptgear create existing_prompt --version v1 \
  --system "Updated system prompt" \
  --overwrite
```

**Create new version:**
```bash
# Create initial version
promptgear create chatbot --version v1 --system "Hello v1"

# Create new version - automatically becomes latest
promptgear create chatbot --version v2 --system "Hello v2"
```

---

## � Version Management

Prompt Gear uses sequence-based version management for reliable and consistent version tracking.

### How it works:

1. **Sequence Numbers**: Each prompt version gets an auto-incrementing sequence number (1, 2, 3...)
2. **Latest Tracking**: Exactly one version per prompt is marked as "latest"
3. **Automatic Updates**: Creating a new version automatically updates the latest flag
4. **Deletion Handling**: Deleting the latest version promotes the highest sequence number

### Examples:

```bash
# Create initial version (sequence_number=1, is_latest=True)
promptgear create chatbot --version v1 --system "Hello v1"

# Create new version (sequence_number=2, is_latest=True)
# v1 automatically becomes is_latest=False
promptgear create chatbot --version v2 --system "Hello v2"

# Get latest version (no version specified)
promptgear get chatbot              # Returns v2

# Get specific version
promptgear get chatbot --version v1  # Returns v1

# Delete latest version
promptgear delete chatbot --version v2
# v1 is automatically promoted to latest

# Create new version after deletion
promptgear create chatbot --version v3 --system "Hello v3"
# Gets sequence_number=3 (continues from where we left off)
```

### Version Information:

All versions include metadata:
- `sequence_number`: Auto-incrementing number for ordering
- `is_latest`: Boolean flag indicating the latest version
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp

---

### `promptgear get`

Retrieve a specific prompt template.

```bash
promptgear get NAME [VERSION] [OPTIONS]
```

**Arguments:**
- `NAME`: Prompt name (required)
- `VERSION`: Prompt version (optional, defaults to latest version)

**Options:**
- `--version, -v VERSION`: Specify prompt version explicitly
- `--format FORMAT`: Output format (`yaml`, `json`, `table`)
- `--help`: Show help message

**Examples:**

**Get latest version:**
```bash
promptgear get chatbot_greeting
```

**Get specific version:**
```bash
promptgear get chatbot_greeting --version v1
# or
promptgear get chatbot_greeting v1
```

**JSON output:**
```bash
promptgear get chatbot_greeting --format json
```

**YAML output:**
```bash
promptgear get chatbot_greeting --format yaml
```

---

### `promptgear list`

List all prompts or versions of a specific prompt.

```bash
promptgear list [NAME] [OPTIONS]
```

**Arguments:**
- `NAME`: Prompt name (optional, filters by name)

**Options:**
- `--format FORMAT`: Output format (`table`, `json`, `yaml`)
- `--help`: Show help message

**Examples:**

**List all prompts:**
```bash
promptgear list
```

**List specific prompt versions:**
```bash
promptgear list chatbot_greeting
```

**JSON output:**
```bash
promptgear list --format json
```

---

### `promptgear delete`

Delete a specific prompt template version.

```bash
promptgear delete NAME VERSION [OPTIONS]
```

**Arguments:**
- `NAME`: Prompt name (required)
- `VERSION`: Prompt version (required)

**Options:**
- `--confirm`: Skip confirmation prompt
- `--help`: Show help message

**Examples:**

**Delete with confirmation:**
```bash
promptgear delete old_prompt v1
```

**Delete without confirmation:**
```bash
promptgear delete old_prompt v1 --confirm
```

**Version management behavior:**
- When deleting the latest version, the version with the highest sequence number is automatically promoted to latest
- Deleting a non-latest version doesn't affect the latest flag
- If only one version exists, deleting it removes the entire prompt

**Examples:**

```bash
# If you have versions: v1 (seq=1), v2 (seq=2, latest), v3 (seq=3)
promptgear delete chatbot v3
# Result: v2 becomes latest (highest remaining sequence number)

# Delete the current latest version
promptgear delete chatbot v2
# Result: v1 becomes latest

# Delete the last remaining version
promptgear delete chatbot v1
# Result: Entire prompt is removed
```

---

### `promptgear versions`

List all versions of a specific prompt with version metadata.

```bash
promptgear versions NAME [OPTIONS]
```

**Arguments:**
- `NAME`: Prompt name (required)

**Options:**
- `--format FORMAT`: Output format (`table`, `json`, `yaml`)
- `--help`: Show help message

**Examples:**

**List versions:**
```bash
promptgear versions chatbot_greeting
```

**JSON output:**
```bash
promptgear versions chatbot_greeting --format json
```

**Sample output:**
```
┌─────────┬─────────────────┬───────────┬─────────────────────┬─────────────────────┐
│ Version │ Sequence Number │ Is Latest │ Created At          │ Updated At          │
├─────────┼─────────────────┼───────────┼─────────────────────┼─────────────────────┤
│ v1      │ 1               │ False     │ 2024-01-15 10:00:00 │ 2024-01-15 10:00:00 │
│ v2      │ 2               │ False     │ 2024-01-15 11:00:00 │ 2024-01-15 11:00:00 │
│ v3      │ 3               │ True      │ 2024-01-15 12:00:00 │ 2024-01-15 12:00:00 │
└─────────┴─────────────────┴───────────┴─────────────────────┴─────────────────────┘
```

**Understanding the output:**
- **Version**: The user-defined version name
- **Sequence Number**: Auto-incrementing number for ordering (1, 2, 3...)
- **Is Latest**: Boolean indicating which version is currently marked as latest
- **Created At**: Timestamp when the version was created
- **Updated At**: Timestamp when the version was last modified

---

### `promptgear status`

Show backend status and statistics.

```bash
promptgear status [OPTIONS]
```

**Options:**
- `--verbose, -v`: Show detailed information
- `--help`: Show help message

**Examples:**

**Basic status:**
```bash
promptgear status
```

**Verbose status:**
```bash
promptgear status --verbose
```

**Sample output:**
```
Backend: PostgreSQL
Database: postgresql://user@localhost:5432/prompts
Status: Connected ✓
Statistics:
  Total prompts: 25
  Total versions: 45
  Most recent: chatbot_greeting:v3 (2024-01-15)
```

## 🔧 Configuration

### Environment Variables

CLI commands respect these environment variables:

```env
PROMPT_GEAR_BACKEND=filesystem|sqlite|postgres
PROMPT_GEAR_PROMPT_DIR=./prompts
PROMPT_GEAR_DB_URL=database_connection_string
PROMPT_GEAR_POOL_SIZE=5
PROMPT_GEAR_MAX_CONNECTIONS=20
PROMPT_GEAR_DEBUG=0|1
```

### Configuration File

You can also use a configuration file:

```yaml
# .promptgear.yml
backend: postgres
database_url: postgresql://user:pass@localhost/prompts
pool_size: 10
max_connections: 50
```

## 💡 Tips and Best Practices

### 1. Version Management

```bash
# Create progressive versions
promptgear create my_prompt --version v1 --system "Basic prompt"
promptgear create my_prompt --version v2 --system "Improved prompt"
promptgear create my_prompt --version v3 --system "Production prompt"

# List to see evolution
promptgear versions my_prompt
```

### 2. Configuration Management

```bash
# Use JSON for complex configurations
promptgear create llm_prompt --version v1 \
  --system "You are helpful" \
  --user "Answer: {{question}}" \
  --config '{
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.9,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1
  }'
```

### 3. Interactive Mode

Use interactive mode for complex prompts:

```bash
promptgear create complex_prompt --interactive
```

This will prompt you for each field interactively.

### 4. Batch Operations

```bash
# Create multiple versions
for version in v1 v2 v3; do
  promptgear create test_prompt --version $version \
    --system "System for $version" \
    --user "User for $version"
done

# List all
promptgear list
```

### 5. Backup and Migration

```bash
# Export all prompts to JSON
promptgear list --format json > prompts_backup.json

# Check status before operations
promptgear status --verbose
```

## 🚨 Error Handling

### Common Errors

1. **Prompt already exists**
   ```bash
   # Error: Prompt already exists
   promptgear create existing_prompt --version v1 --system "New"
   
   # Solution: Use --overwrite
   promptgear create existing_prompt --version v1 --system "New" --overwrite
   ```

2. **Prompt not found**
   ```bash
   # Error: Prompt not found
   promptgear get nonexistent_prompt v1
   
   # Solution: Check available prompts
   promptgear list
   ```

3. **Database connection error**
   ```bash
   # Error: Could not connect to database
   promptgear status
   
   # Solution: Check your .env file and database server
   ```

4. **Invalid JSON configuration**
   ```bash
   # Error: Invalid JSON
   promptgear create test --config '{"invalid": json}'
   
   # Solution: Validate JSON
   promptgear create test --config '{"valid": "json"}'
   ```

### Debug Mode

Enable debug logging:

```bash
export PROMPT_GEAR_DEBUG=1
promptgear create test_prompt --version v1 --system "Debug mode"
```

## 🔗 Integration Examples

### With Shell Scripts

```bash
#!/bin/bash
# deploy_prompts.sh

# Create production prompts
promptgear create chatbot --version prod \
  --system "$(cat prompts/chatbot_system.txt)" \
  --user "$(cat prompts/chatbot_user.txt)" \
  --config "$(cat prompts/chatbot_config.json)"

# Verify deployment
promptgear get chatbot prod
```

### With CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Deploy prompts
  run: |
    promptgear init --backend postgres
    promptgear create prod_prompt --version v1 \
      --system "${{ secrets.SYSTEM_PROMPT }}" \
      --user "${{ secrets.USER_PROMPT }}"
```

### With Docker

```dockerfile
FROM python:3.11-slim

RUN pip install prompt-gear
COPY .env /app/.env
WORKDIR /app

CMD ["promptgear", "status"]
```

## 📚 Next Steps

- Learn the [Python SDK](python-sdk.md)
- Read [Best Practices](best-practices.md)
- Check out [Examples](examples.md)
- Explore [Configuration](configuration.md)
