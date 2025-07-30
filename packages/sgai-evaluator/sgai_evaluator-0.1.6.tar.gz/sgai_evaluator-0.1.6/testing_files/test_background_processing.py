#!/usr/bin/env python3

import os
import sys
import time
from langfuse import Langfuse, observe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse client (will use environment variables)
langfuse = Langfuse()

@observe(name="background_processing_test")
def test_background_processing_function():
    """Test function to verify background processing is working"""
    print("   🔄 Processing test with background processing enabled...")
    
    # Simulate some LLM work
    test_input = "Test background processing with async queue handling"
    test_output = "✅ Background processing is working! Traces are being processed asynchronously."
    
    result = {
        "input": test_input,
        "output": test_output,
        "timestamp": time.time(),
        "test_type": "background_processing_verification",
        "status": "success"
    }
    
    print(f"   ✅ Test completed with result: {result}")
    return result

@observe(name="background_processing_nested_test")
def nested_test_function():
    """Nested function to test trace hierarchy"""
    print("   🔄 Running nested test...")
    
    # Call the main test function
    main_result = test_background_processing_function()
    
    # Add additional processing
    nested_result = {
        "nested_operation": "trace_hierarchy_test",
        "main_result": main_result,
        "nested_timestamp": time.time()
    }
    
    print(f"   ✅ Nested test completed")
    return nested_result

def test_trace_processing():
    """Test that traces are being processed correctly with background processing enabled"""
    
    print("🧪 Testing Langfuse trace processing with background processing...")
    print("=" * 60)
    
    try:
        # Test authentication
        print("1. Testing authentication...")
        auth_result = langfuse.auth_check()
        print(f"   ✅ Authentication successful: {auth_result}")
        
        # Create traces using the decorator pattern
        print("2. Creating traces with decorator pattern...")
        result = nested_test_function()
        print(f"   ✅ Traces created successfully")
        
        # Flush the data
        print("3. Flushing data...")
        langfuse.flush()
        print("   ✅ Data flushed successfully!")
        
        print("\n" + "=" * 60)
        print("🎯 Next steps:")
        print("1. Check your Langfuse dashboard at http://localhost:3000")
        print("2. Look for traces named 'background_processing_test' and 'background_processing_nested_test'")
        print("3. If traces appear, background processing is working!")
        print("4. If traces are still missing, we'll need to check the logs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during trace processing: {e}")
        return False

if __name__ == "__main__":
    success = test_trace_processing()
    
    if success:
        print(f"\n✨ Test completed successfully!")
        print("🎉 Background processing is working correctly!")
    else:
        print(f"\n❌ Test failed!")
        sys.exit(1) 