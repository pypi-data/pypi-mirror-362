/**
 * Universal Tracing Middleware for Agentic Setups
 * =============================================
 * 
 * This module provides a framework-agnostic tracing interface that can work with
 * any tracing backend (Langfuse, OpenTelemetry, etc.) through a simple adapter pattern.
 * It also supports native framework integrations when available.
 */

import { Langfuse } from 'langfuse';

interface SpanContext {
  name: string;
  attributes?: Record<string, any>;
  parentId?: string;
}

interface TracingBackend {
  startSpan(context: SpanContext): string;
  endSpan(spanId: string): void;
  updateSpan(spanId: string, attributes: Record<string, any>): void;
}

class LangfuseBackend implements TracingBackend {
  private tracer: Langfuse;
  private spans: Map<string, any>;

  constructor(tracer: Langfuse) {
    this.tracer = tracer;
    this.spans = new Map();
  }

  startSpan(context: SpanContext): string {
    const trace = this.tracer.trace({
      name: context.name,
      metadata: context.attributes,
    });
    
    const span = trace.span({
      name: context.name,
    });

    this.spans.set(span.id, span);
    return span.id;
  }

  endSpan(spanId: string): void {
    const span = this.spans.get(spanId);
    if (span) {
      span.end();
      this.spans.delete(spanId);
    }
  }

  updateSpan(spanId: string, attributes: Record<string, any>): void {
    const span = this.spans.get(spanId);
    if (span) {
      span.update({ metadata: attributes });
    }
  }
}

let currentBackend: TracingBackend | null = null;

export function setTracingBackend(backend: TracingBackend) {
  currentBackend = backend;
}

export function getTracer(): TracingBackend {
  if (!currentBackend) {
    throw new Error('No tracing backend configured');
  }
  return currentBackend;
}

export function trace(name: string, attributes: Record<string, any> = {}) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const spanId = getTracer().startSpan({ name, attributes });

      try {
        const result = await originalMethod.apply(this, args);
        getTracer().updateSpan(spanId, { result });
        getTracer().endSpan(spanId);
        return result;
      } catch (error: any) {
        getTracer().updateSpan(spanId, { error: error?.message || 'Unknown error' });
        getTracer().endSpan(spanId);
        throw error;
      }
    };

    return descriptor;
  };
}

export class SpanManager {
  private spanId: string;

  constructor(name: string, attributes: Record<string, any> = {}) {
    this.spanId = getTracer().startSpan({ name, attributes });
  }

  updateSpan(attributes: Record<string, any>) {
    getTracer().updateSpan(this.spanId, attributes);
  }

  end() {
    getTracer().endSpan(this.spanId);
  }

  async wrap<T>(fn: () => Promise<T>): Promise<T> {
    try {
      const result = await fn();
      this.updateSpan({ result });
      this.end();
      return result;
    } catch (error: any) {
      this.updateSpan({ error: error?.message || 'Unknown error' });
      this.end();
      throw error;
    }
  }
}

export function createTracer(config: { publicKey: string; secretKey: string; baseUrl?: string }) {
  const tracer = new Langfuse({
    publicKey: config.publicKey,
    secretKey: config.secretKey,
    baseUrl: config.baseUrl,
  });
  
  setTracingBackend(new LangfuseBackend(tracer));
  return tracer;
} 