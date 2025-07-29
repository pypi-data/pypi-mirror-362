# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Patronus Python SDK is a library for systematic evaluation of Large Language Models (LLMs). It provides tools to build, test, and improve LLM applications with customizable tasks, evaluators, and comprehensive experiment tracking.

## Development Commands

### Setup and Installation
```bash
# Install project with all dependencies
uv sync --all-groups

# Install specific feature sets
uv pip install -e ".[experiments]"  # For experiments support (includes pandas)
uv pip install -e ".[examples]"     # For running examples
```

### Code Quality
```bash
# Format code
uv run ruff format src/ examples/

# Lint code with auto-fix
uv run ruff check --fix src/ examples/

# Type checking
uv run --group lint mypy src/
uv run --group lint pyright src/

# Run all pre-commit checks
pre-commit run --all-files
```

### Documentation
```bash
# Serve docs locally (http://localhost:8000)
uv run --group docs mkdocs serve

# Build documentation
uv run --group docs mkdocs build
```

## Architecture Overview

### Core Modules Structure
- **src/patronus/api/**: **[DEPRECATED]** Legacy API client - DO NOT use for new features
- **src/patronus/tracing/**: Function tracing decorators and utilities
- **src/patronus/evaluations/**: Evaluation framework with remote and custom evaluators
- **src/patronus/experiments/**: Experiment running and tracking system
- **src/patronus/datasets/**: Dataset management for experiments
- **src/patronus/prompts/**: Prompt management (local and API-based)
- **src/patronus/integrations/**: LLM framework integrations (OpenAI, Anthropic, LangChain, CrewAI, PydanticAI)
- **src/patronus/context/**: Logging and context management utilities
- **src/patronus/cli/**: Command-line interface

### Key Design Patterns
1. **Configuration**: Hierarchical configuration system supporting environment variables (PATRONUS_*), YAML files, and code-based config
2. **Tracing**: Decorator-based tracing with OpenTelemetry integration for distributed systems
3. **Evaluations**: Flexible evaluator system supporting both remote (API-based) and local custom evaluators
4. **Experiments**: Dataset-driven experiment framework with comprehensive result tracking

### Integration Points
- **OpenTelemetry**: Full OTLP support for tracing with HTTP/protobuf protocols
- **LLM Frameworks**: Native integrations via decorators and context managers
- **Export**: Results can be exported to CSV and other formats

## Important Development Notes

1. **Python Version**: Requires Python 3.9+
2. **String Style**: Use double quotes for strings
3. **Docstring Convention**: Google style docstrings
4. **Line Length**: 120 characters max (configured in Ruff)
5. **Version Management**: Uses git-based dynamic versioning - version is automatically determined from git tags
6. **Workspace**: The `examples/` directory is a uv workspace member with its own dependencies
7. **API Client**: Use `from patronus_api import Client, AsyncClient` for new features - the `patronus.api` module is deprecated
8. **Examples**: When adding new features, always update or add corresponding examples in the `examples/` directory and update their documentation pages

## Testing

No test files found in the repository. When implementing tests, consider the project's modular structure and the need to test:
- API client interactions
- Tracing functionality
- Evaluator implementations
- Experiment workflows
- Integration points with various LLM frameworks

## Common Development Tasks

### Adding a New Integration
1. Create module in `src/patronus/integrations/`
2. Implement tracing decorators or context managers
3. Use `from patronus_api import Client, AsyncClient` for API interactions
4. Add example in `examples/` directory (separate package)
5. Update documentation in `docs/` including the examples documentation page

### Creating Custom Evaluators
1. Use the `@evaluator` decorator from `patronus.evaluations`
2. Return `EvaluationResult` with pass/fail status and optional metadata
3. Can be synchronous or asynchronous functions

### Working with Experiments
1. Define datasets using the Dataset class
2. Create task functions that process dataset rows
3. Configure evaluators (remote or custom)
4. Run experiments with `p.experiment()` providing dataset, task, and evaluators