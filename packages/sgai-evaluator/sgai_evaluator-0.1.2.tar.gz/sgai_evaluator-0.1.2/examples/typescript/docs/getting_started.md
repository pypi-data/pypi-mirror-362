# Universal Tracing Middleware for Agent Observability (TypeScript)

This guide explains how to add comprehensive observability to your TypeScript agents using Langfuse's tracing capabilities. The middleware provides both method decorators for simple use cases, helper functions for more control, and automatic framework integration detection.

## Installation

```bash
# Install dependencies
npm install langfuse dotenv
npm install --save-dev @types/node

# For Node.js < 18
npm install langfuse-node
```

## Native Framework Integration

Our middleware automatically detects and configures native Langfuse integrations for popular frameworks. This means minimal Langfuse-specific code in your agent implementations!

```bash
# .env file
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_secret
FRAMEWORK=vercel-ai  # Specify which framework you're using
```

```typescript
// Important: Import the middleware to initialize framework detection
import './middleware';
```

### Supported Frameworks

The middleware automatically configures:

- **Vercel AI SDK**: Import the middleware and use the SDK normally
- **LangChain.js**: Import the middleware for automatic tracing of chains and agents
- **Semantic Kernel**: Import the middleware for automatic tracing of kernel operations

Example with Vercel AI SDK:

```typescript
// Import middleware to initialize framework detection
import './middleware';

// Then use your framework as normal
import { StreamingTextResponse, Message } from 'ai';
import { OpenAI } from 'openai';

const openai = new OpenAI();

export async function POST(req: Request) {
  const { messages } = await req.json();
  
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    stream: true,
    messages
  });
  
  // Tracing happens automatically!
  return new StreamingTextResponse(response.body);
}
```

### Manual Framework Selection

Set the `FRAMEWORK` environment variable to enable native integration:

```bash
# .env file
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_secret
FRAMEWORK=vercel-ai  # or langchain, semantic-kernel, etc.
```

```typescript
// Import middleware to initialize framework detection
import './middleware';
```

## Quick Start: Using the @trace Decorator

For frameworks without native integration or for custom tracing needs, use the `@trace` decorator. This automatically captures:
- Method inputs and outputs
- Execution time
- Nested call hierarchy
- Error handling

```typescript
import { trace, flush } from './middleware';

class MyAgent {
  @trace()
  async processQuery(query: string): Promise<string> {
    return `Processed: ${query}`;
  }

  @trace('custom-name', {
    tags: ['customer-support'],
    userId: 'user123',
    metadata: { source: 'chat' }
  })
  async anotherMethod(): Promise<string> {
    // This will be a child span of the parent trace
    const result = await this.processQuery('test');
    return result;
  }
}

// Don't forget to flush in short-lived applications
await flush();
```

## Advanced Usage: Spans and Generations

For more control over your traces, use the span and generation helpers. This is especially useful when you need to:
- Add custom metadata during execution
- Create specific types of spans (e.g., generations for LLM calls)
- Track usage and costs
- Handle complex async operations

```typescript
import { startSpan, startGeneration } from './middleware';

class AdvancedAgent {
  async handleQuery(query: string, userId: string): Promise<string> {
    // Create a span for the query processing
    const span = startSpan('process-query', {
      input: { query },
      metadata: { userId },
      tags: ['processing']
    });

    return await span.execute(async () => {
      // Create a nested generation for LLM call
      const generation = startGeneration(
        'generate-response',
        'gpt-4',
        {
          modelParameters: {
            temperature: 0.7,
            maxTokens: 2000
          },
          metadata: {
            source: 'customer-support'
          }
        }
      );

      const response = await generation.execute(async () => {
        // Your LLM call here
        const completion = await openai.chat.completions.create({
          model: 'gpt-4',
          messages: [{ role: 'user', content: query }]
        });

        return completion.choices[0].message.content;
      });

      return response;
    });
  }
}
```

## Choosing the Right Approach

1. **Use Native Framework Integration when**:
   - You're using a supported framework (Vercel AI SDK, LangChain.js, etc.)
   - You want minimal Langfuse-specific code in your agent implementation
   - You want the most optimized tracing experience
   - **Remember**: You still need to `import './middleware'` to initialize the framework detection

2. **Use @trace when**:
   - You want automatic input/output capture
   - Your tracing needs are straightforward
   - You prefer clean, decorator-based code
   - You want to track method-level metrics

3. **Use Spans and Generations when**:
   - You need to add custom metadata during execution
   - You're making LLM calls (use startGeneration)
   - You want to track usage and costs
   - You need to handle complex async operations

## Available Functions

| Function | Description |
|----------|-------------|
| `import './middleware'` | Initializes framework detection and integration |
| `@trace()` | Method decorator for automatic tracing |
| `startSpan()` | Creates a new span with execution context |
| `startGeneration()` | Creates a span for LLM calls with cost tracking |
| `flush()` | Ensures all traces are sent to Langfuse |

## Example: Combining Both Approaches

You can mix and match approaches based on your needs:

```typescript
import { trace, startGeneration } from './middleware';

class HybridAgent {
  @trace('handle-query', {
    tags: ['customer-support'],
    metadata: { source: 'chat' }
  })
  async handleQuery(query: string): Promise<string> {
    // Method is traced via decorator
    
    // Use generation for LLM call with cost tracking
    const generation = startGeneration(
      'generate-response',
      'gpt-4',
      {
        modelParameters: {
          temperature: 0.7
        },
        metadata: {
          source: 'customer-support'
        }
      }
    );

    const response = await generation.execute(async () => {
      const completion = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: query }]
      });

      return completion.choices[0].message.content;
    });

    return response;
  }
}
```

## Best Practices

1. **Framework Integration Best Practices**:
   - Set up proper environment variables (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)
   - Import the middleware module early in your application startup
   - Specify your framework with the FRAMEWORK environment variable
   - Minimal Langfuse-specific code in your agent implementation

2. **Decorator (@trace) Best Practices**:
   - Use meaningful trace names
   - Add relevant tags for filtering
   - Include user and session IDs when available
   - Add metadata for debugging context

3. **Span and Generation Best Practices**:
   - Always use startGeneration for LLM calls
   - Track usage and costs for better monitoring
   - Add relevant metadata during execution
   - Keep span hierarchy logical

4. **General Tips**:
   - Initialize Langfuse once and reuse the instance
   - Always await flush() in serverless environments
   - Add proper error handling
   - Use meaningful names and tags

## Environment Setup

1. **Set up environment variables**:
   ```bash
   # .env file
   LANGFUSE_PUBLIC_KEY=your_key
   LANGFUSE_SECRET_KEY=your_secret
   LANGFUSE_HOST=your_host  # Optional
   LANGFUSE_RELEASE=1.0.0   # Optional
   FRAMEWORK=vercel-ai      # Optional, for native integration
   ```

2. **Import middleware**:
   ```typescript
   // Import middleware early in your application
   import './middleware';
   ```

3. **Run the example**:
   ```bash
   ts-node examples/typescript/langfuse-integration.ts
   ```

4. **Check Langfuse UI** to see your traces with:
   - Proper hierarchy
   - Cost tracking
   - Usage metrics
   - Custom metadata 