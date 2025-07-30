// @ts-check
/**
 * Universal Tracing Middleware for Agentic Setups
 * =============================================
 * 
 * This module provides a framework-agnostic tracing interface that can work with
 * any tracing backend (Langfuse, OpenTelemetry, etc.) through a simple adapter pattern.
 * It also supports native framework integrations when available.
 */

import { Langfuse } from 'langfuse';
import dotenv from 'dotenv';

// Type declarations for process.env
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      LANGFUSE_PUBLIC_KEY?: string;
      LANGFUSE_SECRET_KEY?: string;
      LANGFUSE_HOST?: string;
      LANGFUSE_RELEASE?: string;
      TRACING_BACKEND?: string;
      SERVICE_NAME?: string;
      FRAMEWORK?: string;
    }
  }
}

dotenv.config();

// Default to Langfuse, but allow other implementations
const DEFAULT_TRACER = process.env.TRACING_BACKEND || 'langfuse';

/**
 * Attempts to detect and configure native framework integrations.
 * Returns true if a native integration was configured.
 */
async function setupNativeIntegration(): Promise<boolean> {
  // Check if a specific framework is configured
  const framework = process.env.FRAMEWORK?.toLowerCase();
  
  if (!framework) {
    return false;
  }

  try {
    // Initialize Langfuse client for native integration
    const client = new Langfuse({
      publicKey: process.env.LANGFUSE_PUBLIC_KEY,
      secretKey: process.env.LANGFUSE_SECRET_KEY,
      baseUrl: process.env.LANGFUSE_HOST || 'https://cloud.langfuse.com'
    });

    // Verify credentials are provided
    if (!process.env.LANGFUSE_PUBLIC_KEY || !process.env.LANGFUSE_SECRET_KEY) {
      console.warn('Langfuse credentials not provided');
      return false;
    }

    console.log(`Native ${framework} integration enabled`);
    return true;

  } catch (e) {
    console.warn('Framework detection failed:', e);
    return false;
  }
}

// Try to set up native integration
let USING_NATIVE_INTEGRATION = false;
setupNativeIntegration().then(result => {
  USING_NATIVE_INTEGRATION = result;
});

// Core types for tracing
interface SpanContext {
  name: string;
  input?: any;
  metadata?: Record<string, any>;
  userId?: string;
  sessionId?: string;
  tags?: string[];
}

interface GenerationContext extends SpanContext {
  model: string;
  modelParameters?: Record<string, any>;
}

interface Span {
  update(data: Record<string, any>): void;
  end(): void;
}

// Abstract tracing backend interface
abstract class TracingBackend {
  abstract startSpan(context: SpanContext): Span;
  abstract startGeneration(context: GenerationContext): Span;
  abstract flush(): Promise<void>;
}

// Langfuse implementation
class LangfuseBackend extends TracingBackend {
  private client: Langfuse;

  constructor() {
    super();
    this.client = new Langfuse({
      publicKey: process.env.LANGFUSE_PUBLIC_KEY,
      secretKey: process.env.LANGFUSE_SECRET_KEY,
      baseUrl: process.env.LANGFUSE_HOST || 'https://cloud.langfuse.com',
      release: process.env.LANGFUSE_RELEASE || '1.0.0',
      requestTimeout: 10000,
      enabled: true
    });

    this.client.on("error", (error: unknown) => {
      if (error instanceof Error) {
        console.error("Langfuse error:", error.message);
      } else {
        console.error("Langfuse error:", String(error));
      }
    });
  }

  startSpan(context: SpanContext): Span {
    if (USING_NATIVE_INTEGRATION) {
      // When using native integration, return a no-op span
      return {
        update: () => {},
        end: () => {}
      };
    }

    const trace = this.client.trace({
      name: context.name,
      input: context.input,
      metadata: context.metadata,
      userId: context.userId,
      sessionId: context.sessionId,
      tags: context.tags
    });

    return {
      update: (data: Record<string, any>) => {
        if (trace) {
          trace.update(data);
        }
      },
      end: () => {
        if (trace) {
          trace.update({
            metadata: { status: 'completed' }
          });
        }
      }
    };
  }

  startGeneration(context: GenerationContext): Span {
    if (USING_NATIVE_INTEGRATION) {
      // When using native integration, return a no-op span
      return {
        update: () => {},
        end: () => {}
      };
    }

    const generation = this.client.generation({
      name: context.name,
      model: context.model,
      startTime: new Date(),
      modelParameters: context.modelParameters,
      input: context.input,
      metadata: context.metadata
    });

    return {
      update: (data: Record<string, any>) => {
        if (generation) {
          generation.update(data);
        }
      },
      end: () => {
        if (generation) {
          generation.update({
            metadata: { status: 'completed' }
          });
        }
      }
    };
  }

  async flush(): Promise<void> {
    await this.client.shutdownAsync();
  }
}

// Factory function to get the configured backend
function getTracer(): TracingBackend {
  if (DEFAULT_TRACER === 'langfuse') {
    return new LangfuseBackend();
  }
  // Add more backends here as needed
  throw new Error(`Unknown tracing backend: ${DEFAULT_TRACER}`);
}

// Global tracer instance
const _tracer = getTracer();

/**
 * Decorator factory for tracing methods
 */
export function trace(name?: string, options: Record<string, any> = {}) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    if (USING_NATIVE_INTEGRATION) {
      // When using native integration, return the original method
      return descriptor;
    }

    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const context: SpanContext = {
        name: name || propertyKey,
        input: args,
        metadata: options.metadata,
        tags: options.tags,
        userId: options.userId,
        sessionId: options.sessionId
      };

      const span = _tracer.startSpan(context);

      try {
        const result = await originalMethod.apply(this, args);
        span.update({ output: result, metadata: { status: 'success' } });
        return result;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        span.update({ metadata: { status: 'error', error: errorMessage } });
        throw error;
      } finally {
        span.end();
      }
    };

    return descriptor;
  };
}

/**
 * Create a new span in the trace
 */
export function startSpan(name: string, options: Record<string, any> = {}) {
  if (USING_NATIVE_INTEGRATION) {
    // When using native integration, return a simplified executor
    return {
      async execute<T>(fn: () => Promise<T>): Promise<T> {
        return await fn();
      }
    };
  }

  const context: SpanContext = {
    name,
    input: options.input,
    metadata: options.metadata,
    userId: options.userId,
    sessionId: options.sessionId,
    tags: options.tags
  };

  const span = _tracer.startSpan(context);

  return {
    async execute<T>(fn: () => Promise<T>): Promise<T> {
      try {
        const result = await fn();
        span.update({ output: result, metadata: { status: 'success' } });
        return result;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        span.update({ metadata: { status: 'error', error: errorMessage } });
        throw error;
      } finally {
        span.end();
      }
    }
  };
}

/**
 * Create a new generation in the trace for LLM calls
 */
export function startGeneration(
  name: string,
  model: string,
  options: Record<string, any> = {}
) {
  if (USING_NATIVE_INTEGRATION) {
    // When using native integration, return a simplified executor
    return {
      async execute<T>(fn: () => Promise<T>): Promise<T> {
        return await fn();
      }
    };
  }

  const context: GenerationContext = {
    name,
    model,
    input: options.input,
    metadata: options.metadata,
    userId: options.userId,
    sessionId: options.sessionId,
    tags: options.tags,
    modelParameters: options.modelParameters
  };

  const span = _tracer.startGeneration(context);

  return {
    async execute<T>(fn: () => Promise<T>): Promise<T> {
      try {
        const result = await fn();
        span.update({
          output: result,
          completionStartTime: new Date(),
          usage: options.usage,
          metadata: { status: 'success' }
        });
        return result;
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        span.update({ metadata: { status: 'error', error: errorMessage } });
        throw error;
      } finally {
        span.end();
      }
    }
  };
}

/**
 * Ensure all events are flushed in short-lived environments
 */
export async function flush() {
  await _tracer.flush();
} 