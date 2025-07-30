# Examples

Real-world examples and tutorials for using Prompt Gear effectively.

## 🚀 Basic Examples

### 1. Simple Chatbot

```python
from promptgear import PromptManager

# Initialize
pm = PromptManager()

# Create chatbot prompt
pm.create_prompt(
    name="chatbot",
    version="v1",
    system_prompt="You are a friendly and helpful assistant.",
    user_prompt="User: {{message}}\nAssistant:",
    config={
        "temperature": 0.7,
        "max_tokens": 500
    }
)

# Use the prompt
prompt = pm.get_prompt("chatbot", "v1")
user_message = "Hello, how are you?"
full_prompt = prompt.user_prompt.replace("{{message}}", user_message)

print(f"System: {prompt.system_prompt}")
print(f"User: {full_prompt}")
print(f"Config: {prompt.config}")
```

### 2. Code Reviewer

```python
# Create code review prompt
pm.create_prompt(
    name="code_reviewer",
    version="v1",
    system_prompt="""You are an expert code reviewer. 
    Provide constructive feedback on code quality, security, and best practices.""",
    user_prompt="""Please review this code:

Language: {{language}}
Code:
```{{language}}
{{code}}
```

Focus on:
- Code quality and readability
- Potential bugs or security issues
- Performance improvements
- Best practices adherence""",
    config={
        "temperature": 0.3,
        "max_tokens": 1000
    }
)

# Use for code review
prompt = pm.get_prompt("code_reviewer", "v1")
review_prompt = prompt.user_prompt.replace("{{language}}", "python").replace("{{code}}", """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
""")

print(review_prompt)
```

### 3. Multi-Version Prompt Management

```python
# Create progressive versions with automatic latest management
versions = [
    {
        "version": "v1",
        "system": "You are a helpful assistant.",
        "user": "{{question}}"
    },
    {
        "version": "v2", 
        "system": "You are a helpful assistant. Be concise and accurate.",
        "user": "Question: {{question}}\nPlease provide a clear answer."
    },
    {
        "version": "v3",
        "system": "You are a helpful assistant. Be concise, accurate, and provide examples when helpful.",
        "user": """Question: {{question}}
        
Please provide:
1. A clear answer
2. An example if applicable
3. Any important considerations"""
    }
]

for version_info in versions:
    prompt = pm.create_prompt(
        name="qa_assistant",
        version=version_info["version"],
        system_prompt=version_info["system"],
        user_prompt=version_info["user"],
        config={"temperature": 0.7}
    )
    print(f"Created {prompt.version} (sequence: {prompt.sequence_number}, latest: {prompt.is_latest})")

# List all versions with metadata
versions = pm.list_versions("qa_assistant")
print(f"Available versions: {versions}")

# Get latest version (v3 is automatically latest)
latest_prompt = pm.get_prompt("qa_assistant")
print(f"Latest version: {latest_prompt.version} (sequence: {latest_prompt.sequence_number})")

# Version management example
print("\n--- Version Management Demo ---")

# Delete latest version (v3) - v2 becomes latest
pm.delete_prompt("qa_assistant", "v3")
latest_after_delete = pm.get_prompt("qa_assistant")
print(f"After deleting v3, latest is now: {latest_after_delete.version}")

# Create new version after deletion
new_version = pm.create_prompt(
    name="qa_assistant",
    version="v4",
    system_prompt="You are an expert assistant with enhanced capabilities.",
    user_prompt="{{question}}",
    config={"temperature": 0.8}
)
print(f"New version: {new_version.version} (sequence: {new_version.sequence_number})")
```

## 🌐 Web Application Examples

### 1. FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from promptgear import PromptManager, PromptNotFoundError

app = FastAPI(title="Prompt Service")
pm = PromptManager()

class PromptRequest(BaseModel):
    name: str
    version: str
    variables: dict = {}

class PromptResponse(BaseModel):
    system_prompt: str
    user_prompt: str
    config: dict

@app.get("/prompt/{name}/{version}", response_model=PromptResponse)
async def get_prompt(name: str, version: str):
    try:
        prompt = pm.get_prompt(name, version)
        return PromptResponse(
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            config=prompt.config
        )
    except PromptNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt not found")

@app.get("/prompt/{name}", response_model=PromptResponse)
async def get_latest_prompt(name: str):
    """Get the latest version of a prompt."""
    try:
        prompt = pm.get_prompt(name)  # Gets latest version
        return PromptResponse(
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            config=prompt.config
        )
    except PromptNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt not found")

@app.post("/prompt/{name}/{version}/render")
async def render_prompt(name: str, version: str, request: PromptRequest):
    try:
        prompt = pm.get_prompt(name, version)
        
        # Replace variables in user prompt
        rendered_user_prompt = prompt.user_prompt
        for key, value in request.variables.items():
            rendered_user_prompt = rendered_user_prompt.replace(f"{{{{{key}}}}}", str(value))
        
        return {
            "system_prompt": prompt.system_prompt,
            "user_prompt": rendered_user_prompt,
            "config": prompt.config
        }
    except PromptNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt not found")

@app.get("/prompts")
async def list_prompts():
    prompts = pm.list_prompts()
    return [{"name": p.name, "version": p.version} for p in prompts]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Flask Integration

```python
from flask import Flask, jsonify, request
from promptgear import PromptManager, PromptNotFoundError

app = Flask(__name__)
pm = PromptManager()

@app.route('/prompt/<name>/<version>', methods=['GET'])
def get_prompt(name, version):
    try:
        prompt = pm.get_prompt(name, version)
        return jsonify({
            "name": prompt.name,
            "version": prompt.version,
            "system_prompt": prompt.system_prompt,
            "user_prompt": prompt.user_prompt,
            "config": prompt.config
        })
    except PromptNotFoundError:
        return jsonify({"error": "Prompt not found"}), 404

@app.route('/prompt/<name>/<version>', methods=['POST'])
def create_prompt(name, version):
    data = request.get_json()
    try:
        prompt = pm.create_prompt(
            name=name,
            version=version,
            system_prompt=data['system_prompt'],
            user_prompt=data['user_prompt'],
            config=data.get('config', {})
        )
        return jsonify({"message": "Prompt created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/prompts', methods=['GET'])
def list_prompts():
    prompts = pm.list_prompts()
    return jsonify([{
        "name": p.name,
        "version": p.version,
        "created_at": p.created_at.isoformat() if hasattr(p, 'created_at') else None
    } for p in prompts])

if __name__ == '__main__':
    app.run(debug=True)
```

## 🤖 AI Framework Integration

### 1. OpenAI Integration

```python
import openai
from promptgear import PromptManager

class OpenAIPromptService:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.pm = PromptManager()
    
    def chat_completion(self, prompt_name, version, variables=None, **kwargs):
        # Get prompt from Prompt Gear
        prompt = self.pm.get_prompt(prompt_name, version)
        
        # Replace variables
        user_prompt = prompt.user_prompt
        if variables:
            for key, value in variables.items():
                user_prompt = user_prompt.replace(f"{{{{{key}}}}}", str(value))
        
        # Merge config with kwargs
        config = {**prompt.config, **kwargs}
        
        # Make API call
        response = self.client.chat.completions.create(
            model=config.get("model", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 500)
        )
        
        return response.choices[0].message.content

# Usage
service = OpenAIPromptService("your-api-key")

# Create customer support prompt
pm = PromptManager()
pm.create_prompt(
    name="customer_support",
    version="v1",
    system_prompt="You are a helpful customer support representative.",
    user_prompt="Customer issue: {{issue}}\nHow can I help resolve this?",
    config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 300
    }
)

# Use the service
response = service.chat_completion(
    "customer_support", 
    "v1", 
    variables={"issue": "My order hasn't arrived yet"}
)
print(response)
```

### 2. LangChain Integration

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from promptgear import PromptManager

class LangChainPromptService:
    def __init__(self, llm):
        self.llm = llm
        self.pm = PromptManager()
    
    def create_chain(self, prompt_name, version):
        # Get prompt from Prompt Gear
        prompt = self.pm.get_prompt(prompt_name, version)
        
        # Extract variables from prompt
        import re
        variables = re.findall(r'\{\{(\w+)\}\}', prompt.user_prompt)
        
        # Create LangChain prompt template
        template = f"{prompt.system_prompt}\n\n{prompt.user_prompt}"
        lc_prompt = PromptTemplate(
            template=template,
            input_variables=variables
        )
        
        # Create chain
        chain = LLMChain(llm=self.llm, prompt=lc_prompt)
        return chain

# Usage
llm = OpenAI(temperature=0.7)
service = LangChainPromptService(llm)

# Create summarization prompt
pm = PromptManager()
pm.create_prompt(
    name="summarizer",
    version="v1",
    system_prompt="You are an expert at summarizing text concisely.",
    user_prompt="Please summarize the following text:\n\n{{text}}\n\nSummary:",
    config={"temperature": 0.3}
)

# Create and use chain
chain = service.create_chain("summarizer", "v1")
result = chain.run(text="Your long text here...")
print(result)
```

## 📊 Advanced Use Cases

### 1. A/B Testing Framework

```python
import random
from dataclasses import dataclass
from typing import Dict, List
from promptgear import PromptManager

@dataclass
class ABTestResult:
    variant: str
    prompt_name: str
    version: str
    response: str
    user_feedback: float = None

class ABTestingService:
    def __init__(self):
        self.pm = PromptManager()
        self.results: List[ABTestResult] = []
    
    def create_ab_test(self, base_name: str, variants: Dict[str, dict]):
        """Create A/B test variants"""
        for variant_name, prompt_config in variants.items():
            version = f"ab_{variant_name}"
            self.pm.create_prompt(
                name=base_name,
                version=version,
                system_prompt=prompt_config["system_prompt"],
                user_prompt=prompt_config["user_prompt"],
                config=prompt_config.get("config", {}),
                overwrite=True
            )
    
    def get_test_prompt(self, base_name: str, variants: List[str], user_id: str = None):
        """Get a prompt variant for testing"""
        # Simple random selection (could be more sophisticated)
        variant = random.choice(variants)
        version = f"ab_{variant}"
        
        prompt = self.pm.get_prompt(base_name, version)
        return prompt, variant
    
    def record_result(self, result: ABTestResult):
        """Record test result"""
        self.results.append(result)
    
    def analyze_results(self, base_name: str) -> Dict:
        """Analyze A/B test results"""
        variant_results = {}
        for result in self.results:
            if result.prompt_name == base_name:
                if result.variant not in variant_results:
                    variant_results[result.variant] = []
                variant_results[result.variant].append(result)
        
        analysis = {}
        for variant, results in variant_results.items():
            feedback_scores = [r.user_feedback for r in results if r.user_feedback is not None]
            analysis[variant] = {
                "total_uses": len(results),
                "avg_feedback": sum(feedback_scores) / len(feedback_scores) if feedback_scores else None,
                "feedback_count": len(feedback_scores)
            }
        
        return analysis

# Usage
ab_service = ABTestingService()

# Create A/B test variants
ab_service.create_ab_test("email_subject", {
    "formal": {
        "system_prompt": "You write professional email subjects.",
        "user_prompt": "Create a professional subject line for: {{content}}",
        "config": {"temperature": 0.3}
    },
    "casual": {
        "system_prompt": "You write friendly, casual email subjects.",
        "user_prompt": "Create a friendly subject line for: {{content}}",
        "config": {"temperature": 0.7}
    }
})

# Get test prompt
prompt, variant = ab_service.get_test_prompt("email_subject", ["formal", "casual"])
print(f"Using variant: {variant}")
print(f"Prompt: {prompt.user_prompt}")
```

### 2. Prompt Performance Monitoring

```python
import time
from functools import wraps
from dataclasses import dataclass
from typing import Dict, List
from promptgear import PromptManager

@dataclass
class PromptMetrics:
    prompt_name: str
    version: str
    execution_time: float
    success: bool
    error_message: str = None
    timestamp: float = None

class PromptMonitor:
    def __init__(self):
        self.pm = PromptManager()
        self.metrics: List[PromptMetrics] = []
    
    def monitor_prompt(self, prompt_name: str, version: str):
        """Decorator to monitor prompt performance"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    self.metrics.append(PromptMetrics(
                        prompt_name=prompt_name,
                        version=version,
                        execution_time=execution_time,
                        success=True,
                        timestamp=time.time()
                    ))
                    
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    
                    self.metrics.append(PromptMetrics(
                        prompt_name=prompt_name,
                        version=version,
                        execution_time=execution_time,
                        success=False,
                        error_message=str(e),
                        timestamp=time.time()
                    ))
                    
                    raise
            return wrapper
        return decorator
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        report = {}
        
        for metric in self.metrics:
            key = f"{metric.prompt_name}:{metric.version}"
            if key not in report:
                report[key] = {
                    "total_calls": 0,
                    "successful_calls": 0,
                    "failed_calls": 0,
                    "avg_execution_time": 0,
                    "min_execution_time": float('inf'),
                    "max_execution_time": 0
                }
            
            report[key]["total_calls"] += 1
            if metric.success:
                report[key]["successful_calls"] += 1
            else:
                report[key]["failed_calls"] += 1
            
            report[key]["min_execution_time"] = min(
                report[key]["min_execution_time"], 
                metric.execution_time
            )
            report[key]["max_execution_time"] = max(
                report[key]["max_execution_time"], 
                metric.execution_time
            )
        
        # Calculate averages
        for key in report:
            successful_metrics = [m for m in self.metrics 
                                if f"{m.prompt_name}:{m.version}" == key and m.success]
            if successful_metrics:
                report[key]["avg_execution_time"] = sum(
                    m.execution_time for m in successful_metrics
                ) / len(successful_metrics)
        
        return report

# Usage
monitor = PromptMonitor()

@monitor.monitor_prompt("chatbot", "v1")
def chat_with_bot(message):
    prompt = monitor.pm.get_prompt("chatbot", "v1")
    # Simulate processing
    time.sleep(0.1)
    return f"Response to: {message}"

# Use the monitored function
for i in range(10):
    chat_with_bot(f"Message {i}")

# Get performance report
report = monitor.get_performance_report()
print("Performance Report:")
for prompt_key, metrics in report.items():
    print(f"\n{prompt_key}:")
    print(f"  Total calls: {metrics['total_calls']}")
    print(f"  Success rate: {metrics['successful_calls']/metrics['total_calls']:.2%}")
    print(f"  Avg execution time: {metrics['avg_execution_time']:.3f}s")
```

### 3. Multi-Language Prompt System

```python
from enum import Enum
from typing import Dict, Optional
from promptgear import PromptManager

class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"

class MultiLanguagePromptManager:
    def __init__(self):
        self.pm = PromptManager()
    
    def create_multilingual_prompt(self, base_name: str, version: str, 
                                 prompts: Dict[Language, dict], 
                                 config: dict = None):
        """Create prompts for multiple languages"""
        for language, prompt_data in prompts.items():
            localized_name = f"{base_name}_{language.value}"
            self.pm.create_prompt(
                name=localized_name,
                version=version,
                system_prompt=prompt_data["system_prompt"],
                user_prompt=prompt_data["user_prompt"],
                config=config or {},
                overwrite=True
            )
    
    def get_localized_prompt(self, base_name: str, version: str, 
                           language: Language, fallback_language: Language = Language.ENGLISH):
        """Get prompt in specific language with fallback"""
        try:
            localized_name = f"{base_name}_{language.value}"
            return self.pm.get_prompt(localized_name, version)
        except:
            if language != fallback_language:
                fallback_name = f"{base_name}_{fallback_language.value}"
                return self.pm.get_prompt(fallback_name, version)
            raise

# Usage
ml_pm = MultiLanguagePromptManager()

# Create multilingual greeting prompts
ml_pm.create_multilingual_prompt("greeting", "v1", {
    Language.ENGLISH: {
        "system_prompt": "You are a friendly assistant.",
        "user_prompt": "Greet the user named {{name}} warmly."
    },
    Language.SPANISH: {
        "system_prompt": "Eres un asistente amigable.",
        "user_prompt": "Saluda cálidamente al usuario llamado {{name}}."
    },
    Language.FRENCH: {
        "system_prompt": "Vous êtes un assistant amical.",
        "user_prompt": "Saluez chaleureusement l'utilisateur nommé {{name}}."
    }
})

# Get localized prompt
spanish_prompt = ml_pm.get_localized_prompt("greeting", "v1", Language.SPANISH)
print(f"Spanish prompt: {spanish_prompt.user_prompt}")
```

## 🔧 DevOps and Deployment

### 1. CI/CD Pipeline Integration

```python
#!/usr/bin/env python3
"""
Prompt deployment script for CI/CD pipeline
"""

import json
import os
import sys
from typing import Dict, List
from promptgear import PromptManager

class PromptDeployer:
    def __init__(self, config_file: str = None):
        self.pm = PromptManager(config_file=config_file)
        self.deployment_log = []
    
    def load_prompts_from_file(self, file_path: str) -> List[Dict]:
        """Load prompts from JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def deploy_prompts(self, prompts_data: List[Dict], dry_run: bool = False):
        """Deploy prompts to the configured backend"""
        for prompt_data in prompts_data:
            try:
                if dry_run:
                    print(f"[DRY RUN] Would deploy: {prompt_data['name']}:{prompt_data['version']}")
                else:
                    self.pm.create_prompt(
                        name=prompt_data['name'],
                        version=prompt_data['version'],
                        system_prompt=prompt_data['system_prompt'],
                        user_prompt=prompt_data['user_prompt'],
                        config=prompt_data.get('config', {}),
                        overwrite=True
                    )
                    print(f"✓ Deployed: {prompt_data['name']}:{prompt_data['version']}")
                
                self.deployment_log.append({
                    "status": "success",
                    "prompt": f"{prompt_data['name']}:{prompt_data['version']}",
                    "dry_run": dry_run
                })
                
            except Exception as e:
                error_msg = f"✗ Failed to deploy {prompt_data['name']}:{prompt_data['version']}: {e}"
                print(error_msg)
                self.deployment_log.append({
                    "status": "error",
                    "prompt": f"{prompt_data['name']}:{prompt_data['version']}",
                    "error": str(e),
                    "dry_run": dry_run
                })
    
    def validate_deployment(self, prompts_data: List[Dict]) -> bool:
        """Validate that all prompts were deployed successfully"""
        for prompt_data in prompts_data:
            try:
                self.pm.get_prompt(prompt_data['name'], prompt_data['version'])
            except Exception as e:
                print(f"✗ Validation failed for {prompt_data['name']}:{prompt_data['version']}: {e}")
                return False
        
        print("✓ All prompts validated successfully")
        return True
    
    def generate_deployment_report(self) -> Dict:
        """Generate deployment report"""
        successful = [log for log in self.deployment_log if log['status'] == 'success']
        failed = [log for log in self.deployment_log if log['status'] == 'error']
        
        return {
            "total_prompts": len(self.deployment_log),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.deployment_log) if self.deployment_log else 0,
            "errors": failed
        }

def main():
    """Main deployment script"""
    if len(sys.argv) < 2:
        print("Usage: python deploy_prompts.py <prompts_file.json> [--dry-run]")
        sys.exit(1)
    
    prompts_file = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    # Determine environment
    env = os.getenv("ENVIRONMENT", "development")
    config_file = f"{env}.env"
    
    # Initialize deployer
    deployer = PromptDeployer(config_file=config_file)
    
    # Load prompts
    prompts_data = deployer.load_prompts_from_file(prompts_file)
    
    # Deploy prompts
    deployer.deploy_prompts(prompts_data, dry_run=dry_run)
    
    # Validate deployment (only if not dry run)
    if not dry_run:
        success = deployer.validate_deployment(prompts_data)
        if not success:
            sys.exit(1)
    
    # Generate report
    report = deployer.generate_deployment_report()
    print(f"\nDeployment Report:")
    print(f"Total prompts: {report['total_prompts']}")
    print(f"Successful: {report['successful']}")
    print(f"Failed: {report['failed']}")
    print(f"Success rate: {report['success_rate']:.2%}")
    
    if report['failed'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 2. Backup and Recovery

```python
#!/usr/bin/env python3
"""
Prompt backup and recovery utility
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from promptgear import PromptManager

class PromptBackupManager:
    def __init__(self, config_file: str = None):
        self.pm = PromptManager(config_file=config_file)
    
    def backup_all_prompts(self, backup_dir: str = "backups") -> str:
        """Backup all prompts to JSON file"""
        os.makedirs(backup_dir, exist_ok=True)
        
        # Get all prompts
        all_prompts = self.pm.list_prompts()
        
        # Convert to serializable format
        backup_data = []
        for prompt in all_prompts:
            backup_data.append({
                "name": prompt.name,
                "version": prompt.version,
                "system_prompt": prompt.system_prompt,
                "user_prompt": prompt.user_prompt,
                "config": prompt.config,
                "created_at": prompt.created_at.isoformat() if hasattr(prompt, 'created_at') else None
            })
        
        # Create backup file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"prompts_backup_{timestamp}.json")
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✓ Backed up {len(backup_data)} prompts to {backup_file}")
        return backup_file
    
    def restore_from_backup(self, backup_file: str, overwrite: bool = False):
        """Restore prompts from backup file"""
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        restored_count = 0
        skipped_count = 0
        
        for prompt_data in backup_data:
            try:
                # Check if prompt exists
                if not overwrite and self.pm.prompt_exists(prompt_data['name'], prompt_data['version']):
                    print(f"⚠ Skipping {prompt_data['name']}:{prompt_data['version']} (already exists)")
                    skipped_count += 1
                    continue
                
                # Restore prompt
                self.pm.create_prompt(
                    name=prompt_data['name'],
                    version=prompt_data['version'],
                    system_prompt=prompt_data['system_prompt'],
                    user_prompt=prompt_data['user_prompt'],
                    config=prompt_data['config'],
                    overwrite=overwrite
                )
                
                print(f"✓ Restored {prompt_data['name']}:{prompt_data['version']}")
                restored_count += 1
                
            except Exception as e:
                print(f"✗ Failed to restore {prompt_data['name']}:{prompt_data['version']}: {e}")
        
        print(f"\nRestore complete:")
        print(f"  Restored: {restored_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"  Total in backup: {len(backup_data)}")

def main():
    """Main backup/restore script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prompt Backup and Recovery")
    parser.add_argument("action", choices=["backup", "restore"], help="Action to perform")
    parser.add_argument("--file", help="Backup file path (for restore)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing prompts")
    parser.add_argument("--config", help="Configuration file")
    
    args = parser.parse_args()
    
    manager = PromptBackupManager(config_file=args.config)
    
    if args.action == "backup":
        manager.backup_all_prompts()
    elif args.action == "restore":
        if not args.file:
            print("Error: --file is required for restore")
            return
        manager.restore_from_backup(args.file, overwrite=args.overwrite)

if __name__ == "__main__":
    main()
```

## 🧪 Testing Examples

### 1. Comprehensive Test Suite

```python
import unittest
import tempfile
import os
from promptgear import PromptManager, PromptNotFoundError, PromptAlreadyExistsError
from promptgear.filesystem_backend import FilesystemBackend
from promptgear.sqlite_backend import SQLiteBackend

class TestPromptManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.backend = FilesystemBackend(self.test_dir)
        self.pm = PromptManager(backend=self.backend)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_create_prompt(self):
        """Test prompt creation"""
        prompt = self.pm.create_prompt(
            name="test",
            version="v1",
            system_prompt="Test system",
            user_prompt="Test user",
            config={"temperature": 0.7}
        )
        
        self.assertEqual(prompt.name, "test")
        self.assertEqual(prompt.version, "v1")
        self.assertEqual(prompt.system_prompt, "Test system")
        self.assertEqual(prompt.user_prompt, "Test user")
        self.assertEqual(prompt.config["temperature"], 0.7)
    
    def test_get_prompt(self):
        """Test prompt retrieval"""
        # Create first
        self.pm.create_prompt("test", "v1", "System", "User")
        
        # Then get
        prompt = self.pm.get_prompt("test", "v1")
        self.assertEqual(prompt.name, "test")
        self.assertEqual(prompt.system_prompt, "System")
    
    def test_prompt_not_found(self):
        """Test error handling for missing prompts"""
        with self.assertRaises(PromptNotFoundError):
            self.pm.get_prompt("nonexistent", "v1")
    
    def test_prompt_already_exists(self):
        """Test error handling for duplicate prompts"""
        self.pm.create_prompt("test", "v1", "System", "User")
        
        with self.assertRaises(PromptAlreadyExistsError):
            self.pm.create_prompt("test", "v1", "System", "User")
    
    def test_update_prompt(self):
        """Test prompt updating"""
        self.pm.create_prompt("test", "v1", "Original", "Original")
        
        updated = self.pm.update_prompt(
            "test", "v1", 
            system_prompt="Updated"
        )
        
        self.assertEqual(updated.system_prompt, "Updated")
        self.assertEqual(updated.user_prompt, "Original")  # Unchanged
    
    def test_list_prompts(self):
        """Test prompt listing"""
        # Create test prompts
        self.pm.create_prompt("test1", "v1", "System1", "User1")
        self.pm.create_prompt("test2", "v1", "System2", "User2")
        self.pm.create_prompt("test1", "v2", "System1v2", "User1v2")
        
        # Test list all
        all_prompts = self.pm.list_prompts()
        self.assertEqual(len(all_prompts), 3)
        
        # Test list by name
        test1_prompts = self.pm.list_prompts("test1")
        self.assertEqual(len(test1_prompts), 2)
    
    def test_list_versions(self):
        """Test version listing"""
        # Create multiple versions
        self.pm.create_prompt("test", "v1", "System1", "User1")
        self.pm.create_prompt("test", "v2", "System2", "User2")
        self.pm.create_prompt("test", "v3", "System3", "User3")
        
        versions = self.pm.list_versions("test")
        self.assertEqual(set(versions), {"v1", "v2", "v3"})
    
    def test_delete_prompt(self):
        """Test prompt deletion"""
        self.pm.create_prompt("test", "v1", "System", "User")
        
        # Verify exists
        self.assertTrue(self.pm.prompt_exists("test", "v1"))
        
        # Delete
        success = self.pm.delete_prompt("test", "v1")
        self.assertTrue(success)
        
        # Verify deleted
        self.assertFalse(self.pm.prompt_exists("test", "v1"))

class TestMultipleBackends(unittest.TestCase):
    """Test prompt manager with different backends"""
    
    def test_filesystem_backend(self):
        """Test filesystem backend"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend(tmpdir)
            pm = PromptManager(backend=backend)
            
            pm.create_prompt("test", "v1", "System", "User")
            prompt = pm.get_prompt("test", "v1")
            
            self.assertEqual(prompt.name, "test")
            
            # Verify file was created
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "test", "v1.yaml")))
    
    def test_sqlite_backend(self):
        """Test SQLite backend"""
        backend = SQLiteBackend(":memory:")
        pm = PromptManager(backend=backend)
        
        pm.create_prompt("test", "v1", "System", "User")
        prompt = pm.get_prompt("test", "v1")
        
        self.assertEqual(prompt.name, "test")

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Test with Docker

```python
import unittest
import docker
import time
from promptgear import PromptManager
from promptgear.postgres_backend import PostgresBackend

class TestPostgresIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up PostgreSQL container for testing"""
        cls.client = docker.from_env()
        
        # Start PostgreSQL container
        cls.container = cls.client.containers.run(
            "postgres:15",
            environment={
                "POSTGRES_DB": "test_prompts",
                "POSTGRES_USER": "test",
                "POSTGRES_PASSWORD": "test"
            },
            ports={"5432/tcp": 5433},
            detach=True,
            remove=True
        )
        
        # Wait for PostgreSQL to be ready
        time.sleep(5)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up PostgreSQL container"""
        cls.container.stop()
    
    def setUp(self):
        """Set up test environment"""
        self.backend = PostgresBackend(
            "postgresql://test:test@localhost:5433/test_prompts"
        )
        self.pm = PromptManager(backend=self.backend)
    
    def test_crud_operations(self):
        """Test CRUD operations with PostgreSQL"""
        # Create
        prompt = self.pm.create_prompt(
            "test_postgres", "v1", "System", "User", {"temp": 0.7}
        )
        self.assertEqual(prompt.name, "test_postgres")
        
        # Read
        retrieved = self.pm.get_prompt("test_postgres", "v1")
        self.assertEqual(retrieved.system_prompt, "System")
        
        # Update
        updated = self.pm.update_prompt(
            "test_postgres", "v1", system_prompt="Updated"
        )
        self.assertEqual(updated.system_prompt, "Updated")
        
        # Delete
        success = self.pm.delete_prompt("test_postgres", "v1")
        self.assertTrue(success)
    
    def test_concurrent_access(self):
        """Test concurrent access to PostgreSQL"""
        import threading
        
        def create_prompts(thread_id):
            for i in range(10):
                self.pm.create_prompt(
                    f"thread_{thread_id}_prompt_{i}", "v1", 
                    f"System {i}", f"User {i}"
                )
        
        threads = []
        for i in range(3):
            thread = threading.Thread(target=create_prompts, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify all prompts were created
        all_prompts = self.pm.list_prompts()
        self.assertEqual(len(all_prompts), 30)  # 3 threads × 10 prompts each

if __name__ == '__main__':
    unittest.main()
```

## 📚 Next Steps

These examples demonstrate various ways to use Prompt Gear in real-world scenarios. For more information:

- Read [Best Practices](best-practices.md) for production usage
- Check [Configuration](configuration.md) for setup details
- Explore [Backends](backends.md) for storage options
- Review [Troubleshooting](troubleshooting.md) for common issues

Remember to adapt these examples to your specific use case and requirements!
