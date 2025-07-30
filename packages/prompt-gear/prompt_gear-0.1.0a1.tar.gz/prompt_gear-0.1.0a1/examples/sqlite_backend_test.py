"""
Test SQLite backend with Python SDK.
"""
from promptgear import PromptManager


def test_sqlite_backend():
    """Test SQLite backend functionality."""
    print("=== Testing SQLite Backend ===")
    
    # Create manager (will use SQLite backend from .env)
    pm = PromptManager()
    
    print(f"Backend type: {pm.config.backend}")
    print(f"Database URL: {pm.config.db_url}")
    
    # Create a prompt
    print("\n1. Creating prompt...")
    prompt = pm.create_prompt(
        name="python_sdk_test",
        version="v1",
        system_prompt="You are a Python SDK test assistant",
        user_prompt="SDK test: {{input}}",
        config={
            "temperature": 0.6,
            "max_tokens": 800,
            "model": "gpt-4"
        }
    )
    print(f"Created: {prompt.name}:{prompt.version}")
    
    # Get the prompt
    print("\n2. Getting prompt...")
    retrieved = pm.get_prompt("python_sdk_test", "v1")
    print(f"Retrieved: {retrieved.name}:{retrieved.version}")
    print(f"Config: {retrieved.config}")
    
    # Update the prompt
    print("\n3. Updating prompt...")
    updated = pm.update_prompt(
        "python_sdk_test", "v1",
        system_prompt="Updated Python SDK test assistant",
        config={
            "temperature": 0.8,
            "max_tokens": 1000,
            "model": "gpt-4-turbo"
        }
    )
    print(f"Updated config: {updated.config}")
    
    # Create another version
    print("\n4. Creating another version...")
    pm.create_prompt(
        name="python_sdk_test",
        version="v2",
        system_prompt="Version 2 of Python SDK test",
        user_prompt="V2 test: {{input}}",
        config={"temperature": 0.9}
    )
    
    # List versions
    print("\n5. Listing versions...")
    versions = pm.list_versions("python_sdk_test")
    print(f"Versions: {versions}")
    
    # List all prompts
    print("\n6. Listing all prompts...")
    prompts = pm.list_prompts()
    print(f"Total prompts: {len(prompts)}")
    for p in prompts:
        print(f"  - {p.name}:{p.version}")
    
    # Test database stats
    print("\n7. Database stats...")
    if hasattr(pm.backend, 'get_stats'):
        stats = pm.backend.get_stats()
        print(f"Stats: {stats}")
    
    print("\n=== SQLite Backend Test Completed ===")


if __name__ == "__main__":
    test_sqlite_backend()
