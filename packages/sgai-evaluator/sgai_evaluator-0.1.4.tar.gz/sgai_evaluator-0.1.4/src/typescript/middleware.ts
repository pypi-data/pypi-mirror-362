/**
 * Universal Tracing Middleware for Agentic Setups
 * =============================================
 * 
 * This module provides a framework-agnostic tracing interface that can work with
 * any tracing backend (Langfuse, OpenTelemetry, etc.) through a simple adapter pattern.
 * It also supports native framework integrations when available.
 */

import { Langfuse } from 'langfuse';

// Default to Langfuse, but allow other implementations
const DEFAULT_TRACER = process.env.SGAI_TRACER || 'langfuse';

interface SpanContext {
  name: string;
  input?: any;
  metadata?: Record<string, any>;
  userId?: string;
  sessionId?: string;
  tags?: string[];
}

interface TracingBackend {
  startSpan(context: SpanContext): any;
  endSpan(span: any, output?: any): void;
  updateSpan(span: any, data: Record<string, any>): void;
  startGeneration(context: SpanContext, model: string, options?: Record<string, any>): any;
  flush(): Promise<void>;
}

async function setupNativeIntegration(): Promise<boolean> {
  try {
    // Try OpenAI SDK integration
    if (await import('openai')) {
      const { OpenAIInstrumentor } = await import('@openinference/instrumentation-openai');
      new OpenAIInstrumentor().instrument();
      return true;
    }

    // Try LangChain.js integration
    if (await import('langchain')) {
      const { LangchainInstrumentation } = await import('@langfuse/langchain');
      LangchainInstrumentation.setup();
      return true;
    }

    // Try Vercel AI SDK integration
    if (await import('@vercel/ai')) {
      const { VercelInstrumentor } = await import('@openinference/instrumentation-vercel');
      new VercelInstrumentor().instrument();
      return true;
    }

    // Try BeeAI integration
    if (await import('beeai')) {
      const { BeeAIInstrumentor } = await import('@openinference/instrumentation-beeai');
      new BeeAIInstrumentor().instrument();
      return true;
    }

    // Try Mastra integration
    if (await import('mastra')) {
      const { MastraInstrumentor } = await import('@openinference/instrumentation-mastra');
      new MastraInstrumentor().instrument();
      return true;
    }

    // Try MCP integration
    if (await import('mcp')) {
      const { MCPInstrumentor } = await import('@openinference/instrumentation-mcp');
      new MCPInstrumentor().instrument();
      return true;
    }

  } catch (e) {
    console.warn(`Warning: Framework detection failed: ${e}`);
  }

  return false;
}

class LangfuseBackend implements TracingBackend {
  private client: Langfuse;

  constructor() {
    this.client = new Langfuse();
  }

  startSpan(context: SpanContext) {
    const trace = this.client.trace({
      name: context.name,
      userId: context.userId,
      sessionId: context.sessionId,
      tags: context.tags,
      metadata: context.metadata
    });

    const span = trace.span({
      name: context.name,
      input: context.input
    });

    return { trace, span };
  }

  endSpan(span: any, output?: any) {
    if (output !== undefined) {
      span.span.end({ output });
    } else {
      span.span.end();
    }
  }

  updateSpan(span: any, data: Record<string, any>) {
    span.span.update(data);
  }

  startGeneration(context: SpanContext, model: string, options: Record<string, any> = {}) {
    const trace = this.client.trace({
      name: context.name,
      userId: context.userId,
      sessionId: context.sessionId,
      tags: context.tags,
      metadata: context.metadata
    });

    const generation = trace.generation({
      name: context.name,
      model,
      input: context.input,
      ...options
    });

    return { trace, generation };
  }

  async flush(): Promise<void> {
    await this.client.flush();
  }
}

// Initialize native integration
let USING_NATIVE_INTEGRATION = false;
setupNativeIntegration().then(result => {
  USING_NATIVE_INTEGRATION = result;
});

// Singleton tracer instance
let tracer: TracingBackend | null = null;

function getTracer(): TracingBackend {
  if (!tracer) {
    if (DEFAULT_TRACER === 'langfuse') {
      tracer = new LangfuseBackend();
    } else {
      throw new Error(`Unsupported tracer type: ${DEFAULT_TRACER}`);
    }
  }
  return tracer;
}

// Decorator factory for tracing
function trace(name?: string, options: Record<string, any> = {}) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const isAsync = originalMethod.constructor.name === 'AsyncFunction';

    if (isAsync) {
      descriptor.value = async function (...args: any[]) {
        const spanName = name || propertyKey;
        const span = getTracer().startSpan({ name: spanName, ...options });

        try {
          const result = await originalMethod.apply(this, args);
          getTracer().endSpan(span, result);
          return result;
        } catch (error) {
          getTracer().updateSpan(span, { error: error.message });
          getTracer().endSpan(span);
          throw error;
        }
      };
    } else {
      descriptor.value = function (...args: any[]) {
        const spanName = name || propertyKey;
        const span = getTracer().startSpan({ name: spanName, ...options });

        try {
          const result = originalMethod.apply(this, args);
          getTracer().endSpan(span, result);
          return result;
        } catch (error) {
          getTracer().updateSpan(span, { error: error.message });
          getTracer().endSpan(span);
          throw error;
        }
      };
    }

    return descriptor;
  };
}

// Context manager for spans
class SpanManager {
  private span: any;

  constructor(context: SpanContext | string, options: Record<string, any> = {}) {
    const spanContext = typeof context === 'string' 
      ? { name: context, ...options }
      : { ...context, ...options };
    this.span = getTracer().startSpan(spanContext);
  }

  enter() {
    return this.span;
  }

  exit(err?: Error) {
    if (err) {
      getTracer().updateSpan(this.span, { error: err.message });
    }
    getTracer().endSpan(this.span);
  }
}

// Context manager for generations
class GenerationManager {
  private generation: any;

  constructor(name: string, model: string, options: Record<string, any> = {}) {
    this.generation = getTracer().startGeneration({ name }, model, options);
  }

  enter() {
    return this.generation;
  }

  exit(err?: Error) {
    if (err) {
      getTracer().updateSpan(this.generation, { error: err.message });
    }
    getTracer().endSpan(this.generation);
  }
}

// Helper function to create a span context manager
function startSpan(context: SpanContext | string, options: Record<string, any> = {}) {
  return new SpanManager(context, options);
}

// Helper function to create a generation context manager
function startGeneration(name: string, model: string, options: Record<string, any> = {}) {
  return new GenerationManager(name, model, options);
}

// Helper function to flush traces
async function flush(): Promise<void> {
  await getTracer().flush();
}

export {
  trace,
  startSpan,
  startGeneration,
  flush,
  SpanContext,
  TracingBackend,
  LangfuseBackend,
  getTracer
}; 