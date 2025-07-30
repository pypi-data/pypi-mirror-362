"""
SGAI Evaluator - Getting Started Example
======================================

This example demonstrates the basic usage of the SGAI Evaluator package
for tracing agent applications.
"""

import os
from sgai_evaluator import trace, start_span, start_generation

# Optional: Configure the tracing backend
os.environ['SGAI_TRACER'] = 'langfuse'  # Default
os.environ['SGAI_SERVICE_NAME'] = 'my_agent_service'

# Example 1: Function Decorator
@trace(name="process_user_input", tags=["example", "user-input"])
def process_user_input(text: str) -> str:
    # Your processing logic here
    return f"Processed: {text}"

# Example 2: Manual Span
def manual_operation():
    with start_span("data_transformation", tags=["example"]) as span:
        # Your operation logic here
        result = "transformed data"
        span.update(output=result)
        return result

# Example 3: LLM Generation
def generate_response(prompt: str) -> str:
    with start_generation("text_generation", model="gpt-4") as span:
        # Simulate LLM call
        response = f"AI response to: {prompt}"
        span.update(output=response)
        return response

def main():
    # Example 1: Using the decorator
    result1 = process_user_input("Hello, AI!")
    print(f"Decorator result: {result1}")

    # Example 2: Using manual span
    result2 = manual_operation()
    print(f"Manual span result: {result2}")

    # Example 3: Using generation span
    result3 = generate_response("What is the weather?")
    print(f"Generation result: {result3}")

if __name__ == "__main__":
    main() 