"""
Advanced usage examples for Prompt Gear.
"""
from promptgear import PromptManager, PromptTemplate
from promptgear.core import PromptNotFoundError, PromptAlreadyExistsError
import json


def example_langchain_integration():
    """Example of using Prompt Gear with LangChain-style applications."""
    print("=== LangChain Integration Example ===")
    
    pm = PromptManager()
    
    # Create prompts for different use cases
    prompts_config = [
        {
            "name": "code_reviewer",
            "version": "v1",
            "system_prompt": "You are an expert code reviewer. Analyze the code and provide constructive feedback.",
            "user_prompt": "Please review this code:\n\n```{{language}}\n{{code}}\n```\n\nFocus on: {{focus_areas}}",
            "config": {"temperature": 0.3, "max_tokens": 1000}
        },
        {
            "name": "summarizer",
            "version": "v1", 
            "system_prompt": "You are a professional text summarizer. Create concise, accurate summaries.",
            "user_prompt": "Summarize the following text in {{max_sentences}} sentences:\n\n{{text}}",
            "config": {"temperature": 0.5, "max_tokens": 500}
        },
        {
            "name": "translator",
            "version": "v1",
            "system_prompt": "You are a professional translator. Translate text accurately while maintaining tone and context.",
            "user_prompt": "Translate the following text from {{source_language}} to {{target_language}}:\n\n{{text}}",
            "config": {"temperature": 0.2, "max_tokens": 800}
        }
    ]
    
    # Create all prompts
    for prompt_config in prompts_config:
        try:
            prompt = pm.create_prompt(**prompt_config)
            print(f"✓ Created prompt: {prompt.name}:{prompt.version}")
        except PromptAlreadyExistsError:
            print(f"⚠ Prompt {prompt_config['name']}:{prompt_config['version']} already exists")
    
    # Use the prompts
    print("\n--- Using Code Reviewer ---")
    code_reviewer = pm.get_prompt("code_reviewer", "v1")
    formatted_prompt = code_reviewer.user_prompt.replace("{{language}}", "python").replace("{{code}}", "def add(a, b):\n    return a + b").replace("{{focus_areas}}", "performance, readability, best practices")
    print(f"System: {code_reviewer.system_prompt}")
    print(f"User: {formatted_prompt}")
    print(f"Config: {code_reviewer.config}")
    
    print("\n--- Using Summarizer ---")
    summarizer = pm.get_prompt("summarizer", "v1")
    formatted_prompt = summarizer.user_prompt.replace("{{max_sentences}}", "3").replace("{{text}}", "This is a very long text that needs to be summarized into key points...")
    print(f"System: {summarizer.system_prompt}")
    print(f"User: {formatted_prompt}")


def example_version_management():
    """Example of managing different versions of prompts."""
    print("\n=== Version Management Example ===")
    
    pm = PromptManager()
    
    # Create multiple versions of a prompt
    versions = [
        {
            "version": "v1",
            "system_prompt": "You are a helpful assistant.",
            "user_prompt": "{{question}}",
            "config": {"temperature": 0.7}
        },
        {
            "version": "v2",
            "system_prompt": "You are a helpful and friendly assistant.",
            "user_prompt": "{{question}}\n\nPlease provide a detailed answer.",
            "config": {"temperature": 0.8, "max_tokens": 1000}
        },
        {
            "version": "v3",
            "system_prompt": "You are a helpful, friendly, and knowledgeable assistant.",
            "user_prompt": "Question: {{question}}\n\nPlease provide a comprehensive answer with examples.",
            "config": {"temperature": 0.9, "max_tokens": 1500, "top_p": 0.9}
        }
    ]
    
    for version_config in versions:
        try:
            pm.create_prompt(
                name="qa_assistant",
                **version_config
            )
            print(f"✓ Created qa_assistant:{version_config['version']}")
        except PromptAlreadyExistsError:
            print(f"⚠ qa_assistant:{version_config['version']} already exists")
    
    # List all versions
    print(f"\nVersions of qa_assistant: {pm.list_versions('qa_assistant')}")
    
    # Compare versions
    print("\n--- Version Comparison ---")
    for version in pm.list_versions('qa_assistant'):
        prompt = pm.get_prompt('qa_assistant', version)
        print(f"\n{version}:")
        print(f"  System: {prompt.system_prompt}")
        print(f"  Config: {prompt.config}")


def example_prompt_templates():
    """Example of using prompts as templates."""
    print("\n=== Prompt Template Usage Example ===")
    
    pm = PromptManager()
    
    # Create a flexible prompt template
    try:
        pm.create_prompt(
            name="email_writer",
            version="v1",
            system_prompt="You are a professional email writer. Write clear, concise, and appropriate emails.",
            user_prompt="""Write a {{tone}} email about {{subject}}.

Recipient: {{recipient}}
Purpose: {{purpose}}
Key points to include:
{{key_points}}

Additional context: {{context}}""",
            config={"temperature": 0.6, "max_tokens": 800}
        )
        print("✓ Created email_writer template")
    except PromptAlreadyExistsError:
        print("⚠ email_writer already exists")
    
    # Use the template with different parameters
    email_template = pm.get_prompt("email_writer", "v1")
    
    scenarios = [
        {
            "tone": "formal",
            "subject": "project update",
            "recipient": "team manager",
            "purpose": "provide weekly progress update",
            "key_points": "- Completed user authentication\n- Working on database integration\n- On track for deadline",
            "context": "This is for our weekly standup meeting"
        },
        {
            "tone": "friendly",
            "subject": "meeting rescheduling",
            "recipient": "colleague",
            "purpose": "reschedule our meeting",
            "key_points": "- Current time doesn't work\n- Suggest alternative times\n- Apologize for inconvenience",
            "context": "We had a meeting planned for tomorrow"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['subject']} ---")
        formatted_prompt = email_template.user_prompt
        for key, value in scenario.items():
            formatted_prompt = formatted_prompt.replace("{{" + key + "}}", str(value))
        print(f"System: {email_template.system_prompt}")
        print(f"User: {formatted_prompt}")


def example_configuration_management():
    """Example of managing different configurations."""
    print("\n=== Configuration Management Example ===")
    
    pm = PromptManager()
    
    # Create prompts with different configurations for different environments
    environments = {
        "development": {"temperature": 0.9, "max_tokens": 2000, "top_p": 0.95},
        "staging": {"temperature": 0.7, "max_tokens": 1500, "top_p": 0.9},
        "production": {"temperature": 0.5, "max_tokens": 1000, "top_p": 0.8}
    }
    
    for env, config in environments.items():
        try:
            pm.create_prompt(
                name="chatbot",
                version=f"{env}_v1",
                system_prompt="You are a helpful customer service chatbot.",
                user_prompt="Customer query: {{query}}\n\nPlease provide helpful assistance.",
                config=config
            )
            print(f"✓ Created chatbot:{env}_v1 with config: {config}")
        except PromptAlreadyExistsError:
            print(f"⚠ chatbot:{env}_v1 already exists")
    
    # Show how to use different configurations
    print("\n--- Environment-specific Usage ---")
    for env in environments:
        try:
            prompt = pm.get_prompt("chatbot", f"{env}_v1")
            print(f"\n{env.upper()} environment:")
            print(f"  Temperature: {prompt.config.get('temperature')}")
            print(f"  Max tokens: {prompt.config.get('max_tokens')}")
            print(f"  Top-p: {prompt.config.get('top_p')}")
        except PromptNotFoundError:
            print(f"  {env} configuration not found")


def main():
    """Run all examples."""
    example_langchain_integration()
    example_version_management()
    example_prompt_templates()
    example_configuration_management()
    
    print("\n=== All Examples Completed ===")


if __name__ == "__main__":
    main()
