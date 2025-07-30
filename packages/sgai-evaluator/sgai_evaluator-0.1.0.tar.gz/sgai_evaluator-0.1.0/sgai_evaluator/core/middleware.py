"""
Universal Tracing Middleware for Agentic Setups
===============================================

This module provides a framework-agnostic tracing interface that can work with
any tracing backend (Langfuse, OpenTelemetry, etc.) through a simple adapter pattern.
It also supports native framework integrations when available.
"""

import os
import importlib
from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Dict, Any, Callable, Union
from contextlib import contextmanager
import asyncio
from dataclasses import dataclass

# Default to Langfuse, but allow other implementations
DEFAULT_TRACER = os.getenv('SGAI_TRACER', 'langfuse')

def _setup_native_integration():
    """
    Attempts to detect and configure native framework integrations.
    Returns True if a native integration was configured.
    """
    try:
        # Try OpenAI Agents SDK integration
        if importlib.util.find_spec("agents"):
            import logfire
            logfire.configure(
                service_name=os.getenv('SGAI_SERVICE_NAME', 'agent_service'),
                send_to_logfire=False
            )
            logfire.instrument_openai_agents()
            return True
            
        # Try Google ADK integration
        if importlib.util.find_spec("google.adk"):
            from langfuse import get_client
            client = get_client()
            if client.auth_check():
                return True
                
        # Try CrewAI integration
        if importlib.util.find_spec("crewai"):
            from langfuse.crewai import CrewAIInstrumentation
            CrewAIInstrumentation.setup()
            return True
            
        # Try LangChain integration
        if importlib.util.find_spec("langchain"):
            from langfuse.langchain import LangchainInstrumentation
            LangchainInstrumentation.setup()
            return True
            
    except Exception as e:
        print(f"Warning: Framework detection failed: {e}")
        
    return False

# Try to set up native integration
USING_NATIVE_INTEGRATION = _setup_native_integration()

@dataclass
class SpanContext:
    """
    Context for a trace span
    
    Args:
        name: Name of the span
        input: Optional input data to record
        metadata: Optional metadata to attach
        user_id: Optional user identifier
        session_id: Optional session identifier
        tags: Optional list of tags
    """
    name: str
    input: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    tags: Optional[list] = None

class TracingBackend(ABC):
    """Abstract base class for tracing backends"""
    
    @abstractmethod
    def start_span(self, context: SpanContext) -> Any:
        """Start a new span"""
        pass
        
    @abstractmethod
    def end_span(self, span: Any, output: Optional[Any] = None):
        """End a span"""
        pass
        
    @abstractmethod
    def update_span(self, span: Any, **kwargs):
        """Update span data"""
        pass
        
    @abstractmethod
    def start_generation(self, context: SpanContext, model: str, **kwargs) -> Any:
        """Start an LLM generation span"""
        pass
        
    @abstractmethod
    def flush(self):
        """Flush traces to backend"""
        pass

class LangfuseBackend(TracingBackend):
    """Langfuse implementation of tracing backend"""
    
    def __init__(self):
        try:
            from langfuse import Langfuse
            self.client = Langfuse()
        except ImportError:
            raise ImportError(
                "Langfuse package is required for LangfuseBackend. "
                "Install it with: pip install langfuse"
            )
    
    def trace(self, name: Optional[str] = None, **kwargs):
        """
        A decorator that uses Langfuse's @observe for automatic tracing.
        
        Args:
            name: Optional name for the trace/span. If not provided, uses function name.
            **kwargs: Additional keyword arguments passed to observe.
            
        Returns:
            Decorated function with tracing enabled.
        """
        from langfuse import observe
        
        def decorator(func):
            # Use Langfuse's built-in observe decorator
            traced_func = observe(name=name or func.__name__, **kwargs)(func)
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await traced_func(*args, **kwargs)
                
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return traced_func(*args, **kwargs)
                
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
        
    def start_span(self, context: SpanContext) -> Any:
        if USING_NATIVE_INTEGRATION:
            # When using native integration, we don't need to create spans
            return None
            
        return self.client.start_as_current_span(
            name=context.name,
            input=context.input,
            metadata=context.metadata,
            user_id=context.user_id,
            session_id=context.session_id,
            tags=context.tags
        )
        
    def end_span(self, span: Any, output: Optional[Any] = None):
        if USING_NATIVE_INTEGRATION or not span:
            return
            
        if output is not None:
            span.update(output=output)
        span.end()
        
    def update_span(self, span: Any, **kwargs):
        if USING_NATIVE_INTEGRATION or not span:
            return
            
        span.update(**kwargs)
        
    def start_generation(self, context: SpanContext, model: str, **kwargs) -> Any:
        if USING_NATIVE_INTEGRATION:
            # When using native integration, we don't need to create spans
            return None
            
        return self.client.start_as_current_generation(
            name=context.name,
            model=model,
            input=context.input,
            metadata=context.metadata,
            user_id=context.user_id,
            session_id=context.session_id,
            tags=context.tags,
            **kwargs
        )
        
    def flush(self):
        self.client.flush()

# Factory function to get the configured backend
def get_tracer() -> TracingBackend:
    """Get the configured tracing backend"""
    if DEFAULT_TRACER == 'langfuse':
        return LangfuseBackend()
    # Add more backends here as needed
    raise ValueError(f"Unknown tracing backend: {DEFAULT_TRACER}")

# Global tracer instance
_tracer = get_tracer()

def trace(name: Optional[str] = None, **kwargs):
    """
    A decorator that provides automatic tracing, independent of the backend.
    This will create custom spans even if native integration is present.
    WARNING: You may get duplicate traces if both native and custom spans are used for the same function.
    
    Args:
        name: Optional name for the trace/span. If not provided, uses function name.
        **kwargs: Additional keyword arguments passed to the span context.
        
    Returns:
        Decorated function with tracing enabled.
    """
    # If using Langfuse, delegate to its observe decorator for better integration
    if DEFAULT_TRACER == 'langfuse':
        return _tracer.trace(name, **kwargs)
        
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **func_kwargs):
            context = SpanContext(
                name=name or func.__name__,
                input={"args": args, "kwargs": func_kwargs},
                **kwargs
            )
            
            with start_span(context) as span:
                try:
                    result = await func(*args, **func_kwargs)
                    if span:
                        _tracer.update_span(span, output=result)
                    return result
                except Exception as e:
                    if span:
                        _tracer.update_span(span, error=str(e))
                    raise
                    
        @wraps(func)
        def sync_wrapper(*args, **func_kwargs):
            context = SpanContext(
                name=name or func.__name__,
                input={"args": args, "kwargs": func_kwargs},
                **kwargs
            )
            
            with start_span(context) as span:
                try:
                    result = func(*args, **func_kwargs)
                    if span:
                        _tracer.update_span(span, output=result)
                    return result
                except Exception as e:
                    if span:
                        _tracer.update_span(span, error=str(e))
                    raise
                    
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

@contextmanager
def start_span(context: Union[str, SpanContext], **kwargs):
    """
    Start a new span using the configured backend.
    This will create custom spans even if native integration is present.
    WARNING: You may get duplicate traces if both native and custom spans are used for the same function.
    
    Args:
        context: Either a string name for the span or a SpanContext object
        **kwargs: Additional keyword arguments for the span context if using string name
        
    Yields:
        The created span object
    """
    if isinstance(context, str):
        context = SpanContext(name=context, **kwargs)
        
    span = _tracer.start_span(context)
    try:
        yield span
    finally:
        _tracer.end_span(span)

@contextmanager
def start_generation(name: str, model: str, **kwargs):
    """
    Start a new generation span using the configured backend.
    This will create custom spans even if native integration is present.
    WARNING: You may get duplicate traces if both native and custom spans are used for the same function.
    
    Args:
        name: Name for the generation span
        model: Name/identifier of the model being used
        **kwargs: Additional keyword arguments for the span context
        
    Yields:
        The created generation span object
    """
    context = SpanContext(name=name, **kwargs)
    span = _tracer.start_generation(context, model, **kwargs)
    try:
        yield span
    finally:
        _tracer.end_span(span)

def flush():
    """Flush traces to the configured backend."""
    _tracer.flush() 