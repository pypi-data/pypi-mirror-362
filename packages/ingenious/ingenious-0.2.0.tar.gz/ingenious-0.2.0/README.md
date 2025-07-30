# Insight Ingenious

An enterprise-grade Python library for quickly setting up APIs to interact with AI Agents, featuring tight integrations with Microsoft Azure services and comprehensive utilities for debugging and customization.

## Quick Start

Get up and running in 5 minutes with Azure OpenAI!

### Prerequisites
- Python 3.13 or higher
- Azure OpenAI API credentials
- [uv package manager](https://docs.astral.sh/uv/)

### 5-Minute Setup

1. **Install and Initialize**:
    ```bash
    # From your project directory - choose installation based on features needed
    uv add ingenious[standard]    # Most common: includes SQL agent support
    # OR
    uv add ingenious[azure-full]  # Full Azure integration
    # OR
    uv add ingenious             # Minimal installation

    # Add required dependencies for knowledge-base and SQL workflows
    uv add chromadb aiofiles autogen-ext

    # Initialize project
    uv run ingen init
    ```

2. **Configure Credentials**:
    Copy the example template and add your Azure OpenAI credentials:
    ```bash
    # Copy environment template (choose based on your needs)
    cp .env.example .env          # Full configuration options
    # OR
    cp .env.development .env      # Minimal development setup
    # OR
    cp .env.azure-full .env       # Full Azure integration

    # Edit .env file with your actual credentials
    nano .env
    ```

    **Required configuration (add to .env file)**:
    ```bash
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY=your-api-key-here
    AZURE_OPENAI_BASE_URL=https://your-resource.openai.azure.com/

    # Model Configuration (pydantic-settings format)
    INGENIOUS_MODELS__0__MODEL=gpt-4.1-nano
    INGENIOUS_MODELS__0__API_TYPE=rest
    INGENIOUS_MODELS__0__API_VERSION=2024-12-01-preview
    INGENIOUS_MODELS__0__DEPLOYMENT=gpt-4.1-nano
    INGENIOUS_MODELS__0__API_KEY=your-actual-api-key-here
    INGENIOUS_MODELS__0__BASE_URL=https://your-resource.openai.azure.com/

    # Basic required settings
    INGENIOUS_CHAT_SERVICE__TYPE=multi_agent
    INGENIOUS_CHAT_HISTORY__DATABASE_TYPE=sqlite
    INGENIOUS_CHAT_HISTORY__DATABASE_PATH=./.tmp/chat_history.db
    INGENIOUS_CHAT_HISTORY__MEMORY_PATH=./.tmp
    ```

3. **Validate Configuration**:
    ```bash
    uv run ingen validate  # Check configuration before starting
    ```

    > **Note**: Ingenious now uses **pydantic-settings** for configuration via environment variables. Legacy YAML configuration files (`config.yml`, `profiles.yml`) are no longer supported and must be migrated to environment variables with `INGENIOUS_` prefixes using the migration script at `scripts/migrate_config.py`.

4. **Start the Server**:
    ```bash
    # Start server on port 8000 (override default port 80)
    uv run ingen serve --port 8000
    ```

5. **Verify Health**:
    ```bash
    # Check server health
    curl http://localhost:8000/api/v1/health
    ```

6. **Test with Core Workflows**:

    Create test files to avoid JSON escaping issues:
    ```bash
    # Create test files for each workflow
    echo '{"user_prompt": "Analyze this customer feedback: Great product", "conversation_flow": "classification-agent"}' > test_classification.json
    echo '{"user_prompt": "Search for documentation about setup", "conversation_flow": "knowledge-base-agent"}' > test_knowledge.json
    echo '{"user_prompt": "Show me all tables in the database", "conversation_flow": "sql-manipulation-agent"}' > test_sql.json

    # Test each workflow
    curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d @test_classification.json
    curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d @test_knowledge.json
    curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d @test_sql.json
    ```

That's it! You should see a JSON response with AI analysis of the input.

**Next Steps - Test Additional Workflows**:

7. **Test bike-insights Workflow (Requires `ingen init` first)**:

    The `bike-insights` workflow is part of the project template and must be initialized first:
    ```bash
    # First initialize project to get bike-insights workflow
    ingen init

    # Create bike-insights test data file
    cat > test_bike_insights.json << 'EOF'
{
  "user_prompt": "{\"revision_id\": \"test-v1\", \"identifier\": \"test-001\", \"stores\": [{\"name\": \"Test Store\", \"location\": \"NSW\", \"bike_sales\": [{\"product_code\": \"MB-TREK-2021-XC\", \"quantity_sold\": 2, \"sale_date\": \"2023-04-01\", \"year\": 2023, \"month\": \"April\", \"customer_review\": {\"rating\": 4.5, \"comment\": \"Great bike\"}}], \"bike_stock\": []}]}",
  "conversation_flow": "bike-insights"
}
EOF

    # Test bike-insights workflow
    curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d @test_bike_insights.json
    ```

**Important Notes**:
- **Core Library Workflows** (`classification-agent`, `knowledge-base-agent`, `sql-manipulation-agent`) are always available and accept simple text prompts
- **Template Workflows** like `bike-insights` require JSON-formatted data with specific fields and are only available after running `ingen init`
- The `bike-insights` workflow is the recommended "Hello World" example for new users

## CLI Commands

**Core commands:**
- `ingen init` - Initialize a new project with templates and configuration
- `ingen serve` - Start the API server with web interface
- `ingen workflows [workflow_name]` - List available workflows and their requirements
- `ingen test` - Run agent workflow tests
- `ingen validate` - Validate system configuration and requirements
- `ingen help [topic]` - Show detailed help and getting started guide
- `ingen status` - Check system status and configuration
- `ingen version` - Show version information

**Data processing commands:**
- `ingen document-processing extract <path>` - Extract text from documents (PDF, DOCX, images)
- `ingen dataprep crawl <url>` - Web scraping utilities using Scrapfly

**Help and information:**
- `ingen --help` - Show comprehensive help
- `ingen <command> --help` - Get help for specific commands

For complete CLI reference, see [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md).

## API Endpoints

When the server is running, the following endpoints are available:

**Core API:**
- `POST /api/v1/chat` - Chat with AI workflows
- `GET /api/v1/health` - Health check endpoint

**Diagnostics:**
- `GET /api/v1/workflows` - List all workflows and their status
- `GET /api/v1/workflow-status/{workflow_name}` - Check specific workflow configuration
- `GET /api/v1/diagnostic` - System diagnostic information

**Prompt Management:**
- `GET /api/v1/revisions/list` - List available prompt revisions
- `GET /api/v1/workflows/list` - List workflows with prompts
- `GET /api/v1/prompts/list/{revision_id}` - List prompt templates for revision
- `GET /api/v1/prompts/view/{revision_id}/{filename}` - View prompt content
- `POST /api/v1/prompts/update/{revision_id}/{filename}` - Update prompt template

**Authentication (if enabled):**
- `POST /api/v1/auth/login` - JWT login
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `GET /api/v1/auth/verify` - Verify JWT token

**Web Interfaces:**
- API documentation available at `/docs`

**Additional Routes:**
- `GET /api/v1/conversations/{thread_id}` - Retrieve conversation history
- `PUT /api/v1/messages/{message_id}/feedback` - Submit message feedback

## Workflow Categories

Insight Ingenious provides multiple conversation workflows with different configuration requirements:

### Core Library Workflows (Always Available)
These workflows are built into the Ingenious library and available immediately:

- `classification-agent` - Route input to specialized agents based on content (Azure OpenAI only)
- `knowledge-base-agent` - Search knowledge bases using local ChromaDB (STABLE - recently fixed)
- `sql-manipulation-agent` - Execute SQL queries using local SQLite (STABLE - recently fixed)

> **Note**: Core workflows support both hyphenated (`classification-agent`) and underscored (`classification_agent`) naming formats for backward compatibility.

### Template Workflows (Available via `ingen init`)
These workflows are created when you initialize a new project and serve as examples for custom development:

- `bike-insights` - Comprehensive bike sales analysis showcasing multi-agent coordination (**Created by `ingen init`** - demonstrates custom workflow development)

> **Note**: The `bike-insights` workflow is the recommended starting point and "Hello World" example for new Ingenious users. It's only available after running `ingen init` to create the project template.

### Configuration Requirements by Workflow
- **Minimal setup** (Azure OpenAI only): `classification-agent`, `bike-insights`
- **Local implementations** (STABLE): `knowledge-base-agent` (ChromaDB), `sql-manipulation-agent` (SQLite)
- **Azure integrations** (EXPERIMENTAL): Azure Search for knowledge base, Azure SQL for database queries

> **Important**: Local implementations (ChromaDB, SQLite) are stable and work out-of-the-box. Azure integrations are experimental and contain known bugs. For production use, stick with local implementations. Use `ingen workflows` to check configuration requirements for each workflow.

### Required Dependencies

Some workflows require additional dependencies:

```bash
# For knowledge-base-agent (ChromaDB)
uv add chromadb

# For sql-manipulation-agent (SQLite support)
uv add aiofiles

# For updated autogen compatibility
uv add autogen-ext
```

## Installation Options

Choose the installation option that matches your intended use case:

### Minimal Installation
```bash
uv add ingenious
```
**Includes**: Core chat functionality, classification-agent workflow
**Use for**: Basic API development, testing Azure OpenAI connectivity

### Standard Installation (Recommended)
```bash
uv add ingenious[standard]
```
**Includes**: Core features + SQL agent support (pandas, database connectivity)
**Use for**: Most production deployments with local database features

### Azure Full Integration
```bash
uv add ingenious[azure-full]
```
**Includes**: Standard features + Azure services (Azure SQL, Blob Storage, Search)
**Use for**: Full cloud deployment with Azure integrations

### Complete Feature Set
```bash
uv add ingenious[full]
```
**Includes**: All features including document processing, ML capabilities, data preparation
**Use for**: Advanced use cases requiring all available features

### Knowledge Base Features
```bash
uv add ingenious[knowledge-base]
# OR manually install dependencies
uv add ingenious && uv add chromadb aiofiles autogen-ext
```
**Includes**: Core features + ChromaDB and ML capabilities for knowledge-base-agent
**Use for**: Local knowledge base and search functionality (STABLE)


## Project Structure

- `ingenious/`: Core framework code
  - `api/`: FastAPI routes and endpoints
    - `routes/`: Individual route modules (auth, chat, diagnostic, etc.)
  - `auth/`: JWT authentication and security
  - `cli/`: Command-line interface modules
    - `commands/`: Individual command implementations
  - `config/`: Configuration management (pydantic-settings based)
    - `main_settings.py`: Primary settings class
    - `models.py`: Configuration model definitions
    - `environment.py`: Environment handling
  - `core/`: Core logging and error handling
  - `dataprep/`: Web scraping and data preparation utilities
  - `db/`: Database integration (SQLite and Azure SQL)
  - `document_processing/`: PDF/document text extraction
  - `errors/`: Custom exception classes
  - `external_services/`: OpenAI and other service integrations
  - `files/`: File storage (local and Azure Blob)
  - `main/`: FastAPI application factory and middleware
  - `models/`: Pydantic data models and schemas
  - `services/`: Core business logic and services
    - `chat_services/multi_agent/`: Multi-agent conversation flows
      - `conversation_flows/`: Individual workflow implementations
  - `templates/`: Jinja2 prompt templates and HTML
  - `utils/`: Utility functions and helpers
  - `ingenious_extensions_template/`: Template for custom projects
    - `services/chat_services/multi_agent/conversation_flows/bike_insights/`: Sample workflow

- `scripts/`: Utility scripts
  - `migrate_config.py`: Migrate YAML configs to environment variables
- `tests/`: Test suite
  - `unit/`: Unit tests
  - `integration/`: Integration tests

## Documentation

For detailed documentation, see the [docs](https://insight-services-apac.github.io/ingenious/) or view locally in the `docs/` directory.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/Insight-Services-APAC/ingenious/blob/main/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the terms specified in the [LICENSE](https://github.com/Insight-Services-APAC/ingenious/blob/main/LICENSE) file.
