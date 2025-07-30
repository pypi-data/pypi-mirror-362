import asyncio
import unittest
from unittest.mock import patch, MagicMock, ANY, call
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


# Add the examples/python directory to the Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples', 'python')))

from agent_example import CustomerSupportAgent

class TestTracingMiddleware(unittest.TestCase):

    @patch('middleware.LangfuseTracingMiddleware._get_tracer')
    def test_handle_query_calls_tracer_with_correct_params(self, mock_get_tracer):
        # Arrange
        # Mock the context manager returned by _get_tracer
        mock_tracer = MagicMock()
        mock_tracer.update_trace = MagicMock()
        mock_tracer.update = MagicMock()
        
        mock_context_manager = MagicMock()
        mock_context_manager.__enter__.return_value = mock_tracer
        mock_context_manager.__exit__.return_value = None
        mock_get_tracer.return_value = mock_context_manager

        # Instantiate the agent
        agent = CustomerSupportAgent()
        
        # Act
        query = "I have an issue with my subscription."
        customer_id = "cust_789"
        session_id = "sess_abc"
        
        async def run_test():
            await agent.handle_query(query, customer_id, session_id)
        
        asyncio.run(run_test())

        # Assert
        # Find the handle_query call and verify its parameters
        handle_query_calls = [
            call for call in mock_get_tracer.mock_calls 
            if call[0] == '' and call[1][0] == 'handle_customer_query'
        ]
        self.assertTrue(len(handle_query_calls) > 0, "No calls found for handle_customer_query")
        
        # Get the first handle_query call's kwargs
        handle_query_kwargs = handle_query_calls[0][2]  # kwargs are in the third position
        self.assertIn('user_id', handle_query_kwargs, "user_id not found in handle_query trace kwargs")
        self.assertEqual(handle_query_kwargs['user_id'], customer_id)
        self.assertIn('session_id', handle_query_kwargs, "session_id not found in handle_query trace kwargs")
        self.assertEqual(handle_query_kwargs['session_id'], session_id)
        
        # Check other method calls exist
        generate_response_calls = [
            call for call in mock_get_tracer.mock_calls 
            if call[0] == '' and call[1][0] == 'generate_response'
        ]
        self.assertTrue(len(generate_response_calls) > 0, "No calls found for generate_response")

        analyze_intent_calls = [
            call for call in mock_get_tracer.mock_calls 
            if call[0] == '' and call[1][0] == 'analyze_intent'
        ]
        self.assertTrue(len(analyze_intent_calls) > 0, "No calls found for analyze_intent")

        analyze_sentiment_calls = [
            call for call in mock_get_tracer.mock_calls 
            if call[0] == '' and call[1][0] == 'analyze_sentiment'
        ]
        self.assertTrue(len(analyze_sentiment_calls) > 0, "No calls found for analyze_sentiment")

        # Check that tags were set via update_trace
        mock_tracer.update_trace.assert_any_call(tags=["customer_support", "agent"])

if __name__ == '__main__':
    unittest.main() 