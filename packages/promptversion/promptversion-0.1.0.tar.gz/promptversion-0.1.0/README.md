# PromptVersion

*Simple prompt version control for AI development*

[![PyPI version](https://badge.fury.io/py/promptversion.svg)](https://badge.fury.io/py/promptversion)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PromptVersion is a lightweight tool for managing AI prompts with version control, templating, and variable injection. Think "Git for prompts" - but simpler.

## Why PromptVersion?

- 📝 **Templated YAML prompts** with variable injection
- 🏷️ **Semantic versioning** for prompt iterations  
- 🚀 **Simple CLI** for prompt management
- 🐍 **Clean Python API** for integration
- 📁 **No external dependencies** - just files and Git

## Quick Start

### Installation

```bash
pip install promptversion
```

### Initialize a repository

```bash
promptversion init
```

### Create your first prompt

```bash
promptversion create classifier --description "Ticket classifier"
```

### Use in Python

```python
from promptversion import PromptVersion

pv = PromptVersion()

# Render with variables
result = pv.render("classifier", {
    "ticket": "I can't log into my account",
    "max_categories": 3
})

# Use with any LLM
import openai
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": result}]
)
```

## Features

- **Templated YAML prompts** with variable injection
- **Internal version control** with semantic versioning
- **Simple CLI** for prompt management
- **Clean Python API** for integration

## Prompt Format

Prompts are stored as YAML files in the `prompts/` directory:

```yaml
name: "classifier"
version: "1.0.0"
description: "Classifies support tickets"

variables:
  max_categories:
    default: 5
    type: "integer"
  language:
    default: "en" 
    type: "string"

template: |
  You are a support ticket classifier.
  
  Classify this ticket into up to {{max_categories}} categories.
  Respond in {{language}}.
  
  Ticket: {{ticket}}
```

## CLI Commands

- `promptversion init` - Initialize repository
- `promptversion create <n>` - Create new prompt
- `promptversion edit <n>` - Edit prompt
- `promptversion commit <n>` - Commit changes
- `promptversion tag <n> <tag>` - Tag version
- `promptversion list` - List all prompts
- `promptversion show <n>` - Show prompt details
- `promptversion test <n>` - Test prompt rendering
- `promptversion versions <n>` - Show version history

## Python API

```python
from promptversion import PromptVersion

# Initialize
pv = PromptVersion()

# Get prompt
prompt = pv.get("classifier")

# Render with variables
result = prompt.render({"ticket": "Login issue"})

# Get specific version
prompt_v1 = pv.get("classifier", version="1.0.0")

# List all prompts
prompts = pv.list_prompts()
```

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/promptversion
cd promptversion

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black promptversion tests
```

## License

MIT License
