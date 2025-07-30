"""
PostgreSQL backend usage example.
"""
import os
import asyncio
from promptgear import PromptManager, PromptTemplate

# Set up environment for PostgreSQL backend
os.environ['PROMPT_GEAR_BACKEND'] = 'postgres'
os.environ['PROMPT_GEAR_DB_URL'] = 'postgresql://promptgear:promptgear123@localhost:5432/promptgear'
os.environ['PROMPT_GEAR_POSTGRES_POOL_SIZE'] = '5'
os.environ['PROMPT_GEAR_POSTGRES_MAX_CONNECTIONS'] = '20'


def main():
    """Main function to demonstrate PostgreSQL backend usage."""
    try:
        # Initialize the manager with PostgreSQL backend
        manager = PromptManager()
        
        print("🐘 PostgreSQL Backend Example")
        print("=" * 40)
        
        # Create some example prompts
        prompts = [
            PromptTemplate(
                name="chatbot",
                version="v1",
                system_prompt="You are a helpful AI assistant specializing in customer support.",
                user_prompt="User query: {query}\nPlease provide a helpful response.",
                config={
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "model": "gpt-4",
                    "category": "customer_support"
                }
            ),
            PromptTemplate(
                name="code_reviewer",
                version="v1",
                system_prompt="You are an expert code reviewer. Focus on code quality, security, and best practices.",
                user_prompt="Please review this code:\n\n{code}\n\nLanguage: {language}",
                config={
                    "temperature": 0.3,
                    "max_tokens": 800,
                    "model": "gpt-4",
                    "category": "development"
                }
            ),
            PromptTemplate(
                name="translator",
                version="v1",
                system_prompt="You are a professional translator with expertise in multiple languages.",
                user_prompt="Translate the following text from {source_lang} to {target_lang}:\n\n{text}",
                config={
                    "temperature": 0.2,
                    "max_tokens": 1000,
                    "model": "gpt-3.5-turbo",
                    "category": "translation"
                }
            ),
            PromptTemplate(
                name="summarizer",
                version="v1",
                system_prompt="You are an expert at creating concise, informative summaries.",
                user_prompt="Please summarize the following text:\n\n{content}",
                config={
                    "temperature": 0.4,
                    "max_tokens": 300,
                    "model": "gpt-4",
                    "category": "content"
                }
            )
        ]
        
        # Save all prompts
        print("📝 Saving prompts...")
        for prompt in prompts:
            manager.backend.save_prompt(prompt)
            print(f"   ✓ Saved: {prompt.name} v{prompt.version}")
        
        # List all prompts
        print("\n📋 All prompts:")
        all_prompts = manager.list_prompts()
        for prompt in all_prompts:
            print(f"   • {prompt.name} v{prompt.version}")
        
        # Demonstrate search functionality
        print("\n🔍 Search examples:")
        
        # Search by name
        results = manager.backend.search_prompts("code", field="name")
        print(f"   Search 'code' in names: {len(results)} results")
        for r in results:
            print(f"     - {r.name} v{r.version}")
        
        # Search by system prompt content
        results = manager.backend.search_prompts("assistant", field="system_prompt")
        print(f"   Search 'assistant' in system prompts: {len(results)} results")
        for r in results:
            print(f"     - {r.name} v{r.version}")
        
        # Demonstrate config-based queries
        print("\n⚙️ Config-based queries:")
        
        # Find prompts with specific model
        gpt4_prompts = manager.backend.get_prompts_by_config({"model": "gpt-4"})
        print(f"   GPT-4 prompts: {len(gpt4_prompts)} found")
        for p in gpt4_prompts:
            print(f"     - {p.name} v{p.version}")
        
        # Find prompts by category
        dev_prompts = manager.backend.get_prompts_by_config({"category": "development"})
        print(f"   Development prompts: {len(dev_prompts)} found")
        for p in dev_prompts:
            print(f"     - {p.name} v{p.version}")
        
        # Create multiple versions of a prompt
        print("\n🔄 Version management:")
        
        # Create v2 of chatbot with different config
        chatbot_v2 = PromptTemplate(
            name="chatbot",
            version="v2",
            system_prompt="You are an advanced AI assistant with specialized knowledge in technical support.",
            user_prompt="Technical query: {query}\nUser level: {user_level}\nPlease provide a detailed technical response.",
            config={
                "temperature": 0.6,
                "max_tokens": 800,
                "model": "gpt-4",
                "category": "technical_support"
            }
        )
        
        manager.backend.save_prompt(chatbot_v2)
        print(f"   ✓ Created: {chatbot_v2.name} v{chatbot_v2.version}")
        
        # List versions of chatbot
        versions = manager.list_versions("chatbot")
        print(f"   Chatbot versions: {versions}")
        
        # Get database statistics
        print("\n📊 Database statistics:")
        stats = manager.backend.get_stats()
        print(f"   Total prompts: {stats['total_prompts']}")
        print(f"   Unique names: {stats['unique_names']}")
        print(f"   Pool size: {stats['pool_size']}")
        print(f"   Max connections: {stats['max_connections']}")
        print(f"   Database: {stats['database_version']}")
        
        # Show recent prompts
        print("\n📅 Recent prompts:")
        for recent in stats['recent_prompts'][:3]:
            print(f"   • {recent['name']} v{recent['version']} - {recent['created_at']}")
        
        # Show config usage statistics
        print("\n📈 Config usage statistics:")
        for config_stat in stats['config_stats'][:5]:
            print(f"   • {config_stat['key']}: {config_stat['count']} prompts")
        
        # Demonstrate prompt retrieval and usage
        print("\n🚀 Using prompts:")
        
        # Get a specific prompt
        code_review_prompt = manager.get_prompt("code_reviewer", "v1")
        if code_review_prompt:
            print(f"   Retrieved: {code_review_prompt.name} v{code_review_prompt.version}")
            print(f"   System prompt: {code_review_prompt.system_prompt[:50]}...")
            print(f"   User prompt: {code_review_prompt.user_prompt[:50]}...")
        
        # Advanced search across all fields
        print("\n🔍 Advanced search:")
        search_results = manager.backend.search_prompts("helpful", field="all")
        print(f"   Search 'helpful' across all fields: {len(search_results)} results")
        for result in search_results:
            print(f"     - {result.name} v{result.version}")
        
        print("\n✅ PostgreSQL backend example completed successfully!")
        
    except ImportError as e:
        print(f"❌ PostgreSQL backend not available: {e}")
        print("   Install PostgreSQL support with: pip install psycopg2-binary")
        print("   Or use the filesystem/sqlite backend instead")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure PostgreSQL is running and accessible")
        print("   Check your database connection settings")


if __name__ == "__main__":
    main()
