# Prompt Gear Documentation

Welcome to the Prompt Gear documentation! This guide will help you understand and use Prompt Gear effectively.

## 📚 Documentation Structure

- **[Installation & Setup](installation.md)** - Getting started with Prompt Gear
- **[CLI Reference](cli-reference.md)** - Complete command-line interface documentation
- **[Python SDK](python-sdk.md)** - Using Prompt Gear in your Python applications
- **[Configuration](configuration.md)** - Backend configuration and environment setup
- **[Best Practices](best-practices.md)** - Recommended usage patterns and tips
- **[Backends](backends.md)** - Detailed information about storage backends
- **[Examples](examples.md)** - Real-world usage examples and tutorials
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

## 🚀 Quick Start

1. **Install Prompt Gear**
   ```bash
   pip install prompt-gear
   ```

2. **Initialize in your project**
   ```bash
   promptgear init --backend filesystem
   ```

3. **Create your first prompt**
   ```bash
   promptgear create my_prompt --version v1 \
     --system "You are helpful" \
     --user "Hello {{name}}"
   ```

4. **Use in Python**
   ```python
   from promptgear import PromptManager
   
   pm = PromptManager()
   prompt = pm.get_prompt("my_prompt", "v1")
   ```

## 🎯 Key Features

- **Multi-backend storage**: Filesystem (YAML), SQLite, PostgreSQL
- **YAML-based format**: Human-readable and version-controllable
- **Dual interface**: CLI tool + Python SDK
- **Flexible configuration**: Environment-based configuration
- **Production-ready**: Connection pooling, error handling, and optimization
- **Advanced version management**: Sequence-based versioning with automatic latest tracking
- **Metadata support**: Creation timestamps, sequence numbers, and version flags
- **Consistent behavior**: Unified version management across all backends

## 📖 Learn More

- [Installation & Setup](installation.md) - Start here if you're new to Prompt Gear
- [CLI Reference](cli-reference.md) - Complete command reference
- [Python SDK](python-sdk.md) - Integration guide for developers
- [Best Practices](best-practices.md) - Tips for effective prompt management

## 🆘 Need Help?

- Check the [Troubleshooting](troubleshooting.md) guide
- Look at [Examples](examples.md) for real-world usage
- Review [Configuration](configuration.md) for setup issues

## 📝 License

MIT License - see the project root for details.
