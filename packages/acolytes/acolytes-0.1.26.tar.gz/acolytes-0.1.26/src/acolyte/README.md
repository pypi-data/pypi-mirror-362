# ACOLYTE Python Package

This is the core Python package for ACOLYTE - Your Local AI Programming Assistant.

## Package Structure

```
acolyte/
├── api/         # FastAPI endpoints and WebSocket handlers
├── core/        # Core infrastructure (logging, database, exceptions)
├── dream/       # Deep analysis and optimization system
├── embeddings/  # Vector embedding generation
├── install/     # Installation and setup utilities
│   └── commands/  # Refactored CLI commands
│       ├── doctor.py          # System diagnostics
│       ├── index.py           # Index command implementation
│       ├── progress_monitor.py # Progress tracking utilities
│       └── validators.py      # Command validation helpers
├── models/      # Pydantic models and schemas
├── rag/         # Retrieval Augmented Generation system
├── semantic/    # Natural language processing
├── services/    # Business logic services
└── cli.py       # Command-line interface entry point
```

## Key Components

- **CLI**: Main entry point for the `acolyte` command
  - Refactored for better maintainability
  - Complex commands moved to `install/commands/`
  - Cleaner separation of concerns
- **API**: OpenAI-compatible REST API
- **Services**: Core business logic (chat, indexing, git, etc.)
- **RAG**: Code search and retrieval system
- **Dream**: Autonomous code analysis system

## CLI Architecture

The CLI has been refactored to improve maintainability and debugging:

- **cli.py**: Main entry point, command registration
- **install/commands/**: Modular command implementations
  - `validators.py`: Shared validation logic for commands
  - `progress_monitor.py`: WebSocket and HTTP progress monitoring
  - `index.py`: Indexing command implementation
  - `doctor.py`: System diagnostics and repair

This structure allows for:
- Easier debugging of individual commands
- Reusable validation and utility functions
- Better separation of concerns
- Simplified testing

## Installation

This package is installed as part of the ACOLYTE system:

```bash
pip install git+https://github.com/unmasSk/acolyte.git
```

## Development

For development work:

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/acolyte
```

## License

See LICENSE file in the project root.
