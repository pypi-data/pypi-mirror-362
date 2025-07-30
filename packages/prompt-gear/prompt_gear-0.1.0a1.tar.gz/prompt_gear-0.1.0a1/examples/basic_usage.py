"""
Example usage of Prompt Gear.
"""
from promptgear import PromptManager, PromptTemplate


def main():
    """Example usage."""
    print("=== Prompt Gear Example ===")
    
    # Initialize manager
    pm = PromptManager()
    
    # Create a prompt
    print("\n1. Creating a prompt...")
    prompt = pm.create_prompt(
        name="chatbot_greeting",
        version="v1",
        system_prompt="You are a helpful assistant that speaks politely and professionally.",
        user_prompt="Hello! How can I help you today? {{user_input}}",
        config={
            "temperature": 0.7,
            "max_tokens": 512,
            "top_p": 0.9
        }
    )
    print(f"Created: {prompt.name}:{prompt.version}")
    
    # Get the prompt
    print("\n2. Getting the prompt...")
    retrieved = pm.get_prompt("chatbot_greeting", "v1")
    print(f"System prompt: {retrieved.system_prompt}")
    print(f"User prompt: {retrieved.user_prompt}")
    print(f"Config: {retrieved.config}")
    
    # Create another version
    print("\n3. Creating another version...")
    pm.create_prompt(
        name="chatbot_greeting",
        version="v2",
        system_prompt="You are a helpful assistant that speaks casually and friendly.",
        user_prompt="Hey there! What's up? {{user_input}}",
        config={
            "temperature": 0.8,
            "max_tokens": 256
        }
    )
    
    # List all versions
    print("\n4. Listing versions...")
    versions = pm.list_versions("chatbot_greeting")
    print(f"Versions: {versions}")
    
    # List all prompts
    print("\n5. Listing all prompts...")
    prompts = pm.list_prompts()
    for p in prompts:
        print(f"  - {p.name}:{p.version}")
    
    # Use prompt in a template
    print("\n6. Using prompt as template...")
    template = pm.get_prompt("chatbot_greeting", "v1")
    user_input = "I need help with Python programming"
    formatted_prompt = template.user_prompt.replace("{{user_input}}", user_input)
    print(f"Formatted prompt: {formatted_prompt}")
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
