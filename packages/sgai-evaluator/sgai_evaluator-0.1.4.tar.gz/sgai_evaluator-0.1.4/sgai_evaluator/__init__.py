"""
SGAI Evaluator
=============

A universal tracing middleware for agent applications with support for multiple tracing backends.
Just import this package and it will automatically set up tracing.
"""

from .core.middleware import (
    trace,
    start_span,
    start_generation,
    flush,
    TracingBackend,
    SpanContext,
    get_tracer,
    _setup_native_integration
)

__version__ = "0.1.0"

# Automatically set up native integration when the package is imported
USING_NATIVE_INTEGRATION = _setup_native_integration()

__all__ = [
    'trace',
    'start_span',
    'start_generation',
    'flush',
    'TracingBackend',
    'SpanContext',
    'get_tracer'
] 