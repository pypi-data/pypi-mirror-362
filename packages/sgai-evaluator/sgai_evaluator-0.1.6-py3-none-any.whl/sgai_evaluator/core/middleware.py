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

# Global agent name
_AGENT_NAME = None

def set_agent_name(name: str):
    """Set the agent name that will be used to tag all traces."""
    global _AGENT_NAME
    _AGENT_NAME = name

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

        # Try Agno integration
        if importlib.util.find_spec("agno"):
            from openinference.instrumentation.agno import AgnoInstrumentor
            AgnoInstrumentor().instrument()
            return True

        # Try OpenAI SDK integration
        if importlib.util.find_spec("openai"):
            from openinference.instrumentation.openai import OpenAIInstrumentor
            OpenAIInstrumentor().instrument()
            return True

        # Try LlamaIndex integration
        if importlib.util.find_spec("llama_index"):
            from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
            LlamaIndexInstrumentor().instrument()
            return True

        # Try DSPy integration
        if importlib.util.find_spec("dspy"):
            from openinference.instrumentation.dspy import DSPyInstrumentor
            DSPyInstrumentor().instrument()
            return True

        # Try AWS Bedrock integration
        if importlib.util.find_spec("boto3"):
            from openinference.instrumentation.bedrock import BedrockInstrumentor
            BedrockInstrumentor().instrument()
            return True

        # Try MCP integration
        if importlib.util.find_spec("mcp"):
            from openinference.instrumentation.mcp import MCPInstrumentor
            MCPInstrumentor().instrument()
            return True

        # Try MistralAI integration
        if importlib.util.find_spec("mistralai"):
            from openinference.instrumentation.mistralai import MistralAIInstrumentor
            MistralAIInstrumentor().instrument()
            return True

        # Try Portkey integration
        if importlib.util.find_spec("portkey"):
            from openinference.instrumentation.portkey import PortkeyInstrumentor
            PortkeyInstrumentor().instrument()
            return True

        # Try Guardrails integration
        if importlib.util.find_spec("guardrails"):
            from openinference.instrumentation.guardrails import GuardrailsInstrumentor
            GuardrailsInstrumentor().instrument()
            return True

        # Try VertexAI integration
        if importlib.util.find_spec("vertexai"):
            from openinference.instrumentation.vertexai import VertexAIInstrumentor
            VertexAIInstrumentor().instrument()
            return True

        # Try Haystack integration
        if importlib.util.find_spec("haystack"):
            from openinference.instrumentation.haystack import HaystackInstrumentor
            HaystackInstrumentor().instrument()
            return True

        # Try liteLLM integration
        if importlib.util.find_spec("litellm"):
            from openinference.instrumentation.litellm import LiteLLMInstrumentor
            LiteLLMInstrumentor().instrument()
            return True

        # Try Groq integration
        if importlib.util.find_spec("groq"):
            from openinference.instrumentation.groq import GroqInstrumentor
            GroqInstrumentor().instrument()
            return True

        # Try Instructor integration
        if importlib.util.find_spec("instructor"):
            from openinference.instrumentation.instructor import InstructorInstrumentor
            InstructorInstrumentor().instrument()
            return True

        # Try Anthropic integration
        if importlib.util.find_spec("anthropic"):
            from openinference.instrumentation.anthropic import AnthropicInstrumentor
            AnthropicInstrumentor().instrument()
            return True

        # Try BeeAI integration
        if importlib.util.find_spec("beeai"):
            from openinference.instrumentation.beeai import BeeAIInstrumentor
            BeeAIInstrumentor().instrument()
            return True

        # Try Google GenAI integration
        if importlib.util.find_spec("google.generativeai"):
            from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor
            GoogleGenAIInstrumentor().instrument()
            return True

        # Try Autogen AgentChat integration
        if importlib.util.find_spec("autogen"):
            from openinference.instrumentation.autogen_agentchat import AutogenAgentChatInstrumentor
            AutogenAgentChatInstrumentor().instrument()
            return True

        # Try PydanticAI integration
        if importlib.util.find_spec("pydantic_ai"):
            from openinference.instrumentation.pydantic_ai import PydanticAIInstrumentor
            PydanticAIInstrumentor().instrument()
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
            Decorated function that creates a trace.
        """
        from langfuse.decorators import observe
        
        def decorator(func):
            # Use Langfuse's built-in observe decorator
            base_decorator = observe(name=name, **kwargs)
            decorated_func = base_decorator(func)
            
            @wraps(func)
            async def async_wrapper(*args, **func_kwargs):
                result = await decorated_func(*args, **func_kwargs)
                # Add agent name tag if set
                if _AGENT_NAME:
                    self.client.update_current_trace(tags=[_AGENT_NAME])
                return result
                
            @wraps(func)
            def sync_wrapper(*args, **func_kwargs):
                result = decorated_func(*args, **func_kwargs)
                # Add agent name tag if set
                if _AGENT_NAME:
                    self.client.update_current_trace(tags=[_AGENT_NAME])
                return result
                
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper
            
        return decorator
    
    def start_span(self, context: SpanContext) -> Any:
        """Start a new span"""
        if isinstance(context, str):
            context = SpanContext(name=context)
            
        # Add agent name to tags if set
        if _AGENT_NAME:
            if context.tags:
                context.tags.append(_AGENT_NAME)
            else:
                context.tags = [_AGENT_NAME]
                
        span = self.client.start_span(
            name=context.name,
            input=context.input,
            metadata=context.metadata,
            user_id=context.user_id,
            session_id=context.session_id,
            tags=context.tags
        )
        return span
        
    def end_span(self, span: Any, output: Optional[Any] = None):
        """End a span"""
        span.end(output=output)
        
    def update_span(self, span: Any, **kwargs):
        """Update span data"""
        span.update(**kwargs)
        
    def start_generation(self, context: SpanContext, model: str, **kwargs) -> Any:
        """Start an LLM generation span"""
        if isinstance(context, str):
            context = SpanContext(name=context)
            
        # Add agent name to tags if set
        if _AGENT_NAME:
            if context.tags:
                context.tags.append(_AGENT_NAME)
            else:
                context.tags = [_AGENT_NAME]
                
        gen = self.client.start_generation(
            name=context.name,
            model=model,
            input=context.input,
            metadata=context.metadata,
            user_id=context.user_id,
            session_id=context.session_id,
            tags=context.tags,
            **kwargs
        )
        return gen
        
    def flush(self):
        """Flush traces to backend"""
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