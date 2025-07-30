# SGAI Evaluator

A universal tracing middleware for agent applications with support for multiple tracing backends. This package provides a framework-agnostic tracing interface that can work with any tracing backend (currently supporting Langfuse, with extensibility for others) through a simple adapter pattern.

## Features

- 🔄 Universal tracing interface with pluggable backends
- 🤖 Automatic framework detection and integration
  - OpenAI Agents SDK
  - Google ADK
  - CrewAI
  - LangChain
- 🎯 Manual instrumentation support
  - Function decorators
  - Context managers
  - Span management
- 🔌 Extensible backend system
- 🚀 Async/sync support

## Installation

```bash
pip install sgai-evaluator
```

## Quick Start

```python
from sgai_evaluator import trace, start_span, start_generation

# Decorate functions for automatic tracing
@trace(name="my_function")
def my_function(arg1, arg2):
    return arg1 + arg2

# Use context managers for manual tracing
with start_span("manual_operation") as span:
    # Do something
    result = perform_operation()
    span.update(output=result)

# Track LLM generations
with start_generation("text_generation", model="gpt-4") as span:
    response = llm.generate("Hello!")
    span.update(output=response)
```

## Configuration

The package uses environment variables for configuration:

- `SGAI_TRACER`: The tracing backend to use (default: 'langfuse')
- `SGAI_SERVICE_NAME`: Service name for framework integrations (default: 'agent_service')

For Langfuse backend:
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_HOST` (optional)

## API Reference

### Decorators

#### `@trace(name=None, **kwargs)`

Decorator for automatic function tracing.

```python
@trace(name="custom_name", tags=["tag1", "tag2"])
def my_function():
    pass
```

### Context Managers

#### `start_span(context, **kwargs)`

Start a new trace span.

```python
with start_span("operation_name", tags=["tag1"]) as span:
    result = operation()
    span.update(output=result)
```

#### `start_generation(name, model, **kwargs)`

Start a new LLM generation span.

```python
with start_generation("text_gen", model="gpt-4") as span:
    response = llm.generate("prompt")
    span.update(output=response)
```

### Utility Functions

#### `flush()`

Manually flush traces to the backend.

```python
from sgai_evaluator import flush

# After operations
flush()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 