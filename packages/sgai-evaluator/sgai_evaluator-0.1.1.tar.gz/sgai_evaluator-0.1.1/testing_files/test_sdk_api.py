#!/usr/bin/env python3
"""
Test script to check Langfuse SDK API methods
"""

import os
from langfuse import Langfuse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse client (will use environment variables)
langfuse = Langfuse()

print("🔍 Checking Langfuse SDK API methods...")
print(f"📦 SDK Version: {langfuse._version if hasattr(langfuse, '_version') else 'Unknown'}")
print(f"📋 Available methods: {[method for method in dir(langfuse) if not method.startswith('_')]}")

# Test simple trace creation
print("\n🧪 Testing basic trace creation...")
try:
    # Try different APIs
    print("Testing: langfuse.trace()")
    trace = langfuse.trace(name="test_trace", input="test input")
    print(f"✅ Success: {trace.id}")
    
    print("Testing: langfuse.generation()")
    generation = langfuse.generation(
        name="test_generation",
        input="test input",
        output="test output"
    )
    print(f"✅ Success: {generation.id}")
    
    langfuse.flush()
    print("✅ All methods work!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("📋 Trying alternative API...")
    try:
        # Try the @observe decorator approach
        from langfuse.decorators import observe
        
        @observe()
        def test_function():
            return "test result"
        
        result = test_function()
        print(f"✅ @observe decorator works: {result}")
        langfuse.flush()
        
    except Exception as e2:
        print(f"❌ Alternative API also failed: {e2}") 