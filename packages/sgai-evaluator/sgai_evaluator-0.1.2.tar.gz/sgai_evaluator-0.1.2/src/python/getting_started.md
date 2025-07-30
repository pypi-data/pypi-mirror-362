# Universal Tracing Middleware for Agent Observability

This guide explains how to add comprehensive observability to your agents using Langfuse's tracing capabilities. The middleware provides both high-level decorators for simple use cases and lower-level functions for more control, as well as automatic framework integration detection.

## New: Combine Native Integration and Custom Spans

**The middleware now allows you to use both native integration and custom spans/decorators at the same time.**
- Native integration will automatically trace supported frameworks (OpenAI Agents, Google ADK, LangChain, CrewAI, etc.).
- You can supplement this with your own custom spans and attributes using the `@trace` decorator and context managers, even when native integration is active.
- **Warning:** If you use both for the same function, you may see duplicate traces/spans in Langfuse.

---

## Quick Start: Add Tracing to Your Project

### 1. With Native Integration Only (Automatic Tracing)

Just import the middleware early in your project. The middleware will detect supported frameworks and enable native tracing automatically.

```python
# .env file
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
LANGFUSE_HOST=http://xxxxxx

# Import the middleware to initialize framework detection
import middleware

# Use your framework as normal (e.g., OpenAI Agents, Google ADK, LangChain, CrewAI)
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

result = await Runner.run(agent, "Tell me about middleware.")
print(result.final_output)
```

---

### 2. With Custom Spans/Decorators (Supplement Native Integration)

You can add custom spans and attributes to any function or code block, even if native integration is active.

```python
from middleware import trace, start_span, start_generation, flush

class MyAgent:
    @trace(name="custom_process_query")
    async def process_query(self, query: str) -> str:
        # This will create a custom span in addition to any native tracing
        return "Processed: " + query

    async def advanced_method(self, query: str):
        # Manual span for more control
        with start_span(name="manual_span_example") as span:
            span.update(metadata={"custom": "value"})
            # Nested generation span for LLM call
            with start_generation(name="llm_call", model="gpt-4") as gen:
                response = await self.llm_call(query)
                gen.update(output=response)
            return response

# Don't forget to flush in short-lived applications
flush()
```

---

## When to Use Each Approach

- **Native Integration:**
  - Use when you want automatic, framework-level tracing with minimal code changes.
  - Just import the middleware and use your framework as normal.

- **Custom Spans/Decorators:**
  - Use when you want to trace custom business logic, add extra attributes, or instrument code outside of the supported frameworks.
  - You can use `@trace`, `start_span`, and `start_generation` anywhere in your code, even if native integration is active.
  - **Warning:** If you use both for the same function, you may see duplicate traces/spans in Langfuse.

---

## Example: Combining Both Approaches

You can mix and match approaches based on your needs:

```python
from middleware import trace, start_generation

class HybridAgent:
    @trace(name="handle_query")
    async def handle_query(self, query: str) -> str:
        # Method is traced via decorator (custom span)
        # Native integration may also trace this if using a supported framework
        with start_generation(
            name="generate_response",
            model="gpt-4"
        ) as generation:
            response = await self.llm.generate(query)
            generation.update(
                output=response,
                metadata={"tokens": len(response)}
            )
        return response
```

---

## Best Practices

- Set up proper environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`)
- Import the middleware module early in your application startup
- Use native integration for automatic tracing of supported frameworks
- Use custom spans/decorators for business logic, extra attributes, or code outside supported frameworks
- Always call `flush()` in short-lived applications
- Use meaningful names for spans and add relevant metadata for debugging
- Be aware of possible duplicate traces if you use both native and custom tracing for the same function

---

## Troubleshooting

- If you see duplicate traces, check if both native and custom tracing are applied to the same function.
- Only use parameters supported by Langfuse's `observe` decorator in `@trace`.
- If you need to add custom metadata during execution, use the context manager approach (`start_span`, `start_generation`).
- If you get import errors, check your package structure and Python path.

---

## Running the Example

For a complete example showing both approaches, see `examples/python/agent_example.py`.

1. **Set up environment**:
   ```bash
   pip install -r requirements.txt
   # Set up Langfuse credentials in .env
   LANGFUSE_PUBLIC_KEY=your_key
   LANGFUSE_SECRET_KEY=your_secret
   LANGFUSE_HOST=your_host  # Optional
   ```
2. **Run the example**:
   ```bash
   python examples/python/agent_example.py
   ```
3. **Check Langfuse UI** to see your traces! 