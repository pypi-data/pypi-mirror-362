"""
SGAI Evaluator
=============

A universal tracing middleware for agent applications with support for multiple tracing backends.
"""

from .core.middleware import (
    trace,
    start_span,
    start_generation,
    flush,
    TracingBackend,
    SpanContext,
    get_tracer
)

__version__ = "0.1.0"
__all__ = [
    'trace',
    'start_span',
    'start_generation',
    'flush',
    'TracingBackend',
    'SpanContext',
    'get_tracer'
] 