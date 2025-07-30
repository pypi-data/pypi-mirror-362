import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Validate required environment variables
required_env_vars = ['LANGFUSE_PUBLIC_KEY', 'LANGFUSE_SECRET_KEY', 'LANGFUSE_HOST']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print("\nError: Missing required environment variables:")
    for var in missing_vars:
        print(f"- {var}")
    print("\nPlease set these variables in your .env file or environment.")
    sys.exit(1)

# Add the examples/python directory to the Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples', 'python')))

from agent_example import CustomerSupportAgent

async def test_middleware_integration():
    """Integration test for middleware with Langfuse - no mocks."""
    print("\nTesting middleware integration with Langfuse...")
    print(f"Using Langfuse host: {os.getenv('LANGFUSE_HOST')}")
    
    # Create agent instance
    agent = CustomerSupportAgent()
    
    # Test parameters
    query = "I have an issue with my subscription"
    customer_id = "test_customer_123"
    
    print(f"\nSending test query: {query}")
    print(f"Customer ID: {customer_id}")
    
    try:
        # This should create multiple traces through the middleware
        result = await agent.handle_query(
            query=query,
            customer_id=customer_id
        )
        
        print("\nQuery handled successfully!")
        print("Result:", result)
        print("\nCheck Langfuse dashboard for traces with:")
        print(f"- Customer ID: {customer_id}")
        print("- Trace names: handle_query, generate_response, analyze_intent, analyze_sentiment")
        
        # Validate result structure
        expected_keys = {'response', 'intent', 'sentiment', 'customer_id', 'timestamp'}
        missing_keys = expected_keys - set(result.keys())
        if missing_keys:
            print(f"\nWarning: Missing expected keys in result: {missing_keys}")
        
        return result
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        print("\nTraceback:")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    try:
        result = asyncio.run(test_middleware_integration())
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        sys.exit(1) 