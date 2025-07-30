# SGAI Evaluator TypeScript Middleware

A universal tracing middleware for agent applications with support for multiple tracing backends. This package provides automatic tracing setup - just import it and it works! This is the TypeScript implementation of the SGAI Evaluator middleware, providing a framework-agnostic tracing interface that can work with various tracing backends (Langfuse, OpenTelemetry, etc.) through a simple adapter pattern.

## **Features**

🔄 Zero-configuration setup - just import and go!

🤖 Automatic framework detection and integration

  * OpenAI Agents SDK
  * Google ADK
  * CrewAI
  * LangChain

🎯 Manual instrumentation if needed

🔌 Extensible backend system

🚀 Async/sync support

## Installation

```bash
npm install @stackgen-ai/sgai-evaluator
```

## Usage

### Basic Usage

```typescript
import { trace, startSpan, startGeneration } from '@stackgen-ai/sgai-evaluator';

// Using the decorator
@trace('myFunction')
async function myFunction() {
  // Your code here
}

// Using span context manager
async function example() {
  const span = startSpan('operation-name');
  try {
    const result = await someOperation();
    span.exit();
    return result;
  } catch (error) {
    span.exit(error);
    throw error;
  }
}

// Using generation context manager for LLM calls
async function llmExample() {
  const gen = startGeneration('llm-call', 'gpt-4');
  try {
    const result = await llmOperation();
    gen.exit();
    return result;
  } catch (error) {
    gen.exit(error);
    throw error;
  }
}
```

### Configuration

The middleware can be configured through environment variables:

```bash
# Choose the tracing backend (defaults to 'langfuse')
SGAI_TRACER=langfuse

# For Langfuse configuration
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com  # Optional
```

### Framework Integrations

The middleware automatically detects and instruments the following frameworks:

- OpenAI SDK
- LangChain.js
- Vercel AI SDK
- BeeAI
- Mastra
- MCP

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test

# Lint
npm run lint
```

## License

Same as the parent project 