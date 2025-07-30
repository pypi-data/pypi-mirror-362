"""
Example: Customer Support Agent with Universal Tracing Middleware
================================================================

This example shows how to use Langfuse's built-in tracing capabilities through
a simple middleware layer for a customer support agent.

NOTE: If running this file directly as a script, use a relative import for middleware:
    from . import middleware
If running from the parent directory or as a package, adjust the import accordingly.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from . import middleware  # Use relative import for local package/module

# Import tracing utilities from middleware
trace = middleware.trace
start_generation = middleware.start_generation
flush = middleware.flush

class CustomerSupportAgent:
    """Example customer support agent with tracing middleware."""

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.client = AsyncOpenAI()
        self.system_prompt = """You are a helpful customer support agent. 
        Provide clear, concise answers to customer queries."""

    @trace(name="handle_customer_query")
    async def handle_query(
        self, 
        query: str, 
        customer_id: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle a customer support query with full tracing."""
        
        # Analyze intent
        intent = await self.analyze_intent(query)
        
        # Analyze sentiment
        sentiment = await self.analyze_sentiment(query)
        
        # Generate response
        response = await self.generate_response(query, intent, sentiment)
        
        return {
            "response": response,
            "intent": intent,
            "sentiment": sentiment,
            "customer_id": customer_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    @trace(name="analyze_intent")
    async def analyze_intent(self, query: str) -> str:
        """Analyze the intent of the customer query."""
        prompt = f"Analyze the intent of this customer query: {query}"
        
        with start_generation(name="intent-analysis", model=self.model) as generation:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze customer query intent briefly."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            generation.update(output=result)
            return result

    @trace(name="analyze_sentiment")
    async def analyze_sentiment(self, query: str) -> str:
        """Analyze the sentiment of the customer query."""
        prompt = f"What is the sentiment of this customer message: {query}"
        
        with start_generation(name="sentiment-analysis", model=self.model) as generation:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze message sentiment briefly."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            generation.update(output=result)
            return result

    @trace(name="generate_response")
    async def generate_response(self, query: str, intent: str, sentiment: str) -> str:
        """Generate a response to the customer query."""
        prompt = f"""
        Customer query: {query}
        Intent: {intent}
        Sentiment: {sentiment}
        Generate an appropriate response.
        """
        
        with start_generation(name="response-generation", model=self.model) as generation:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            generation.update(output=result)
            return result

async def main():
    agent = CustomerSupportAgent()
    customer_id = str(uuid.uuid4())
    
    try:
        result = await agent.handle_query(
            "I have an issue with my subscription billing",
            customer_id
        )
        print(f"\nResponse: {result['response']}")
        print(f"Intent: {result['intent']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Customer ID: {result['customer_id']}")
        print(f"Timestamp: {result['timestamp']}")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        flush()  # Ensure all traces are sent

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 