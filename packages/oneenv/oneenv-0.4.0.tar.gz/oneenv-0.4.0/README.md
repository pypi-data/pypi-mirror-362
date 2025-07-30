# OneEnv 🌟

[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

**Python environment variable management made simple.**

OneEnv automatically discovers environment variable templates from your installed packages and manages them with namespaces.

## Core Features 🎯

### 1. 🏗️ Intelligent Scaffolding System
Organize environment templates by categories (Database, VectorStore, LLM, etc.) with structured discovery and selective generation.

### 2. 📦 Package Environment Variable Discovery
Automatically collect environment variable templates from all installed packages - no manual configuration required.

### 3. 🏷️ Namespace Management
Organize environment variables by service/component with intelligent fallback.

### 4. 🛠️ Tool-Friendly APIs
Programmatic access to template structure for building custom scaffolding tools and integrations.

## Installation 📦

```bash
pip install oneenv
```

## Quick Start 🚀

### Generate Environment Template
```bash
oneenv template
```

### Explore Available Templates
```bash
# View all available categories and options
oneenv template --structure

# Get detailed info for a specific category
oneenv template --info Database

# Preview a specific option
oneenv template --preview Database postgres

# Generate custom configuration
oneenv template --generate Database:postgres VectorStore:chroma
```

### Use Named Environments
```python
import oneenv

# Load different environments
oneenv.env().load_dotenv("common.env")
oneenv.env("database").load_dotenv("database.env")
oneenv.env("web").load_dotenv("web.env")

# Get values with namespace fallback
db_host = oneenv.env("database").get("HOST", "localhost")
web_port = oneenv.env("web").get("PORT", "8000")
timeout = oneenv.env("database").get("TIMEOUT", "30")  # Falls back to common
```

## Example: Before vs After

**Before OneEnv:**
```python
# Scattered environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
WEB_HOST = os.getenv("WEB_HOST")
API_KEY = os.getenv("API_KEY")
```

**After OneEnv:**
```python
# Organized by namespace
db_url = oneenv.env("database").get("URL")
web_host = oneenv.env("web").get("HOST")
api_key = oneenv.env("api").get("KEY")
```

## How It Works

1. **Discovery**: OneEnv finds environment variable templates from installed packages
2. **Generation**: Creates consolidated `.env.example` files
3. **Namespace**: Loads variables into separate namespaces with fallback to common settings

## Advanced Usage: Scaffolding System 🏗️

OneEnv's intelligent scaffolding system organizes templates by categories and provides powerful APIs for custom tool development:

### Interactive Template Discovery
```bash
# Discover available templates
oneenv template --structure

# Get category details with variable counts
oneenv template --info Database

# Preview what variables an option provides
oneenv template --preview Database postgres

# Generate templates with specific selections
oneenv template --generate Database:postgres VectorStore:chroma LLM:openai

# JSON output for automation
oneenv template --structure --json
```

### Programmatic API for Custom Tools 🛠️

Build sophisticated scaffolding tools using OneEnv's comprehensive APIs:

```python
import oneenv

# Discovery API
structure = oneenv.get_all_template_structure()
print("Available categories:", list(structure.keys()))
# Output: {'Database': ['postgres', 'sqlite'], 'VectorStore': ['chroma', 'pinecone']}

# Validation API
if oneenv.has_category("Database"):
    options = oneenv.get_options("Database")
    print(f"Database options: {options}")

# Information API
info = oneenv.get_category_info("Database")
print(f"Total variables: {info['total_variables']}")
print(f"Critical variables: {info['critical_variables']}")

# Preview API
preview = oneenv.get_option_preview("Database", "postgres")
for var_name, config in preview['variables'].items():
    print(f"{var_name}: {config['importance']} - {config['description']}")

# Generation API
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

content = oneenv.generate_template(".env.example", selections)
print("Generated custom template with selected components!")
```

### Create Package Templates 📦

Developers can create discoverable templates using the new scaffolding format:

```python
# mypackage/templates.py
def database_template():
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL connection URL",
                    "default": "postgresql://user:pass@localhost:5432/dbname",
                    "required": True,
                    "importance": "critical"
                },
                "DATABASE_POOL_SIZE": {
                    "description": "Connection pool size",
                    "default": "10",
                    "required": False,
                    "importance": "important"
                }
            }
        },
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLite database file path",
                    "default": "sqlite:///app.db",
                    "required": True,
                    "importance": "critical"
                }
            }
        }
    ]
```

Register in `pyproject.toml`:
```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
```

**Key Features:**
- **Category-based organization** - Group related templates (Database, VectorStore, LLM, etc.)
- **Multiple options per category** - Provide alternatives (postgres, sqlite, mysql)
- **Importance levels** - Critical, Important, Optional for better user guidance
- **Automatic discovery** - Users automatically see your templates with `oneenv template --structure`

## Learn More 📚

### Step-by-Step Tutorials

#### 🌱 **Basics** (5-10 min each)
1. **[Basic dotenv Usage](docs/tutorials/01-basic-dotenv.md)** - Learn environment variable fundamentals and OneEnv basics
2. **[Auto Template Generation](docs/tutorials/02-template-generation.md)** - Discover how OneEnv automatically finds and generates environment templates  
3. **[Named Environments](docs/tutorials/03-named-environments.md)** - Master namespace management with intelligent fallback

#### 🚀 **Practical** (10-15 min each)
4. **[Multi-Service Management](docs/tutorials/04-multi-service.md)** - Configure complex applications with multiple services
5. **[Custom Templates](docs/tutorials/05-custom-templates.md)** - Create reusable project-specific templates
6. **[Production Best Practices](docs/tutorials/06-production-tips.md)** - Secure configuration management for production environments

#### ⚡ **Advanced** (15-20 min each)
7. **[Plugin Development](docs/tutorials/07-plugin-development.md)** - Build distributable OneEnv plugins for the community
8. **[CI/CD Integration](docs/tutorials/08-cicd-integration.md)** - Automate configuration management in your deployment pipeline

#### 🚀 **New Scaffolding Features** (10-20 min each)
9. **[New Template Creation](docs/tutorials/09-new-template-creation.md)** - Create discoverable templates using the new scaffolding format
10. **[Scaffolding Tool Creation](docs/tutorials/10-scaffolding-tool-creation.md)** - Build custom scaffolding tools with OneEnv's APIs
11. **[Practical Guide](docs/tutorials/11-practical-guide.md)** - Real-world examples for RAG systems, web apps, and more

### 📚 **Documentation**
- **[Scaffolding Usage Guide](docs/user-guides/scaffolding-usage.md)** - Comprehensive guide to the scaffolding system
- **[API Reference](docs/api-reference/scaffolding-api.md)** - Complete API documentation for custom tool development

**Start here:** [Step 1: Basic dotenv Usage](docs/tutorials/01-basic-dotenv.md)

## License ⚖️

MIT License