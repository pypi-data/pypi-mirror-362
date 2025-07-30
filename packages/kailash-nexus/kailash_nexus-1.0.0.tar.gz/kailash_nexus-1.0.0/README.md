# Kailash Nexus - Zero Configuration Workflow Orchestration

A truly zero-configuration platform that allows enterprise users to focus on creating workflows without learning infrastructure complexity.

## What is Nexus?

Nexus embodies the zero-config philosophy: **just call `create_nexus()` and start!**

- **Zero Parameters**: No configuration files, environment variables, or setup required
- **Progressive Enhancement**: Start simple, add features as needed
- **Multi-Channel**: API, CLI, and MCP access unified
- **Auto-Discovery**: Workflows are automatically found and registered
- **Enterprise Ready**: Built-in auth, monitoring, and plugin system

## Quick Start

```python
from nexus import create_nexus

# That's it! Zero configuration needed.
create_nexus().start()
```

## Core Features

### 1. Zero Configuration Initialization
```python
from nexus import create_nexus

# Create and start with zero parameters
n = create_nexus()
n.start()

# Check health
print(n.health_check())
```

### 2. Automatic Workflow Discovery
Place workflows in your directory using these patterns:
- `workflows/*.py`
- `*.workflow.py`
- `workflow_*.py`
- `*_workflow.py`

Example workflow file (`my_workflow.py`):
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_node("LLMAgentNode", "agent", {"model": "gpt-4"})
```

Nexus automatically discovers and registers it!

### 3. Progressive Enhancement
Start simple and add features as needed:

```python
from nexus import create_nexus

n = create_nexus()
n.enable_auth()           # Add authentication
n.enable_monitoring()     # Add metrics collection
n.use_plugin("rate_limit") # Add rate limiting
n.start()
```

### 4. Multi-Channel Access
Your workflows are automatically available via:

- **REST API**: `http://localhost:8000/workflows/{name}`
- **CLI**: `nexus run {name}`
- **MCP**: Model Context Protocol integration

### 5. Smart Defaults
- API server on port 8000 (auto-finds available port)
- MCP server on port 3001 (auto-finds available port)
- Health endpoint at `/health`
- Auto CORS and documentation enabled
- Graceful error handling and isolation

## Architecture

Nexus is built as a separate application using Kailash SDK components:

```
┌─ kailash_nexus_app/
├── core.py          # Zero-config wrapper around SDK
├── discovery.py     # Auto-discovery of workflows
├── plugins.py       # Progressive enhancement system
├── channels.py      # Multi-channel configuration
└── __init__.py      # Simple `create_nexus()` function
```

### Key Principles

1. **SDK as Building Blocks**: Uses existing Kailash SDK without modification
2. **Zero Config by Default**: No parameters required for basic usage
3. **Progressive Enhancement**: Add complexity only when needed
4. **Smart Defaults**: Everything just works out of the box

## Plugin System

Built-in plugins include:

- **Auth Plugin**: Authentication and authorization
- **Monitoring Plugin**: Performance metrics and health checks
- **Rate Limit Plugin**: Request rate limiting

Create custom plugins:
```python
from kailash_nexus_app.plugins import NexusPlugin

class MyPlugin(NexusPlugin):
    @property
    def name(self):
        return "my_plugin"

    @property
    def description(self):
        return "My custom plugin"

    def apply(self, nexus_instance):
        # Enhance nexus functionality
        nexus_instance.my_feature = True
```

## Testing

Comprehensive test suite with 52 tests:

```bash
# Run all tests
python -m pytest tests/ -v

# Unit tests only (45 tests)
python -m pytest tests/unit/ -v

# Integration tests only (7 tests)
python -m pytest tests/integration/ -v
```

## Use Cases

### Data Scientists
```python
# Just start and focus on workflows
from nexus import create_nexus
create_nexus().start()
```

### DevOps Engineers
```python
# Add production features progressively
from nexus import create_nexus

create_nexus().enable_auth().enable_monitoring().start()
```

### AI Developers
```python
# Register AI workflows automatically
from nexus import create_nexus
from kailash.workflow.builder import WorkflowBuilder

n = create_nexus()

# Manual registration
workflow = WorkflowBuilder()
workflow.add_node("LLMAgentNode", "ai", {"model": "gpt-4"})
n.register("ai-assistant", workflow)

n.start()
```

## Comparison with v1

| Feature | Nexus v1 | Nexus v2 (This Implementation) |
|---------|----------|--------------------------------|
| Configuration | 200+ lines | 0 lines |
| Startup | Complex setup | `create_nexus().start()` |
| Channels | Manual config | Auto-configured |
| Discovery | None | Automatic |
| Enhancement | Built-in complexity | Progressive plugins |

## Implementation Status

✅ **Core Features Implemented**:
- Zero-config initialization
- Workflow discovery and auto-registration
- Plugin system for progressive enhancement
- Channel configuration with smart defaults
- Comprehensive test suite (52 tests passing)

⏳ **Future Enhancements**:
- Real SDK gateway integration
- Production deployment patterns
- Advanced enterprise features

This implementation demonstrates the true zero-config vision: a platform where enterprise users can focus on creating workflows without infrastructure complexity.
